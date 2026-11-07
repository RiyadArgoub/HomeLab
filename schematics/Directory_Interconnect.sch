<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.6.2">
  <drawing>
    <settings>
      <setting alwaysvectorfont="no" verticaltext="up"/>
    </settings>
    <grid distance="2.54" unitdist="mm" unit="mm" style="lines" multiple="1" display="no"/>
    <layers>
      <layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
      <layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
      <layer number="93" name="Pins" color="2" fill="1" visible="yes" active="yes"/>
      <layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
      <layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
      <layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
      <layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
    </layers>
    <schematic xreflabel="%F%N/%S.%C" xrefpart="/%S.%C">
      <libraries>
        <library name="PROTOTYPE_MODULES">
          <packages>
            <package name="GENERIC_ESP32_DEVKIT">
              <pad name="1" x="0.0" y="0" drill="0.8" diameter="1.8"/>
              <pad name="2" x="2.54" y="0" drill="0.8" diameter="1.8"/>
              <pad name="3" x="5.08" y="0" drill="0.8" diameter="1.8"/>
              <pad name="4" x="7.62" y="0" drill="0.8" diameter="1.8"/>
              <pad name="5" x="10.16" y="0" drill="0.8" diameter="1.8"/>
              <pad name="6" x="12.7" y="0" drill="0.8" diameter="1.8"/>
              <pad name="7" x="15.24" y="0" drill="0.8" diameter="1.8"/>
              <pad name="8" x="17.78" y="0" drill="0.8" diameter="1.8"/>
              <pad name="9" x="20.32" y="0" drill="0.8" diameter="1.8"/>
              <pad name="10" x="22.86" y="0" drill="0.8" diameter="1.8"/>
              <pad name="11" x="25.4" y="0" drill="0.8" diameter="1.8"/>
              <pad name="12" x="27.94" y="0" drill="0.8" diameter="1.8"/>
              <pad name="13" x="30.48" y="0" drill="0.8" diameter="1.8"/>
              <pad name="14" x="33.02" y="0" drill="0.8" diameter="1.8"/>
              <pad name="15" x="35.56" y="0" drill="0.8" diameter="1.8"/>
              <pad name="16" x="38.1" y="0" drill="0.8" diameter="1.8"/>
              <pad name="17" x="40.64" y="0" drill="0.8" diameter="1.8"/>
              <pad name="18" x="43.18" y="0" drill="0.8" diameter="1.8"/>
            </package>
            <package name="GENERIC_ST7789V">
              <pad name="1" x="0.0" y="0" drill="0.8" diameter="1.8"/>
              <pad name="2" x="2.54" y="0" drill="0.8" diameter="1.8"/>
              <pad name="3" x="5.08" y="0" drill="0.8" diameter="1.8"/>
              <pad name="4" x="7.62" y="0" drill="0.8" diameter="1.8"/>
              <pad name="5" x="10.16" y="0" drill="0.8" diameter="1.8"/>
              <pad name="6" x="12.7" y="0" drill="0.8" diameter="1.8"/>
              <pad name="7" x="15.24" y="0" drill="0.8" diameter="1.8"/>
              <pad name="8" x="17.78" y="0" drill="0.8" diameter="1.8"/>
            </package>
            <package name="GENERIC_MICROSD_SPI">
              <pad name="1" x="0.0" y="0" drill="0.8" diameter="1.8"/>
              <pad name="2" x="2.54" y="0" drill="0.8" diameter="1.8"/>
              <pad name="3" x="5.08" y="0" drill="0.8" diameter="1.8"/>
              <pad name="4" x="7.62" y="0" drill="0.8" diameter="1.8"/>
              <pad name="5" x="10.16" y="0" drill="0.8" diameter="1.8"/>
              <pad name="6" x="12.7" y="0" drill="0.8" diameter="1.8"/>
            </package>
            <package name="GENERIC_LCD1602_I2C">
              <pad name="1" x="0.0" y="0" drill="0.8" diameter="1.8"/>
              <pad name="2" x="2.54" y="0" drill="0.8" diameter="1.8"/>
              <pad name="3" x="5.08" y="0" drill="0.8" diameter="1.8"/>
              <pad name="4" x="7.62" y="0" drill="0.8" diameter="1.8"/>
            </package>
            <package name="GENERIC_JOYSTICK">
              <pad name="1" x="0.0" y="0" drill="0.8" diameter="1.8"/>
              <pad name="2" x="2.54" y="0" drill="0.8" diameter="1.8"/>
              <pad name="3" x="5.08" y="0" drill="0.8" diameter="1.8"/>
              <pad name="4" x="7.62" y="0" drill="0.8" diameter="1.8"/>
            </package>
            <package name="GENERIC_BUTTON_POWER">
              <pad name="1" x="0.0" y="0" drill="0.8" diameter="1.8"/>
              <pad name="2" x="2.54" y="0" drill="0.8" diameter="1.8"/>
            </package>
            <package name="GENERIC_BUTTON_BACK">
              <pad name="1" x="0.0" y="0" drill="0.8" diameter="1.8"/>
              <pad name="2" x="2.54" y="0" drill="0.8" diameter="1.8"/>
            </package>
            <package name="GENERIC_BUTTON_PRESS">
              <pad name="1" x="0.0" y="0" drill="0.8" diameter="1.8"/>
              <pad name="2" x="2.54" y="0" drill="0.8" diameter="1.8"/>
            </package>
            <package name="GENERIC_BUTTON_STOP">
              <pad name="1" x="0.0" y="0" drill="0.8" diameter="1.8"/>
              <pad name="2" x="2.54" y="0" drill="0.8" diameter="1.8"/>
            </package>
            <package name="GENERIC_PIEZO">
              <pad name="1" x="0.0" y="0" drill="0.8" diameter="1.8"/>
              <pad name="2" x="2.54" y="0" drill="0.8" diameter="1.8"/>
            </package>
          </packages>
          <symbols>
            <symbol name="ESP32_DEVKIT">
              <wire x1="-5.08" y1="-88.9" x2="22.86" y2="5.08" width="0.254" layer="94"/>
              <text x="-2.54" y="1.27" size="2.54" layer="95">&gt;NAME</text>
              <pin name="3V3" x="25.4" y="0.0" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GND" x="25.4" y="-5.08" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO23" x="25.4" y="-10.16" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO18" x="25.4" y="-15.24" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO19" x="25.4" y="-20.32" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO16" x="25.4" y="-25.4" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO17" x="25.4" y="-30.48" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO14" x="25.4" y="-35.56" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO13" x="25.4" y="-40.64" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO21" x="25.4" y="-45.72" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO22" x="25.4" y="-50.8" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO34" x="25.4" y="-55.88" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO35" x="25.4" y="-60.96" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO32" x="25.4" y="-66.04" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO33" x="25.4" y="-71.12" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO25" x="25.4" y="-76.2" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO26" x="25.4" y="-81.28" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GPIO27" x="25.4" y="-86.36" visible="pin" length="short" direction="pas" rot="R180"/>
            </symbol>
            <symbol name="ST7789V">
              <wire x1="-5.08" y1="-38.1" x2="22.86" y2="5.08" width="0.254" layer="94"/>
              <text x="-2.54" y="1.27" size="2.54" layer="95">&gt;NAME</text>
              <pin name="VCC" x="25.4" y="0.0" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GND" x="25.4" y="-5.08" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="DIN" x="25.4" y="-10.16" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="CLK" x="25.4" y="-15.24" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="CS" x="25.4" y="-20.32" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="DC" x="25.4" y="-25.4" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="RST" x="25.4" y="-30.48" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="BL" x="25.4" y="-35.56" visible="pin" length="short" direction="pas" rot="R180"/>
            </symbol>
            <symbol name="MICROSD_SPI">
              <wire x1="-5.08" y1="-27.939999999999998" x2="22.86" y2="5.08" width="0.254" layer="94"/>
              <text x="-2.54" y="1.27" size="2.54" layer="95">&gt;NAME</text>
              <pin name="VCC" x="25.4" y="0.0" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GND" x="25.4" y="-5.08" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="MOSI" x="25.4" y="-10.16" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="SCK" x="25.4" y="-15.24" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="MISO" x="25.4" y="-20.32" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="CS" x="25.4" y="-25.4" visible="pin" length="short" direction="pas" rot="R180"/>
            </symbol>
            <symbol name="LCD1602_I2C">
              <wire x1="-5.08" y1="-17.78" x2="22.86" y2="5.08" width="0.254" layer="94"/>
              <text x="-2.54" y="1.27" size="2.54" layer="95">&gt;NAME</text>
              <pin name="VCC" x="25.4" y="0.0" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GND" x="25.4" y="-5.08" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="SDA" x="25.4" y="-10.16" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="SCL" x="25.4" y="-15.24" visible="pin" length="short" direction="pas" rot="R180"/>
            </symbol>
            <symbol name="JOYSTICK">
              <wire x1="-5.08" y1="-17.78" x2="22.86" y2="5.08" width="0.254" layer="94"/>
              <text x="-2.54" y="1.27" size="2.54" layer="95">&gt;NAME</text>
              <pin name="VCC" x="25.4" y="0.0" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GND" x="25.4" y="-5.08" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="VRX" x="25.4" y="-10.16" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="VRY" x="25.4" y="-15.24" visible="pin" length="short" direction="pas" rot="R180"/>
            </symbol>
            <symbol name="BUTTON_POWER">
              <wire x1="-5.08" y1="-10.16" x2="22.86" y2="5.08" width="0.254" layer="94"/>
              <text x="-2.54" y="1.27" size="2.54" layer="95">&gt;NAME</text>
              <pin name="GPIO" x="25.4" y="0.0" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GND" x="25.4" y="-5.08" visible="pin" length="short" direction="pas" rot="R180"/>
            </symbol>
            <symbol name="BUTTON_BACK">
              <wire x1="-5.08" y1="-10.16" x2="22.86" y2="5.08" width="0.254" layer="94"/>
              <text x="-2.54" y="1.27" size="2.54" layer="95">&gt;NAME</text>
              <pin name="GPIO" x="25.4" y="0.0" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GND" x="25.4" y="-5.08" visible="pin" length="short" direction="pas" rot="R180"/>
            </symbol>
            <symbol name="BUTTON_PRESS">
              <wire x1="-5.08" y1="-10.16" x2="22.86" y2="5.08" width="0.254" layer="94"/>
              <text x="-2.54" y="1.27" size="2.54" layer="95">&gt;NAME</text>
              <pin name="GPIO" x="25.4" y="0.0" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GND" x="25.4" y="-5.08" visible="pin" length="short" direction="pas" rot="R180"/>
            </symbol>
            <symbol name="BUTTON_STOP">
              <wire x1="-5.08" y1="-10.16" x2="22.86" y2="5.08" width="0.254" layer="94"/>
              <text x="-2.54" y="1.27" size="2.54" layer="95">&gt;NAME</text>
              <pin name="GPIO" x="25.4" y="0.0" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="GND" x="25.4" y="-5.08" visible="pin" length="short" direction="pas" rot="R180"/>
            </symbol>
            <symbol name="PIEZO">
              <wire x1="-5.08" y1="-10.16" x2="22.86" y2="5.08" width="0.254" layer="94"/>
              <text x="-2.54" y="1.27" size="2.54" layer="95">&gt;NAME</text>
              <pin name="PLUS" x="25.4" y="0.0" visible="pin" length="short" direction="pas" rot="R180"/>
              <pin name="MINUS" x="25.4" y="-5.08" visible="pin" length="short" direction="pas" rot="R180"/>
            </symbol>
          </symbols>
          <devicesets>
            <deviceset name="ESP32_DEVKIT" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="ESP32_DEVKIT" x="0" y="0" addlevel="always"/>
              </gates>
              <devices>
                <device name="" package="GENERIC_ESP32_DEVKIT">
                  <connects>
                    <connect gate="G$1" pin="3V3" pad="1"/>
                    <connect gate="G$1" pin="GND" pad="2"/>
                    <connect gate="G$1" pin="GPIO23" pad="3"/>
                    <connect gate="G$1" pin="GPIO18" pad="4"/>
                    <connect gate="G$1" pin="GPIO19" pad="5"/>
                    <connect gate="G$1" pin="GPIO16" pad="6"/>
                    <connect gate="G$1" pin="GPIO17" pad="7"/>
                    <connect gate="G$1" pin="GPIO14" pad="8"/>
                    <connect gate="G$1" pin="GPIO13" pad="9"/>
                    <connect gate="G$1" pin="GPIO21" pad="10"/>
                    <connect gate="G$1" pin="GPIO22" pad="11"/>
                    <connect gate="G$1" pin="GPIO34" pad="12"/>
                    <connect gate="G$1" pin="GPIO35" pad="13"/>
                    <connect gate="G$1" pin="GPIO32" pad="14"/>
                    <connect gate="G$1" pin="GPIO33" pad="15"/>
                    <connect gate="G$1" pin="GPIO25" pad="16"/>
                    <connect gate="G$1" pin="GPIO26" pad="17"/>
                    <connect gate="G$1" pin="GPIO27" pad="18"/>
                  </connects>
                  <technologies>
                    <technology name=""/>
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="ST7789V" prefix="DS" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="ST7789V" x="0" y="0" addlevel="always"/>
              </gates>
              <devices>
                <device name="" package="GENERIC_ST7789V">
                  <connects>
                    <connect gate="G$1" pin="VCC" pad="1"/>
                    <connect gate="G$1" pin="GND" pad="2"/>
                    <connect gate="G$1" pin="DIN" pad="3"/>
                    <connect gate="G$1" pin="CLK" pad="4"/>
                    <connect gate="G$1" pin="CS" pad="5"/>
                    <connect gate="G$1" pin="DC" pad="6"/>
                    <connect gate="G$1" pin="RST" pad="7"/>
                    <connect gate="G$1" pin="BL" pad="8"/>
                  </connects>
                  <technologies>
                    <technology name=""/>
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="MICROSD_SPI" prefix="J" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="MICROSD_SPI" x="0" y="0" addlevel="always"/>
              </gates>
              <devices>
                <device name="" package="GENERIC_MICROSD_SPI">
                  <connects>
                    <connect gate="G$1" pin="VCC" pad="1"/>
                    <connect gate="G$1" pin="GND" pad="2"/>
                    <connect gate="G$1" pin="MOSI" pad="3"/>
                    <connect gate="G$1" pin="SCK" pad="4"/>
                    <connect gate="G$1" pin="MISO" pad="5"/>
                    <connect gate="G$1" pin="CS" pad="6"/>
                  </connects>
                  <technologies>
                    <technology name=""/>
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="LCD1602_I2C" prefix="DS" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="LCD1602_I2C" x="0" y="0" addlevel="always"/>
              </gates>
              <devices>
                <device name="" package="GENERIC_LCD1602_I2C">
                  <connects>
                    <connect gate="G$1" pin="VCC" pad="1"/>
                    <connect gate="G$1" pin="GND" pad="2"/>
                    <connect gate="G$1" pin="SDA" pad="3"/>
                    <connect gate="G$1" pin="SCL" pad="4"/>
                  </connects>
                  <technologies>
                    <technology name=""/>
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="JOYSTICK" prefix="J" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="JOYSTICK" x="0" y="0" addlevel="always"/>
              </gates>
              <devices>
                <device name="" package="GENERIC_JOYSTICK">
                  <connects>
                    <connect gate="G$1" pin="VCC" pad="1"/>
                    <connect gate="G$1" pin="GND" pad="2"/>
                    <connect gate="G$1" pin="VRX" pad="3"/>
                    <connect gate="G$1" pin="VRY" pad="4"/>
                  </connects>
                  <technologies>
                    <technology name=""/>
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="BUTTON_POWER" prefix="SW" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="BUTTON_POWER" x="0" y="0" addlevel="always"/>
              </gates>
              <devices>
                <device name="" package="GENERIC_BUTTON_POWER">
                  <connects>
                    <connect gate="G$1" pin="GPIO" pad="1"/>
                    <connect gate="G$1" pin="GND" pad="2"/>
                  </connects>
                  <technologies>
                    <technology name=""/>
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="BUTTON_BACK" prefix="SW" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="BUTTON_BACK" x="0" y="0" addlevel="always"/>
              </gates>
              <devices>
                <device name="" package="GENERIC_BUTTON_BACK">
                  <connects>
                    <connect gate="G$1" pin="GPIO" pad="1"/>
                    <connect gate="G$1" pin="GND" pad="2"/>
                  </connects>
                  <technologies>
                    <technology name=""/>
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="BUTTON_PRESS" prefix="SW" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="BUTTON_PRESS" x="0" y="0" addlevel="always"/>
              </gates>
              <devices>
                <device name="" package="GENERIC_BUTTON_PRESS">
                  <connects>
                    <connect gate="G$1" pin="GPIO" pad="1"/>
                    <connect gate="G$1" pin="GND" pad="2"/>
                  </connects>
                  <technologies>
                    <technology name=""/>
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="BUTTON_STOP" prefix="SW" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="BUTTON_STOP" x="0" y="0" addlevel="always"/>
              </gates>
              <devices>
                <device name="" package="GENERIC_BUTTON_STOP">
                  <connects>
                    <connect gate="G$1" pin="GPIO" pad="1"/>
                    <connect gate="G$1" pin="GND" pad="2"/>
                  </connects>
                  <technologies>
                    <technology name=""/>
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="PIEZO" prefix="BZ" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="PIEZO" x="0" y="0" addlevel="always"/>
              </gates>
              <devices>
                <device name="" package="GENERIC_PIEZO">
                  <connects>
                    <connect gate="G$1" pin="PLUS" pad="1"/>
                    <connect gate="G$1" pin="MINUS" pad="2"/>
                  </connects>
                  <technologies>
                    <technology name=""/>
                  </technologies>
                </device>
              </devices>
            </deviceset>
          </devicesets>
        </library>
      </libraries>
      <attributes/>
      <variantdefs/>
      <classes>
        <class number="0" name="default" width="0" drill="0"/>
      </classes>
      <parts>
        <part name="U1" library="PROTOTYPE_MODULES" deviceset="ESP32_DEVKIT" device=""/>
        <part name="DS1" library="PROTOTYPE_MODULES" deviceset="ST7789V" device=""/>
        <part name="J1" library="PROTOTYPE_MODULES" deviceset="MICROSD_SPI" device=""/>
        <part name="DS2" library="PROTOTYPE_MODULES" deviceset="LCD1602_I2C" device=""/>
        <part name="J2" library="PROTOTYPE_MODULES" deviceset="JOYSTICK" device=""/>
        <part name="SW1" library="PROTOTYPE_MODULES" deviceset="BUTTON_POWER" device=""/>
        <part name="SW2" library="PROTOTYPE_MODULES" deviceset="BUTTON_BACK" device=""/>
        <part name="SW3" library="PROTOTYPE_MODULES" deviceset="BUTTON_PRESS" device=""/>
        <part name="SW4" library="PROTOTYPE_MODULES" deviceset="BUTTON_STOP" device=""/>
        <part name="BZ1" library="PROTOTYPE_MODULES" deviceset="PIEZO" device=""/>
      </parts>
      <sheets>
        <sheet>
          <plain>
            <text x="12.7" y="287" size="4.0" layer="97">ESP32 COMPUTER DIRECTORY CONSOLE</text>
            <text x="12.7" y="280.0" size="1.8" layer="97">MODULE-LEVEL WIRING SCHEMATIC -- NOT A PCB FABRICATION DESIGN</text>
            <text x="12.7" y="275.4" size="1.8" layer="97">IMPORTANT: LCD 1602 I2C only attach directly to 3.3V if module supports 3.3V.</text>
            <text x="12.7" y="270.8" size="1.8" layer="97">If I2C LCD board requires 5V, insert bidirectional level shifter on SDA/SCL.</text>
            <text x="12.7" y="266.2" size="1.8" layer="97">ST7789 BL pin is NOT shown as powered: verify module backlight requirements.</text>
            <text x="12.7" y="261.6" size="1.8" layer="97">All GPIO logic is 3.3V. Separate suitable 5V USB power powers ESP32 DevKit.</text>
            <text x="12.7" y="257.0" size="1.8" layer="97">Red POWER button triggers DEEP SLEEP; it does not physically cut the supply.</text>
          </plain>
          <instances>
            <instance part="U1" gate="G$1" x="15" y="264" rot="R0" smashed="no"/>
            <instance part="DS1" gate="G$1" x="115" y="264" rot="R0" smashed="no"/>
            <instance part="J1" gate="G$1" x="115" y="196" rot="R0" smashed="no"/>
            <instance part="DS2" gate="G$1" x="115" y="135" rot="R0" smashed="no"/>
            <instance part="J2" gate="G$1" x="115" y="96" rot="R0" smashed="no"/>
            <instance part="SW1" gate="G$1" x="198" y="259" rot="R0" smashed="no"/>
            <instance part="SW2" gate="G$1" x="198" y="227" rot="R0" smashed="no"/>
            <instance part="SW3" gate="G$1" x="198" y="195" rot="R0" smashed="no"/>
            <instance part="SW4" gate="G$1" x="198" y="163" rot="R0" smashed="no"/>
            <instance part="BZ1" gate="G$1" x="198" y="125" rot="R0" smashed="no"/>
          </instances>
          <busses/>
          <nets>
            <net name="P3V3" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="3V3"/>
                <wire x1="40.4" y1="264.0" x2="50.56" y2="264.0" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="264.0" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS1" gate="G$1" pin="VCC"/>
                <wire x1="140.4" y1="264.0" x2="150.56" y2="264.0" width="0.1524" layer="91"/>
                <label x="148.02" y="264.0" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="J1" gate="G$1" pin="VCC"/>
                <wire x1="140.4" y1="196.0" x2="150.56" y2="196.0" width="0.1524" layer="91"/>
                <label x="148.02" y="196.0" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS2" gate="G$1" pin="VCC"/>
                <wire x1="140.4" y1="135.0" x2="150.56" y2="135.0" width="0.1524" layer="91"/>
                <label x="148.02" y="135.0" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="J2" gate="G$1" pin="VCC"/>
                <wire x1="140.4" y1="96.0" x2="150.56" y2="96.0" width="0.1524" layer="91"/>
                <label x="148.02" y="96.0" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="GND" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GND"/>
                <wire x1="40.4" y1="258.92" x2="50.56" y2="258.92" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="258.92" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS1" gate="G$1" pin="GND"/>
                <wire x1="140.4" y1="258.92" x2="150.56" y2="258.92" width="0.1524" layer="91"/>
                <label x="148.02" y="258.92" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="J1" gate="G$1" pin="GND"/>
                <wire x1="140.4" y1="190.92" x2="150.56" y2="190.92" width="0.1524" layer="91"/>
                <label x="148.02" y="190.92" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS2" gate="G$1" pin="GND"/>
                <wire x1="140.4" y1="129.92" x2="150.56" y2="129.92" width="0.1524" layer="91"/>
                <label x="148.02" y="129.92" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="J2" gate="G$1" pin="GND"/>
                <wire x1="140.4" y1="90.92" x2="150.56" y2="90.92" width="0.1524" layer="91"/>
                <label x="148.02" y="90.92" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="SW1" gate="G$1" pin="GND"/>
                <wire x1="223.4" y1="253.92" x2="233.56" y2="253.92" width="0.1524" layer="91"/>
                <label x="231.02" y="253.92" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="SW2" gate="G$1" pin="GND"/>
                <wire x1="223.4" y1="221.92" x2="233.56" y2="221.92" width="0.1524" layer="91"/>
                <label x="231.02" y="221.92" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="SW3" gate="G$1" pin="GND"/>
                <wire x1="223.4" y1="189.92" x2="233.56" y2="189.92" width="0.1524" layer="91"/>
                <label x="231.02" y="189.92" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="SW4" gate="G$1" pin="GND"/>
                <wire x1="223.4" y1="157.92" x2="233.56" y2="157.92" width="0.1524" layer="91"/>
                <label x="231.02" y="157.92" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="BZ1" gate="G$1" pin="MINUS"/>
                <wire x1="223.4" y1="119.92" x2="233.56" y2="119.92" width="0.1524" layer="91"/>
                <label x="231.02" y="119.92" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="SPI_MOSI_GPIO23" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO23"/>
                <wire x1="40.4" y1="253.84" x2="50.56" y2="253.84" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="253.84" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS1" gate="G$1" pin="DIN"/>
                <wire x1="140.4" y1="253.84" x2="150.56" y2="253.84" width="0.1524" layer="91"/>
                <label x="148.02" y="253.84" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="J1" gate="G$1" pin="MOSI"/>
                <wire x1="140.4" y1="185.84" x2="150.56" y2="185.84" width="0.1524" layer="91"/>
                <label x="148.02" y="185.84" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="SPI_SCK_GPIO18" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO18"/>
                <wire x1="40.4" y1="248.76" x2="50.56" y2="248.76" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="248.76" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS1" gate="G$1" pin="CLK"/>
                <wire x1="140.4" y1="248.76" x2="150.56" y2="248.76" width="0.1524" layer="91"/>
                <label x="148.02" y="248.76" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="J1" gate="G$1" pin="SCK"/>
                <wire x1="140.4" y1="180.76" x2="150.56" y2="180.76" width="0.1524" layer="91"/>
                <label x="148.02" y="180.76" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="SPI_MISO_GPIO19" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO19"/>
                <wire x1="40.4" y1="243.68" x2="50.56" y2="243.68" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="243.68" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="J1" gate="G$1" pin="MISO"/>
                <wire x1="140.4" y1="175.68" x2="150.56" y2="175.68" width="0.1524" layer="91"/>
                <label x="148.02" y="175.68" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="TFT_CS_GPIO16" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO16"/>
                <wire x1="40.4" y1="238.6" x2="50.56" y2="238.6" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="238.6" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS1" gate="G$1" pin="CS"/>
                <wire x1="140.4" y1="243.68" x2="150.56" y2="243.68" width="0.1524" layer="91"/>
                <label x="148.02" y="243.68" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="TFT_DC_GPIO17" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO17"/>
                <wire x1="40.4" y1="233.52" x2="50.56" y2="233.52" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="233.52" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS1" gate="G$1" pin="DC"/>
                <wire x1="140.4" y1="238.6" x2="150.56" y2="238.6" width="0.1524" layer="91"/>
                <label x="148.02" y="238.6" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="TFT_RST_GPIO14" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO14"/>
                <wire x1="40.4" y1="228.44" x2="50.56" y2="228.44" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="228.44" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS1" gate="G$1" pin="RST"/>
                <wire x1="140.4" y1="233.52" x2="150.56" y2="233.52" width="0.1524" layer="91"/>
                <label x="148.02" y="233.52" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="SD_CS_GPIO13" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO13"/>
                <wire x1="40.4" y1="223.36" x2="50.56" y2="223.36" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="223.36" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="J1" gate="G$1" pin="CS"/>
                <wire x1="140.4" y1="170.6" x2="150.56" y2="170.6" width="0.1524" layer="91"/>
                <label x="148.02" y="170.6" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="I2C_SDA_GPIO21" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO21"/>
                <wire x1="40.4" y1="218.28" x2="50.56" y2="218.28" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="218.28" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS2" gate="G$1" pin="SDA"/>
                <wire x1="140.4" y1="124.84" x2="150.56" y2="124.84" width="0.1524" layer="91"/>
                <label x="148.02" y="124.84" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="I2C_SCL_GPIO22" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO22"/>
                <wire x1="40.4" y1="213.2" x2="50.56" y2="213.2" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="213.2" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="DS2" gate="G$1" pin="SCL"/>
                <wire x1="140.4" y1="119.76" x2="150.56" y2="119.76" width="0.1524" layer="91"/>
                <label x="148.02" y="119.76" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="JOY_X_GPIO34" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO34"/>
                <wire x1="40.4" y1="208.12" x2="50.56" y2="208.12" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="208.12" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="J2" gate="G$1" pin="VRX"/>
                <wire x1="140.4" y1="85.84" x2="150.56" y2="85.84" width="0.1524" layer="91"/>
                <label x="148.02" y="85.84" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="JOY_Y_GPIO35" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO35"/>
                <wire x1="40.4" y1="203.04" x2="50.56" y2="203.04" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="203.04" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="J2" gate="G$1" pin="VRY"/>
                <wire x1="140.4" y1="80.76" x2="150.56" y2="80.76" width="0.1524" layer="91"/>
                <label x="148.02" y="80.76" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="POWER_GPIO32" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO32"/>
                <wire x1="40.4" y1="197.95999999999998" x2="50.56" y2="197.95999999999998" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="197.95999999999998" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="SW1" gate="G$1" pin="GPIO"/>
                <wire x1="223.4" y1="259.0" x2="233.56" y2="259.0" width="0.1524" layer="91"/>
                <label x="231.02" y="259.0" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="BACK_GPIO33" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO33"/>
                <wire x1="40.4" y1="192.88" x2="50.56" y2="192.88" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="192.88" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="SW2" gate="G$1" pin="GPIO"/>
                <wire x1="223.4" y1="227.0" x2="233.56" y2="227.0" width="0.1524" layer="91"/>
                <label x="231.02" y="227.0" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="PRESS_GPIO25" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO25"/>
                <wire x1="40.4" y1="187.8" x2="50.56" y2="187.8" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="187.8" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="SW3" gate="G$1" pin="GPIO"/>
                <wire x1="223.4" y1="195.0" x2="233.56" y2="195.0" width="0.1524" layer="91"/>
                <label x="231.02" y="195.0" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="STOP_GPIO26" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO26"/>
                <wire x1="40.4" y1="182.72" x2="50.56" y2="182.72" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="182.72" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="SW4" gate="G$1" pin="GPIO"/>
                <wire x1="223.4" y1="163.0" x2="233.56" y2="163.0" width="0.1524" layer="91"/>
                <label x="231.02" y="163.0" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
            <net name="PIEZO_GPIO27" class="0">
              <segment>
                <pinref part="U1" gate="G$1" pin="GPIO27"/>
                <wire x1="40.4" y1="177.64" x2="50.56" y2="177.64" width="0.1524" layer="91"/>
                <label x="48.019999999999996" y="177.64" size="1.27" layer="95" rot="R0"/>
              </segment>
              <segment>
                <pinref part="BZ1" gate="G$1" pin="PLUS"/>
                <wire x1="223.4" y1="125.0" x2="233.56" y2="125.0" width="0.1524" layer="91"/>
                <label x="231.02" y="125.0" size="1.27" layer="95" rot="R0"/>
              </segment>
            </net>
          </nets>
        </sheet>
      </sheets>
    </schematic>
  </drawing>
</eagle>
