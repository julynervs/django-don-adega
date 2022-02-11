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

from time import sleep

def get_pedidos(pagina):
    """
    Função que faz requisição GET pedidos pela API do bling 
    """
    url = f"https://bling.com.br/Api/v2/pedidos/page={pagina}/json/?apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19"
    payload='apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    sleep(0.5)
    return response.text

def coloca_pedidos_no_banco(pagina):
    """
    Esta função recebe o retorno de get_contatos(),
    faz o tratamento dos dados do JSON
    e salva essas informações no banco de dados do Django
    """
    import json
    from bling.models import Pedido
    from bling.models import Item

    # formata json recebido
    json = json.loads(get_pedidos(pagina))
    lista_pedidos = json['retorno']['pedidos']

    print("\n")
    print("#"*10)
    print(f"Página {pagina}")
    print("#"*10)

    c = []
    # percorre a lista de todos os pedidos
    for n in range(len(lista_pedidos)):
        pedido_bling = lista_pedidos[n]['pedido']
        chaves = list(lista_pedidos[n]['pedido'].keys())
        # print(pedido_bling)
        # break
        nome_cliente_bling = pedido_bling['cliente']['nome']

        # # identifica o cliente que fez o pedido
        # # e obtém o mesmo do banco de dados
        # nome_contato = Contato.objects.filter(nome=nome_cliente_bling).order_by('id').first()
        # print(nome_contato.id)

        pedido_db = Pedido.objects.create(
                        data = pedido_bling['data']
        )

        pedido_db.save()

        if "itens" in pedido_bling:
            itens_bling = pedido_bling['itens']
            print("Itens:")
            for item in itens_bling:
                item = item['item']
                item_db = Item.objects.create(
                            codigo = item['codigo'],
                            descricao = item['descricao'],
                            quantidade = item['quantidade'],
                            valor_unidade = item['valorunidade'],
                            preco_custo = item['precocusto'],
                            desconto_item = item['descontoItem'],
                            peso_bruto = item['pesoBruto'],
                            largura = item['largura'],
                            altura = item['altura'],
                            profundidade = item['profundidade'],
                            unidade_medida = item['unidadeMedida'],
                            gtin = item['gtin'],
                            pedido = pedido_db,
                )
                item_db.save()

        # nome_contato = Contato.objects.filter(nome=nome_cliente_bling).order_by('id').first()
        # print(nome_contato.id)
        break


coloca_pedidos_no_banco(1)