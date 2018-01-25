#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)
Adafruit_BNO055 bno = Adafruit_BNO055();

void setup(void)
{
  Serial.begin(9600);
  /* Initialise the sensor */
  if(!bno.begin())
  {
  /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
}
//Visualización valores de la IMU
void loop(void)
{
  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);

  /* Display the floating point data */
  //Serial.print("X: ");
  Serial.print(euler.x());
  Serial.print(",");
  //Serial.println("s"); //  Para separar en python los grados obtenidos de cada plano 
  //Serial.print(" Y: ");
  Serial.print(euler.y());
  Serial.print(",");
  //Serial.println("d"); // Separación 
  //Serial.print(" Z: ");
  Serial.println(euler.z());
  
  delay(BNO055_SAMPLERATE_DELAY_MS);
}
