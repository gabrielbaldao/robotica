import curses

import RPi.GPIO as GPIO
from threading import Thread
import _thread
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


pinoMotorA = 17
pinoMotorA1 = 18
pwmAglobal = 50
pwmBglobal = 50
pinoMotorB = 22
pinoMotorB1 = 23
frequencia = 1000

GPIO.setup(pinoMotorA, GPIO.OUT)
GPIO.setup(pinoMotorA1, GPIO.OUT)
GPIO.setup(pinoMotorB, GPIO.OUT)
GPIO.setup(pinoMotorB1, GPIO.OUT)

pwm1 = GPIO.PWM(pinoMotorA, frequencia)
pwm2 = GPIO.PWM(pinoMotorA1, frequencia)
pwm1.start(0)
pwm2.start(0)

pwm3 = GPIO.PWM(pinoMotorB, frequencia)
pwm4 = GPIO.PWM(pinoMotorB1, frequencia)
pwm3.start(0)
pwm4.start(0)


class MotorDireita():
    motor = None

    def __new__(cls, *args, **kwargs):
        if not cls.motor:
            cls.motor = super(MotorDireita, cls).__new__(cls, *args, **kwargs)
        return cls.motor

    def __init__(self):
        self.ptk = 0

    def iniciar(self):
        self.sentidoFrente = False
        self.rpm = 0
        self.zerarValores()
        self.valorPWMAtual = 0
        self.emMovimento = False


    def sentido(self, booleano):
        if (booleano != self.sentidoFrente):
            if (self.emMovimento):
                self.frenagem()
                print("freiou")
            else:
                print("aceleracao")
                # self.aceleracao()
        else:
            print("Sentido j? inicializado")
        self.sentidoFrente = booleano

    def setMovimento(self, valor):
        self.emMovimento = valor
    def alterarRPM(self, valor, tagDestino):
        print("saiu for")
        # time.sleep(10)
        print("vai while")
        while self.rpm < valor and self.valorPWMAtual < 100  :
            print(self.valorPWMAtual)
            self.valorPWMAtual += 1
            self.alterarPWM(self.valorPWMAtual)
            time.sleep(0.1)

        print("PWM " + str(self.valorPWMAtual) + " RPM " + str(self.rpm))

    def zerarValores(self):
        global pwm1
        global pwm2
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)

    def alterarPWM(self, valor):
        global pwm1
        global pwm2
        self.valorPWMAtual = valor
        # print("Sentido ",self.sentidoFrente)
        if (self.sentidoFrente):
            pwm1.ChangeDutyCycle(valor)
        else:
            pwm2.ChangeDutyCycle(valor)

    def aceleracao(self):
        for i in range(0, 100, 1):
            if (self.rpm < 250):
                self.alterarPWM(i)
                time.sleep(0.001)

    def frenagem(self):
        for i in range(int(self.valorPWMAtual), 0, -1):
            self.alterarPWM(i)
            time.sleep(0.001)
            self.zerarValores()
    def pausar(self):
        MotorDireita().alterarPWM(0)
    def continuar(self):
        global pwmAglobal
        if(self.emMovimento):
            print("pwm ligando ", pwmAglobal)
            MotorDireita().aceleracao()
            MotorDireita().alterarPWM(pwmAglobal)

MotorDireita().iniciar()





def avancar():
    global pwmAglobal, pwmBglobal
    if pwmAglobal < 100:
        pwmAglobal+=5
        MotorDireita().alterarPWM(pwmAglobal)
    if pwmBglobal < 100:
        pwmBglobal+=5
        # MotorEsquerda().alterarPWM(pwmBglobal)

def voltar():
    global pwmAglobal, pwmBglobal
    if pwmAglobal > 0:
        pwmAglobal-=5
        MotorDireita().alterarPWM(pwmAglobal)
    if pwmBglobal > 0:
        pwmBglobal-=5
        # MotorEsquerda().alterarPWM(pwmBglobal)

def esquerda():
    global pwmAglobal, pwmBglobal
    if pwmAglobal < 100:
        pwmAglobal+=10
        MotorDireita().alterarPWM(pwmAglobal)
    if pwmBglobal > 0:
        pwmBglobal-=10
        # MotorEsquerda().alterarPWM(pwmBglobal)

def direita():
    global pwmAglobal, pwmBglobal
    if pwmAglobal > 0:
        pwmAglobal-=10
        MotorDireita().alterarPWM(pwmAglobal)
    if pwmBglobal < 100:
        pwmBglobal+=10
        # MotorEsquerda().alterarPWM(pwmBglobal)
def para():
    global pwmAglobal, pwmBglobal
    MotorDireita().alterarPWM(0)
    # MotorEsquerda().alteraPWM(0)

try:
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(1)
    stdscr.refresh()
    while 1:
        c = stdscr.getch()
        if c == ord('w'):
            # avancar()
            print('frente')
        elif c == ord('s'):
            # voltar()
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


