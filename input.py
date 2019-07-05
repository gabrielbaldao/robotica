import curses
# import wiringpi2 as wiringpi  

import RPi.GPIO as GPIO
# from threading import Thread
# import _thread
import time

# import pygame
# from pygame.locals import *

GPIO.cleanup()  
# wiringpi.wiringPiSetupGpio()  

# pygame.init()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


width, height = 1280, 1000
# screen=pygame.display.set_mode((width, height))

pinoMotorA = 18
pinoMotorA1 = 4 #marrom
pinoMotorA2 = 22 #preto
pinoMotorB = 13
pinoMotorB1 = 12 #verde
pinoMotorB2 = 16 #amarelo
pwmAglobal = 100
pwmBglobal = 100

frequencia = 1000

GPIO.setup(pinoMotorA, GPIO.OUT)
GPIO.setup(pinoMotorA1, GPIO.OUT)
GPIO.setup(pinoMotorA2, GPIO.OUT)
GPIO.setup(pinoMotorB, GPIO.OUT)
GPIO.setup(pinoMotorB1, GPIO.OUT)
GPIO.setup(pinoMotorB2, GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
# wiringpi.pinMode(pinoMotorA, 2)
# wiringpi.pinMode(pinoMotorA1, 1)
# wiringpi.pinMode(pinoMotorA2, 1)
# wiringpi.pinMode(pinoMotorB,2)
# wiringpi.pinMode(pinoMotorB1, 1)
# wiringpi.pinMode(pinoMotorB2, 1)
GPIO.output(26,GPIO.HIGH)
pwm1 = GPIO.PWM(pinoMotorA, frequencia)
pwm2 = GPIO.PWM(pinoMotorB, frequencia)
pwm1.start(0)
pwm2.start(0)






GPIO.output(pinoMotorA1,0)
GPIO.output(pinoMotorB1,0)

GPIO.output(pinoMotorA2,0)
GPIO.output(pinoMotorB2,0)



class MotorDireita():
    motor = None
    sentidoFrente = False
    valorPWMAtual = 0
    emMovimento = False

    def __new__(cls, *args, **kwargs):
        if not cls.motor:
            cls.motor = super(MotorDireita, cls).__new__(cls, *args, **kwargs)
        return cls.motor

    def __init__(self):
        self.ptk = 0

    def iniciar(self):
        self.sentidoFrente = False
        self.zerarValores()
        self.valorPWMAtual = 0
        self.emMovimento = False



    def sentido(self, booleano):
        if (booleano != self.sentidoFrente):
            self.sentidoFrente = booleano
            if (self.emMovimento):
                self.frenagem()
            self.aceleracao()
        else:
            print("Sentido j? inicializado")

    def setMovimento(self, valor):
        self.emMovimento = valor

    def zerarValores(self):
        # global pwm1
        global pwm1
        global pinoMotorA1
        global pinoMotorA2
        GPIO.output(pinoMotorA1, 1)
        GPIO.output(pinoMotorA2, 1)
        pwm1.ChangeDutyCycle(0)

        # pwm1.ChangeDutyCycle(0)

    def alterarPWM(self, valor):
        # global pwm1
        global pinoMotorA1
        global pinoMotorA2
        global pwm1
        self.valorPWMAtual = valor
        pwm1.ChangeDutyCycle(valor)
        if (self.sentidoFrente):
            self.ligaPorta(pinoMotorA2)
            
            self.desligaPorta(pinoMotorA1)
        else:
            self.ligaPorta(pinoMotorA1)
            self.desligaPorta(pinoMotorA2)
    def ligaPorta(self, porta):
        print("\nLiga ", porta)
        global GPIO
        GPIO.output(porta, GPIO.HIGH)

    def desligaPorta(self, porta):
        global GPIO
        GPIO.output(porta, GPIO.LOW)
    def aceleracao(self):
        for i in range(0, 100, 1):
            self.alterarPWM(i)
            time.sleep(0.001)

    def frenagem(self):
        self.zerarValores()
class MotorEsquerda():
    motor = None
    sentidoFrente = False
    valorPWMAtual = 0
    emMovimento = False

    def __new__(cls, *args, **kwargs):
        if not cls.motor:
            cls.motor = super(MotorEsquerda, cls).__new__(cls, *args, **kwargs)
        return cls.motor

    def __init__(self):
        self.ptk = 0

    def iniciar(self):
        self.sentidoFrente = False
        self.zerarValores()
        self.valorPWMAtual = 0
        self.emMovimento = False



    def sentido(self, booleano):
        if (booleano != self.sentidoFrente):
            self.sentidoFrente = booleano
            if (self.emMovimento):
                self.frenagem()
            self.aceleracao()
        else:
            print("Sentido j? inicializado")

    def setMovimento(self, valor):
        self.emMovimento = valor

    def zerarValores(self):
        # global pwm1
        global pwm2
        global pinoMotorB1
        global pinoMotorB2
        GPIO.output(pinoMotorB1, 1)
        GPIO.output(pinoMotorB2, 1)
        pwm2.ChangeDutyCycle(0)

        # pwm2.ChangeDutyCycle(0)

    def alterarPWM(self, valor):
        # global pwm1
        global pinoMotorB1
        global pinoMotorB2
        global pwm2
        self.valorPWMAtual = valor
        pwm2.ChangeDutyCycle(valor)
        if (self.sentidoFrente):
            self.desligaPorta(pinoMotorB1)
            self.ligaPorta(pinoMotorB2)
        else:
            self.ligaPorta(pinoMotorB1)
            self.desligaPorta(pinoMotorB2)
    def ligaPorta(self,porta):
        global GPIO
        print("\nLiga: ",porta)
        GPIO.output(porta, GPIO.HIGH)

    def desligaPorta(self,porta):
        global GPIO
        GPIO.output(porta, GPIO.LOW)
    def aceleracao(self):
        for i in range(0, 100, 1):
            self.alterarPWM(i)
            time.sleep(0.001)

    def frenagem(self):
        self.zerarValores()


# MotorDireita().iniciar()
MotorEsquerda().iniciar()

esquerdaContador = 1
direitaContador = 1

def maior(valor1, valor2):
    if valor1 > valor2:
        return valor1
    return valor2

def avancar():
    global pwmAglobal, pwmBglobal
    if pwmAglobal < 100:
        pwmAglobal+=5
        MotorDireita().aceleracao()
        MotorDireita().alterarPWM(pwmAglobal)
    if pwmBglobal < 100:
        pwmBglobal+=5
        MotorEsquerda().aceleracao()
        MotorEsquerda().alterarPWM(pwmBglobal)

def voltar():
    global pwmAglobal, pwmBglobal
    if pwmAglobal > 0:
        pwmAglobal-=5
        MotorDireita().aceleracao()
        MotorDireita().alterarPWM(pwmAglobal)
    if pwmBglobal > 0:
        pwmBglobal-=5
        MotorEsquerda().aceleracao()
        MotorEsquerda().alterarPWM(pwmBglobal)

def esquerda():
    global pwmAglobal, pwmBglobal
    global esquerdaContador, direitaContador
    if esquerdaContador == 1:
        igual = maior(pwmAglobal, pwmBglobal)
        pwmAglobal = igual
        pwmBglobal = igual
    
    if pwmAglobal < 100:
        pwmAglobal=pwmAglobal+esquerdaContador*10 if pwmAglobal+esquerdaContador*10 < 100 else 100
        MotorDireita().alterarPWM(pwmAglobal)
    if pwmBglobal > 0:
        pwmBglobal-=10
        MotorEsquerda().alterarPWM(pwmBglobal)
    esquerdaContador += 1
    direitaContador =1

def direita():
    global pwmAglobal, pwmBglobal
    global esquerdaContador, direitaContador
    if direitaContador == 1:
        igual = maior(pwmAglobal, pwmBglobal)
        pwmAglobal = igual
        pwmBglobal = igual
    if pwmAglobal > 0:
        pwmAglobal-=10
        MotorDireita().alterarPWM(pwmAglobal)
    if pwmBglobal < 100:
        pwmBglobal= pwmBglobal+direitaContador*10 if pwmBglobal+direitaContador*10 < 100 else 100
        MotorEsquerda().alterarPWM(pwmBglobal)
    direitaContador +=1
    esquerdaContador = 1
def para():
    global pwmAglobal, pwmBglobal
    MotorDireita().alterarPWM(0)
    MotorEsquerda().alteraPWM(0)

def sentido(var):
    global pwmAglobal, pwmBglobal
    sentidoMotor(MotorEsquerda(), not var, pwmBglobal)
    sentidoMotor(MotorDireita(), var, pwmAglobal)
    
    # MotorDireita().sentido(var)
    # MotorDireita().aceleracao()
    # MotorDireita().alterarPWM(pwmBglobal)
    # MotorDireita().setMovimento(True)

    # MotorEsquerda().sentido(not var)
    # MotorEsquerda().aceleracao()
    # MotorEsquerda().alterarPWM(pwmBglobal)
    # MotorEsquerda().setMovimento(True)
def sentidoMotor(motor, var, pwm):
    print("Sentido motor ", var)
    motor.sentido(var)
    motor.aceleracao()
    motor.alterarPWM(pwm)
    motor.setMovimento(True)


# MotorEsquerda().aceleracao()
# MotorDireita().aceleracao()


#while True:
#    print("Inicio do while")
#    time.sleep(2)



try:
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(1)
    stdscr.refresh()
    while 1:
        print("\n")
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == K_w:
        #             print("Botao de keydown")
        #     if event.type == pygame.KEYUP:
        #         if event.ke == K_w:
        #             print("Evento de key up")
        c = stdscr.getch()
        print(" ")
        if c == ord('y'):
            print('y')
            MotorEsquerda().aceleracao()
        elif c == ord('u'):
            MotorDireita().aceleracao()
        elif c == ord('i'):
            MotorDireita().frenagem()
        elif c == ord('o'):
            MotorEsquerda().frenagem()
        elif c == ord('w'):
            # avancar()
            print(pwmAglobal)
            print(pwmBglobal)
            sentido(True)
            print('frente')
        elif c == ord('s'):
            # voltar()
            sentido(False)
            print('tras')
        elif c == ord('a'):
            esquerda()
            print('esquerda')
        elif c == ord('d'):
            direita()
            print('direita')
        elif c == ord('8'):
            avancar()
            print('aumenta PWM')
        elif c == ord('2'):
            voltar()
            print('diminui PWM')
        elif c == ord('e'):

            print('para')
        elif c == ord('q'):
            exit(0)
        else:
            print('Comando desconhecido')

finally:
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


