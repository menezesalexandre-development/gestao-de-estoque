import requests

data = {
    "id": 0,
    "nome": "PS3",
    "categoria": "Tecnologia",
    "tipo": "Videogame",
    "preco": 833.90,
    "qtd_estoque": 50,
    "qtd_estoque_minima": 10
}

api_url = "http://127.0.0.1:8000/cadastrar_produto"
post_request = requests.post(api_url, json=data)

if post_request.status_code == 200:
    print(post_request)
    print("success")
else:
    print(post_request)
    print("failure")
