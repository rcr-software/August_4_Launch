# Telemetry Test (with possibility for multiprocessing)

On August 4th, 2017, RCR will be performing a test launch of our two stage rocket.  The rcr-software team is using this time to test the design of our new telemetry system as well as hopefully implement some parallel processing using openMP.  The current test plan is to relay values from the RF module on board the rocket to the ground station as fast as possible to develop a clear understanding of the limitations of the telemetry system as well as start developing requirements and redundancies to mitigate chances of data being lost in transmission.

On-Board Avionics
  Microcomputer/Microcontroller: BeagleBone Black Rev. D
      Operating System: Debian 8.7 2017-03-19 4GB SD IoT (https://debian.beagleboard.org/images/bone-debian-8.7-iot-armhf-2017-03-19-4gb.img.xz)

  RF Transmitter/Receiver: XBee SX SMD with multidirectional antenna

  Additional Sensors: Adafruit BMP280

Ground Station
  Microcomputer/Microcontroller: Raspberry Pi 3
      Operating System: Raspbian Jessie

  RF Transmitter/Receiver: XBee SX SMD with multidirectional antenna
