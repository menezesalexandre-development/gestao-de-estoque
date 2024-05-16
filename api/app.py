from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mysql.connector import connect, Error
from typing import List

app = FastAPI()

# BASE DE DADOS
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'gestao-de-estoque'
}


class Produto(BaseModel):
    id: int = None
    nome: str
    categoria: str
    tipo: str
    preco: float
    qtd_estoque: int
    qtd_estoque_minima: int
    fornecedor: str


# CONEXÃO COM BASE DE DADOS
def get_db_connection():
    try:
        connection = connect(**DATABASE_CONFIG)
        return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


# LER PRODUTOS:
@app.get("/", response_model=List[Produto])
def ler_estoque():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM produtos ORDER BY id")
            produtos = cursor.fetchall()
            return [Produto(
                id=row[0],
                nome=row[1],
                categoria=row[2],
                tipo=row[3],
                preco=row[4],
                qtd_estoque=row[5],
                qtd_estoque_minima=row[6],
                fornecedor=row[7]
            ) for row in produtos]
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()


# CRIAR PRODUTO:
@app.post("/cadastrar_produto", response_model=Produto)
def cadastrar_produto(produto: Produto):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = ("INSERT INTO produtos (nome, categoria, tipo, preco, qtd_estoque, qtd_estoque_minima, fornecedor) "
                     "VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s)")
            values = (produto.nome, produto.categoria, produto.tipo, produto.preco, produto.qtd_estoque, produto.qtd_estoque_minima, produto.fornecedor)
            cursor.execute(query, values)
            connection.commit()
            produto.id = cursor.lastrowid
            return produto
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()


# DELETAR PRODUTO:
@app.delete("/deletar_produto/{produto_id}")
def deletar_produto(produto_id: int):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Produto not found")
            connection.commit()
            return {"detail": "Produto deletado com sucesso!"}
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()


# ATUALIZAR PRODUTO:
@app.put("/atualizar_produto/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto: Produto):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = ("UPDATE produtos SET nome = %s, categoria = %s, tipo = %s, preco = %s, qtd_estoque = %s, "
                     "qtd_estoque_minima = %s, fornecedor = %s WHERE id = %s")
            values = (produto.nome, produto.categoria, produto.tipo, produto.preco, produto.qtd_estoque,
                      produto.qtd_estoque_minima, produto.fornecedor, produto_id)
            cursor.execute(query, values)
            connection.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Produto não encontrado")
            return produto
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()
