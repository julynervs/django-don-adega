#%%
from time import sleep
import requests
import json
import logging

def get_produtos(pagina):
    url = f"https://bling.com.br/Api/v2/produtos/page={pagina}/json/?apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19"
    payload='apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    sleep(0.4)

    # verifica se a requisição deu certo
    if response.status_code == 200:
        # formata json recebido
        response = json.loads(response.text)
        response = response['retorno']
        # caso tenha erros retornados pelo json
        if 'erros' in response.keys():
            print(response['erros'])
            logging.error(response['erros'])
            return False
        # se não tiver erro no json
        else:
            return True
    # erro de requisição status code (quando for diferente de 200)
    else:
        logging.error(f"Status code: {response.status_code}")
        return False

#%%
# Agenda #
# 16/02: começamos a verificar determinados erros da requisição
# Para amanhã (17/02): continuar a verificação com relação aos
#                     erros que o bling retorna e continuar api_db_produtos.py