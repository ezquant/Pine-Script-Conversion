import backtrader as bt

class BreakoutSniper(bt.Strategy):
    params = (
        ('lookback_period', 365),
        ('hold', 30),
    )

    def __init__(self):
        self.highest_high = bt.ind.Highest(self.data.high, period=self.p.lookback_period)
        self.lowest_low = bt.ind.Lowest(self.data.low, period=self.p.lookback_period)
        self.order = None
        self.long_entry_bar = None
        self.short_entry_bar = None

    def next(self):
        # 检查是否有持仓并持有时间
        if self.position:
            if self.position.size > 0:  # 多头持仓
                if self.long_entry_bar is not None and len(self) - self.long_entry_bar >= self.p.hold:
                    self.close()  # 平多
                    self.long_entry_bar = None
            elif self.position.size < 0:  # 空头持仓
                if self.short_entry_bar is not None and len(self) - self.short_entry_bar >= self.p.hold:
                    self.close()  # 平空
                    self.short_entry_bar = None

        # 突破做多
        if self.data.high[0] >= self.highest_high[0]:
            if not self.position or self.position.size <= 0:
                self.order = self.buy()
                self.long_entry_bar = len(self)
                self.short_entry_bar = None  # 避免多空同时持仓

        # 跌破做空
        elif self.data.low[0] <= self.lowest_low[0]:
            if not self.position or self.position.size >= 0:
                self.order = self.sell()
                self.short_entry_bar = len(self)
                self.long_entry_bar = None  # 避免多空同时持仓

# 用法举例
if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(BreakoutSniper)
    # 加载数据
    data = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=datetime(2020,1,1), todate=datetime(2021,1,1))
    cerebro.adddata(data)
    cerebro.run()
    cerebro.plot()