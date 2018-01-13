# What is Facial Recognizing Drug Dispenser
Facial Recognizing Drug Dispenser is a smart drug dispensing system which allows patients to get the pills they have to take via face recognizing technique and enables healthcare professionals to dynamically config prescriptions for each of their patients.

# How we make it
## 0. Overview
[Github link for our project](https://https://github.com/NTUEE-ESLab/2017Fall-smart-pill-dispenser)
![](https://my.ntu.edu.tw/Test/20180112173543.jpg)
p.s. In project demo we use MM chocolate beans to represent real pills.
## 1. App
Caregivers can set patient's personal information and prescription in our Mobile App easily through an interactive chatroom.
![]()
Login Screen             | Device Menu | Chatroom
:-------------------------:|:-------------------------:|:-----------
![](https://i.imgur.com/WRPUbDb.png =225x375)  |![](https://i.imgur.com/Tnj0izh.png =225x375)|![](https://i.imgur.com/Ex1tjVh.png =225x375)

## 2. Raspberry Pi
An Raspberry Pi is used to recognize patients(by sending photos to the remote server where facial recognition is performed), fetch user prescription from server and send drug delivery signals to Arduino.
## 3. Server
A remote server is responsible for facial recognition and data storage. Our server receives photos taken by a Raspberry Pi, identify who is taking the medicine, then returns the corresponding prescription fetched from database to Raspberry Pi.
## 4. Arduino
### Main function
The Arduino drives dispenser(s) to dispense drugs with specified number and types after receiving drug-dispensing requests from Rpi. 
### How to use it
#### 1. Connect the pins between Arduino and Rpi
We use I2C to connect Arduino and Rpi, so
#### 2. Connect the pins between Arduino and dispenser(s) 
Folling [this tutorial](http://yehnan.blogspot.tw/2013/09/arduinotower-pro-sg90.html) of SG-90, connect the signal pin, 5V pin, and the GND pin between the Arduino and the dispenser.

In our project we use the digital pin 9 as the signal pin of dispenser A; the digital pin 10 as the signal pin of dispenser B
#### 3. Upload the code to Arduino
Upload the code in "arduino.ino" to Arduino.
#### 4. Check the functionality of Arduino from Rpi side
With Arduino on, run "i2c-pi-arduino_test.py" in Rpi, and input the numbers of drug A and drug B respectively. You can thus check whether Arduino receive the correct values from the screen output.
## 5. Dispenser(s) with SG-90 servo motor(s)
### Main function
Each time when the dispenser is called by Arduino, it uses its servo motor SG-90 to rotate the round disk on the bottom of its cup by shaking it back and forth continuously( [see this demo video](https://drive.google.com/file/d/12Qg_4VxAPz-3_LBOeaAZ1OhXzHrLSbA5jA/view)), make one pill pass the hole of its cup, and thus finish dispensing one pill of drug.
![all components of the drug dispenser](https://my.ntu.edu.tw/Test/20180113095200.jpg)
### How to use it
#### 1. Assembly all components in **the picture in Main function section** together and you will see the whole structure like this:
![assembled dispenser](https://my.ntu.edu.tw/Test/20180113095607.jpg)
![](https://my.ntu.edu.tw/Test/20180113095652.jpg)
# Results 
[The operation of drug dispenser](https://photos.app.goo.gl/EeoVgY1gCzidloPn2)

# References
1. [OpenCV Face Recognizer API](https://docs.opencv.org/3.0-beta/modules/face/doc/facerec/index.html)