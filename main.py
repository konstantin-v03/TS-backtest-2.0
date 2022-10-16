import backtrader as bt
from datetime import datetime, timezone
from binance.client import Client
import candlesticks_handler as ch
import points as p

cerebro = bt.Cerebro()
cerebro.addstrategy(p.Points)
cerebro.broker.setcash(10000)
cerebro.broker.setcommission(commission=0.001)

data = bt.feeds.PandasData(dataname=ch.f_klines_by_datetime('btcusdt',
                                                            Client.KLINE_INTERVAL_5MINUTE,
                                                            datetime(2021, 1, 1, tzinfo=timezone.utc),
                                                            datetime(2022, 1, 1, tzinfo=timezone.utc)),
                           datetime=ch.OPEN_TIME,
                           open=ch.OPEN,
                           high=ch.HIGH,
                           low=ch.LOW,
                           close=ch.CLOSE,
                           volume=ch.VOLUME)

cerebro.adddata(data)
print('<START> Brokerage account: $%.2f' % cerebro.broker.getvalue())
cerebro.run()
print('<FINISH> Brokerage account: $%.2f' % cerebro.broker.getvalue())
cerebro.plot(style='candlestick', loc='grey', grid=False)
