#!/usr/bin/env python3
import sys
import requests
import json
import os

def launch(name, symbol, description, image_path, wallet_address, agent_id='consiliarius_bolt'):
    base_url = 'https://clawpump.tech'
    
    # Step 1: Upload Image
    print(f'正在上傳圖片: {image_path}...')
    with open(image_path, 'rb') as f:
        files = {'image': f}
        upload_res = requests.post(f'{base_url}/api/upload', files=files)
    
    if not upload_res.json().get('success'):
        return f'圖片上傳失敗: {upload_res.text}'
    
    image_url = upload_res.json()['imageUrl']
    print(f'圖片上傳成功: {image_url}')

    # Step 2: Launch Token
    payload = {
        'name': name,
        'symbol': symbol,
        'description': description,
        'imageUrl': image_url,
        'agentId': agent_id,
        'agentName': 'Consiliarius',
        'walletAddress': wallet_address
    }
    
    print(f'正在發布代幣 {symbol}...')
    launch_res = requests.post(f'{base_url}/api/launch', json=payload)
    return json.dumps(launch_res.json(), indent=2, ensure_ascii=False)

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print('用法: clawpump_launcher.py [name] [symbol] [description] [image_path] [wallet_address]')
        sys.exit(1)
    
    result = launch(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    print(result)