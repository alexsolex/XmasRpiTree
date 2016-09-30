# -*- coding: utf-8 -*-
import pygame
import config
import twitterauth as tw
import time, traceback
from requests import exceptions as ex

#pip install tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import RPi.GPIO as GPIO
global SeqRunning
SeqRunning = False

def btn_pushed(channel):
    """a button on GPIO has been pushed"""
    #time.sleep(0.4)
    #if GPIO.input(channel):
    if channel == pin_button:
        if SeqRunning:
            print("A sequence is already running !")
        else:
            print("Manual run of the Sequence !")
            run_light_sequence()
    


class StdOutListener(StreamListener):
    """A listener handles tweets that are received from the stream."""

    def on_status(self,status):
        print(status.created_at)
        print(status.user.name)
        print(status.text.encode('utf8'))
        
        run_light_sequence()
        
    def on_error(self,status_code):
        if status_code == 420:
            print("Error 420 : Rate Limit Error : need to wait")
            return False
        if status_code == 406:
            print("Error 406 : Search Not Acceptable")
            global ok
            ok = False
            return False
        else:
            if status_code>=500 and status_code<600: #Error 5xx
                print("Error %s"%status_code)
                return True #dont stop the filer
            else:
                print("UnHandled error status %s"%status_code)
        
        

def run_light_sequence():
    global SeqRunning
    if SeqRunning:
        print "Sequence already running. Pass this one..."
    else:
        SeqRunning = True
        for t in config.SEQUENCE:
            if t[0] == 0: 
                time.sleep(t[1] / 1000.0)
            else:
                light = Lights[t[0]]
                light.switch(t[1])
        SeqRunning = False

class pinout:
    """Represent a GPIO pin"""
    def __init__(self,name,pin):
        self.name = name
        self.pin = pin
        self.status = False
        
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, not self.status) #prepare off
        

    def switch(self,state):
        """Turn the pin On (state=True) or Off (state=False)"""
        self.status = not state
        self.output()
        
    def output(self):
        print "%s <pin#%s> is %s" % (self.name,self.pin,"'off'" if self.status else "'on'")
        GPIO.output(self.pin, self.status)

    def on(self):
        self.status = True
        self.output()

    def off(self):
        self.status = False
        self.output()

    def __repr__(self):
        return "%s <pin#%s> is %s" % (self.name,self.pin,"'off'" if self.status else "'on'")                           
    
    
if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BOARD) # use board pin numbers
    
    # define pin as input
    pin_button = config.PIN_BUTTON 
    GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.add_event_detect(pin_button, GPIO.RISING, callback=btn_pushed)
    
    #Generate and set up the outputs on the GPIO
    Lights = {}
    for pin in config.GPIO_pins:
        Lights[pin.get("id")] = pinout(pin.get("name"),pin.get("id"))

    #for informations estimate how long is going to last a single sequence
    SEQUENCE_time = 0
    for t in config.SEQUENCE:
        if t[0] == 0:
            SEQUENCE_time += t[1]
    print "Each light sequence is going to last %s ms" % SEQUENCE_time

    #Ready for the show !

    #test the sequence at start time
    run_light_sequence()

    #set the twitter search handler
    l = StdOutListener()
    auth = OAuthHandler(tw.apiKey,tw.apiSecret)
    auth.set_access_token(tw.accessToken,tw.accessTokenSecret)

    stream = Stream(auth,l)
     
    #run the live search stream
    ok = True
    time_retry = 10
    print "Go for a '%s' search !" % config.FilterTrack
    while ok:
        try:
            stream.filter(track=config.FilterTrack,
                          follow = config.FilterFollow,
                          locations = config.FilterLocations, 
                          languages = config.FilterLanguages)
            print("Filtering stopped")
        except ex.RequestException as err:
            print("Erreur de connexion internet !")
            print(err)
            print("nouvelle tentative dans %s sec" % time_retry)
            time.sleep(time_retry)
        except KeyboardInterrupt:
            print ("annulation par l'utilisateur. Fin du script")
            ok = False
        except Exception as err:
            print("autre erreur non gérée... Sortie !")
            traceback.print_exc()

            ok = False
            
    print("Bye Bye")