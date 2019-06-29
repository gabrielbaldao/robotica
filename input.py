import curses

import RPi.GPIO as GPIO
from threading import Thread
import _thread
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


pinoMotorA = 17
pinoMotorA1 = 18
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


class Motor():
    motor = None

    def __new__(cls, *args, **kwargs):
        if not cls.motor:
            cls.motor = super(Motor, cls).__new__(cls, *args, **kwargs)
        return cls.motor

    def __init__(self):
        self.ptk = 0

    def iniciar(self):
        self.motorPode = True
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
        global ultimaTag
        print("saiu for")
        # time.sleep(10)
        print("vai while")
        while self.rpm < valor and self.valorPWMAtual < 100 and not (ultimaTag in tagDestino) and self.motorPode:
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
        Motor().alterarPWM(0)
    def continuar(self):
        global pwmGlobal
        if(self.emMovimento):
            print("pwm ligando ", pwmGlobal)
            Motor().aceleracao()
            Motor().alterarPWM(pwmGlobal)

Motor().iniciar()










try:
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(1)
    stdscr.refresh()
    while 1:
        c = stdscr.getch()
        if c == ord('w'):
            print('frente')
        elif c == ord('s'):
            print('tras')
        elif c == ord('a'):
            print('esquerda')
        elif c == ord('d'):
            print('direita')
        elif c == ord('8'):
            print('aumenta PWM')
        elif c == ord('2'):
            print('diminui PWM')
        elif c == ord('q'):
            exit(0)
        else:
            print('Comando desconhecido')

finally:
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


