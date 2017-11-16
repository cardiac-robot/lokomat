# coding=utf-8

import sys
import qi
from naoqi import ALModule
from naoqi import ALBroker
import almath
import logging
import time
import random
import threading

class RobotModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.session.connect("tcp://" + self.ip + ":" + str(self.port))
        self.session = qi.Session()

        self.tts = self.session.service("ALTextToSpeech")
        self.animatedSpeechProxy = self.session.service("ALAnimatedSpeech")
        self.motion = self.session.service("ALMotion")

        self.motion.wakeUp()
        self.motion.setBreathConfig([["Bpm", 6], ["Amplitude", 0.9]])
        self.motion.setBreathEnabled("Body", True)
        self.motion.setStiffnesses('Head', 1.0)



        self.configuration = {"bodyLanguageMode":"contextual"}

    def setLanguage(self, value):
        self.tts.setLanguage(value)

    def setVolume(self, value):
        self.tts.setVolume(value)

    def say(self, textToSay):
        self.tts.say(textToSay)


    def lookAtPatient(self): 
        names = ["HeadYaw", "HeadPitch"]
        angleLists = [ 30.0*almath.TO_RAD, -30.0*almath.TO_RAD]
        timeLists  = [1.0, 1.2]
        isAbsolute = True
        self.motion.angleInterpolation(names, angleLists, timeLists, isAbsolute)



class RobotController(object):

    def __init__(self, name  ="Palin" ,ip = '10.30.0.110', port = 9559, useSpanish = True):
        self.ip = ip
        self.port = port
        self.useSpanish = useSpanish
        self.session = qi.Session()
        self.robotName = name

        self.go_on = True
        
        print('b')
        #myBroker = ALBroker("myBroker", "0.0.0.0", 0, self.ip, self.port)
        #self.module = RobotModule( name = 'module')

        self.session.connect("tcp://" + self.ip + ":" + str(self.port))

        print('vv')

        self.tts = self.session.service("ALTextToSpeech")
        self.setLanguage('Spanish')
        self.animatedSpeechProxy = self.session.service("ALAnimatedSpeech")
        self.motion = self.session.service("ALMotion")
        '''
        self.motion = self.session.service("ALMotion")
        self.motion.wakeUp()
        self.motion.setBreathConfig([["Bpm", 6], ["Amplitude", 0.9]])
        self.motion.setBreathEnabled("Body", True)
        self.motion.setStiffnesses('Head', 1.0)
        '''


        self.configuration = {"bodyLanguageMode":"contextual"}

    def setLanguage(self, value):
        self.tts.setLanguage(value)

    def setVolume(self, value):
        self.tts.setVolume(value)

    def say(self, textToSay):
        self.tts.say(textToSay)


    def lookAtPatient(self): 
        names = ["HeadYaw", "HeadPitch"]
        angleLists = [ 30.0*almath.TO_RAD, -30.0*almath.TO_RAD]
        timeLists  = [1.0, 1.2]
        isAbsolute = True
        self.motion.angleInterpolation(names, angleLists, timeLists, isAbsolute)


    def set_limits(self):
        self.hr = 50

    def set_sentences(self):
        self.welcomeSentence = "Hola, \\pau=400\\ mi nombre es " + self.robotName + ". \\pau=500\\ Te estaré acompañando en la sesión. \\pau=500\\ Estoy aquí para cuidar tus signos y ayudarte a mejorar en tu rehabilitación."
        self.hrIsUpSentence = 'Parece que estás empezando a estar cansado,\\pau=400\\ todo está bien?'
        self.postureCorrectionSentence = 'Trata de enderezarte,\\pau=400\\ pon la espalda recta'
        self.sayGoodBye = "Fue un placer acompañarte durante la sessión.\\pau=400\\ Nos vemos la próxima ocasión. "


    def connect_to_robot(self):

        try:
            self.session.connect("tcp://" + self.ip + ":" + str(self.port))

        except RuntimeError:
            logging.debug("Can't connect to Naoqi at ip \"" + self.ip + "\" on port " + str(self.port) +".\n"
                          "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)



    #binding functions to the interface

    def start_session(self):
        self.motion.wakeUp()
        self.tts.say(self.welcomeSentence)
        



    def set_data(self, data):
        self.ecg = data['ecg']
        self.angles1 = data['imu1']
        self.angles2 = data['imu2']


        if self.ecg['hr'] > self.hr:
            self.say(self.hrIsUpSentence)

        if self.angles1['yaw'] < 90:
            self.say(self.postureCorrectionSentence)

        
    
    def shutdown(self):
        self.tts.say(self.sayGoodBye)
        if self.motion.robotIsWakeUp():
            self.motion.rest()



def main():


    nao = RobotController(ip = '10.30.0.110', useSpanish = True)
    
    
    nao.set_sentences()
    nao.set_limits()

    print('x')

#    nao.connect_to_robot()

    #global module
#    module = nao.module

     

    def process(nao):
        go_on = True
        while go_on:
            print('.....')
            a = random.random()
            cont = 10 * a
            data = {'ecg': 100*cont, 'imu': [cont, cont, cont] }
            print (data)
            nao.get_data(data)
            time.sleep(5)

    print('a')  
    threading.Thread(target  = process , args =(nao,)).start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        nao.go_on = False


if __name__ == '__main__':
    main()
