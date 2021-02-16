# ChessBoard
I am building a automated chess board that moves pieces by itself through voice commands
running on raspberry pi 3 and DRV8825 motor controllerswith nema 17 stepper motors

# Videos
Prototype stage 1.21.21 [video](https://youtu.be/2joaITZlWBY)

Prototype stage 2.10.21 [video](https://www.youtube.com/watch?v=23EdfVoHuEU&feature=youtu.be&ab_channel=AndrewChen)

Test with real chess pieces after tuning magnet size and electromagnet voltage [video](https://youtu.be/bjvCjh__WXg)

# Photos
Created a custom circuit board for motor controllers that allow for replacement if one burns out.
![](Circuit_Back.jpg)
![](Circuit_Front.jpg)

## Automated Chess Board Controlled
* uses stepper motors to control x and y axis and an electromagnet to move pieces
* There are a lot of commits because I push to github then pull it over ssh on the raspberry pi.
* google voice api to use voice control
* [motor set up (old version)](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/powering-motors)
* Switched to [Pololu DRV8825 Stepper motor controller](https://www.youtube.com/watch?v=LUbhPKBL_IU&t=1412s&ab_channel=rdagger68)
* [possible chess program for playing against cpu](https://code-projects.org/simple-chess-game-in-python-with-source-code/)
