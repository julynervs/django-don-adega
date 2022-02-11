"""
Este script é responsável por transferir os dados dos contatos cadastrados no Bling
para o banco de dados sqlite do Django.

"""
import requests
import os
import sys

sys.path.insert(1, os.path.abspath("."))

import donadega.settings
import donadega.wsgi

def get_pedidos():
    """
    Função que faz requisição GET pedidos pela API do bling 
    """
    url = "https://bling.com.br/Api/v2/pedidos/json/?apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19"

    payload='apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

def coloca_pedido_no_banco():
    """
    Função que recebe o retorno de get_contatos(),
    faz o tratamento dos dados do JSON
    e salva essas informações no banco de dados do Django
    """
    import json
    from bling.models import Pedido
    from bling.models import Contato

    # formata json recebido
    json = json.loads(get_pedidos())
    lista_pedidos = json['retorno']['pedidos']

    # percorre a lista de todos os pedidos
    for n in range(len(lista_pedidos)):
        pedido_bling = lista_pedidos[n]['pedido']
        chaves = list(lista_pedidos[n]['pedido'].keys())
        
        nome_cliente_bling = pedido_bling['cliente']['nome']
        # print(nome_cliente_bling)
        # cliente_db = Contato.objects.get()

        c = Contato.objects.get(nome='Don Adega Goiatuba')
        print(c)

        # pedido.cliente = Contato.objects.get(nome=nome_cliente_bling)
        # pedido.save()
coloca_pedido_no_banco()