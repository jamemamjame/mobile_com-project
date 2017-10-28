import Sender as sender
import Receiver as receiver
import random as rd
import matplotlib.pyplot as plt
import numpy as np


def RandomAndWriteInput(file_name, num):
    f = open(file_name, 'w')
    randBit = ''
    for i in range(0, num):
        randBit += str(rd.randint(0, 1))
    f.write(randBit)
    f.close()


def readInput(file_name):
    f = open(file_name, 'r')
    arrNum = [int(char) for char in f.read()]
    f.close()
    return arrNum


if __name__ == '__main__':
    file_name = 'input.txt'

    numBit = 100
    RandomAndWriteInput(file_name, numBit)

    bit = readInput(file_name)

    sder = sender.Sender(bit)
    # sder.plotByChanel(n_chanel=0)
    # sder.plotByChanel(n_chanel=1)
    time_domain = sder.generateTimeDomain()
    sder.plotTimeDomain()

    # print('time_domain:')
    # print(time_domain)

    print('---------------------')

    recver = receiver.Receiver(time_domain, n_sample=sder.N_SAMPLE, n_subcarrier=sder.N_SUB_CARRIER)
    recver.generateFrequencyDomain()
    recver.plotGraph()

    # print('avgImX:')
    # print(avgImX)
    # print('avgImX size = {}'.format(len(avgImX)))
    # for i, val in enumerate(avgImX):
    #     if np.abs(val) > 0.01:
    #         print(i, val)
    #
    # print('avgReX:')
    # print(avgReX)
    # print('avgReX size = {}'.format(len(avgReX)))
    # for i, val in enumerate(avgReX):
    #     if np.abs(val) > 0.01:
    #         print(i, val)

    pass
