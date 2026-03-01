#!/usr/bin/env python3
import sys
import requests
import json

def analyze_order_book(symbol='BTCUSDC', limit=100):
    # 判斷是否為永續合約 (The Leap 競賽格式如 BTCUSDC.P)
    is_perp = symbol.endswith('.P') or 'USDC' in symbol
    if is_perp:
        clean_symbol = symbol.replace('.P', '')
        url = f'https://fapi.binance.com/fapi/v1/depth?symbol={clean_symbol}&limit={limit}'
    else:
        url = f'https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'bids' not in data:
            print(f'API 回傳異常: {data}')
            return

        bids = [[float(p), float(q)] for p, q in data['bids']] # 買單
        asks = [[float(p), float(q)] for p, q in data['asks']] # 賣單
        
        support_wall = max(bids, key=lambda x: x[1])
        resistance_wall = max(asks, key=lambda x: x[1])
        
        print(f'--- {symbol} 交易簿分析報告 ---')
        print(f'當前偵測深度: {limit} 檔')
        print(f'最強支撐位: {support_wall[0]} (掛單量: {support_wall[1]})')
        print(f'最強壓力位: {resistance_wall[0]} (掛單量: {resistance_wall[1]})')
        
        total_bid_vol = sum(q for p, q in bids)
        total_ask_vol = sum(q for p, q in asks)
        imbalance = (total_bid_vol - total_ask_vol) / (total_bid_vol + total_ask_vol)
        print(f'盤面失衡度: {imbalance:.4f} (正值偏多, 負值偏空)')
        
    except Exception as e:
        print(f'發生錯誤: {e}')

if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'BTCUSDC'
    analyze_order_book(symbol)