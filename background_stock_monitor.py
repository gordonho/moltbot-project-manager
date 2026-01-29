#!/usr/bin/env python3
"""
后台股票监控脚本
监控股票300300的价格，当价格高于13元或低于12元时发送通知
"""

import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
import sys

def get_stock_price(symbol):
    """获取股票当前价格"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period='1d')
        if not hist.empty:
            return hist['Close'].iloc[-1]
        else:
            return None
    except Exception as e:
        print(f"获取 {symbol} 价格时出错: {str(e)}")
        return None

def send_notification(subject, message):
    """发送邮件通知"""
    try:
        # 邮件配置
        smtp_server = "smtp.qq.com"
        smtp_port = 587
        sender_email = "hogordon@qq.com"
        sender_password = "wjfpdjjqeyadeaea"  # 这是授权码，不是登录密码
        recipient_email = "hgdemail@qq.com"

        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # 邮件正文
        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        # 连接SMTP服务器并发送邮件
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"通知已发送: {subject}")
        return True
    except Exception as e:
        print(f"发送通知时出错: {str(e)}")
        return False

def monitor_stock():
    """监控股票价格"""
    symbol = "300300.SZ"
    print(f"开始监控股票 {symbol}，价格阈值：低于12元或高于13元")
    print(f"监控开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("监控将持续运行，直到手动停止 (Ctrl+C)")
    
    last_price = None
    last_notification_time = None
    
    while True:
        try:
            current_price = get_stock_price(symbol)
            
            if current_price is None:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 无法获取股票价格，跳过此次检查")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 当前价格: {current_price:.2f}元")
                
                # 检查是否需要发送通知
                should_notify = False
                notification_type = ""
                
                if current_price > 13.0:
                    if last_price is None or last_price <= 13.0:  # 只在跨越阈值时通知
                        should_notify = True
                        notification_type = "高于13元"
                elif current_price < 12.0:
                    if last_price is None or last_price >= 12.0:  # 只在跨越阈值时通知
                        should_notify = True
                        notification_type = "低于12元"
                
                if should_notify:
                    subject = f"股票300300价格提醒：价格{notification_type}"
                    message = f"""股票300300（海峡创新）价格提醒

当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
股票代码: 300300.SZ
当前价格: {current_price:.2f}元
状态: 价格{notification_type}

请及时关注。"""
                    send_notification(subject, message)
                    last_notification_time = datetime.now()
                
                last_price = current_price
            
            # 等待30分钟再检查
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 等待30分钟后进行下次检查...")
            time.sleep(1800)  # 30分钟
            
        except KeyboardInterrupt:
            print("\n监控已手动停止")
            break
        except Exception as e:
            print(f"监控过程中发生错误: {str(e)}")
            time.sleep(300)  # 出错时等待5分钟再继续

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 测试获取价格功能
        symbol = "300300.SZ"
        price = get_stock_price(symbol)
        if price:
            print(f"股票 {symbol} 当前价格: {price:.2f}元")
        else:
            print("无法获取股票价格")
    else:
        # 启动监控
        monitor_stock()

if __name__ == "__main__":
    main()