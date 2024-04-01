################################################################################################################################################################################################
#   
#   New features:
#   - New plot.csv format. Timestamp,value.
#   - Minor changes to matplotlib graph.
#
#   IMPORTANT:  - Make shure, you start the DMM in continuous mode! (from the manual: To disable the Auto Power Off function, hold down the SEL button when turning on the product, you will hear five beeps if you have successfully disabled the function.
#               - Works just with adminitrator rights!!! (https://github.com/riktw/AN9002_info/issues/1#issuecomment-1155512464)
#               - Use the ESC button to stop logging 
#        
#   When I got my AN9002 from Banggood (220628), I considered it as DOA (couldn't connect to Android, Windows, or Ubuntu). 
#   Complained (but got of course no answer) and started reading about BLE. I have to admit the complaint was wrong.
#   I stumbled in my research over https://github.com/riktw/AN9002_info and it worked just amazingly from scratch. @riktw, thanks a lot!
#   My main case of application for the script are measurements on my 3D printer.
#           
#   Read https://github.com/ludwich66/Bluetooth-DMM/wiki and https://justanotherelectronicsblog.com/?p=930 for background information.           
#           
#   Lisence: riktw https://github.com/riktw/AN9002_info/blob/main/LICENSE, hcet14 beerware.          
#   All changes in 'an9002_data_logger.py' and 'multimeter.py' (compared to originals from riktw) are marked with #hcet14.        
#   Important code parts are marked with ##hcet14 (just one)!        
#           
#   Runs for me with AN9002 and Bluetooth activated:        
#   - Ubuntu        
#   Ubuntu 20.04.4 LTS        
#   Python 3.8.10        
#   - Windows          
#   10 Pro 10.0.19043 Build 19043        
#   Python 3.10.5        
#           
#   Remarks/bugs: 
#   -I get this warning under Ubuntu:
#   QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-root'     
#   Don't know why and I don't care. Maybe https://unix.stackexchange.com/questions/382789/qstandardpaths-xdg-runtime-dir-not-set-defaulting-to-tmp-runtime-root-when explains it.        
#   -I get this warning under Windows:        
#   LogData.py:143: DeprecationWarning: There is no current event loop loop = asyncio.get_event_loop() (I didn't change line 143)
#   - Windows: The generated csv file has empty lines between every entry.    
#           
#   Keep in mind that I'm just a code snippets collector and no python programmer (you'll find out...)!       
#           
#   version_240401       
#           
################################################################################################################################################################################################

#import sys                                                                                                             #hcet14 not needed
import asyncio  
#import platform                                                                                                        #hcet14 not needed
#import logging                                                                                                         #hcet14 not needed
import keyboard
import csv

from multimeter import *
import matplotlib.pyplot as plt
from bleak import BleakClient
from datetime import datetime, timedelta                                                                                #hcet14

address = "4c:72:74:6a:8a:f6"                                                                                           ##hcet14 change to your MAC address!


CHARACTERISTIC_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"                                                            #hcet14 I don't understand riktw's original comment. I didn't change this UUID.

dataGraph = []
realtimes = []                                                                                                          #hcet14
multimeter = AN9002()
lastDisplayedUnit = ""

def notification_handler(sender, data):
    global dataGraph
    global multimeter
    global lastDisplayedUnit
    global displayedData                                                                                                #hcet14  
    """Simple notification handler which prints the data received."""
    #print("Data multimeter: {0}".format(data.hex(' ') ))
    multimeter.SetMeasuredValue(data)
    displayedData = multimeter.GetDisplayedValue()
    if multimeter.overloadFlag:
        displayedData = -1                                                                                              #hcet14 the matplotlib graph doesn't loose the x-axis anymore, when 'O.L' is shown on the display if the input is out of range.
        print("Overload")
        
    unit = multimeter.GetDisplayedUnit()
    if lastDisplayedUnit == "":
        lastDisplayedUnit = unit

    if unit != lastDisplayedUnit:
        lastDisplayedUnit = unit
        dataGraph.clear()
        realtimes.clear()                                                                                               #hcet14
        plt.clf()
    
    now = datetime.now()                                                                                                #hcet14
    realtimes.append(now.strftime("%H:%M:%S.%f"))                                                                       #hcet14   
    dataGraph.append(displayedData)                                                                                     
    plt.xlabel('Number of measurements', rotation=0, labelpad=5)                                                        #hcet14
    plt.ylabel(unit, rotation=0, labelpad=10)                                                                           #hcet14
    print(str(displayedData) + " " + unit)  

async def run(address):
    client = BleakClient(address)
     
    try:
        await client.connect()
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        
        while(1):
            if keyboard.is_pressed("esc"):                                                                              #hcet14 change if you want to use another key to stop logging
                print("an9002.csv will be stored in the directory, where you started 'an9002_data_logger.py'!");        #hcet14
                break;

            else:                
                plt.plot(dataGraph, color='b')
                plt.draw()
                plt.pause(0.1)
                await asyncio.sleep(0.5)       
                print("Connection ==",client.is_connected)                                                              #hcet14
                print("lastDisplayedUnit ==",lastDisplayedUnit)                                                         #hcet14
                
    except asyncio.CancelledError as e:                                                                                 #hcet14 this is never used
        print("Stopping asyncio.sleep(0.5)")                                                                            #hcet14 this is never used
                                                                                                    
    finally:                                                                                        
        await client.stop_notify(CHARACTERISTIC_UUID)                                               
        await client.disconnect()                                                                                                    
                                                                                                    
if __name__ == "__main__":                                                                          
    loop = asyncio.get_event_loop()                                                                 
    loop.set_debug(False)                                                                           
    loop.run_until_complete(run(address))                                                           
                                                                                                    
    with open('an9002.csv', 'w') as f:                                                                                  #hcet14
        wr = csv.writer(f)                                                                                 
                                                                                                           
        if lastDisplayedUnit == '°C' or lastDisplayedUnit == '°F':                                                        #hcet14
            wr.writerow(['Time[hh:mm:ss.µs]', 'Temperature[' + lastDisplayedUnit + ']'])                                #hcet14
        elif lastDisplayedUnit == 'nF':                                                                                 #hcet14
            wr.writerow(['Time[hh:mm:ss.µs]', 'Capacity[' + lastDisplayedUnit + ']'])                                   #hcet14
        elif lastDisplayedUnit == 'mV' or lastDisplayedUnit == 'V':                                                     #hcet14
            wr.writerow(['Time[hh:mm:ss.µs]', 'Voltage[' + lastDisplayedUnit + ']'])                                    #hcet14
        elif lastDisplayedUnit == 'µA' or lastDisplayedUnit == 'mA' or lastDisplayedUnit == 'A':                        #hcet14
            wr.writerow(['Time[hh:mm:ss.µs]', 'Current[' + lastDisplayedUnit + ']'])                                    #hcet14    
        else:                                                                                                           #hcet14
            lastDisplayedUnit == 'Ω' or lastDisplayedUnit == 'kΩ' or lastDisplayedUnit == 'MΩ'                          #hcet14
            wr.writerow(['Time[hh:mm:ss.µs]', 'Resistance[' + lastDisplayedUnit + ']'])                                 #hcet14    
                                                                                                           
        wr.writerows(zip(realtimes, dataGraph))                                                                         #hcet14
                                                                                                    