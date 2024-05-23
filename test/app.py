import requests

id = 122

api_url = f'http://127.0.0.1:8000/deletar_produto/{id}'
post_request = requests.delete(api_url)

if post_request.status_code == 200:
    print(post_request)
    print("success")
else:
    print(post_request)
    print("failure")
