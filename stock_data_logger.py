#!/usr/bin/env python3
"""
股票数据记录脚本
记录股票300300的每次查询数据，用于后续分析
"""

import yfinance as yf
import csv
import os
from datetime import datetime
import json
import sys

class StockDataLogger:
    def __init__(self, symbol="300300.SZ", data_dir="./stock_data"):
        self.symbol = symbol
        self.data_dir = data_dir
        self.csv_file = os.path.join(data_dir, f"{symbol}_historical_data.csv")
        self.ensure_directories()
        self.create_csv_if_not_exists()
    
    def ensure_directories(self):
        """确保数据目录存在"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def create_csv_if_not_exists(self):
        """创建CSV文件（如果不存在）"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # 写入表头
                writer.writerow([
                    'timestamp', 'date', 'time', 'open', 'high', 'low', 'close', 
                    'volume', 'price_change', 'change_percentage'
                ])
    
    def get_current_data(self):
        """获取当前股票数据"""
        try:
            stock = yf.Ticker(self.symbol)
            hist = stock.history(period='1d')
            
            if hist.empty:
                return None
            
            current_data = hist.iloc[-1]
            
            # 获取前一天的数据以计算涨跌
            prev_hist = stock.history(period='2d')
            if len(prev_hist) >= 2:
                prev_close = prev_hist.iloc[-2]['Close']
                price_change = current_data['Close'] - prev_close
                change_percentage = (price_change / prev_close) * 100
            else:
                price_change = 0
                change_percentage = 0
            
            return {
                'timestamp': datetime.now().isoformat(),
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M:%S'),
                'open': round(float(current_data['Open']), 2),
                'high': round(float(current_data['High']), 2),
                'low': round(float(current_data['Low']), 2),
                'close': round(float(current_data['Close']), 2),
                'volume': int(current_data['Volume']),
                'price_change': round(price_change, 2),
                'change_percentage': round(change_percentage, 2)
            }
        except Exception as e:
            print(f"获取 {self.symbol} 数据时出错: {str(e)}")
            return None
    
    def log_data(self):
        """记录当前数据到CSV文件"""
        data = self.get_current_data()
        
        if data is None:
            print("无法获取股票数据")
            return False
        
        # 检查是否已经记录了今天的同一时间数据（避免重复记录）
        today_records = self.get_today_records()
        current_time = data['time']
        
        # 检查是否已有相同时间的数据
        for record in today_records:
            if record['time'] == current_time:
                print(f"已在 {current_time} 记录过数据，跳过重复记录")
                return True
        
        # 写入数据到CSV
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                data['timestamp'],
                data['date'],
                data['time'],
                data['open'],
                data['high'],
                data['low'],
                data['close'],
                data['volume'],
                data['price_change'],
                data['change_percentage']
            ])
        
        print(f"已记录 {self.symbol} 数据:")
        print(f"  时间: {data['date']} {data['time']}")
        print(f"  开盘: {data['open']}元")
        print(f"  收盘: {data['close']}元")
        print(f"  最高: {data['high']}元")
        print(f"  最低: {data['low']}元")
        print(f"  成交量: {data['volume']:,}")
        print(f"  涨跌额: {data['price_change']}元")
        print(f"  涨跌幅: {data['change_percentage']}%")
        
        return True
    
    def get_today_records(self):
        """获取今天的所有记录"""
        records = []
        if not os.path.exists(self.csv_file):
            return records
        
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            today = datetime.now().strftime('%Y-%m-%d')
            for row in reader:
                if row['date'] == today:
                    records.append(row)
        return records
    
    def get_latest_record(self):
        """获取最新记录"""
        if not os.path.exists(self.csv_file):
            return None
        
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            if rows:
                return rows[-1]
        return None
    
    def get_statistics(self):
        """获取统计数据"""
        if not os.path.exists(self.csv_file):
            return None
        
        records = []
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            records = list(reader)
        
        if not records:
            return None
        
        closes = [float(r['close']) for r in records]
        volumes = [int(r['volume']) for r in records]
        
        stats = {
            'total_records': len(records),
            'first_record_date': records[0]['date'],
            'last_record_date': records[-1]['date'],
            'latest_price': float(records[-1]['close']),
            'highest_price': max(closes),
            'lowest_price': min(closes),
            'avg_price': sum(closes) / len(closes),
            'highest_volume': max(volumes),
            'lowest_volume': min(volumes),
            'avg_volume': sum(volumes) / len(volumes)
        }
        
        return stats

def main():
    logger = StockDataLogger()
    
    if len(sys.argv) > 1 and sys.argv[1] == "log":
        # 记录当前数据
        logger.log_data()
    elif len(sys.argv) > 1 and sys.argv[1] == "stats":
        # 显示统计信息
        stats = logger.get_statistics()
        if stats:
            print("股票300300数据统计:")
            print(f"  总记录数: {stats['total_records']}")
            print(f"  首次记录日期: {stats['first_record_date']}")
            print(f"  最近记录日期: {stats['last_record_date']}")
            print(f"  当前价格: {stats['latest_price']:.2f}元")
            print(f"  历史最高价: {stats['highest_price']:.2f}元")
            print(f"  历史最低价: {stats['lowest_price']:.2f}元")
            print(f"  平均价格: {stats['avg_price']:.2f}元")
            print(f"  最高成交量: {stats['highest_volume']:,}")
            print(f"  最低成交量: {stats['lowest_volume']:,}")
            print(f"  平均成交量: {int(stats['avg_volume']):,}")
        else:
            print("暂无统计数据")
    elif len(sys.argv) > 1 and sys.argv[1] == "latest":
        # 显示最新记录
        latest = logger.get_latest_record()
        if latest:
            print("最新记录:")
            print(f"  时间: {latest['date']} {latest['time']}")
            print(f"  价格: {latest['close']}元")
            print(f"  涨跌: {latest['price_change']}元 ({latest['change_percentage']}%)")
            print(f"  成交量: {int(latest['volume']):,}")
        else:
            print("暂无记录")
    else:
        # 默认行为：记录数据并显示最新记录
        print("记录当前股票数据...")
        success = logger.log_data()
        if success:
            print("\n最新记录:")
            latest = logger.get_latest_record()
            if latest:
                print(f"  时间: {latest['date']} {latest['time']}")
                print(f"  价格: {latest['close']}元")
                print(f"  涨跌: {latest['price_change']}元 ({latest['change_percentage']}%)")
                print(f"  成交量: {int(latest['volume']):,}")

if __name__ == "__main__":
    main()