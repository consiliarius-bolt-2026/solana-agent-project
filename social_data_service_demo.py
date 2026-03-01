#!/usr/bin/env python3
import sys
import json
import random
from datetime import datetime

def generate_mock_data(topic):
    # 模擬 Playwright 在 2025 年抓取到的社群數據 (避免無 API 限制的問題)
    sentiments = ['Bullish', 'Neutral', 'Bearish']
    platforms = ['X/Twitter', 'Discord', 'Reddit']
    data = []
    for i in range(5):
        data.append({
            'timestamp': datetime.now().isoformat(),
            'platform': random.choice(platforms),
            'topic': topic,
            'content': f'Mock post content about {topic} number {i}',
            'engagement': random.randint(10, 1000),
            'sentiment_score': round(random.uniform(-1, 1), 2)
        })
    return data

def main():
    if len(sys.argv) < 2:
        print('Usage: social_data_service_demo.py <topic>')
        sys.exit(1)
    
    topic = sys.argv[1]
    result = {
        'service_name': 'Consiliarius DaaS Demo 2025',
        'status': 'Success',
        'extracted_at': datetime.now().isoformat(),
        'data': generate_mock_data(topic)
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()