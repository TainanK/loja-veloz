from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# estoque inicial com alguns produtos de exemplo
estoque = {
    1: {"produto_id": 1, "nome": "Camiseta", "quantidade": 100},
    2: {"produto_id": 2, "nome": "Calca", "quantidade": 50},
    3: {"produto_id": 3, "nome": "Tenis", "quantidade": 30},
}


class Reserva(BaseModel):
    produto_id: int
    quantidade: int


@app.get("/health")
def health():
    return {"status": "ok", "servico": "estoque"}


@app.get("/estoque")
def listar():
    return list(estoque.values())


@app.get("/estoque/{produto_id}")
def get_produto(produto_id: int):
    item = estoque.get(produto_id)
    if not item:
        raise HTTPException(status_code=404, detail="produto nao encontrado")
    return item


@app.post("/estoque/reservar")
def reservar(reserva: Reserva):
    item = estoque.get(reserva.produto_id)
    if not item:
        raise HTTPException(status_code=404, detail="produto nao encontrado")
    if item["quantidade"] < reserva.quantidade:
        raise HTTPException(status_code=400, detail="quantidade insuficiente em estoque")

    estoque[reserva.produto_id]["quantidade"] -= reserva.quantidade
    return {"mensagem": "reserva feita", "restante": estoque[reserva.produto_id]["quantidade"]}


@app.post("/estoque/devolver")
def devolver(reserva: Reserva):
    item = estoque.get(reserva.produto_id)
    if not item:
        raise HTTPException(status_code=404, detail="produto nao encontrado")

    estoque[reserva.produto_id]["quantidade"] += reserva.quantidade
    return {"mensagem": "devolucao feita", "atual": estoque[reserva.produto_id]["quantidade"]}
