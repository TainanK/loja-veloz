from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

# guardo os pagamentos em memoria mesmo, nao precisa de banco aqui
pagamentos = {}


class PagamentoCreate(BaseModel):
    pedido_id: int
    valor: float
    metodo: str


@app.get("/health")
def health():
    return {"status": "ok", "servico": "pagamentos"}


@app.post("/pagamentos", status_code=201)
def processar(pagamento: PagamentoCreate):
    # simula aprovacao com 90% de chance
    aprovado = random.random() > 0.1

    registro = {
        "id": len(pagamentos) + 1,
        "pedido_id": pagamento.pedido_id,
        "valor": pagamento.valor,
        "metodo": pagamento.metodo,
        "status": "aprovado" if aprovado else "recusado"
    }
    pagamentos[pagamento.pedido_id] = registro
    return registro


@app.get("/pagamentos/{pedido_id}")
def get_pagamento(pedido_id: int):
    p = pagamentos.get(pedido_id)
    if not p:
        raise HTTPException(status_code=404, detail="pagamento nao encontrado")
    return p
