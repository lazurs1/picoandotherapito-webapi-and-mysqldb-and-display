from machine import Pin, I2C
from time import sleep
import bmp280
import dht
import network
import urequests
 
ssid = 'FDI-IT' #'lazurs2.4'
password = 'Carrot.panic99' #'Donna01!'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
# PICO - Pins
# sda=Pin(16), scl=Pin(17) 
sda=machine.Pin(0)
scl=machine.Pin(1)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
dht22sensor = dht.DHT22(Pin(2))
dht11sensor = dht.DHT22(Pin(19))
while True:
    bme = bmp280.BME280(i2c=i2c)
    temp = bme.temperature
    ## hum = bme.humidity      No humidity in BMP280
    pres = bme.pressure
    # tempf temp Fahrenheit
    tempfbmp280= round((bme.read_temperature()/100) * (9/5) + 32,2)
    #print(type(tempf))
    #print(bme.read_temperature())
    #print(tempf)
    tempf = str(round(tempfbmp280, 2)) + 'F'
    print('BMP280 Temperature:', tempf, '  Pressure: ',pres)
    #print('Humidity: ', hum)
    dht22sensor.measure()
    #dht11temp =  dht11sensor.temperature()/* 1.8 + 32
    dht22temp = (dht22sensor.temperature()*9/5)+32
    dht22hum = dht22sensor.humidity()
    print("DHT-22 Temperature: {}°F   Humidity: {:.0f}% ".format(dht22temp, dht22hum))
    
    tempdiffdht22bmp280=tempfbmp280 - dht22temp
    #print("Temp Diff: ", tempdiffdht22bmp280)
    dht11sensor.measure()
    #dht11temp =  dht11sensor.temperature()/* 1.8 + 32
    dht11temp = 0 #(dht11sensor.temperature()*9/5)+32
    dht11hum = 0 #dht11sensor.humidity()
    #print("Temp: " + str(dht11temp))
    #print("Humidity: {:.0f}% " . format(dht11hum))
    #print ("Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(dht11temp, dht11hum))
    #print("DHT-11 Temperature: {}°F   Humidity: {}%" .format(dht11temp, dht11hum))
    #print("https://python.faith/dax/posttest.php?Devices=testPIPICOW&Sensor_name=DHT11&Sensor_Humidity=" + str(dht11hum))
    #+ "&Sensor_Temp=" + dht11temp + "&DateTime=12/27/2002&Sensor2_name=DHT22&Sensor2_Humidity=" + dht22hum + "&Sensor2_Temp=" + dht22temp)
    pushData="https://python.faith/dax/posttest.php?Devices=Novi Server Room PI Pico W&Sensor_name=BMP280&Sensor_Humidity=" + str(dht11hum) + "&Sensor_Temp=" + str(tempfbmp280) + "&DateTime=12/27/2002&Sensor2_name=DHT22&Sensor2_Humidity=" + str(dht22hum) + "&Sensor2_Temp=" + str(dht22temp)
    #print(pushData)
    r = urequests.get(pushData)
    #print(r.content)
    r.close()
    sleep(3)
