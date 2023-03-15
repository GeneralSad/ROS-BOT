#include "ros/ros.h"
#include "std_msgs/String.h"

int main(int argc, char **argv){

	ros::init(argc,argv,"mypublishernode2");
	ros::NodeHandle n;
	ros::Publisher publisher = n.advertise<std_msgs::String>("/mytopic2", 1000);
	ros::Rate loop_rate(3); //frequentie Hz
	
	while (ros::ok()){
		std_msgs::String msg;
		msg.data = "mymessage2!";
		publisher.publish(msg);
		ros::spinOnce();
		loop_rate.sleep();
	}
	
	return 0;
	
}