import RPi.GPIO as GPIO
import dht11
import sys
import urllib2
from time import sleep
import datetime
import csv
import smtplib

MAX_TEMP = 32
MAX_HUMIDITY = 70
SENDER = "yourid@gmail.com"
RECEIVER = "theirid@live.com"

def send_warning(val):
    try:

	sender = SENDER
	receiver = RECEIVER
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(sender, "#password")
	subject = "Warning"
	text = "Please check the room humidity and temperature!"
	if val == 0:
	    subject = "Temperature risen above %d C!" % MAX_TEMP
	    text = "Warning the temperature has increased above %d" % MAX_TEMP
	elif val == 1:
	    subject = "Humdity risen above %d percent!" % MAX_HUMIDITY
	    text = "Warning the humidity has increased above %d" % MAX_HUMIDITY
	from email.Message import Message
	m = Message()
	m['X-Priority'] = '2'
	m['Subject'] = subject
	m.set_payload(text)
	server.sendmail(sender,receiver,m.as_string())
	print("Warning sent")

    except Exception, ex:
		print(ex)

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
instance = dht11.DHT11(pin=21)

while True:
    try:
        result = instance.read()
	if result.is_valid():
	    temp = result.temperature
            humi = result.humidity

	    if int(temp) > MAX_TEMP:
		send_warning(0)
	    if int(humi) > MAX_HUMIDITY:
		send_warning(1)

	    currentDT = datetime.datetime.now()
	    date = currentDT.strftime("%Y/%m/%d")
	    time = currentDT.strftime("%H:%M:%S")
	    
	    myCsvRow = [date, time, temp, humi]
	    
	    print(myCsvRow)
	    
	    with open(r'TempHumidity.csv', 'a') as fd:
		writer = csv.writer(fd);
		writer.writerow(myCsvRow)
	    
        myAPI = 'CBFP8AE0778SB523' 
        baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
        url = urllib2.urlopen(baseURL + 
	    '&field1=%s&field2=%s' % (temp, humi))

		sleep(120)
	    
        else:
            print("Error while accessing GPIO, \
	    data will be ready after 2 seconds")
	    
	    sleep(2)
	    
    except Exception as e:
        print (e)
        break
