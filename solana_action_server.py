from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import base64
import os
from solders.transaction import Transaction
from solders.message import Message
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solana.rpc.api import Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SAFETY CHECK: Use environment variable for API Key
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY", "your-helius-api-key-here")
RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"

@app.get("/actions.json")
async def get_actions_json():
    return {"rules": [{"pathPattern": "/api/**", "apiPath": "/api/**"}]}

@app.get("/api/memo")
async def get_memo_info():
    return {
        "icon": "https://solana.com/src/img/branding/solana-logo-scientific-2.svg",
        "label": "Send Memo",
        "title": "x402 DaaS Memo (Gasless)",
        "description": "透過 Helius Paymaster 代付 Gas 的 Solana Action。",
        "links": {
            "actions": [
                {
                    "label": "Send Memo",
                    "href": "/api/memo",
                    "parameters": [{"name": "memo", "label": "Enter your memo"}]
                }
            ]
        }
    }

@app.post("/api/memo")
async def post_memo_action(request: Request):
    try:
        body = await request.json()
        account_pubkey_str = body.get("account")
        if not account_pubkey_str:
            return {"error": "Missing account"}
        
        memo_text = body.get("memo", "Hello from Consiliarius x402")
        user_pubkey = Pubkey.from_string(account_pubkey_str)
        
        # 1. 建立一個簡單的 Memo 指令 (使用 Memo Program: MemoSq4gqAB23UFs86tg885a5FvN48X6Kne85f1IS5)
        memo_program_id = Pubkey.from_string("MemoSq4gqAB23UFs86tg885a5FvN48X6Kne85f1IS5")
        instruction = Instruction(
            program_id=memo_program_id,
            accounts=[],
            data=bytes(memo_text, "utf-8")
        )
        
        # 2. 構建交易
        client = Client(RPC_URL)
        latest_blockhash = client.get_latest_blockhash().value.blockhash
        
        msg = Message.new_with_blockhash(
            [instruction],
            user_pubkey,
            latest_blockhash
        )
        
        tx = Transaction.new_unsigned(msg)
        
        # 3. 序列化並回傳
        serialized_tx = base64.b64encode(bytes(tx)).decode("utf-8")
        
        return {
            "transaction": serialized_tx,
            "message": "Memo transaction created!"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
