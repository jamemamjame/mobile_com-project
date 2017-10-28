import numpy as np
import pprint as pp
from time import time
import matplotlib.pyplot as plt


class Sender:
    Mega = 10 ** 6
    Kilo = 10 ** 3

    # Constant variable
    MID_FREQ = 3
    DIFF_FREQ_PER_SUBCARRIER = 1

    N_SUB_CARRIER = 5
    N_SAMPLE = 100
    N_CHANEL = 0

    FACTOR_TIME = 1 / N_SAMPLE
    BIT_LIST = []
    TIME_DOMAIN = []

    def __init__(self, bit_list):
        self.BIT_LIST = bit_list
        self.N_CHANEL = int(len(self.BIT_LIST) / (2 * self.N_SUB_CARRIER))

        print('From Sender'.upper())
        print('Original bit size: {}'.format(len(self.BIT_LIST)))
        print('BandWidth: {} Hz'.format(self.MID_FREQ))
        print('N_SUB_CARRIER: {}'.format(self.N_SUB_CARRIER))
        print('N_SAMPLE: {}\n'.format(self.N_SAMPLE))
        print('N_CHANEL: {}\n'.format(self.N_CHANEL))

        return

    def gen_sin_wave(self, freq, time, phase=0):
        return np.sin((2 * np.pi * freq * time) + phase)

    def getPhase_QPSK(self, bit):
        if bit == [0, 0]:
            return np.pi / 4  # 45 degree
        if bit == [0, 1]:
            return (3 * np.pi) / 4  # 135 degree
        if bit == [1, 0]:
            return (5 * np.pi) / 4  # 275 degree
        if bit == [1, 1]:
            return (7 * np.pi) / 4  # 315 degree

    def getFrequency(self, n_curSub):
        '''
        this function return the proper frequency when we know number sub_carrier
        :param n_curSub:
        :param n_Sub:
        :return:
        '''

        # calculate mid index
        idx_mid = int(self.N_SUB_CARRIER / 2)
        # calculate absolute of different freq
        diff_freq = np.abs(idx_mid - n_curSub) * self.DIFF_FREQ_PER_SUBCARRIER

        if n_curSub < idx_mid:
            return self.MID_FREQ - diff_freq
        if n_curSub > idx_mid:
            return self.MID_FREQ + diff_freq
        else:
            return self.MID_FREQ



    def getSumPerTime(self, t, listSignal):
        # check error
        if len(listSignal) != 2 * self.N_SUB_CARRIER:
            print('listSignal/s size not correct')
            exit(0)
            return

        sumWave = 0

        # loop for access each sub_carrier
        for i in range(0, self.N_SUB_CARRIER):
            f = self.getFrequency(n_curSub=i)
            phase = self.getPhase_QPSK([listSignal[i * 2], listSignal[(i * 2) + 1]])

            # calculate sun wave
            a = self.gen_sin_wave(freq=f, time=t, phase=phase)
            sumWave += a

        return sumWave

    def generateTimeDomain(self):
        print('Generate time domain signal by Sender...')

        # cut input and send it to processing
        self.TIME_DOMAIN = []  # list of wave (last output)
        t0 = time()
        t = 0
        for i in range(0, self.N_CHANEL):

            # cut list to small list which has size = 2 x num_sub_carrier
            block_size = 2 * self.N_SUB_CARRIER
            block = self.BIT_LIST[(block_size * i): (block_size * i) + block_size]

            for j in range(0, self.N_SAMPLE):
                self.TIME_DOMAIN.append(self.getSumPerTime(t=t, listSignal=block))
                t += self.FACTOR_TIME

        print('done in {} sec.'.format(time() - t0))

        return self.TIME_DOMAIN

    def plotTimeDomain(self):
        time_start = 0
        time_stop = int(len(self.TIME_DOMAIN) / self.N_SAMPLE)

        plt.title('Time Domain')
        plt.grid(True)
        plt.plot(np.arange(start=time_start, stop=time_stop, step=self.FACTOR_TIME, dtype=float),
                 np.array(self.TIME_DOMAIN))
        plt.show()

    def plotByChanel(self, n_chanel=0):
        '''
        1 chanel contains N_SUB_CARRIER sub carriers
        This function get which chanel you want to see multi graph
        :return:
        '''

        if n_chanel < self.N_CHANEL:

            # cut list to small list which has size = 2 x num_sub_carrier
            block_size = 2 * self.N_SUB_CARRIER
            block_select = self.BIT_LIST[(block_size * n_chanel): (block_size * n_chanel) + block_size]

            plt.title('plot chanel: {}, value: {}'.format(n_chanel, block_select))
            plt.grid(True)

            for i in range(0, self.N_SUB_CARRIER):
                sub_carrier_list = []
                t = n_chanel  # time will start at same n_chanel
                f = self.getFrequency(i)
                tmpBit = list([block_select[2 * i], block_select[2 * i + 1]])
                ph = self.getPhase_QPSK(tmpBit)

                for j in range(0, self.N_SAMPLE):
                    sub_carrier_list.append(self.gen_sin_wave(freq=f, time=t, phase=ph))
                    t += self.FACTOR_TIME

                plt.plot(np.array(sub_carrier_list), label='value: {},'.format(tmpBit))

            plt.legend(loc='best')
            plt.show()

        else:
            print('can not plot grapg by chanel')
