#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <wiringPi.h>
#include "RCSwitch.h"

using namespace std::string_literals;

std::map<const std::string, std::pair<int,int>> commands
{
	{"lights_on"s, {16777173, 10}},
	{"lights_dim"s, {16777077, 10}},
	{"fan_off"s, {16776981, 10}},
	{"fan_low"s, {16777093, 10}},
	{"fan_med"s, {16777029, 10}},
	{"fan_high"s, {16777157, 10}}
};

void usage()
{
}

int main (int argc, char** argv)
{
	if(argc < 2)
	{
    	usage();
    	return 1;
  	}

  	std::cout << "Turning lights on\n";
  	wiringPiSetup();

  	RCSwitch sw;
  	sw.enableTransmit(0);
  	sw.setProtocol(6);

  	auto command = commands[argv[1]];
	sw.setRepeatTransmit(command.second);
	std::cout << "Command = " << command.first << ", repeat = " << command.second << '\n';
  	
	sw.send(command.first, 24);
  	std::cout << "done\n";
  	return 0;
}
