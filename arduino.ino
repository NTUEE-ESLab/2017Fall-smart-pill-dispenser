#include <Wire.h>
#include <Servo.h> 
#define SLAVE_ADDRESS 0x04
//variables for i2c communicating
static int number = 0;


int state = 0;


//variables for servo control
int incomingByte = 0; 
Servo myservo1;
Servo myservo2;
int startPt =  600;
int endPt = 2300;
int shift = 200;
bool increaseAngle1;
bool increaseAngle2;
int pillNum1;
int pillNum2;


void setup() {
  Serial.begin(9600); // start serial for output
//setup for servo control
  myservo1.attach(9, 500, 2400); // 修正脈衝寬度範圍
  myservo1.write(0); // 一開始先置中90度
  myservo1.writeMicroseconds(650);
  
  myservo2.attach(10, 500, 2400); // 修正脈衝寬度範圍
  myservo2.write(0); // 一開始先置中90度
  myservo2.writeMicroseconds(650);
  
  increaseAngle1 = true;
  increaseAngle2 = true;
  delay(3000);
    
//setup for i2c communicating
  pinMode(8, OUTPUT);
  
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.println("Ready!");
}


void loop() {
  Serial.print(">>> # of pills of drug A: ");
  Serial.println(pillNum1);
  Serial.print(">>> # of pills of drug B: ");
  Serial.println(pillNum2);
  int countA = pillNum1;
  int countB = pillNum2;
  for(int i = 0; i < max(pillNum1, pillNum2); i++){
    Serial.print(">>>>> Round ");
    Serial.println(i);
    if(countA > 0){
      Serial.print(">>> shot for A! No.");
      Serial.println(i);
      fire1pill_1();
      countA--;
    }else{
      Serial.println(">>> Drug A done!");
    }
    if(countB > 0){
      Serial.print(">>> shot for B! No.");
      Serial.println(i);
      fire1pill_2();
      countB--;
    }else{
      Serial.println(">>> Drug B done!");
    }
    
  }
  pillNum1 = 0;
  pillNum2 = 0;
  delay(1000);
  
}
/////////////////////////////////////////////////
// functions for i2c
/////////////////////////////////////////////////
// callback for received data
void receiveData(int byteCount){
  while(Wire.available()) {
      number = Wire.read();
      Serial.print(">>> encoded data received: ");
      Serial.println(number);
      pillNum1 = number / 16;
      pillNum2 = number % 16;


  }
}


// callback for sending data
void sendData(){
  Wire.write(number);
}


///////////////////////////////////////////////
// functions for servo control
///////////////////////////////////////////////
void fire1pill_1(){
  get1MM_1(increaseAngle1);
  if(increaseAngle1){
    increaseAngle1 = false;
  }else{
    increaseAngle1 = true;
  }
}
void fire1pill_2(){
  get1MM_2(increaseAngle2);
  if(increaseAngle2){
    increaseAngle2 = false;
  }else{
    increaseAngle2 = true;
  }
}
void get1MM_1(bool isincreaseAngle1){
  if(isincreaseAngle1){
    Serial.println(">>> angle ++ ing ");
    myservo1.writeMicroseconds(endPt - shift);
    for(int i = endPt - shift; i <= endPt; i+=100){
      myservo1.writeMicroseconds(i); // 直接以脈衝寬度控制
      delay(100);
      if(i != 500)myservo1.writeMicroseconds(i - 100);
      delay(100);
    }


    for(int i = endPt; i >= endPt - shift; i-=100){
      myservo1.writeMicroseconds(i); // 直接以脈衝寬度控制
      delay(100);
      if(i != 2400)myservo1.writeMicroseconds(i + 100);
      delay(100);
    }
    delay(200);
    
  }else{
    Serial.println(">>> angle -- ing ");
    myservo1.writeMicroseconds(startPt + shift);
    for(int i = startPt +  shift; i <= startPt; i-=100){
      myservo1.writeMicroseconds(i); // 直接以脈衝寬度控制
      delay(100);
      if(i != 2400)myservo1.writeMicroseconds(i + 100);
      delay(100);
    }


    for(int i = startPt; i <= startPt + startPt; i+=100){
      myservo1.writeMicroseconds(i); // 直接以脈衝寬度控制
      delay(100);
      if(i != 500)myservo1.writeMicroseconds(i - 100);
      delay(100);
    }


    delay(200);
    
  }
  
}
void get1MM_2(bool isincreaseAngle2){
  if(isincreaseAngle2){
    Serial.println(">>> angle ++ ing ");
    myservo2.writeMicroseconds(endPt - shift);
    for(int i = endPt - shift; i <= endPt; i+=100){
      myservo2.writeMicroseconds(i); // 直接以脈衝寬度控制
      delay(100);
      if(i != 500)myservo2.writeMicroseconds(i - 100);
      delay(100);
    }


    for(int i = endPt; i >= endPt - shift; i-=100){
      myservo2.writeMicroseconds(i); // 直接以脈衝寬度控制
      delay(100);
      if(i != 2400)myservo2.writeMicroseconds(i + 100);
      delay(100);
    }
    delay(200);
    
  }else{
    Serial.println(">>> angle -- ing ");
    myservo2.writeMicroseconds(startPt + shift);
    for(int i = startPt +  shift; i <= startPt; i-=100){
      myservo2.writeMicroseconds(i); // 直接以脈衝寬度控制
      delay(100);
      if(i != 2400)myservo2.writeMicroseconds(i + 100);
      delay(100);
    }


    for(int i = startPt; i <= startPt + startPt; i+=100){
      myservo2.writeMicroseconds(i); // 直接以脈衝寬度控制
      delay(100);
      if(i != 500)myservo2.writeMicroseconds(i - 100);
      delay(100);
    }


    delay(200);
    
  }
  
}