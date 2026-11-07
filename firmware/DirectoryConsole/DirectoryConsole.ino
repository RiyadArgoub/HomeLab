/*
  Computer Directory Console v0.2 PROTOTYPE
  ESP32-WROOM-32 DevKit, ST7789V 240x320, I2C 1602, microSD, BLE, joystick.
  Only square buttons are used. Joystick SW is NOT used.
  POWER = deep sleep / RTC wake, NOT an electrical power disconnect.
  LCD backlight is switched off in deep sleep; TFT BL wired to 3.3V stays on.
  STOP = password-protected remote shutdown REQUEST, NOT a safety E-stop.
  Real commands require Python manager armed + explicit GUI confirmation.
  Install Arduino libraries: Adafruit GFX, Adafruit ST7735 and ST7789,
  LiquidCrystal_I2C, ESP32 Arduino BLE (comes with esp32 board core).
  microSD card root: /computers.csv + /heather.bmp etc. (24-bit 120x120 BMPs).
*/
#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <esp_sleep.h>

// GPIO matches the original preliminary README pin map.
#define TFT_CS 16
#define TFT_DC 17
#define TFT_RST 14
#define SD_CS 13
#define SPI_CLK 18
#define SPI_MISO 19
#define SPI_MOSI 23
#define I2C_SDA 21
#define I2C_SCL 22
#define JOY_X 34
#define JOY_Y 35
#define BTN_POWER 32
#define BTN_BACK 33
#define BTN_PRESS 25
#define BTN_STOP 26
#define PIEZO 27

// Change if up/down or left/right are inverted on your joystick.
const bool INVERT_X = false;
const bool INVERT_Y = false;
const int JOY_THRESHOLD = 1050;
const char* TEST_PASSWORD = "1912"; // PUBLIC TEST VALUE ONLY, NOT SECURITY.
const char* SERVICE_UUID = "f23a0001-6cf8-4c4c-a3f2-120c95e7ca13";
const char* RX_UUID = "f23a0002-6cf8-4c4c-a3f2-120c95e7ca13";
const char* TX_UUID = "f23a0003-6cf8-4c4c-a3f2-120c95e7ca13";

Adafruit_ST7789 tft(TFT_CS,TFT_DC,TFT_RST);
LiquidCrystal_I2C lcd(0x27,16,2); // Change to 0x3F if your backpack uses that address.
BLECharacteristic* txChar=nullptr;
bool bleConnected=false;
bool sdReady=false;

struct Computer {
  String name,role,host,mac,avatar,status,notes;
};
const int MAX_PC=128;
const int VISIBLE_ROWS=9;
Computer computers[MAX_PC];
int countPC=0;
int selected=0;
int firstVisible=0;
bool syncBatch=false;
int syncExpected=0;
int centerX=2048,centerY=2048;

enum View { DIRECTORY, DETAIL, STOP_CONFIRM, PASSWORD, CHOOSE_SCOPE, RESULT };
View view=DIRECTORY;
int confirmYes=0; // Default NO (0), explicit right = YES (1)
int keypadRow=0,keypadCol=0;
String typedPassword="";
int scopeChoice=0; // 0: selected computer, 1: all
String resultMessage="";
unsigned long nextDraw=0;
unsigned long lastButtonTime=0;
unsigned long powerHeld=0;
bool lastPowerDown=false;
int lastDirection=0;

struct BleFrame {char line[241];};
QueueHandle_t rxFrames=nullptr;

void chirp(int freq,int ms){
  tone(PIEZO,freq,ms); delay(ms+15); noTone(PIEZO);
}
void validTone(){chirp(1000,50);}
void errorTone(){chirp(280,180);}
void successTone(){chirp(800,85);chirp(1200,130);}

void lcdLines(const String& a,const String& b){
  lcd.clear();lcd.setCursor(0,0);lcd.print(a.substring(0,16));
  lcd.setCursor(0,1);lcd.print(b.substring(0,16));
}
void defaults(){
  const char* names[]={"Heather-PC1","Lindsay-PC2","Zoey-PC3","Gwen-PC4","Courtney-PC5"};
  const char* roles[]={"AI","NAS","SERVER","WORKSTATION","LAB"};
  const char* avatars[]={"heather.bmp","lindsay.bmp","zoey.bmp","gwen.bmp","courtney.bmp"};
  countPC=5;
  for(int i=0;i<countPC;i++){
    computers[i].name=names[i]; computers[i].role=roles[i];
    computers[i].host=""; computers[i].mac="";
    computers[i].avatar=avatars[i];
    computers[i].status="UNKNOWN";computers[i].notes="Placeholder info";
  }
}
String fieldAt(const String& line,int index){
  int start=0;
  for(int i=0;i<index;i++){
    int separator=line.indexOf('|',start);
    if(separator<0)return "";
    start=separator+1;
  }
  int end=line.indexOf('|',start);
  if(end<0)end=line.length();
  return line.substring(start,end);
}
void loadCsv(){
  if(!sdReady)return;
  File f=SD.open("/computers.csv",FILE_READ);
  if(!f){Serial.println("No computers.csv, using defaults");return;}
  int i=0;
  while(f.available() && i<MAX_PC){
    String line=f.readStringUntil('\n');line.trim();
    if(line.length()==0 || line.startsWith("#"))continue;
    computers[i].name=fieldAt(line,0);
    computers[i].role=fieldAt(line,1);
    computers[i].host=fieldAt(line,2);
    computers[i].mac=fieldAt(line,3);
    computers[i].avatar=fieldAt(line,4);
    computers[i].status="UNKNOWN"; // Never trust last boot's "ONLINE" state.
    computers[i].notes=fieldAt(line,6);
    if(computers[i].name.length())i++;
  }
  f.close();if(i>0)countPC=i;
}
void saveCsv(){
  if(!sdReady)return;
  SD.remove("/computers.csv");
  File f=SD.open("/computers.csv",FILE_WRITE);
  if(!f){Serial.println("SD SAVE FAILED");return;}
  for(int i=0;i<countPC;i++){
    Computer &c=computers[i];
    f.print(c.name+"|"+c.role+"|"+c.host+"|"+c.mac+"|"+c.avatar+"|UNKNOWN|"+c.notes+"\n");
  }
  f.close();
}

uint16_t bmp16(File &f){uint16_t a=f.read();return a|(f.read()<<8);}
uint32_t bmp32(File &f){uint32_t v=0;for(int i=0;i<4;i++)v|=((uint32_t)f.read())<<(i*8);return v;}
void drawAvatar(String filename,int x,int y){
  if(!sdReady){tft.fillRoundRect(x,y,120,120,8,ST77XX_MAGENTA);return;}
  File bmp=SD.open("/"+filename,FILE_READ);
  if(!bmp){tft.fillRoundRect(x,y,120,120,8,ST77XX_MAGENTA);return;}
  if(bmp16(bmp)!=0x4D42){bmp.close();return;}
  (void)bmp32(bmp); (void)bmp32(bmp); uint32_t offset=bmp32(bmp);
  (void)bmp32(bmp); int32_t w=(int32_t)bmp32(bmp),h=(int32_t)bmp32(bmp);
  uint16_t planes=bmp16(bmp),depth=bmp16(bmp);
  uint32_t compression=bmp32(bmp);
  if(w<=0 || h==0 || w>240 || h>240 || depth!=24 || planes!=1 || compression!=0){bmp.close();return;}
  bool bottomUp=h>0;if(h<0)h=-h;
  uint32_t rowSize=(w*3+3)&~3U;
  int limitW=min((int)w,120),limitH=min((int)h,120);
  for(int row=0;row<limitH;row++){
    int sourceY=bottomUp?h-1-row:row;
    bmp.seek(offset+(uint32_t)sourceY*rowSize);
    for(int col=0;col<limitW;col++){
      uint8_t b=bmp.read(),g=bmp.read(),r=bmp.read();
      tft.drawPixel(x+col,y+row,tft.color565(r,g,b));
    }
  }
  bmp.close();
}

void header(const char* text){
  tft.fillScreen(ST77XX_BLACK);
  tft.fillRect(0,0,240,27,tft.color565(13,39,52));
  tft.setTextColor(ST77XX_WHITE);tft.setTextSize(2);tft.setCursor(8,7);tft.print(text);
}
void footer(const char* txt){
  tft.fillRect(0,298,240,22,tft.color565(18,28,38));
  tft.setTextSize(1);tft.setTextColor(ST77XX_CYAN);
  tft.setCursor(6,305);tft.print(txt);
}
void draw(){
  if(view==DIRECTORY){
    header("PC DIRECTORY");
    tft.setTextSize(1);tft.setCursor(8,34);
    tft.setTextColor(bleConnected?ST77XX_GREEN:ST77XX_YELLOW);
    tft.print(bleConnected?"BLE manager connected":"BLE offline / cached directory");
    if(selected < firstVisible) firstVisible=selected;
    if(selected >= firstVisible + VISIBLE_ROWS) firstVisible=selected - VISIBLE_ROWS + 1;
    int maxFirst=max(0,countPC-VISIBLE_ROWS);
    firstVisible=constrain(firstVisible,0,maxFirst);
    for(int row=0; row<VISIBLE_ROWS; row++){
      int i=firstVisible+row;
      if(i>=countPC) break;
      int y=55+row*26;
      if(i==selected)tft.fillRoundRect(5,y,230,24,4,tft.color565(42,69,86));
      tft.setTextSize(1);tft.setTextColor(ST77XX_WHITE);
      tft.setCursor(11,y+8);tft.print(i==selected?"> ":"  ");tft.print(computers[i].name.substring(0,17));
      tft.setTextColor(computers[i].status=="ONLINE"?ST77XX_GREEN:ST77XX_YELLOW);
      tft.setCursor(183,y+8);tft.print(computers[i].status=="ONLINE"?"ON":"??");
    }
    footer((String(firstVisible+1)+"-"+String(min(countPC,firstVisible+VISIBLE_ROWS))+"/"+String(countPC)+"  GREEN: details").c_str());
    lcdLines("DIRECTORY",computers[selected].name);
  }
  else if(view==DETAIL){
    header("COMPUTER INFO");
    drawAvatar(computers[selected].avatar,60,34);
    tft.setTextColor(ST77XX_WHITE);tft.setTextSize(2);
    tft.setCursor(12,165);tft.print(computers[selected].name.substring(0,18));
    tft.setTextSize(1);tft.setCursor(12,199);tft.print("ROLE: "+computers[selected].role);
    tft.setCursor(12,218);tft.print("STATUS: "+computers[selected].status);
    tft.setCursor(12,240);tft.print(computers[selected].notes.substring(0,33));
    footer("GREEN: Wake | BLUE: STOP");
    lcdLines(computers[selected].name,computers[selected].role+" "+computers[selected].status);
  }
  else if(view==STOP_CONFIRM){
    header("STOP REQUEST");
    tft.setTextColor(ST77XX_YELLOW);tft.setTextSize(2);
    tft.setCursor(12,75);tft.print("SHUTDOWN MENU");
    tft.setTextSize(1);tft.setCursor(12,115);tft.print("Requires password + manager approval.");
    tft.setTextSize(2);
    tft.setCursor(31,178);tft.setTextColor(confirmYes?ST77XX_WHITE:ST77XX_GREEN);tft.print("NO");
    tft.setCursor(146,178);tft.setTextColor(confirmYes?ST77XX_GREEN:ST77XX_WHITE);tft.print("YES");
    footer("JOY L/R choose; GREEN enter");
    lcdLines("CONFIRM STOP?",confirmYes?"YES":"NO");
  }
  else if(view==PASSWORD){
    header("PASSCODE");
    tft.setTextColor(ST77XX_WHITE);tft.setTextSize(2);
    tft.setCursor(42,38);tft.print("PIN: ");
    for(int n=0;n<4;n++)tft.print(n<typedPassword.length()?"*":"_");
    for(int r=0;r<3;r++)for(int c=0;c<3;c++){
      int x=23+c*70,y=82+r*65;
      bool chosen=r==keypadRow && c==keypadCol;
      tft.fillRoundRect(x,y,55,52,6,chosen?tft.color565(33,130,80):tft.color565(45,58,75));
      tft.setTextColor(ST77XX_WHITE);tft.setTextSize(3);
      tft.setCursor(x+18,y+15);tft.print(r*3+c+1);
    }
    footer("GREEN: digit | BACK: delete");
    lcdLines("ENTER TEST PIN",String(typedPassword.length())+" / 4 digits");
  }
  else if(view==CHOOSE_SCOPE){
    header("STOP TARGET");
    tft.setTextColor(ST77XX_WHITE);tft.setTextSize(2);
    tft.setCursor(18,79);tft.print("Choose target:");
    tft.setTextColor(scopeChoice==0?ST77XX_GREEN:ST77XX_WHITE);
    tft.setCursor(17,140);tft.print("Selected PC");
    tft.setTextColor(scopeChoice==1?ST77XX_RED:ST77XX_WHITE);
    tft.setCursor(17,196);tft.print("ALL COMPUTERS");
    footer("UP/DOWN; GREEN: send request");
    lcdLines("STOP SCOPE",scopeChoice?"ALL COMPUTERS":"SELECTED ONLY");
  }
  else if(view==RESULT){
    header("REQUEST STATUS");
    tft.setTextColor(ST77XX_CYAN);tft.setTextSize(2);
    tft.setCursor(12,120);tft.print(resultMessage.substring(0,18));
    footer("BACK: return to directory");
    lcdLines("REQUEST",resultMessage);
  }
}
void redraw(){nextDraw=millis();draw();}

class ServerCallbacks:public BLEServerCallbacks {
  void onConnect(BLEServer*)override{bleConnected=true;}
  void onDisconnect(BLEServer*)override{bleConnected=false;BLEDevice::startAdvertising();}
};
class ReceiveCallbacks:public BLECharacteristicCallbacks {
  String buffer;
  void onWrite(BLECharacteristic* chr)override{
    String part=String(chr->getValue().c_str());
    for(size_t i=0;i<part.length();i++){
      char c=part[i];
      if(c=='\n'){
        BleFrame frame={0};buffer.toCharArray(frame.line,sizeof(frame.line));
        if(rxFrames)xQueueSend(rxFrames,&frame,0);
        buffer="";
      }else if(c!='\r'){
        if(buffer.length()<239)buffer+=c;
        else buffer="";
      }
    }
  }
};
void sendLine(String msg){
  if(!bleConnected || !txChar)return;
  msg+='\n';
  for(int i=0;i<msg.length();i+=20){
    String chunk=msg.substring(i,min(i+20,(int)msg.length()));
    txChar->setValue(chunk.c_str());txChar->notify();
    delay(35);
  }
}
void processLine(String line){
  if(line=="PING"){
    sendLine("HELLO");return;
  }
  if(line.startsWith("SYNCBEGIN|")){
    int expected=fieldAt(line,1).toInt();
    if(expected<0 || expected>MAX_PC){sendLine("ERROR|COUNT");return;}
    syncBatch=true;
    syncExpected=expected;
    sendLine("SYNCBEGIN_OK|"+String(expected));
  }else if(line=="SYNCEND"){
    if(syncBatch){
      countPC=constrain(syncExpected,0,MAX_PC);
      if(countPC==0){defaults();}
      selected=constrain(selected,0,max(0,countPC-1));
      firstVisible=0;
      saveCsv();
      syncBatch=false;
      redraw();
      sendLine("SYNCEDALL|"+String(countPC));
    }
  }else if(line.startsWith("SYNC|")){
    int index=fieldAt(line,1).toInt();
    if(index<0 || index>=MAX_PC)return;
    Computer &c=computers[index];
    c.name=fieldAt(line,2);c.role=fieldAt(line,3);c.host=fieldAt(line,4);
    c.mac=fieldAt(line,5);c.avatar=fieldAt(line,6);
    c.status=fieldAt(line,7);c.notes=fieldAt(line,8);
    if(c.name.length()>0){
      if(!syncBatch && index>=countPC)countPC=index+1;
      if(!syncBatch){saveCsv();redraw();}
      sendLine("SYNCED|"+String(index));
    }
  }else if(line.startsWith("STATE|")){
    int index=fieldAt(line,1).toInt();
    if(index>=0 && index<countPC){computers[index].status=fieldAt(line,2);redraw();}
  }else if(line.startsWith("ACK|")){
    resultMessage="MANAGER: "+fieldAt(line,3);
    view=RESULT;redraw();
  }
}
void setupBLE(){
  rxFrames=xQueueCreate(8,sizeof(BleFrame));
  BLEDevice::init("DirectoryConsole");
  BLEServer* server=BLEDevice::createServer();
  server->setCallbacks(new ServerCallbacks());
  BLEService* service=server->createService(SERVICE_UUID);
  BLECharacteristic* rx=service->createCharacteristic(RX_UUID,BLECharacteristic::PROPERTY_WRITE);
  rx->setCallbacks(new ReceiveCallbacks());
  txChar=service->createCharacteristic(TX_UUID,BLECharacteristic::PROPERTY_NOTIFY);
  txChar->addDescriptor(new BLE2902());
  service->start();
  BLEDevice::startAdvertising();
}

void doStop(){
  view=STOP_CONFIRM;confirmYes=0;validTone();redraw();
}
void backButton(){
  if(view==DIRECTORY){errorTone();return;}
  if(view==DETAIL){view=DIRECTORY;}
  else if(view==STOP_CONFIRM){view=DETAIL;}
  else if(view==PASSWORD){
    if(typedPassword.length())typedPassword.remove(typedPassword.length()-1);
    else view=STOP_CONFIRM;
  }
  else if(view==CHOOSE_SCOPE){view=PASSWORD;}
  else if(view==RESULT){view=DIRECTORY;}
  validTone();redraw();
}
void pressButton(){
  if(view==DIRECTORY){view=DETAIL;validTone();redraw();}
  else if(view==DETAIL){
    resultMessage=bleConnected?"WAKE REQUESTED":"BLE OFFLINE";
    if(bleConnected)sendLine("REQ|"+String(selected)+"|WAKE");
    else errorTone();
    view=RESULT;redraw();
  }
  else if(view==STOP_CONFIRM){
    if(!confirmYes){errorTone();view=DETAIL;}
    else {typedPassword="";keypadRow=0;keypadCol=0;view=PASSWORD;validTone();}
    redraw();
  }
  else if(view==PASSWORD){
    typedPassword += String(1+keypadRow*3+keypadCol);
    validTone();
    if(typedPassword.length()==4){
      if(typedPassword==TEST_PASSWORD){
        successTone();scopeChoice=0;view=CHOOSE_SCOPE;
      }else{
        typedPassword="";errorTone();
        // This is a demo PIN and has no rate limiting: DO NOT use for production.
      }
    }
    redraw();
  }
  else if(view==CHOOSE_SCOPE){
    if(!bleConnected){resultMessage="BLE OFFLINE";errorTone();}
    else{
      sendLine("REQ|"+String(scopeChoice?"ALL":String(selected))+"|STOP");
      resultMessage="AWAIT MANAGER";validTone();
    }
    view=RESULT;redraw();
  }
  else errorTone();
}
int joyDirection(){
  int dx=analogRead(JOY_X)-centerX;
  int dy=analogRead(JOY_Y)-centerY;
  if(INVERT_X)dx=-dx;if(INVERT_Y)dy=-dy;
  if(abs(dx)<JOY_THRESHOLD && abs(dy)<JOY_THRESHOLD)return 0;
  if(abs(dx)>abs(dy))return dx>0?2:1; // RIGHT =2, LEFT=1
  return dy>0?4:3; // DOWN =4, UP=3; invert if physically reversed
}
void handleJoy(int dir){
  if(view==DIRECTORY){
    if(dir==3)selected=max(0,selected-1);
    if(dir==4)selected=min(countPC-1,selected+1);
  }else if(view==STOP_CONFIRM){
    if(dir==1)confirmYes=0;
    if(dir==2)confirmYes=1;
  }else if(view==PASSWORD){
    if(dir==1)keypadCol=max(0,keypadCol-1);
    if(dir==2)keypadCol=min(2,keypadCol+1);
    if(dir==3)keypadRow=max(0,keypadRow-1);
    if(dir==4)keypadRow=min(2,keypadRow+1);
  }else if(view==CHOOSE_SCOPE){
    if(dir==3)scopeChoice=0;
    if(dir==4)scopeChoice=1;
  }else{errorTone();return;}
  validTone();redraw();
}
void enterSleep(){
  lcdLines("POWER SAVING","PRESS TO WAKE");
  delay(250); // Let the user see sleep acknowledgment briefly.
  lcd.noBacklight(); // Extinguish the 1602 backlight (if backpack supports it).
  lcd.noDisplay();
  tft.fillScreen(ST77XX_BLACK); // Does NOT shut off a hard-wired TFT BL.
  delay(30);
  noTone(PIEZO);
  // Wait until the POWER button is RELEASED, otherwise the low level
  // would immediately wake the device as soon as it entered sleep.
  while(digitalRead(BTN_POWER)==LOW)delay(10);
  delay(100);
  esp_sleep_enable_ext0_wakeup(GPIO_NUM_32,0);
  esp_deep_sleep_start();
}
void pollPower(){
  bool down=digitalRead(BTN_POWER)==LOW;
  if(down && !lastPowerDown)powerHeld=millis();
  if(down && millis()-powerHeld>1200)enterSleep();
  lastPowerDown=down;
}
void setup(){
  Serial.begin(115200);
  pinMode(TFT_CS,OUTPUT);digitalWrite(TFT_CS,HIGH);
  pinMode(SD_CS,OUTPUT);digitalWrite(SD_CS,HIGH);
  pinMode(PIEZO,OUTPUT);noTone(PIEZO);
  pinMode(BTN_POWER,INPUT_PULLUP);pinMode(BTN_BACK,INPUT_PULLUP);
  pinMode(BTN_PRESS,INPUT_PULLUP);pinMode(BTN_STOP,INPUT_PULLUP);
  Wire.begin(I2C_SDA,I2C_SCL);
  lcd.init();lcd.backlight();lcdLines("DIRECTORY","BOOTING...");
  SPI.begin(SPI_CLK,SPI_MISO,SPI_MOSI);
  tft.init(240,320);tft.setRotation(0);
  tft.fillScreen(ST77XX_BLACK);
  defaults();
  digitalWrite(TFT_CS,HIGH);
  sdReady=SD.begin(SD_CS,SPI,4000000);
  if(sdReady)loadCsv();
  else Serial.println("SD init failed - fallback to sample directory, no BMP images");
  // Calibrate joystick center while untouched.
  analogReadResolution(12);
  long sx=0,sy=0;
  for(int i=0;i<70;i++){sx+=analogRead(JOY_X);sy+=analogRead(JOY_Y);delay(3);}
  centerX=sx/70;centerY=sy/70;
  setupBLE();draw();successTone();
  Serial.println("Computer Directory console prototype ready");
}
void loop(){
  pollPower();
  static bool lastBack=HIGH,lastPress=HIGH,lastStop=HIGH;
  bool back=digitalRead(BTN_BACK),press=digitalRead(BTN_PRESS),stop=digitalRead(BTN_STOP);
  if(millis()-lastButtonTime>170){
    if(lastBack==HIGH && back==LOW){backButton();lastButtonTime=millis();}
    else if(lastPress==HIGH && press==LOW){pressButton();lastButtonTime=millis();}
    else if(lastStop==HIGH && stop==LOW){doStop();lastButtonTime=millis();}
  }
  lastBack=back;lastPress=press;lastStop=stop;
  int direction=joyDirection();
  if(direction==0)lastDirection=0;
  else if(lastDirection==0){lastDirection=direction;handleJoy(direction);}
  if(rxFrames){
    BleFrame frame;
    for(int k=0;k<3 && xQueueReceive(rxFrames,&frame,0)==pdTRUE;k++)processLine(String(frame.line));
  }
  delay(12);
}
