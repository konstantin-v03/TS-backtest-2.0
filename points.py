import backtrader as bt


class Points(bt.Strategy):
    def __init__(self):
        self.lowest = bt.indicators.Lowest(self.data.close, period=96)
        self.highest = bt.indicators.Highest(self.data.close, period=96)

        self.lowest.plotinfo.subplot = False
        self.highest.plotinfo.subplot = False
