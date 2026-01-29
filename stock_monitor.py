#!/usr/bin/env python3
"""
股票监控脚本
用于定期监控和记录特定股票的价格变化
"""

import yfinance as yf
import json
import os
from datetime import datetime
import time
import sys

class StockMonitor:
    def __init__(self, symbols=None):
        """
        初始化股票监控器
        :param symbols: 要监控的股票代码列表
        """
        if symbols is None:
            self.symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        else:
            self.symbols = symbols
        
        # 设置数据保存目录
        self.data_dir = os.path.join(os.path.dirname(__file__), 'stock_data')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_stock_info(self, symbol):
        """
        获取单个股票的信息
        """
        try:
            stock = yf.Ticker(symbol.upper())
            hist = stock.history(period="5d")
            
            if hist.empty:
                return None
                
            latest_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else latest_price
            change = latest_price - previous_close
            change_percent = (change / previous_close) * 100
            
            return {
                'symbol': symbol.upper(),
                'price': latest_price,
                'change': change,
                'change_percent': change_percent,
                'company_name': stock.info.get('longName', 'N/A'),
                'volume': hist['Volume'].iloc[-1],
                'high': hist['High'].iloc[-1],
                'low': hist['Low'].iloc[-1],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"获取 {symbol.upper()} 数据时出错: {str(e)}")
            return None
    
    def get_all_stocks_info(self):
        """
        获取所有监控股票的信息
        """
        stocks_info = []
        for symbol in self.symbols:
            stock_info = self.get_stock_info(symbol)
            if stock_info:
                stocks_info.append(stock_info)
        return stocks_info
    
    def save_to_file(self, stocks_info, filename=None):
        """
        将股票信息保存到文件
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"stock_data_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stocks_info, f, ensure_ascii=False, indent=2)
        
        print(f"股票数据已保存到: {filepath}")
        return filepath
    
    def print_summary(self, stocks_info):
        """
        打印股票信息摘要
        """
        print("=" * 90)
        print(f"{'股票代码':<10} {'公司名称':<25} {'最新价':<10} {'涨跌额':<10} {'涨跌幅':<10} {'交易量':<15} {'高/低':<12}")
        print("=" * 90)
        
        for stock in stocks_info:
            high_low = f"{stock['high']:.2f}/{stock['low']:.2f}"
            print(f"{stock['symbol']:<10} {stock['company_name'][:24]:<25} "
                  f"${stock['price']:<9.2f} {stock['change']:+<9.2f} "
                  f"{stock['change_percent']:+<9.2f}% {stock['volume']:>10,} {high_low:<12}")
        
        print("=" * 90)
        print(f"数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def monitor_continuously(self, interval_minutes=15):
        """
        持续监控股票价格
        :param interval_minutes: 监控间隔（分钟）
        """
        print(f"开始持续监控 {len(self.symbols)} 只股票，每 {interval_minutes} 分钟更新一次...")
        print("按 Ctrl+C 停止监控")
        
        try:
            while True:
                print("\n" + "="*50)
                stocks_info = self.get_all_stocks_info()
                self.print_summary(stocks_info)
                
                # 保存当前数据
                self.save_to_file(stocks_info)
                
                print(f"下次更新: {datetime.now().replace(second=0, microsecond=0).timestamp() + interval_minutes*60:.0f}")
                
                # 等待指定时间
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n监控已停止")
    
    def get_historical_data(self, symbol, period="1mo"):
        """
        获取股票历史数据
        """
        try:
            stock = yf.Ticker(symbol.upper())
            hist = stock.history(period=period)
            return hist
        except Exception as e:
            print(f"获取 {symbol.upper()} 历史数据时出错: {str(e)}")
            return None

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python stock_monitor.py list [股票代码...]          # 获取指定股票的当前信息")
        print("  python stock_monitor.py continuous [间隔(分钟)]      # 持续监控模式")
        print("  python stock_monitor.py historical <股票代码>       # 获取历史数据")
        print("")
        print("示例:")
        print("  python stock_monitor.py list AAPL MSFT GOOGL      # 获取苹果、微软、谷歌的当前信息")
        print("  python stock_monitor.py continuous 30             # 每30分钟监控一次")
        print("  python stock_monitor.py historical AAPL           # 获取苹果的历史数据")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        symbols = sys.argv[2:] if len(sys.argv) > 2 else ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        monitor = StockMonitor(symbols)
        stocks_info = monitor.get_all_stocks_info()
        monitor.print_summary(stocks_info)
        monitor.save_to_file(stocks_info)
    elif command == "continuous":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 15
        symbols = sys.argv[3:] if len(sys.argv) > 3 else ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        monitor = StockMonitor(symbols)
        monitor.monitor_continuously(interval)
    elif command == "historical":
        if len(sys.argv) < 3:
            print("请提供股票代码")
            return
        symbol = sys.argv[2]
        monitor = StockMonitor([symbol])
        hist_data = monitor.get_historical_data(symbol)
        if hist_data is not None:
            print(f"\n{symbol.upper()} 最近5个交易日数据:")
            print(hist_data.tail())
    else:
        print("未知命令。使用 'python stock_monitor.py' 查看帮助信息")

if __name__ == "__main__":
    main()