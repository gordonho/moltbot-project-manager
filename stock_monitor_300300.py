#!/usr/bin/env python3
"""
股票300300监控脚本
当价格高于13元或低于12元时发送通知
"""

import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
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

def check_price_and_notify():
    """检查价格并发送通知"""
    symbol = "300300.SZ"
    current_price = get_stock_price(symbol)
    
    if current_price is None:
        print("无法获取股票价格")
        return False
    
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"股票 {symbol} 当前价格: {current_price:.2f}元")
    
    # 检查是否超出阈值
    if current_price > 13.0:
        subject = f"股票300300价格提醒：价格已超过13元"
        message = f"""股票300300（海峡创新）价格提醒

当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
股票代码: 300300.SZ
当前价格: {current_price:.2f}元
状态: 价格已超过13.00元

请及时关注。"""
        send_notification(subject, message)
        return True
    elif current_price < 12.0:
        subject = f"股票300300价格提醒：价格已低于12元"
        message = f"""股票300300（海峡创新）价格提醒

当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
股票代码: 300300.SZ
当前价格: {current_price:.2f}元
状态: 价格已低于12.00元

请及时关注。"""
        send_notification(subject, message)
        return True
    else:
        print(f"价格在正常范围内 (12.00 - 13.00元)，无需通知")
        return False

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 测试模式
        print("正在测试股票监控脚本...")
        check_price_and_notify()
    else:
        # 正常运行模式
        print("开始监控股票300300价格...")
        print("价格阈值: 低于12元或高于13元时通知")
        check_price_and_notify()

if __name__ == "__main__":
    main()