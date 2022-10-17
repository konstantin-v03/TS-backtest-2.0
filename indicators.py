import backtrader as bt
import numpy as np
import math


class VolatilityIndex(bt.Indicator):
    lines = ('volatility_index', )

    params = (('period', 14),)

    def __init__(self):
        self.lines.volatility_index = 100 * bt.talib.STDDEV(Log(self.data), timeperiod=self.params.period, nbdev=1.0)


class Log(bt.Indicator):
    lines = ('log', )

    def next(self):
        if len(self) > 0:
            self.lines.log[0] = math.log(self.data[0] / self.data[-1])


class Pivothigh(bt.Indicator):
    lines = ('pivothigh',)

    params = (('n', 3), ('fixnan', True), )

    def next(self):
        if len(self) - 1 >= self.params.n * 2:
            max_val = np.nan

            for i in range(-self.params.n * 2, 1):
                if np.isnan(max_val) or self.data[i] > max_val:
                    max_val = self.data[i]

            if self.data[-self.params.n] == max_val:
                self.lines.pivothigh[0] = self.data[-self.params.n]

        if self.params.fixnan:
            if np.isnan(self.lines.pivothigh[0]):
                for i in range(1, len(self) - 1):
                    if not np.isnan(self.lines.pivothigh[-i]):
                        self.lines.pivothigh[0] = self.lines.pivothigh[-i]
                        break


class Pivotlow(bt.Indicator):
    lines = ('pivotlow',)

    params = (('n', 3), ('fixnan', True), )

    def next(self):
        if len(self) - 1 >= self.params.n * 2:
            min_val = np.nan

            for i in range(-self.params.n * 2, 1):
                if np.isnan(min_val) or self.data[i] < min_val:
                    min_val = self.data[i]

            if self.data[-self.params.n] == min_val:
                self.lines.pivotlow[0] = self.data[-self.params.n]

        if self.params.fixnan:
            if np.isnan(self.lines.pivotlow[0]):
                for i in range(1, len(self) - 1):
                    if not np.isnan(self.lines.pivotlow[-i]):
                        self.lines.pivotlow[0] = self.lines.pivotlow[-i]
                        break