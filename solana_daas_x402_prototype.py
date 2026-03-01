#!/usr/bin/env python3
import sys
import json
import subprocess
from datetime import datetime

def run_demo():
    topic = 'Solana_Sentiments'
    # 1. 呼叫數據服務獲取數據
    data_proc = subprocess.run(['python3', '/app/custom_tools/social_data_service_demo.py', topic], capture_output=True, text=True)
    raw_data = json.loads(data_proc.stdout)
    
    # 2. 模擬 x402 鎖定邏輯
    price = 0.05 # 5 cents USD in SOL
    receipt = {
        'service': 'Consiliarius DaaS',
        'status': '402_REQUIRED',
        'payment_address': '8xJ...Solana_Address',
        'amount_sol': price,
        'data_preview': f'First 2 items of {topic} analysis...',
        'instructions': 'Pay to unlock full JSON report.'
    }
    
    # 3. 模擬支付後解鎖結果
    unlocked_result = {
        'transaction_id': '5mY...Tx_Signature',
        'verified': True,
        'payload': raw_data['data']
    }
    
    return {
        'stage_1_request': topic,
        'stage_2_locked': receipt,
        'stage_3_unlocked': unlocked_result
    }

if __name__ == '__main__':
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))