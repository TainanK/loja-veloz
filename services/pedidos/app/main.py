from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/lojaveloz")


def conectar():
    return psycopg2.connect(DATABASE_URL)


def criar_tabela():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id SERIAL PRIMARY KEY,
            cliente VARCHAR(100) NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            status VARCHAR(50) DEFAULT 'pendente',
            criado_em TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.on_event("startup")
def startup():
    try:
        criar_tabela()
    except Exception as e:
        print(f"erro ao criar tabela: {e}")


class PedidoCreate(BaseModel):
    cliente: str
    produto_id: int
    quantidade: int


@app.get("/health")
def health():
    return {"status": "ok", "servico": "pedidos"}


@app.post("/pedidos", status_code=201)
def criar_pedido(pedido: PedidoCreate):
    try:
        conn = conectar()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO pedidos (cliente, produto_id, quantidade) VALUES (%s, %s, %s) RETURNING *",
            (pedido.cliente, pedido.produto_id, pedido.quantidade)
        )
        novo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return dict(novo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pedidos/{pedido_id}")
def get_pedido(pedido_id: int):
    try:
        conn = conectar()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM pedidos WHERE id = %s", (pedido_id,))
        pedido = cur.fetchone()
        cur.close()
        conn.close()
        if not pedido:
            raise HTTPException(status_code=404, detail="pedido nao encontrado")
        return dict(pedido)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pedidos")
def listar_pedidos():
    try:
        conn = conectar()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM pedidos ORDER BY criado_em DESC")
        pedidos = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(p) for p in pedidos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
