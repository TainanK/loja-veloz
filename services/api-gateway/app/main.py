from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI()

# urls dos outros servicos, pego das variaveis de ambiente
PEDIDOS_URL = os.getenv("PEDIDOS_URL", "http://pedidos:8001")
PAGAMENTOS_URL = os.getenv("PAGAMENTOS_URL", "http://pagamentos:8002")
ESTOQUE_URL = os.getenv("ESTOQUE_URL", "http://estoque:8003")


@app.get("/health")
def health():
    return {"status": "ok", "servico": "api-gateway"}


@app.get("/pedidos/{pedido_id}")
async def get_pedido(pedido_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{PEDIDOS_URL}/pedidos/{pedido_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=404, detail="pedido nao encontrado")
        return resp.json()


@app.post("/pedidos")
async def criar_pedido(payload: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{PEDIDOS_URL}/pedidos", json=payload)
        return resp.json()


@app.get("/estoque/{produto_id}")
async def get_estoque(produto_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ESTOQUE_URL}/estoque/{produto_id}")
        return resp.json()


@app.get("/pagamentos/{pedido_id}")
async def get_pagamento(pedido_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{PAGAMENTOS_URL}/pagamentos/{pedido_id}")
        return resp.json()
