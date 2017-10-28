import numpy as np
from time import time
import matplotlib.pyplot as plt


class Receiver:
    N_SUBCARRIER = 0
    N_SAMPLE = 0
    N_2 = 0

    TIME_DOMAIN = []
    list_ReXImX = []

    avgReX, avgImX = [], []

    def __init__(self, time_domain, n_sample=100, n_subcarrier=5):
        self.TIME_DOMAIN = time_domain
        self.N_SAMPLE = n_sample
        self.N_2 = int(self.N_SAMPLE / 2)
        self.N_SUBCARRIER = n_subcarrier

        print('From Receiver'.upper())
        print('N_SAMPLE: {}\n'.format(self.N_SAMPLE))

    def generateFrequencyDomain(self):
        # ลูปเพื่อตัดมาทีละช่องจากหลายๆช่อง
        for i in range(0, int(len(self.TIME_DOMAIN) / self.N_SAMPLE)):
            # tmp_timedomain = ช่องๆนึง
            tmp_timedomain = self.TIME_DOMAIN[int(i * self.N_SAMPLE): int(i * self.N_SAMPLE + self.N_SAMPLE)]
            self.list_ReXImX.append(self.DFT(tmp_timedomain))

        for rex, imx in self.list_ReXImX:
            self.avgReX.extend(rex)
            self.avgImX.extend(imx)

        return self.avgReX, self.avgImX

    def DFT(self, tmp_timedomain):
        '''

        :param tmp_timedomain: wave list which cuted
        :return:
        '''

        ReX, ImX = [], []
        avgReX, avgImX = [], []

        # find ReX, ImX
        print('calculate ReX[] and ImX[]..')
        t0 = time()
        for k in range(0, self.N_2 + 1):  # self.N_2 + 1
            sumCos, sumSin = 0, 0

            for i in range(0, self.N_SAMPLE):
                sumCos += tmp_timedomain[i] * np.cos((2 * np.pi * k * i) / self.N_SAMPLE)
                sumSin += tmp_timedomain[i] * np.sin((2 * np.pi * k * i) / self.N_SAMPLE)

            ReX.append(sumCos)
            ImX.append(-sumSin)
        print('done in: {} sec.'.format(time() - t0))

        # find avgReX, avgImX
        print('calculate avgReX[] and avgImX[]..')
        t0 = time()
        for k in range(0, self.N_2 + 1):  # self.N_2 + 1
            avgReX.append(ReX[k] / self.N_2)
            avgImX.append(-ImX[k] / self.N_2)
        print('done in: {} sec.'.format(time() - t0))

        return avgReX, avgImX

    def plotGraph(self):
        '''
                    (blue,  pink)
            00      t       t
            01      t       b
            10      b       b
            11      b       t

            * top(t), bottom(p)
        :return:
        '''
        width = .6

        plt.title('avgReX and avgImX')
        plt.grid(True)
        plt.ylim(-1, 1)
        plt.bar(range(len(self.avgReX)), self.avgReX, width=width, color="lightblue", label='avgReX')
        plt.bar(range(len(self.avgImX)), self.avgImX, width=width, color="pink", label='avgImX')
        plt.legend(loc='best')
        plt.show()
