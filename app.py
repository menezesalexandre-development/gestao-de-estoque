from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='gestao-de-estoque'
)

cursor = db.cursor()


class Produto(BaseModel):
    id: int
    nome: str
    categoria: str
    tipo: str
    preco: float
    qtd_estoque: int
    qtd_estoque_minima: int
    fornecedor: str


@app.get("/")
def ler_estoque():
    try:
        order_by = 'id'
        cursor.execute(f'SELECT * FROM produtos ORDER BY {order_by}')
        produtos = [
            {'id': row[0], 'nome': row[1], 'categoria': row[2], 'tipo': row[3], 'preco': row[4], 'qtd_estoque': row[5],
             'qtd_estoque_minima': row[6], 'fornecedor': row[7]} for row in cursor.fetchall()]
        return produtos
    except:
        raise HTTPException(status_code=500, detail='Database error')


@app.delete("/delete/{produto_id}")
def deletar_produto(produto_id: int):
    cursor.execute(f'DELETE FROM produtos WHERE `produtos`.`id` = {produto_id}')
    return f'Produto deletado com sucesso!'

