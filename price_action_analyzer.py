#!/usr/bin/env python3
import ccxt
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import os

def get_levels(symbol='BTC/USDT', timeframe='1h', limit=100):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    levels = []
    for i in range(2, len(df) - 2):
        if df['high'][i] > df['high'][i-1] and df['high'][i] > df['high'][i+1] and df['high'][i] > df['high'][i-2] and df['high'][i] > df['high'][i+2]:
            levels.append(('Resistance', df['high'][i], df['timestamp'][i]))
        if df['low'][i] < df['low'][i-1] and df['low'][i] < df['low'][i+1] and df['low'][i] < df['low'][i-2] and df['low'][i] < df['low'][i+2]:
            levels.append(('Support', df['low'][i], df['timestamp'][i]))
    
    return df, levels

if __name__ == '__main__':
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'BTC/USDT'
    output_path = '/workspace/documents/price_action_analysis.png'
    print(f'--- {symbol} 盤面分析中 ---')
    try:
        df, levels = get_levels(symbol)
        
        # 繪圖
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['close'], label='Close Price', color='gray', alpha=0.5)
        
        last_resists = [l for l in levels if l[0] == 'Resistance'][-5:]
        for type, price, ts in last_resists:
            plt.axhline(y=price, color='r', linestyle='--', alpha=0.4)
            plt.text(df['timestamp'].iloc[0], price, f'R: {price}', color='red', fontsize=8)
            print(f'{type}: {price}')

        plt.title(f'{symbol} Price Action Analysis')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(output_path)
        print(f'圖表已儲存至: {output_path}')
    except Exception as e:
        print(f'Error: {e}')