
import socket
import paho.mqtt.client as mqtt
import json
import argparse

from time import sleep
import board
import neopixel

ap = argparse.ArgumentParser()
ap.add_argument("-h", "--host", required=True,
        help="MQTT broker address")
ap.add_argument("-p", "--port", default=1883,
        help="MQTT broker port"")
ap.add_argument("-u", "--username",
	help="MQTT broker user name")
ap.add_argument("-P", "--password",
	help="MQTT broker password")
args = vars(ap.parse_args())


hostname = socket.gethostname()
print('Initializing ' + hostname)


pixels = neopixel.NeoPixel(board.D18, 30)
#pixels[0] = (255, 255, 255)


def led_on(color, brightness=1):
	pixels.brightness = brightness
	pixels.fill(color)


def led_off():
 pixels.fill((0, 0, 0))


def led_strobe(color, interval, duration):
	counter = 0
	while True:
		if counter % 2 == 0:
			pixels.fill(color)
		else:
			pixels.fill((0, 0, 0))
		counter += 1
		sleep(interval)


def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	print(hostname)
	# cameraConnectionPayload =  json.dumps({"name" : hostname, **data})
	# client.publish('leds/settings/' + hostname, cameraConnectionPayload, retain=True)
	client.subscribe('LED/' + hostname + '/#')
	#client.subscribe('LED/#')


def on_message(client, userdata, msg):
	payload = msg.payload.decode("utf-8")
	print(payload)
	if msg.topic == 'LED/' + hostname + '/on':
		print('turn led on')
		led_on((100,147,41), 0.2)
		#led_strobe((100,100,100), 0.2, 10)
		print(json.loads(payload))

	# if msg.topic == 'LED/' + hostname + '/off':
	#   print('turn led off')    
	# 	print(json.loads(payload))
	# if msg.topic == 'LED/' + hostname + '/strobe':
	#   print('turn led off')    
	# 	print(json.loads(payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
print('connecting')
print(args["username"])
print(args["password"])
client.username_pw_set(username=args["username"], password=args["password"])
mqtt_broker_addr = args["host"]
mqtt_broker_port = args["port"]
client.connect(mqtt_broker_addr, mqtt_broker_port, 60)
#client.loop_start()

while True:
	client.loop(.1);
	print('loop startt')
