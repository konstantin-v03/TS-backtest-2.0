import backtrader as bt
from datetime import datetime, timezone
from binance.client import Client
import candlesticks_handler as ch
import points as p

cerebro = bt.Cerebro()
cerebro.addstrategy(p.Points, period=96)
cerebro.broker.setcash(1000000)
cerebro.broker.setcommission(commission=0.001)

start_datatime = datetime(2019, 9, 8, tzinfo=timezone.utc)
end_datatime = datetime(2022, 10, 16, tzinfo=timezone.utc)

data_15m = bt.feeds.PandasData(dataname=ch.f_klines_by_datetime('btcusdt',
                                                            Client.KLINE_INTERVAL_15MINUTE,
                                                            start_datatime,
                                                            end_datatime),
                           datetime=ch.OPEN_TIME,
                           open=ch.OPEN,
                           high=ch.HIGH,
                           low=ch.LOW,
                           close=ch.CLOSE)

data_1d = bt.feeds.PandasData(dataname=ch.f_klines_by_datetime('btcusdt',
                                                            Client.KLINE_INTERVAL_1DAY,
                                                            start_datatime,
                                                            end_datatime),
                           datetime=ch.OPEN_TIME,
                           open=ch.OPEN,
                           high=ch.HIGH,
                           low=ch.LOW,
                           close=ch.CLOSE)

data_1d.plotinfo.plotskip = data_15m

cerebro.adddata(data_15m)
cerebro.adddata(data_1d)
print('<START> Brokerage account: $%.2f' % cerebro.broker.getvalue())
cerebro.run()
print('<FINISH> Brokerage account: $%.2f' % cerebro.broker.getvalue())
cerebro.plot(style='candlestick')
