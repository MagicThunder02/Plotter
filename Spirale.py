#!/usr/bin/env python
# -*- coding: utf-8 -*-
PHI = 1.618033
import math
import matplotlib
import time
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import serial


class Rect:
    px = 0
    py = 0
    r = 0
    ix = []
    iy = []
    flag = 0


class Spiral:
    rects = []

    def __init__(self, x0, y0):
        pass

    def Arco(self, cord):
        # definisco il centro, punto iniziale e finale
        # for i in range(1, len(self.rects) - 1):
        arch = cord.r * math.pi / 2
        segs = arch / 1
        angle = 90 / segs

        # per ogni arco definisco la precisione
        for j in range(int(segs)+1):
            # definisco i punti di interpolazione
            if cord.flag == 0:
                Px = cord.px + cord.r * math.cos(math.radians(angle * j))
                Py = cord.py + cord.r * math.sin(math.radians(angle * j))
            elif cord.flag == 1:

                Px = cord.px - cord.r * math.cos(math.radians(90 - angle * j))
                Py = cord.py + cord.r * math.sin(math.radians(90 - angle * j))
            elif cord.flag == 2:
                Px = cord.px - cord.r * math.cos(math.radians(angle * j))
                Py = cord.py - cord.r * math.sin(math.radians(angle * j))
            else:
                Px = cord.px + cord.r * math.cos(math.radians(90 - angle * j))
                Py = cord.py - cord.r * math.sin(math.radians(90 - angle * j))

            cord.ix.append(Px)
            cord.iy.append(Py)

    def draw(self, cx, cy, max):
        j = 0
        r = PHI
        px = cx
        py = cy
        while j < max:
            rect = Rect()
            rect.px = px
            rect.py = py
            rect.r = r
            rect.ix = []
            rect.iy = []
            # ----------------------------------------------------------- EST
            if j % 4 == 0:
                rect.flag = 0
                self.Arco(rect)
                self.rects.append(rect)
                # preparo i dati per il giro dopo
                py = py - r / PHI
                r = r * PHI
                # ----------------------------------------------------------- NORD
            elif j % 4 == 1:
                rect.flag = 1
                self.Arco(rect)
                self.rects.append(rect)
                px = px + r / PHI
                r = r * PHI
                # ----------------------------------------------------------- OVEST
            elif j % 4 == 2:
                rect.flag = 2
                self.Arco(rect)
                self.rects.append(rect)
                py = py + r / PHI
                r = r * PHI
                # ----------------------------------------------------------- SUD
            else:
                rect.flag = 3
                self.Arco(rect)
                self.rects.append(rect)
                px = px - r / PHI
                r = r * PHI
            j += 1

    def Plot(self):
        px = []
        py = []
        px.append(0)
        py.append(0)
        for j in range(len(self.rects)):
            for k in range(len(self.rects[j].ix)):
                px.append(self.rects[j].ix[k])
                py.append(self.rects[j].iy[k])
                print("point: {},{} : {} {}".format(j, k, round(self.rects[j].ix[k], 3), round(self.rects[j].iy[k], 3)))

        '''
        per avere gli assi autodimensionati
        minx = -px[len(px)-1]
        miny = -px[len(px)-1]
        maxx = px[len(px)-1]
        maxy = px[len(px)-1]
        plt.axis([minx, maxx, miny, maxy])
        '''
        plt.axis("square")
        plt.axis([-100, 100, -100, 100])
        matplotlib.style.use('default')
        plt.plot(px, py, color='green')
        plt.savefig("/home/pi/smart-scale/plot.png")

    def HardPlot(self, ser):
        px = 0
        py = 0
        ser.write('PU;')
        ser.write('PA{},{};'.format(self.rects[0].ix[0], self.rects[0].iy[0]))
        for j in range(len(self.rects)):
            ser.write('SP{};'.format((j % 8) + 1))
            ser.write('PA{},{};'.format(self.rects[j].ix[0], self.rects[j].iy[0]))
            ser.write('PD;')
            for k in range(len(self.rects[j].ix)):
                px = self.rects[j].ix[k]
                py = self.rects[j].iy[k]
                ser.write('PA{},{};'.format(px, py))
            ser.write('PU;')
            time.sleep(3)

        ser.write('PU;')
        ser.write('SP0;')


ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1, parity=serial.PARITY_EVEN)
ser.write('IN;IP0,0,4000,4000;SC0,100,0,100;')
ser.write('SP1;')

print("spirale")
spirale = Spiral(0, 0)
spirale.draw(200, 150, 10)
spirale.Plot()
spirale.HardPlot(ser)
