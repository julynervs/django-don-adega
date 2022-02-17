import logging
import requests
import json

def get_bling(modulo, pagina):
    url = f"https://bling.com.br/Api/v2/{modulo}/page={pagina}/json/?apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19"
    payload='apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    # verifica se a requisição deu certo
    if response.status_code == 200:
        # formata json recebido pela requisição para dicionario
        response = json.loads(response.text)
        response = response['retorno']
        # caso tenha erros retornados pelo json
        if 'erros' in response.keys():
            logging.error(response['erros'])
            return False
        # se não tiver erro no json
        else:
            return response
    # erro de requisição status code (quando for diferente de 200)
    else:
        logging.error(f"Status code: {response.status_code}")
        return False

