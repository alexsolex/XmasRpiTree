# XmasRpiTree
## Intro
Make a christmas tree lighting animation based on twitter search.
As tweets meeting search criteria are published, the app will trigger a sequence which will light some christmas lights.

## Requirement
### Hardware
- Raspberry pi ready to run python scripts (I used a raspbian but some other distros may be good too as they meet other requirements).
- Relay circuits, as many as you can plug on your RPi GPIO.
- 1 male plug to power everything
- as many female plugs as you can use relays
- a box to fit everything into

### SoftWare
- Raspbian OS on the raspberrypi but some other distros may be good too as they meet other requirements
- python 2.x (not tested with other versions)
- tweepy python library

## Installation
### create a twitter app
TODO
### set twitter credentials
- copy 'twitterauth.sample.py' and rename it 'twitterauth.py'.
- open 'twitterauth.py' and set up your twitter app credentials 
### set the things up
Open 'config.py' file and set the things up (evertything is explained in the file)
