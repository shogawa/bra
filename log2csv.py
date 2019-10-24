#! /usr/bin/env python
#-*- coding: utf-8 -*-

import os
import subprocess
import pandas as pd
import numpy as np
import re
from decimal import Decimal, ROUND_HALF_UP
from math import log10, floor
#sho = '[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
sho = r"\d+\s*[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?\s*[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?\s*\(.+?\)"

def shisha(x,sig=3) :
    y = '1e' + str(-(sig-int(floor(log10(abs(x))))-1))
    return Decimal(str(x)).quantize(Decimal(str(y)), ROUND_HALF_UP)

def login(log):
    ld = open(log,"r")
    lines = ld.readlines()
    ld.close()
    return lines

def error(lines,sho=sho):
    ss = ['paramater number', 'parametar', 'err1', 'err2', 'min', 'max', 'tex']
    for line in lines:
        s = re.search(sho,line)
        if s != None:
            s = s.group()
            a = re.split("[\s\(\),]+",s)
            a.pop(-1)
            a = [float(x) for x in a]
            parno = int(a[0])
            par = ((a[1] - a[3]) + (a[2] - a[4])) / 2
            parmax = a[2]
            parmin = a[1]
            err1 = a[4]
            err2 = a[3]
            tex = '$'+str(shisha(par))+'^{'+str(shisha(err1))+'}_{-'+str(shisha(err2))+'}$'
            aa = [parno,par,err1,err2,parmin,parmax,tex]
            ss = np.vstack((ss,aa))
            if a[1] != 0 and a[2] != 0 :
                print(parno,par,err1,err2,tex)
            elif a[1] == 0 and a[2] != 0 :
                print(parno,par,err1,err2,tex,'The lower limit is pegged at the upper boundary value')
            elif a[1] != 0 and a[2] == 0 :
                print(parno,par,err1,err2,tex,'The upper limit is pegged at the lower boundary value')
            else:
                print(parno,par,err1,err2,tex,'The upper and lower limit is pegged at the boundary value')

    return ss

def data2csv(array):
    df = pd.DataFrame(array)
    df.to_csv('error.csv',index=False)

def main():
    lines = login('error.log')
    ss = error(lines,sho)
    print(ss)
    np.savetxt('error.csv', ss, delimiter=',', fmt="%s")


main()
