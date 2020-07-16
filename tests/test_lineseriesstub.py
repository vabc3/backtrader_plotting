import datetime
import backtrader as bt
import backtrader_plotting
from backtrader_plotting.schemes import Tradimo

from testcommon import getdatadir


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.di = bt.ind.DI(period=10)
        self.ddif = self.di.plusDI - self.di.minusDI
        self.crossLong = bt.ind.CrossOver(self.ddif, 20)

    def next(self):
        pos = len(self.data)
        if pos == 45 or pos == 145:
            self.buy(self.datas[0], size=None)

        if pos == 116 or pos == 215:
            self.sell(self.datas[0], size=None)


def test_lineactions():
    cerebro = bt.Cerebro()

    cerebro.addstrategy(MyStrategy)

    data = bt.feeds.YahooFinanceCSVData(
        dataname=getdatadir("orcl-1995-2014.txt"),
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2001, 2, 28),
        reverse=False,
    )
    cerebro.adddata(data)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio)

    cerebro.run()

    b = backtrader_plotting.Bokeh(style='bar', scheme=Tradimo(), output_mode='show')

    figs = cerebro.plot(b)

    assert isinstance(figs[0][0], backtrader_plotting.bokeh.bokeh.FigurePage)
    assert len(figs[0][0].figure_envs) == 4
    assert len(figs[0][0].analyzers) == 1


if __name__ == '__main__':
    test_lineactions()
