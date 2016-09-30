# -*- coding: utf-8 -*-

#
# GPIO Pin settings : Use pin numberring not GPIO output number
#   The GPIOpin number on wich is connected a push button to manually start the lighting sequence
PIN_BUTTON = 16 #GPIO23

#format : a list of dictionnary with "id" and "name" as keys where "id"(int) is the pin_number, and "name"(string) is a name (not really used yet) for the light
GPIO_pins = [
    { "id"    : 11, "name"  : 'light name'},  #a relay is connected to GPIO, using the pin number 7, the given name is 'light name'
    { "id"    : 13, "name"  : 'light name2'}, #a relay is connected to GPIO, using the pin number 7, the given name is 'light name2'
    { "id"    : 15, "name"  : 'light name3'}, #a relay is connected to GPIO, using the pin number 7, the given name is 'light name3'
    { "id"    : 18, "name"  : 'light name4'}  #a relay is connected to GPIO, using the pin number 7, the given name is 'light name4'
    ]
#example with 3 outputs (pin#11,13 and 15)
#GPIO_pins = [
#    { "id": 11, "name": "blue light" },
#    { "id": 13, "name": "red light" },
#    { "id": 15, "name": "green light" },
#    ]

#
# SEQUENCE OF LIGHTING
#

#To turn 'ON' or 'OFF' a light : 
#   format like ( p , s ) where :
#       'p' is the id of the pin in the GPIO_pins list
#       's' is the state : 1 = on / 0 = off
#To insert a pause in the sequence, use 0 as first number, and the time(ms) as second number :
#   ex: (0,500) will do a pause of 500ms

#Sample Sequence using 1 GPIO output numbered 7 :
#SEQUENCE = [ (7,1) , (0,100) , (7,0) , (0,400), (7,1) , (0,100) , (7,0) , (0,400) ]

SEQUENCE = [ (11,0) , (13,0) , (15,0) , (18,0) ,             #---- (all off for init)
            (11,1) , (13,0) , (15,0) , (18,0) , (0,500) ,    #B--- p500 
            (11,0) , (13,1) , (15,0) , (18,0) , (0,500) ,    #-R-- p500
            (11,0) , (13,0) , (15,1) , (18,0) , (0,500) ,    #--G- p500
            (11,0) , (13,0) , (15,0) , (18,1) , (0,500) ,    #---Y p500
            (11,0) , (13,0) , (15,0) , (18,0) , (0,500) ,    #---- p500
            (11,1) , (13,0) , (15,0) , (18,0) , (0,100) ,    #B--- p100
            (11,0) , (13,1) , (15,0) , (18,0) , (0,100) ,    #-R-- p100
            (11,0) , (13,0) , (15,1) , (18,0) , (0,100) ,    #--G- p100
            (11,0) , (13,0) , (15,0) , (18,1) , (0,100) ,    #---Y p100
            (11,1) , (13,1) , (15,1) , (18,1) , (0,1000),    #BRGY p1000
            (11,1) , (13,0) , (15,1) , (18,0) , (0,1000),    #B_G_ p1000
            (11,0) , (13,1) , (15,0) , (18,1) , (0,1000),    #_R_Y p1000
            (11,1) , (13,0) , (15,1) , (18,0) , (0,500),     #B_G_ p500
            (11,0) , (13,1) , (15,0) , (18,1) , (0,500),     #_R_Y p1000
            (11,1) , (13,0) , (15,1) , (18,0) , (0,500),     #
            (11,0) , (13,1) , (15,0) , (18,1) , (0,500),     #
            (11,1) , (13,0) , (15,0) , (18,1) , (0,500),     #
            (11,0) , (13,1) , (15,1) , (18,0) , (0,500),     #
            (11,1) , (13,0) , (15,0) , (18,1) , (0,500),     #
            
            (11,0) , (13,0) , (15,0) , (18,0) ,  ]           #----

#
# TWITTER SEARCH
#   (for app authentication, please fill twitterauth.py with credentials)
#   see https://dev.twitter.com/streaming/reference/post/statuses/filter for more informations on search

#The sequence will play whenever a tweet match this Twitter search 
#Tweets corresponding to words (space means AND, comma means OR. Each string in the list will be searched for like a OR)
FilterTrack = ['place ducale','placeducale','charleville mezieres','charlevillemezieres']

#Tweets by user ID (see http://gettwitterid.com/ for getting specific users ids)
#   ex: ['3362569443'] for @HackArdennes
FilterFollow = None 

#Tweets by location : http://boundingbox.klokantech.com/ for drawing box
#   (use CSV RAW format ex: [4.6034232974,49.7020447479,4.8283393979,49.8231573185] for Charleville-Mezieres)
#   WARNING filter by location will not filter other filters like track, follow or languages
FilterLocations = None

#Tweets with languages (https://tools.ietf.org/html/bcp47)
FilterLanguages = None 