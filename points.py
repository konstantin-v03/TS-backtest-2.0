import numpy as np
import backtrader as bt
import indicators as ind
import math


class Points(bt.Strategy):
    lines = ('s_condition1', 'l_condition1', 's_condition2', 'l_condition2')

    params = dict(period=96, con_max_bars_back=30, trade_min_bars_back=85, atr_period=14)

    def __init__(self):
        self.lowest = bt.indicators.Lowest(self.data.low, period=self.params.period)
        self.highest = bt.indicators.Highest(self.data.high, period=self.params.period)
        self.pivot_high = ind.Pivothigh(self.data.high)
        self.pivot_low = ind.Pivotlow(self.data.low)
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)
        self.volatility_index = ind.VolatilityIndex(self.data1.close)

        self.lowest.plotinfo.subplot = False
        self.highest.plotinfo.subplot = False
        self.pivot_high.plotinfo.subplot = False
        self.pivot_low.plotinfo.subplot = False

        self.order = None

        self.atr.plotinfo.plotskip = True
        self.volatility_index.plotinfo.plotskip = True

    def bars_back(self, data, max_bars_back):
        for i in reversed(range(-max_bars_back, 0)):
            if data[i]:
                return i

        return np.nan

    def notify_order(self, order):
        if not order.status == order.Completed:
            return

        if self.position.size < 0:
            print('Entry short @price: {:.2f}'.format(order.executed.price) + "\n" + str(self.position.size))
        elif self.position.size > 0:
            print('Entry long @price: {:.2f}'.format(order.executed.price) + "\n" + str(self.position.size))
        else:
            print('Close @price: {:.2f}'.format(order.executed.price) + "\n" + str(self.position.size))

    def next(self):
        trig = 100 * (self.highest[0] - self.lowest[0]) / self.lowest[0] > self.volatility_index[0]

        self.lines.s_condition1[0] = trig and \
                                     (self.data.high[-1] == self.highest[-1] and self.data.high[0] < self.highest[
                                         0]) and \
                                     ((self.highest[0] - self.data.low[0]) * 3 < (self.data.low[0] - self.lowest[0]))

        self.lines.l_condition1[0] = trig and \
                                     (self.data.low[-1] == self.lowest[-1] and self.data.low[0] > self.lowest[0]) and \
                                     ((self.data.high[0] - self.lowest[0]) * 3 < (self.highest[0] - self.data.high[0]))

        self.lines.s_condition2[0] = self.pivot_high[-1] > self.pivot_high[0] and not \
            np.isnan(self.bars_back(self.lines.s_condition1, self.params.con_max_bars_back))

        self.lines.l_condition2[0] = self.pivot_low[-1] < self.pivot_low[0] and not \
            np.isnan(self.bars_back(self.lines.l_condition1, self.params.con_max_bars_back))

        if self.lines.s_condition2[0] and \
                np.isnan(self.bars_back(self.lines.s_condition2, self.params.trade_min_bars_back)):
            if self.position.size > 0:
                self.close()

            if self.position.size == 0:
                self.sell()

        if self.lines.l_condition2[0] and \
                np.isnan(self.bars_back(self.lines.l_condition2, self.params.trade_min_bars_back)):
            if self.position.size < 0:
                self.close()

            if self.position.size == 0:
                self.buy()

        if self.position.size > 0:
            self.cancel(self.order)
            self.order = self.sell(exectype=bt.Order.Stop, price=(self.lowest[0] - self.atr[0]))

        if self.position.size < 0:
            self.cancel(self.order)
            self.order = self.buy(exectype=bt.Order.Stop, price=(self.highest[0] + self.atr[0]))