from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
import requests

app = Flask(__name__)

# METÓDO GET:
@app.route("/")
def homepage_read():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='gestao-de-estoque'
    )
    query = 'SELECT * FROM produtos'
    cursor = db.cursor()
    cursor.execute(query)
    produtos = cursor.fetchall()
    return render_template('index.html', produtos=produtos)

# MÉTODO POST:
@app.route("/adicionar_produto", methods=["GET", "POST"])
def adicionar_produto():
    if request.method == "POST":
        data = {
            "id": 0,
            "nome": str(request.form["input_nome"]),
            "categoria": str(request.form["input_categoria"]),
            "tipo": str(request.form["input_tipo"]),
            "preco": float(request.form["input_preco"]),
            "qtd_estoque": int(request.form["input_qtd_estoque"]),
            "qtd_estoque_minima": int(request.form["input_qtd_estoque_minima"])
        }

        api_url = "http://127.0.0.1:8000/cadastrar_produto"
        post_request = requests.post(api_url, json=data)    

        if post_request.status_code == 200:
            print(f"Sucess: {post_request}")
        else:
            print(f"Failure: {post_request}")
    return render_template('add_produto.html')

# MÉTODO PUT:
@app.route("/editar_produto/<int:produto_id>")
def editar_produto(produto_id):
    return f'Editar produto: {produto_id}'

# MÉTODO DELETE:
@app.route("/deletar_produto/<int:produto_id>")
def deletar_produto(produto_id):
    return f'Deletar produto: {produto_id}'

if __name__ == '__main__':
    app.run(debug=True, port=5000)


