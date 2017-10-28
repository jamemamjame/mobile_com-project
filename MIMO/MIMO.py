# -*- coding: utf-8 -*-
"""
@author: Mr.Aphisit Phankosol
"""

import numpy as np
from numpy.linalg import inv as inverse
import matplotlib.pyplot as plt

FREQ = 1
FACTOR_TIME = 0.01
N = 200  # sample

H = np.matrix([[1 / 2, -1j / 8, ],
               [1j / 4, -1j / 16]])
H_inv = inverse(H)

C = np.matrix([[1j], [-1]])
Tx_orgSignal = []  # [[n,n,n,n, << signalOfC[0]], [n,n,n,n, << signalOfC[1]], ..]

print('Variable')
print('H:\n {}'.format(H))
print('H_inv:\n {}'.format(H_inv))
print('C:\n {}'.format(C))
print('------------------------------------')


def gen_sin_wave(freq, time, phase=0):
    return np.sin((2 * np.pi * freq * time) + phase)


def convert2Signal(cmplx):
    '''
    รับจำนวนเชิงซ้อนมาสร้างกราฟ sin
    :param cmplx: complex
    :return: list ที่เก็บ sine wave
    '''
    signal = []
    t = 0
    for i in range(N):
        signal.append(np.abs(cmplx) * gen_sin_wave(freq=FREQ, time=t, phase=np.angle(cmplx)))
        t += FACTOR_TIME
    return signal


def plotSignal(s):
    plt.plot(s)
    plt.show()


def plot_Tx_Original(list_signal):
    '''
    พล็อตกราฟสำหรับ Tx ใดๆ
    :param list_signal:
    :return:
    '''
    plt.title('Tx signal')
    plt.grid(True)
    for i, li in enumerate(list_signal):
        plt.plot(li, label='Tx{}, ({})'.format(i + 1, C.item((i, 0))))
    plt.legend(loc='best')
    plt.show()


def plt_SendingFromTransmittor(send_signal):
    plt.title('Send from Tx')
    plt.grid(True)
    for i in range(0, len(send_signal)):
        for j in range(0, len(send_signal[0])):
            plt.plot(send_signal[i][j], label='Tx{} → Rx{},'.format(i + 1, j + 1))
    plt.legend(loc='best')
    plt.show()


def plt_ReceiveByReceiver(receive_signal):
    plt.title('Receive by Rx')
    plt.grid(True)
    for i in range(0, receive_signal.shape[0]):
        plt.plot(convert2Signal(receive_signal.item((i, 0))), label='Rx{}'.format(i + 1))
    plt.legend(loc='best')
    plt.show()


def plot_PredictSignal(pred_signal):
    plt.title('Predict Original Signal')
    plt.grid(True)
    for i in range(0, pred_signal.shape[0]):
        plt.plot(convert2Signal(pred_signal.item((i, 0))), label='from Tx{}'.format(i + 1))
    plt.legend(loc='best')
    plt.show()


print("About Transceiver..")
print("Convert complex to signal..")
for i in range(0, len(C)):
    Tx_orgSignal.append(convert2Signal(C.item(i, 0)))
plot_Tx_Original(Tx_orgSignal)

print("Calculate send''s signal value into sendSignal matrix..")
# collect data like an array 2D -> X:Rx, Y:Tx
sendSignal = []
for i in range(0, H.shape[0]):
    sendSignal.append([])
    for j in range(0, H.shape[1]):
        sendSignal[i].append(convert2Signal(H.item((i, j)) * C.item((j, 0))))
plt_SendingFromTransmittor(sendSignal)

################################### R E C E I V E R #######################################

print('Calculate Y = H * C..')
# Y = HC
Y = np.dot(H, C)
plt_ReceiveByReceiver(Y)

# print("\n-------------------- Receiver --------------------")
print('Convert Y to predictSignal..')
predSignal = np.dot(H_inv, Y)
plot_PredictSignal(predSignal)
