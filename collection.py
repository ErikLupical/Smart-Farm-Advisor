from machine import Pin, ADC
from time import sleep
import dht
import network
from umqtt.robust import MQTTClient
from config import WIFI_SSID, WIFI_PASS, MQTT_BROKER, MQTT_USER, MQTT_PASS

led_wifi = Pin(2, Pin.OUT)
led_wifi.value(1)  # turn the red led off
led_iot = Pin(12, Pin.OUT)
led_iot.value(1)   # turn the green led off

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    sleep(0.5)
led_wifi.value(0)  # turn the red led on

mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
mqtt.connect()
led_iot.value(0)   # turn the green led on

def res_to_lux(resistance):
    return 562.3413/(resistance*0.001) ** 1.25

h_sensor = dht.DHT11(Pin(32))
s_sensor = ADC(Pin(34))
l_sensor = ADC(Pin(36))

while True:
  try:
    sleep(2)
    
    h_sensor.measure()
    
    # temperature
    temp = h_sensor.temperature()
    temp_f = temp * (9/5) + 32.0
    print('Temperature: %3.1f C' %temp)
    print('Temperature: %3.1f F' %temp_f)
    
    # humidity
    hum = h_sensor.humidity()
    print('Humidity: %3.1f %%' %hum)
    
    # light
    R_1 = 33000
    V_S = 3.3
    V_a = (l_sensor.read_uv()/1000000)
    R_LDR = (V_a*R_1)/(V_S-V_a)
    light = res_to_lux(R_LDR)
    print('Light: %3.1f lux' %light)
    
    print()
    
  except OSError as e:
    print('Failed to read sensor.')