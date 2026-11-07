/*
  Computer Directory Console v0.4 SD-STREAMED

  ESP32-WROOM-32 DevKit + ST7789V 240x320 + I2C 1602 + microSD + BLE + joystick.

  Changes from the previous v0.4 patch:
  - microSD is the primary computer database.
  - Supports up to 128 computer records without storing 128 full Computer objects in RAM.
  - Only the record currently needed is read from /computers.csv.
  - Portrait BMPs are streamed one row at a time from microSD to the TFT.
  - microSD startup is retried up to 5 times before using the 5-PC fallback.
  - Directory view scrolls through all loaded records.

  microSD root:
    /computers.csv
    /heather1.bmp
    /zoey1.bmp
    ...

  BMP format: uncompressed 24-bit BMP, recommended 120x120.
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
#include <esp_heap_caps.h>

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

const bool INVERT_X = false;
const bool INVERT_Y = false;
const int JOY_THRESHOLD = 1050;
const char* TEST_PASSWORD = "1234";
const char* SERVICE_UUID = "f23a0001-6cf8-4c4c-a3f2-120c95e7ca13";
const char* RX_UUID = "f23a0002-6cf8-4c4c-a3f2-120c95e7ca13";
const char* TX_UUID = "f23a0003-6cf8-4c4c-a3f2-120c95e7ca13";

Adafruit_ST7789 tft(TFT_CS, TFT_DC, TFT_RST);
LiquidCrystal_I2C lcd(0x27, 16, 2);
BLECharacteristic* txChar = nullptr;
bool bleConnected = false;
bool sdReady = false;
bool usingSdDirectory = false;

struct Computer {
  String name;
  String role;
  String host;
  String mac;
  String avatar;
  String status;
  String notes;
};

const int MAX_PC = 128;
uint32_t recordOffsets[MAX_PC];                 // 512 bytes total
uint8_t runtimeStatus[MAX_PC];                  // 0 unknown, 1 online, 2 offline
int countPC = 0;
int selected = 0;
int centerX = 2048, centerY = 2048;

const int FALLBACK_COUNT = 5;
const char* FALLBACK_NAMES[FALLBACK_COUNT] = {
  "Heather-PC1", "Lindsay-PC2", "Zoey-PC3", "Gwen-PC4", "Courtney-PC5"
};
const char* FALLBACK_ROLES[FALLBACK_COUNT] = {
  "AI", "NAS", "SERVER", "WORKSTATION", "LAB"
};
const char* FALLBACK_AVATARS[FALLBACK_COUNT] = {
  "heather.bmp", "lindsay.bmp", "zoey.bmp", "gwen.bmp", "courtney.bmp"
};

enum View { DIRECTORY, DETAIL, STOP_CONFIRM, PASSWORD, CHOOSE_SCOPE, RESULT };
View view = DIRECTORY;
int confirmYes = 0;
int keypadRow = 0, keypadCol = 0;
String typedPassword = "";
int scopeChoice = 0;
String resultMessage = "";
unsigned long nextDraw = 0;
unsigned long lastButtonTime = 0;
unsigned long powerHeld = 0;
bool lastPowerDown = false;
int lastDirection = 0;

struct BleFrame { char line[241]; };
QueueHandle_t rxFrames = nullptr;

void chirp(int freq, int ms) {
  tone(PIEZO, freq, ms);
  delay(ms + 15);
  noTone(PIEZO);
}
void validTone() { chirp(1000, 50); }
void errorTone() { chirp(280, 180); }
void successTone() { chirp(800, 85); chirp(1200, 130); }

void lcdLines(const String& a, const String& b) {
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print(a.substring(0, 16));
  lcd.setCursor(0, 1); lcd.print(b.substring(0, 16));
}

String fieldAt(const String& line, int index) {
  int start = 0;
  for (int i = 0; i < index; i++) {
    int separator = line.indexOf('|', start);
    if (separator < 0) return "";
    start = separator + 1;
  }
  int end = line.indexOf('|', start);
  if (end < 0) end = line.length();
  return line.substring(start, end);
}

bool isDataLine(String line) {
  line.trim();
  return line.length() > 0 && !line.startsWith("#") && line.indexOf('|') >= 0;
}

bool parseComputerLine(String line, Computer& c, int index) {
  line.trim();
  if (!isDataLine(line)) return false;

  c.name = fieldAt(line, 0);
  c.role = fieldAt(line, 1);
  c.host = fieldAt(line, 2);
  c.mac = fieldAt(line, 3);
  c.avatar = fieldAt(line, 4);
  c.status = "UNKNOWN";
  c.notes = fieldAt(line, 6);

  if (index >= 0 && index < MAX_PC) {
    if (runtimeStatus[index] == 1) c.status = "ONLINE";
    else if (runtimeStatus[index] == 2) c.status = "OFFLINE";
  }
  return c.name.length() > 0;
}

void fallbackComputer(int index, Computer& c) {
  if (index < 0) index = 0;
  if (index >= FALLBACK_COUNT) index = FALLBACK_COUNT - 1;
  c.name = FALLBACK_NAMES[index];
  c.role = FALLBACK_ROLES[index];
  c.host = "";
  c.mac = "";
  c.avatar = FALLBACK_AVATARS[index];
  c.status = "UNKNOWN";
  c.notes = "Placeholder info";
  if (runtimeStatus[index] == 1) c.status = "ONLINE";
  else if (runtimeStatus[index] == 2) c.status = "OFFLINE";
}

bool buildSdIndex() {
  countPC = 0;
  memset(recordOffsets, 0, sizeof(recordOffsets));
  memset(runtimeStatus, 0, sizeof(runtimeStatus));

  if (!sdReady) return false;

  File f = SD.open("/computers.csv", FILE_READ);
  if (!f) {
    Serial.println("SD OK, but /computers.csv is missing");
    return false;
  }

  while (f.available() && countPC < MAX_PC) {
    uint32_t offset = (uint32_t)f.position();
    String line = f.readStringUntil('\n');
    if (!isDataLine(line)) continue;

    Computer temp;
    if (parseComputerLine(line, temp, countPC)) {
      recordOffsets[countPC] = offset;
      countPC++;
    }
  }
  f.close();

  if (countPC == 0) {
    Serial.println("/computers.csv contains no valid records");
    return false;
  }

  usingSdDirectory = true;
  selected = constrain(selected, 0, countPC - 1);
  Serial.printf("Indexed %d computer(s) from microSD using %u bytes of offsets\n",
                countPC, (unsigned)(countPC * sizeof(uint32_t)));
  return true;
}

bool readSdComputerFromFile(File& f, int index, Computer& c) {
  if (!usingSdDirectory || index < 0 || index >= countPC) return false;
  if (!f.seek(recordOffsets[index])) return false;
  String line = f.readStringUntil('\n');
  return parseComputerLine(line, c, index);
}

bool readComputer(int index, Computer& c) {
  if (index < 0 || index >= countPC) return false;

  if (!usingSdDirectory) {
    fallbackComputer(index, c);
    return true;
  }

  File f = SD.open("/computers.csv", FILE_READ);
  if (!f) return false;
  bool ok = readSdComputerFromFile(f, index, c);
  f.close();
  return ok;
}

void useFallbackDirectory() {
  usingSdDirectory = false;
  countPC = FALLBACK_COUNT;
  selected = constrain(selected, 0, countPC - 1);
  memset(runtimeStatus, 0, sizeof(runtimeStatus));
  Serial.println("Using built-in 5-PC fallback directory");
}

void printSdDiagnostics() {
  if (!sdReady) return;
  uint8_t type = SD.cardType();
  Serial.print("microSD mounted. Type: ");
  if (type == CARD_MMC) Serial.println("MMC");
  else if (type == CARD_SD) Serial.println("SDSC");
  else if (type == CARD_SDHC) Serial.println("SDHC/SDXC");
  else Serial.println("UNKNOWN");
  Serial.printf("Card size: %llu MB\n", SD.cardSize() / (1024ULL * 1024ULL));
}

bool initSdWithRetries() {
  digitalWrite(TFT_CS, HIGH);

  for (int attempt = 1; attempt <= 5; attempt++) {
    Serial.printf("microSD init attempt %d/5...\n", attempt);
    if (SD.begin(SD_CS, SPI, 4000000)) {
      sdReady = true;
      printSdDiagnostics();
      return true;
    }
    SD.end();
    sdReady = false;
    delay(450);
  }

  Serial.println("microSD INIT FAILED after 5 attempts");
  return false;
}

void writeComputerLine(File& f, const Computer& c) {
  f.print(c.name);   f.print('|');
  f.print(c.role);   f.print('|');
  f.print(c.host);   f.print('|');
  f.print(c.mac);    f.print('|');
  f.print(c.avatar); f.print('|');
  f.print("UNKNOWN"); f.print('|');
  f.println(c.notes);
}

// Keeps v0.4 BLE SYNC functional while the microSD remains the database.
// Only one record is held in RAM; the CSV is rewritten through a temporary file.
bool replaceSdRecord(int targetIndex, const Computer& replacement) {
  if (!sdReady || !usingSdDirectory || targetIndex < 0 || targetIndex > countPC) return false;

  SD.remove("/computers.tmp");
  File in = SD.open("/computers.csv", FILE_READ);
  File out = SD.open("/computers.tmp", FILE_WRITE);
  if (!in || !out) {
    if (in) in.close();
    if (out) out.close();
    SD.remove("/computers.tmp");
    return false;
  }

  int dataIndex = 0;
  bool replaced = false;

  while (in.available()) {
    String raw = in.readStringUntil('\n');
    String trimmed = raw;
    trimmed.trim();

    if (isDataLine(trimmed)) {
      if (dataIndex == targetIndex) {
        writeComputerLine(out, replacement);
        replaced = true;
      } else {
        out.println(raw);
      }
      dataIndex++;
    } else {
      out.println(raw);
    }
  }

  if (!replaced && targetIndex == dataIndex && dataIndex < MAX_PC) {
    writeComputerLine(out, replacement);
    replaced = true;
  }

  in.close();
  out.close();

  if (!replaced) {
    SD.remove("/computers.tmp");
    return false;
  }

  SD.remove("/computers.csv");
  if (!SD.rename("/computers.tmp", "/computers.csv")) {
    Serial.println("ERROR: could not rename computers.tmp to computers.csv");
    return false;
  }

  return buildSdIndex();
}

uint16_t bmp16(File& f) {
  uint16_t a = f.read();
  return a | (f.read() << 8);
}
uint32_t bmp32(File& f) {
  uint32_t v = 0;
  for (int i = 0; i < 4; i++) v |= ((uint32_t)f.read()) << (i * 8);
  return v;
}

void drawAvatar(const String& filename, int x, int y) {
  if (!sdReady) {
    tft.fillRoundRect(x, y, 120, 120, 8, ST77XX_MAGENTA);
    Serial.println("Avatar skipped: SD not ready");
    return;
  }

  Serial.printf("Avatar %s | free heap=%u | largest block=%u\n",
                filename.c_str(),
                ESP.getFreeHeap(),
                heap_caps_get_largest_free_block(MALLOC_CAP_8BIT));

  // Make sure the TFT releases the shared SPI bus before opening the SD file.
  digitalWrite(TFT_CS, HIGH);
  File bmp = SD.open("/" + filename, FILE_READ);
  if (!bmp) {
    tft.fillRoundRect(x, y, 120, 120, 8, ST77XX_MAGENTA);
    Serial.println("Avatar open failed: /" + filename);
    return;
  }

  if (bmp16(bmp) != 0x4D42) {
    Serial.println("Avatar is not a BMP: " + filename);
    bmp.close();
    return;
  }

  (void)bmp32(bmp);              // file size
  (void)bmp32(bmp);              // reserved
  uint32_t offset = bmp32(bmp);  // pixel-data offset
  (void)bmp32(bmp);              // DIB header size
  int32_t w = (int32_t)bmp32(bmp);
  int32_t h = (int32_t)bmp32(bmp);
  uint16_t planes = bmp16(bmp);
  uint16_t depth = bmp16(bmp);
  uint32_t compression = bmp32(bmp);

  if (w <= 0 || h == 0 || w > 240 || abs(h) > 240 ||
      depth != 24 || planes != 1 || compression != 0) {
    Serial.printf("Unsupported BMP %s: %ldx%ld, %u bpp, comp=%lu\n",
                  filename.c_str(), (long)w, (long)h, depth,
                  (unsigned long)compression);
    bmp.close();
    return;
  }

  bool bottomUp = (h > 0);
  if (h < 0) h = -h;

  const uint32_t rowSize = (w * 3 + 3) & ~3U;
  const int limitW = min((int)w, 120);
  const int limitH = min((int)h, 120);

  // Only ~600 bytes total for a 120-pixel portrait.
  uint8_t rgbRow[120 * 3];
  uint16_t pixelRow[120];

  for (int row = 0; row < limitH; row++) {
    int sourceY = bottomUp ? (h - 1 - row) : row;
    uint32_t pos = offset + (uint32_t)sourceY * rowSize;

    // SD read phase. TFT stays deselected.
    digitalWrite(TFT_CS, HIGH);
    if (!bmp.seek(pos)) {
      Serial.printf("BMP seek failed at row %d (%s)\n", row, filename.c_str());
      break;
    }

    size_t want = (size_t)limitW * 3;
    size_t got = bmp.read(rgbRow, want);
    if (got != want) {
      Serial.printf("BMP short read at row %d: got %u/%u bytes (%s)\n",
                    row, (unsigned)got, (unsigned)want, filename.c_str());
      break;
    }

    for (int col = 0; col < limitW; col++) {
      int p = col * 3;
      uint8_t b = rgbRow[p + 0];
      uint8_t g = rgbRow[p + 1];
      uint8_t r = rgbRow[p + 2];
      pixelRow[col] = tft.color565(r, g, b);
    }

    // TFT write phase. drawRGBBitmap handles TFT chip-select/transaction.
    tft.drawRGBBitmap(x, y + row, pixelRow, limitW, 1);

    if ((row & 7) == 7) yield();
  }

  bmp.close();
  digitalWrite(TFT_CS, HIGH);

  Serial.printf("Avatar finished | free heap=%u | largest block=%u\n",
                ESP.getFreeHeap(),
                heap_caps_get_largest_free_block(MALLOC_CAP_8BIT));
}

void header(const char* text) {
  tft.fillScreen(ST77XX_BLACK);
  tft.fillRect(0, 0, 240, 27, tft.color565(13, 39, 52));
  tft.setTextColor(ST77XX_WHITE);
  tft.setTextSize(2);
  tft.setCursor(8, 7);
  tft.print(text);
}

void footer(const char* txt) {
  tft.fillRect(0, 298, 240, 22, tft.color565(18, 28, 38));
  tft.setTextSize(1);
  tft.setTextColor(ST77XX_CYAN);
  tft.setCursor(6, 305);
  tft.print(txt);
}

void drawDirectory() {
  header("PC DIRECTORY");
  tft.setTextSize(1);
  tft.setCursor(8, 34);
  tft.setTextColor(bleConnected ? ST77XX_GREEN : ST77XX_YELLOW);
  tft.print(bleConnected ? "BLE manager connected" : "BLE offline / SD directory");

  const int visibleRows = 9;
  int firstVisible = selected - visibleRows / 2;
  if (firstVisible < 0) firstVisible = 0;
  if (firstVisible > countPC - visibleRows) firstVisible = max(0, countPC - visibleRows);

  File csv;
  if (usingSdDirectory) csv = SD.open("/computers.csv", FILE_READ);

  String selectedName = "UNKNOWN";
  for (int row = 0; row < visibleRows; row++) {
    int i = firstVisible + row;
    if (i >= countPC) break;

    Computer c;
    bool ok = false;
    if (usingSdDirectory && csv) ok = readSdComputerFromFile(csv, i, c);
    else if (!usingSdDirectory) { fallbackComputer(i, c); ok = true; }

    if (!ok) {
      c.name = "READ ERROR";
      c.status = "UNKNOWN";
    }

    if (i == selected) selectedName = c.name;

    int y = 55 + row * 26;
    if (i == selected) tft.fillRoundRect(5, y, 230, 24, 4, tft.color565(42, 69, 86));

    tft.setTextSize(1);
    tft.setTextColor(ST77XX_WHITE);
    tft.setCursor(11, y + 8);
    tft.print(i == selected ? "> " : "  ");
    tft.print(c.name.substring(0, 17));

    tft.setTextColor(c.status == "ONLINE" ? ST77XX_GREEN : ST77XX_YELLOW);
    tft.setCursor(183, y + 8);
    tft.print(c.status == "ONLINE" ? "ON" : "??");
  }

  if (csv) csv.close();

  footer("JOY: choose  GREEN: details");
  lcdLines("DIRECTORY", selectedName);
}

void draw() {
  if (countPC <= 0) {
    header("NO DIRECTORY");
    footer("Check microSD / computers.csv");
    lcdLines("NO DIRECTORY", "CHECK SD CARD");
    return;
  }

  if (view == DIRECTORY) {
    drawDirectory();
  }
  else if (view == DETAIL) {
    Computer c;
    if (!readComputer(selected, c)) {
      header("READ ERROR");
      footer("BACK: directory");
      lcdLines("READ ERROR", "CHECK SD CARD");
      return;
    }

    header("COMPUTER INFO");
    drawAvatar(c.avatar, 60, 34);
    tft.setTextColor(ST77XX_WHITE);
    tft.setTextSize(2);
    tft.setCursor(12, 165); tft.print(c.name.substring(0, 18));
    tft.setTextSize(1);
    tft.setCursor(12, 199); tft.print("ROLE: " + c.role);
    tft.setCursor(12, 218); tft.print("STATUS: " + c.status);
    tft.setCursor(12, 240); tft.print(c.notes.substring(0, 33));
    footer("GREEN: Wake | BLUE: STOP");
    lcdLines(c.name, c.role + " " + c.status);
  }
  else if (view == STOP_CONFIRM) {
    header("STOP REQUEST");
    tft.setTextColor(ST77XX_YELLOW); tft.setTextSize(2);
    tft.setCursor(12, 75); tft.print("SHUTDOWN MENU");
    tft.setTextSize(1); tft.setCursor(12, 115);
    tft.print("Requires password + manager approval.");
    tft.setTextSize(2);
    tft.setCursor(31, 178);
    tft.setTextColor(confirmYes ? ST77XX_WHITE : ST77XX_GREEN); tft.print("NO");
    tft.setCursor(146, 178);
    tft.setTextColor(confirmYes ? ST77XX_GREEN : ST77XX_WHITE); tft.print("YES");
    footer("JOY L/R choose; GREEN enter");
    lcdLines("CONFIRM STOP?", confirmYes ? "YES" : "NO");
  }
  else if (view == PASSWORD) {
    header("PASSCODE");
    tft.setTextColor(ST77XX_WHITE); tft.setTextSize(2);
    tft.setCursor(42, 38); tft.print("PIN: ");
    for (int n = 0; n < 4; n++) tft.print(n < typedPassword.length() ? "*" : "_");
    for (int r = 0; r < 3; r++) for (int c = 0; c < 3; c++) {
      int x = 23 + c * 70, y = 82 + r * 65;
      bool chosen = r == keypadRow && c == keypadCol;
      tft.fillRoundRect(x, y, 55, 52, 6,
                        chosen ? tft.color565(33, 130, 80) : tft.color565(45, 58, 75));
      tft.setTextColor(ST77XX_WHITE); tft.setTextSize(3);
      tft.setCursor(x + 18, y + 15); tft.print(r * 3 + c + 1);
    }
    footer("GREEN: digit | BACK: delete");
    lcdLines("ENTER TEST PIN", String(typedPassword.length()) + " / 4 digits");
  }
  else if (view == CHOOSE_SCOPE) {
    header("STOP TARGET");
    tft.setTextColor(ST77XX_WHITE); tft.setTextSize(2);
    tft.setCursor(18, 79); tft.print("Choose target:");
    tft.setTextColor(scopeChoice == 0 ? ST77XX_GREEN : ST77XX_WHITE);
    tft.setCursor(17, 140); tft.print("Selected PC");
    tft.setTextColor(scopeChoice == 1 ? ST77XX_RED : ST77XX_WHITE);
    tft.setCursor(17, 196); tft.print("ALL COMPUTERS");
    footer("UP/DOWN; GREEN: send request");
    lcdLines("STOP SCOPE", scopeChoice ? "ALL COMPUTERS" : "SELECTED ONLY");
  }
  else if (view == RESULT) {
    header("REQUEST STATUS");
    tft.setTextColor(ST77XX_CYAN); tft.setTextSize(2);
    tft.setCursor(12, 120); tft.print(resultMessage.substring(0, 18));
    footer("BACK: return to directory");
    lcdLines("REQUEST", resultMessage);
  }
}

void redraw() {
  nextDraw = millis();
  draw();
}

class ServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer*) override { bleConnected = true; }
  void onDisconnect(BLEServer*) override {
    bleConnected = false;
    BLEDevice::startAdvertising();
  }
};

class ReceiveCallbacks : public BLECharacteristicCallbacks {
  String buffer;
  void onWrite(BLECharacteristic* chr) override {
    String part = String(chr->getValue().c_str());
    for (size_t i = 0; i < part.length(); i++) {
      char c = part[i];
      if (c == '\n') {
        BleFrame frame = {0};
        buffer.toCharArray(frame.line, sizeof(frame.line));
        if (rxFrames) xQueueSend(rxFrames, &frame, 0);
        buffer = "";
      } else if (c != '\r') {
        if (buffer.length() < 239) buffer += c;
        else buffer = "";
      }
    }
  }
};

void sendLine(String msg) {
  if (!bleConnected || !txChar) return;
  msg += '\n';
  for (int i = 0; i < msg.length(); i += 20) {
    String chunk = msg.substring(i, min(i + 20, (int)msg.length()));
    txChar->setValue(chunk.c_str());
    txChar->notify();
    delay(35);
  }
}

void processLine(String line) {
  if (line == "PING") {
    sendLine("HELLO");
    return;
  }

  if (line.startsWith("SYNC|")) {
    int index = fieldAt(line, 1).toInt();
    if (index < 0 || index >= MAX_PC) return;

    Computer c;
    c.name = fieldAt(line, 2);
    c.role = fieldAt(line, 3);
    c.host = fieldAt(line, 4);
    c.mac = fieldAt(line, 5);
    c.avatar = fieldAt(line, 6);
    c.status = fieldAt(line, 7);
    c.notes = fieldAt(line, 8);

    if (c.name.length() && replaceSdRecord(index, c)) {
      redraw();
      sendLine("SYNCED|" + String(index));
    } else {
      sendLine("SYNCFAIL|" + String(index));
    }
  }
  else if (line.startsWith("STATE|")) {
    int index = fieldAt(line, 1).toInt();
    if (index >= 0 && index < countPC) {
      String state = fieldAt(line, 2);
      if (state == "ONLINE") runtimeStatus[index] = 1;
      else if (state == "OFFLINE") runtimeStatus[index] = 2;
      else runtimeStatus[index] = 0;
      redraw();
    }
  }
  else if (line.startsWith("ACK|")) {
    resultMessage = "MANAGER: " + fieldAt(line, 3);
    view = RESULT;
    redraw();
  }
}

void setupBLE() {
  rxFrames = xQueueCreate(8, sizeof(BleFrame));
  BLEDevice::init("DirectoryConsole");
  BLEServer* server = BLEDevice::createServer();
  server->setCallbacks(new ServerCallbacks());
  BLEService* service = server->createService(SERVICE_UUID);
  BLECharacteristic* rx = service->createCharacteristic(RX_UUID, BLECharacteristic::PROPERTY_WRITE);
  rx->setCallbacks(new ReceiveCallbacks());
  txChar = service->createCharacteristic(TX_UUID, BLECharacteristic::PROPERTY_NOTIFY);
  txChar->addDescriptor(new BLE2902());
  service->start();
  BLEDevice::startAdvertising();
}

void doStop() {
  view = STOP_CONFIRM;
  confirmYes = 0;
  validTone();
  redraw();
}

void backButton() {
  if (view == DIRECTORY) { errorTone(); return; }
  if (view == DETAIL) view = DIRECTORY;
  else if (view == STOP_CONFIRM) view = DETAIL;
  else if (view == PASSWORD) {
    if (typedPassword.length()) typedPassword.remove(typedPassword.length() - 1);
    else view = STOP_CONFIRM;
  }
  else if (view == CHOOSE_SCOPE) view = PASSWORD;
  else if (view == RESULT) view = DIRECTORY;
  validTone();
  redraw();
}

void pressButton() {
  if (view == DIRECTORY) {
    view = DETAIL;
    validTone();
    redraw();
  }
  else if (view == DETAIL) {
    resultMessage = bleConnected ? "WAKE REQUESTED" : "BLE OFFLINE";
    if (bleConnected) sendLine("REQ|" + String(selected) + "|WAKE");
    else errorTone();
    view = RESULT;
    redraw();
  }
  else if (view == STOP_CONFIRM) {
    if (!confirmYes) { errorTone(); view = DETAIL; }
    else { typedPassword = ""; keypadRow = 0; keypadCol = 0; view = PASSWORD; validTone(); }
    redraw();
  }
  else if (view == PASSWORD) {
    typedPassword += String(1 + keypadRow * 3 + keypadCol);
    validTone();
    if (typedPassword.length() == 4) {
      if (typedPassword == TEST_PASSWORD) {
        successTone(); scopeChoice = 0; view = CHOOSE_SCOPE;
      } else {
        typedPassword = ""; errorTone();
      }
    }
    redraw();
  }
  else if (view == CHOOSE_SCOPE) {
    if (!bleConnected) {
      resultMessage = "BLE OFFLINE";
      errorTone();
    } else {
      String target = scopeChoice ? String("ALL") : String(selected);
      sendLine("REQ|" + target + "|STOP");
      resultMessage = "AWAIT MANAGER";
      validTone();
    }
    view = RESULT;
    redraw();
  }
  else errorTone();
}

int joyDirection() {
  int dx = analogRead(JOY_X) - centerX;
  int dy = analogRead(JOY_Y) - centerY;
  if (INVERT_X) dx = -dx;
  if (INVERT_Y) dy = -dy;
  if (abs(dx) < JOY_THRESHOLD && abs(dy) < JOY_THRESHOLD) return 0;
  if (abs(dx) > abs(dy)) return dx > 0 ? 2 : 1;
  return dy > 0 ? 4 : 3;
}

void handleJoy(int dir) {
  if (view == DIRECTORY) {
    if (dir == 3) selected = max(0, selected - 1);
    if (dir == 4) selected = min(countPC - 1, selected + 1);
  }
  else if (view == STOP_CONFIRM) {
    if (dir == 1) confirmYes = 0;
    if (dir == 2) confirmYes = 1;
  }
  else if (view == PASSWORD) {
    if (dir == 1) keypadCol = max(0, keypadCol - 1);
    if (dir == 2) keypadCol = min(2, keypadCol + 1);
    if (dir == 3) keypadRow = max(0, keypadRow - 1);
    if (dir == 4) keypadRow = min(2, keypadRow + 1);
  }
  else if (view == CHOOSE_SCOPE) {
    if (dir == 3) scopeChoice = 0;
    if (dir == 4) scopeChoice = 1;
  }
  else {
    errorTone();
    return;
  }
  validTone();
  redraw();
}

void enterSleep() {
  lcdLines("POWER SAVING", "PRESS TO WAKE");
  delay(250);
  lcd.noBacklight();
  lcd.noDisplay();
  tft.fillScreen(ST77XX_BLACK);
  delay(30);
  noTone(PIEZO);
  while (digitalRead(BTN_POWER) == LOW) delay(10);
  delay(100);
  esp_sleep_enable_ext0_wakeup(GPIO_NUM_32, 0);
  esp_deep_sleep_start();
}

void pollPower() {
  bool down = digitalRead(BTN_POWER) == LOW;
  if (down && !lastPowerDown) powerHeld = millis();
  if (down && millis() - powerHeld > 1200) enterSleep();
  lastPowerDown = down;
}

void setup() {
  Serial.begin(115200);
  delay(250);

  pinMode(TFT_CS, OUTPUT); digitalWrite(TFT_CS, HIGH);
  pinMode(SD_CS, OUTPUT);  digitalWrite(SD_CS, HIGH);
  pinMode(PIEZO, OUTPUT);  noTone(PIEZO);
  pinMode(BTN_POWER, INPUT_PULLUP);
  pinMode(BTN_BACK, INPUT_PULLUP);
  pinMode(BTN_PRESS, INPUT_PULLUP);
  pinMode(BTN_STOP, INPUT_PULLUP);

  Wire.begin(I2C_SDA, I2C_SCL);
  lcd.init();
  lcd.backlight();
  lcdLines("DIRECTORY", "BOOTING...");

  SPI.begin(SPI_CLK, SPI_MISO, SPI_MOSI);
  tft.init(240, 320);
  tft.setRotation(0);
  tft.fillScreen(ST77XX_BLACK);

  Serial.printf("Boot heap: free=%u, largest=%u\n",
                ESP.getFreeHeap(),
                heap_caps_get_largest_free_block(MALLOC_CAP_8BIT));

  // Let battery/regulator + TFT settle before microSD startup.
  delay(700);

  if (initSdWithRetries() && buildSdIndex()) {
    Serial.println("microSD directory ACTIVE");
  } else {
    useFallbackDirectory();
  }

  analogReadResolution(12);
  long sx = 0, sy = 0;
  for (int i = 0; i < 70; i++) {
    sx += analogRead(JOY_X);
    sy += analogRead(JOY_Y);
    delay(3);
  }
  centerX = sx / 70;
  centerY = sy / 70;

  setupBLE();
  draw();
  successTone();

  Serial.printf("Ready heap: free=%u, minimum=%u, largest=%u\n",
                ESP.getFreeHeap(), ESP.getMinFreeHeap(),
                heap_caps_get_largest_free_block(MALLOC_CAP_8BIT));
  Serial.println("Computer Directory console v0.4 SD-streamed ready");
}

void loop() {
  pollPower();

  static bool lastBack = HIGH, lastPress = HIGH, lastStop = HIGH;
  bool back = digitalRead(BTN_BACK);
  bool press = digitalRead(BTN_PRESS);
  bool stop = digitalRead(BTN_STOP);

  if (millis() - lastButtonTime > 170) {
    if (lastBack == HIGH && back == LOW) {
      backButton(); lastButtonTime = millis();
    }
    else if (lastPress == HIGH && press == LOW) {
      pressButton(); lastButtonTime = millis();
    }
    else if (lastStop == HIGH && stop == LOW) {
      doStop(); lastButtonTime = millis();
    }
  }

  lastBack = back;
  lastPress = press;
  lastStop = stop;

  int direction = joyDirection();
  if (direction == 0) lastDirection = 0;
  else if (lastDirection == 0) {
    lastDirection = direction;
    handleJoy(direction);
  }

  if (rxFrames) {
    BleFrame frame;
    for (int k = 0; k < 3 && xQueueReceive(rxFrames, &frame, 0) == pdTRUE; k++) {
      processLine(String(frame.line));
    }
  }

  delay(12);
}
