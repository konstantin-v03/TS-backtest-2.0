import backtrader as bt
import numpy as np

import indicators as ind


class Points(bt.Strategy):
    lines = ('s_condition1', 'l_condition1', 's_condition2', 'l_condition2')

    params = dict(period=96, con_max_bars_back=30, trade_min_bars_back=85)

    def __init__(self):
        self.lowest = bt.indicators.Lowest(self.data.low, period=self.params.period)
        self.highest = bt.indicators.Highest(self.data.high, period=self.params.period)
        self.pivot_high = ind.Pivothigh(self.data.high)
        self.pivot_low = ind.Pivotlow(self.data.low)
        self.volatility_index = ind.VolatilityIndex(self.data1.close)

        self.lowest.plotinfo.subplot = False
        self.highest.plotinfo.subplot = False
        self.pivot_high.plotinfo.subplot = False
        self.pivot_low.plotinfo.subplot = False

    def next(self):
        trig = 100 * (self.highest[0] - self.lowest[0]) / self.lowest[0] > self.volatility_index[0]

        self.lines.s_condition1[0] = trig and (self.data.high[-1] == self.highest[-1] and self.data.high[0] < self.highest[0]) and \
            ((self.highest[0] - self.data.low[0]) * 3 < (self.data.low[0] - self.lowest[0]))

        self.lines.l_condition1[0] = trig and (self.data.low[-1] == self.lowest[-1] and self.data.low[0] > self.lowest[0]) and \
            ((self.data.high[0] - self.lowest[0]) * 3 < (self.highest[0] - self.data.high[0]))

        for i in reversed(range(-self.params.con_max_bars_back, 0)):
            self.lines.s_condition2[0] = self.lines.s_condition1[i] and self.pivot_high[-1] > self.pivot_high[0]

            if self.lines.s_condition2[0]:
                break

        for i in reversed(range(-self.params.con_max_bars_back, 0)):
            self.lines.l_condition2[0] = self.lines.l_condition1[i] and self.pivot_low[-1] < self.pivot_low[0]

            if self.lines.l_condition2[0]:
                break

        if self.lines.s_condition2[0]:
            s_condition2_ = 0

            for i in reversed(range(-self.params.trade_min_bars_back, 0)):
                s_condition2_ = self.lines.s_condition2[i]

                if s_condition2_:
                    break

            if not s_condition2_:
                self.sell()

        if self.lines.l_condition2[0]:
            l_condition2_ = 0

            for i in reversed(range(-self.params.trade_min_bars_back, 0)):
                l_condition2_ = self.lines.l_condition2[i]

                if l_condition2_:
                    break

            if not l_condition2_:
                self.buy()








