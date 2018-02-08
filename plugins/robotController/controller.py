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
import functools

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

    def __init__(self,settings = { 'name'           : "Palin",
                                   'ip'             : '192.167.0.101',
                                   'port'           : 9559,
                                   'UseSpanish'     : True,
                                   'MotivationTime' : 300000000

                                 }):
        
        self.settings   = settings
        self.ip         = self.settings['ip']
        self.port       = self.settings['port']
        self.useSpanish = self.settings['UseSpanish']
        self.robotName  = self.settings['name']

        self.session    = qi.Session()
        
        self.go_on = True
        
        print('b')
        #myBroker = ALBroker("myBroker", "0.0.0.0", 0, self.ip, self.port)
        #self.module = RobotModule( name = 'module')

        self.session.connect("tcp://" + self.ip + ":" + str(self.port))

        self.tts = self.session.service("ALTextToSpeech")
        self.setLanguage('Spanish')
        self.animatedSpeechProxy = self.session.service("ALAnimatedSpeech")
        self.motion = self.session.service("ALMotion")
        self.posture = self.session.service("ALRobotPosture")
        #self.recog = self.session.service("RecognitionService")
        #self.lokomat  = self.session.service("LokomatBehaviour")
        self.behavior_mng_service = self.session.service("ALBehaviorManager")
        names = self.behavior_mng_service.getInstalledBehaviors()
        print "Behaviors on the robot:"
        print names

        names = self.behavior_mng_service.getRunningBehaviors()
        print "Running behaviors:"
        print names

        
        '''
        self.motion = self.session.service("ALMotion")
        self.motion.wakeUp()
        self.motion.setBreathConfig([["Bpm", 6], ["Amplitude", 0.9]])
        self.motion.setBreathEnabled("Body", True)
        self.motion.setStiffnesses('Head', 1.0)
        '''


        self.configuration = {"bodyLanguageMode":"contextual"}

    
    #set language method
    def setLanguage(self, value):
        self.tts.setLanguage(value)
    
    #set volume method
    def setVolume(self, value):
        self.tts.setVolume(value)
    
    #say method
    def say(self, textToSay):
        self.tts.say(textToSay)

    #Thread say method threaded
    def threadSay(self, textToSay):
        threading.Thread(target = self.say, args = (textToSay,)).start()


    #look to the patient 
    #TODO: change this method, this must be part of posture module
    def lookAtPatient(self): 
        names = ["HeadYaw", "HeadPitch"]
        angleLists = [ 30.0*almath.TO_RAD, -30.0*almath.TO_RAD]
        timeLists  = [2.0, 2.0]
        isAbsolute = True
        self.motion.angleInterpolation(names, angleLists, timeLists, isAbsolute)

    #limits
    #TODO: this limits and all memory parameters should be located in a database
    def set_limits(self):
        self.hr = 50


    #TODO: sentences shoul be located in a database
    def set_sentences(self):
        self.welcomeSentence = "Hola, \\pau=400\\ mi nombre es " + self.robotName + ". \\pau=500\\ Te estaré acompañando en la sesión. \\pau=500\\ Estoy aquí para cuidar tus signos y ayudarte a mejorar en tu rehabilitación."
        self.sayGoodBye = "Fue un placer acompañarte durante la sessión.\\pau=400\\ Nos vemos la próxima ocasión. "
        self.hrIsUpSentence = 'Parece que estás empezando a estar cansado,\\pau=400\\ todo está bien?'
        self.headPostureCorrectionSentence = "Mejora la posición de tu cabeza"
        self.torsePostureCorrectionSentence = 'Trata de enderezarte,\\pau=400\\ pon la espalda recta'
        self.askBorgScale = 'Que tan cansado te sientes? \\pau=400\\ responde segun la escala'
        self.borgAlertSentence   =  "Al parecer estás muy cansado,\\pau=400\\ voy a llamar al doctor!."
        self.borgRecievedSentence   = "Gracias"

        self.motivationSentence = ["Puedes hacerlo!","Que bien lo haces!","Te felicito!","Sigue así!"]


    #connect to robot method
    def connect_to_robot(self):

        try:
            self.session.connect("tcp://" + self.ip + ":" + str(self.port))

        except RuntimeError:
            logging.debug("Can't connect to Naoqi at ip \"" + self.ip + "\" on port " + str(self.port) +".\n"
                          "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)


    #set routines
    def set_routines(self):
        sayMotivation = functools.partial(self.get_motivation)
        self.sayMotivationTask = qi.PeriodicTask()
        self.sayMotivationTask.setCallback(sayMotivation)
        self.sayMotivationTask.setUsPeriod(self.settings['MotivationTime'])
        self.sayMotivationTask.start(True)


        getBorg = functools.partial(self.get_borg_scale)
        self.askBorgTask = qi.PeriodicTask()
        self.askBorgTask.setCallback(getBorg)
        self.askBorgTask.setUsPeriod(50000000)
        self.askBorgTask.start(True)

    def stop_routines(self):
        self.sayMotivationTask.stop()

    #binding functions to the interface

    def start_session(self):
        self.motion.wakeUp()
        #self.tts.say(self.welcomeSentence)
        #self.animatedSpeechProxy.say(self.welcomeSentence)
        
        #self.posture.goToPosture("StandZero", 1.0)
        self.animatedSpeechProxy.say(self.welcomeSentence)
        time.sleep(10)
        self.bad_posture_behavior()


    


    def get_borg(self, d):

        if d > 11:
            self.tts.say(self.borgAlertSentence)
        else:
            self.tts.say(self.borgRecievedSentence)

    

    #ROUTINE: predefined activities within an specific period of time
    #provide motivation a constant period of time
    def get_motivation(self):
        i = random.randint(0, len(self.motivationSentence) - 1)
        
        self.threadSay(self.motivationSentence[i])

    def get_borg_scale(self):
        self.threadSay(self.askBorgScale)

    #EVENTS: behaviors or activities that are triggered when an event occured
    #posture correction for torse event
    def correct_torse_posture(self):
        self.tts.say(self.torsePostureCorrectionSentence)
    #posture correction for head event
    def correct_head_posture(self):
        self.tts.say(self.headPostureCorrectionSentence)

    #ask hr: when heart rate seems to be high the robot asks if everything goes well
    def ask_hr_high(self):
        self.tts.say(self.hrIsUpSentence)

    #set_data method: validates data each time it is received 
    def set_data(self, data):
        self.ecg = data['ecg']
        self.angles1 = data['imu1']
        self.angles2 = data['imu2']


        if self.ecg['hr'] > self.hr:
            self.say(self.hrIsUpSentence)

        if float(self.angles2['pitch']) > -70: 
            self.correct_torse_posture()
        
        if float(self.angles1['pitch']) > -70:
            self.correct_head_posture()

    #BEHAVIOR
    #posture correction
    def bad_posture_behavior(self):
        threading.Thread(target = self.load_bad_posture_behavior).start()
        

    def load_bad_posture_behavior(self):
        self.behavior_mng_service.runBehavior('therapy-behaviors/correct_posture')


         
    #shutdown method: finishes all processes of the robot
    def shutdown(self):
        self.animatedSpeechProxy.say(self.sayGoodBye)
        if self.motion.robotIsWakeUp():
            self.motion.rest()



def main():

    nao = RobotController(settings = { 'name'           : "Palin",
                                   'ip'             : '192.168.0.103',
                                   'port'           : 9559,
                                   'UseSpanish'     : True,
                                   'MotivationTime' : 10000000  #30 seconds

                                 })
    
    
    nao.set_sentences()
    nao.set_limits()


    t =threading.Thread(target = nao.correct_torse_posture)

    nao.start_session()

    #nao.correct_head_posture()
    time.sleep(10)
    nao.set_routines()
    #t.start()
    time.sleep(40)
    #nao.correct_torse_posture()
    nao.stop_routines()
    nao.shutdown()



    print('x')

#    nao.connect_to_robot()

    #global module
#    module = nao.module

     
'''
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

'''
if __name__ == '__main__':
    main()
