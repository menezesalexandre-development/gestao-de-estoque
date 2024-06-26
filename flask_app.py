from flask import Flask, render_template, request, redirect
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
    query = 'SELECT * FROM produtos ORDER BY id DESC;'
    cursor = db.cursor()
    cursor.execute(query)
    produtos = cursor.fetchall()

    query = 'SELECT COUNT(*) FROM produtos;'
    cursor = db.cursor()
    cursor.execute(query)
    qtd_produtos = cursor.fetchall()

    return render_template('index.html', produtos=produtos, qtd_produtos=qtd_produtos)

# MÉTODO POST:
@app.route("/adicionar_produto", methods=["GET", "POST"])
def adicionar_produto():
    if request.method == "POST":
        try:
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
                return redirect("/")
            else:
                print(f"Failure: {post_request}")
        except ValueError:
            return redirect("/adicionar_produto")

    return render_template('add_produto.html')

# MÉTODO PUT:
@app.route("/editar_produto/<int:produto_id>", methods=["GET", "POST"])
def editar_produto(produto_id):
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='gestao-de-estoque'
    )

    query = f'SELECT nome FROM produtos WHERE id = {produto_id};'
    cursor = db.cursor()
    cursor.execute(query)
    produto_nome = cursor.fetchall()
    
    if request.method == "POST":
        try:
            data = {
                "id": produto_id,
                "nome": str(request.form["input_nome"]),
                "categoria": str(request.form["input_categoria"]),
                "tipo": str(request.form["input_tipo"]),
                "preco": float(request.form["input_preco"]),
                "qtd_estoque": int(request.form["input_qtd_estoque"]),
                "qtd_estoque_minima": int(request.form["input_qtd_estoque_minima"])
            }
            
            api_url = f'http://127.0.0.1:8000/atualizar_produto/{data["id"]}'
            put_request = requests.put(api_url, json=data)

            if put_request.status_code == 200:
                print(put_request)
                print("success")
                return redirect("/")
            else:
                print(put_request)
                print("failure")
        except ValueError:
            return redirect(f"/editar_produto/{produto_id}")
        
    return render_template('editar_produto.html', produto_nome=produto_nome, produto_id=produto_id)

# MÉTODO DELETE:
@app.route("/deletar_produto/<int:produto_id>")
def deletar_produto(produto_id):
    api_url = f'http://127.0.0.1:8000/deletar_produto/{produto_id}'
    delete_request = requests.delete(api_url)

    if delete_request.status_code == 200:
        print(delete_request)
        print("success")
    else:
        print(delete_request)
        print("failure")

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, port=5000)


