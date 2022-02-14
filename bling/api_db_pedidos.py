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
import logging

logging.basicConfig(
            filename='api_db_pedidos.log', encoding='utf-8', level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

### LOGGING ###
# Nível  |  Quando é usando
# DEBUG -> Informação detalhada, tipicamente de interesse apenas quando diagnosticando problemas.
# INFO -> Confirmação de que as coisas estão funcionando como esperado.
# WARNING -> Uma indicação que algo inesperado aconteceu, ou um indicativo que algum problema 
#            em um futuro próximo (ex.: ‘pouco espaço em disco’). 
#            O software está ainda funcionando como esperado.
# ERROR -> Por conta de um problema mais grave, o software não conseguiu executar alguma função.
# CRITICAL -> Um erro grave, indicando que o programa pode não conseguir continuar rodando.

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
    from bling.models import Contato
    from bling.models import Pedido
    from bling.models import Item

    # formata json recebido
    json = json.loads(get_pedidos(pagina))
    lista_pedidos = json['retorno']['pedidos']

    print("\n")
    print("#"*10)
    print(f"Página {pagina}")
    print("#"*10)

    # percorre a lista de todos os pedidos
    for n in range(len(lista_pedidos)):
        pedido_bling = lista_pedidos[n]['pedido']
        chaves = list(lista_pedidos[n]['pedido'].keys())
        # print(pedido_bling)
        # break
        nome_cliente_bling = pedido_bling['cliente']['nome']

        # # identifica o cliente que fez o pedido
        # # e obtém o mesmo do banco de dados
        cliente_db = Contato.objects.filter(nome=nome_cliente_bling).order_by('id').first()
        
        # cria objeto Pedido no banco de dados
        pedido_db = Pedido.objects.create(
                        cliente = cliente_db,
                        data = pedido_bling['data'],
                        numero = pedido_bling['numero'],
                        vendedor = pedido_bling['vendedor'],
                        vlr_frete = pedido_bling['valorfrete'],
                        vlr_desconto = pedido_bling['desconto'].replace(',', '.'),
                        total_produtos = pedido_bling['totalprodutos'],
                        total_venda = pedido_bling['totalvenda'],
                        situacao = pedido_bling['situacao'],
                        data_saida = pedido_bling['dataSaida'],
                        # numero_pedido_loja = pedido_bling['numeroPedidoLoja'],
                        # tipo_integracao = pedido_bling['tipoIntegracao'],
        )

        pedido_db.save()
        sleep(0.1)
        logging.info(f"# Página {pagina}: Pedido {n} {pedido_bling['numero']} cadastrado")
        print(f"# Pedido {n} {pedido_bling['numero']}, Cliente {cliente_db.nome} cadastrado")

        if "itens" in pedido_bling:
            itens_bling = pedido_bling['itens']
            print("Itens:")
            for item in itens_bling:
                item = item['item']
                # valida valores '', quando se espera um numero
                for key in item.keys():
                    if item[key] == '':
                        item[key] = 0
                # cria objeto Item no banco de dados
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
                print(f"- {item['descricao']}")
def main():

    paginas = 250
    for pagina in range(7, paginas):
        # try:
        coloca_pedidos_no_banco(pagina)
        # except Exception as e:
        #     print(e)
        #     print("Não tem mais produtos para cadastrar.")
        #     break
        # else:
        #     print(f"{pagina} páginas foram cadastradas.")
main()