#include "ros/ros.h"
#include "std_msgs/String.h"
#include <iostream>
#include "std_msgs/Float32MultiArray.h"
#include "SparkFunCCS811.h"
#include <Wire.h>

#define GND_PIN 0
#define DATA_PIN 1
#define I2C_ADDRESS 0x5B
#define BAUD_RATE 9600

float CO2Level = 0.0f;
float TVOCLevel = 0.0f;

CCS811 AirSensor(I2C_ADDRESS);

void getAirQuality() {
    //get sensor data, first value CO2, second TVOC, third temperature, Temp is not Supported with current sensor version
    //CO2Level = data[0] uitegelezen van pin
    //TVOCLevel = data[1]

    AirSensor.readAlgorithmResults();

    CO2Level = AirSensor.getCO2();
    TVOCLevel = AirSensor.getTVOC();

    // CO2Level = CO2Level + 2.5f;
    // TVOCLevel = TVOCLevel + 0.5f;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "mypublishernode2");
    ros::NodeHandle n;
    ros::Publisher publisher = n.advertise<std_msgs::Float32MultiArray>("/AirQuality", 1000);
    ros::Rate loop_rate(1); // frequentie Hz
    Wire.begin();
    // std::cout << "Publisher running" << std::endl;
    while (ros::ok())
    {
        if (AirSensor.dataAvailable())
        {
            std_msgs::Float32MultiArray data;
            // get data from sensor, for now just raise
            getAirQuality();
            data.data.push_back(CO2Level);
            data.data.push_back(TVOCLevel);
            publisher.publish(data);
            ros::spinOnce();
            loop_rate.sleep();
        }
        
    }
    return 0;
}