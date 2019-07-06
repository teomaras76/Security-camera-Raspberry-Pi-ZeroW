import RPi.GPIO as GPIO
import time
from subprocess import call
import smtplib
from picamera import PiCamera
from datetime import datetime

import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

#Mail settings
def SendMail(ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = Subject
    msg['From'] = From
    msg['To'] = To

    text = MIMEText("Intruder at home!")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    try:
        s = smtplib.SMTP(Server, Port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(user = UserName, password = UserPassword)
        s.sendmail(From, To, msg.as_string())
        s.quit()
        call([cmd_beg + alarm_msg_2 + cmd_end], shell=True)
    except:
        print("Unable to send mail")
        call([cmd_beg + alarm_msg_3 + cmd_end], shell=True)

Server='smtp.gmail.com'
Port=587
UserName='Insert here your mail account'
UserPassword='Insert here your mail pwd'
From='Insert here your mail account'
To='Insert here which to mail you want to send msg'
Subject='Intruder detected'



#Pi Camera settings
camera = PiCamera()
filename = "Intruder"
#filename = "intruder.h264"


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

cmd_beg ='espeak '
cmd_end ='2>/dev/null '
alarm_msg_1 = '"Hi, I got you!" '
alarm_msg_2 = '"Mail successfully sent" '
alarm_msg_3 = '"It was not possible to send mail" '
alarm_msg_4 = '"Security camera is ON" '

call([cmd_beg + alarm_msg_4 + cmd_end], shell=True)
while True:
    i=GPIO.input(7)
    if i==0:
        print("No intruders")
        time.sleep(0.5)
        #camera.stop_preview()
    elif i==1:
        print("Intruder detected")
        timestamp= datetime.now().strftime("%Y%m%d-%H%M%S")
        print(timestamp)
        #camera.start_recording(filename)
        #camera.start_preview()
        time.sleep(2)
        camera.capture('/home/pi/Desktop/Intruders_log/'+filename+timestamp+".jpg")
        #'/home/tim/Desktop/final_stacked_images/final'+"result_%06d.jpg"
        #camera.close()
        #camera.stop_preview()
        #camera.close()
        
        call([cmd_beg + alarm_msg_1 + cmd_end], shell=True)
        SendMail('/home/pi/Desktop/Intruders_log/'+filename+timestamp+".jpg")
        
        #s = smtplib.SMTP('smtp.gmail.com',587)
        #s.ehlo()
        #s.starttls()
        #s.ehlo()
        #s.login(smtpUser,smtpPass)
        #s.sendmail(fromAdd, toAdd, header + '\n' + body)
        #s.quit()
        #time.sleep(1)
        

