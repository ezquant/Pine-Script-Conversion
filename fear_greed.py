import backtrader as bt
import numpy as np

class FearGreedIndex(bt.Indicator):
    lines = ('fgi',)
    params = (
        ('extreme_fear', -40),
        ('extreme_greed', 100),
        ('rsi_period', 14),
        ('ema_period', 14),
        ('volume_period', 90),
        ('stdev_period', 14),
    )

    def __init__(self):
        # 计算RSI
        self.rsi = bt.indicators.RSI(period=self.p.rsi_period)
        
        # 计算EMA作为公允价值
        self.fair_value = bt.indicators.EMA(period=self.p.ema_period)
        
        # 计算成交量指标
        self.vol_high = bt.indicators.Highest(self.data.volume, period=self.p.volume_period)
        self.vol_low = bt.indicators.Lowest(self.data.volume, period=self.p.volume_period)
        
        # 计算标准差
        self.stdev = bt.indicators.StandardDeviation(period=self.p.stdev_period)

    def next(self):
        # 计算公允价值指标
        fv_indicator = self.data.close[0] / self.fair_value[0]
        
        # 计算成交量指标
        vol_indicator = 1 + (self.data.volume[0] / ((self.vol_high[0] + self.vol_low[0]) / 2))
        
        # 计算标准差指标
        stdev_indicator = 1 + (self.stdev[0] / self.data.close[0])
        
        # 计算最终的恐惧贪婪指数
        self.lines.fgi[0] = (self.rsi[0] - 50) * fv_indicator * vol_indicator * stdev_indicator

    def plot(self, plotinfo=None):
        # 设置绘图参数
        plotinfo = plotinfo or {}
        plotinfo['subplot'] = True
        plotinfo['name'] = 'Fear & Greed Index'
        
        # 添加极端恐惧和贪婪的背景色
        if self.lines.fgi[0] <= self.p.extreme_fear:
            self.plotinfo.plotfill = True
            self.plotinfo.fillcolor = 'red'
            self.plotinfo.fillalpha = 0.1
        elif self.lines.fgi[0] >= self.p.extreme_greed:
            self.plotinfo.plotfill = True
            self.plotinfo.fillcolor = 'green'
            self.plotinfo.fillalpha = 0.1
