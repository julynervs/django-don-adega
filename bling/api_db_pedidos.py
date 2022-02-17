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

"""
## LOGGING ###
Nível  |  Quando é usando
DEBUG -> Informação detalhada, tipicamente de interesse apenas quando diagnosticando problemas.
INFO -> Confirmação de que as coisas estão funcionando como esperado.
WARNING -> Uma indicação que algo inesperado aconteceu, ou um indicativo que algum problema 
           em um futuro próximo (ex.: ‘pouco espaço em disco’). 
           O software está ainda funcionando como esperado.
ERROR -> Por conta de um problema mais grave, o software não conseguiu executar alguma função.
CRITICAL -> Um erro grave, indicando que o programa pode não conseguir continuar rodando.
"""

from get_bling import get_bling

def coloca_pedidos_no_banco(retorno_get):
    """
    Esta função recebe o retorno de get_contatos(),
    faz o tratamento dos dados do JSON
    e salva essas informações no banco de dados do Django
    """
    from bling.models import Contato
    from bling.models import Pedido
    from bling.models import Item

    lista_pedidos = retorno_get['pedidos']

    # percorre a lista de todos os pedidos
    for n in range(len(lista_pedidos)):
        pedido_bling = lista_pedidos[n]['pedido']
        chaves = list(lista_pedidos[n]['pedido'].keys())

        # filtro
        def valor_correto_ou_nada(chave):
            if pedido_bling[chave] == '':
                logging.warning(f"____{chave} do produto {n} incorreta ou não existente, None definido no campo")
                return None
            else:
                logging.info(f"____{chave} do produto {n} cadastrada")
                return pedido_bling[chave]

        # filtro para existencia de um dado no JSON do Bling
        def chave_existe(chave_bling):
            if chave_bling in pedido_bling.keys():
                return True
            else:
                return False   

        # # identifica o cliente que fez o pedido
        # # e obtém o mesmo do banco de dados
        nome_cliente_bling = pedido_bling['cliente']['nome']
        cliente_db = Contato.objects.filter(nome=nome_cliente_bling).order_by('id').first()            
        # cria objetos Pedido no banco de dados
        pedido_db = Pedido.objects.create(cliente = cliente_db)
        # cadastro de datas
        if chave_existe('numeroPedidoLoja'):
            pedido_db = Pedido.objects.create(data = valor_correto_ou_nada('data'))   
            logging.info(f"____numero_pedido_loja do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'numero_pedido_loja' NÃO foi cadastrado por não existir no json")

        if chave_existe('dataSaida'):       
            pedido_db = Pedido.objects.create(data_saida = valor_correto_ou_nada('dataSaida'))
            logging.info(f"____data_saida {n} cadastrado")
        else:
            logging.info(f"____O campo 'data_saida' NÃO foi cadastrado por não existir no json")

        # cadastro de números
        ## int
        if chave_existe('numero'):
            pedido_db = Pedido.objects.create(numero = valor_correto_ou_nada('numero'))
            logging.info(f"____numero do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'numero' NÃO foi cadastrado por não existir no json")
        
        if chave_existe('numeroPedidoLoja'):
            pedido_db = Pedido.objects.create(numero_pedido_loja = valor_correto_ou_nada('numeroPedidoLoja'))
            logging.info(f"____numero_pedido_loja do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'numero_pedido_loja' NÃO foi cadastrado por não existir no json")

        ## float
        if chave_existe('valorfrete'):
            pedido_db = Pedido.objects.create(vlr_frete = valor_correto_ou_nada('valorfrete'))
            logging.info(f"____vlr_frete do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'vlr_frete' NÃO foi cadastrado por não existir no json")
        
        if chave_existe('desconto'):
            pedido_db = Pedido.objects.create(vlr_desconto = valor_correto_ou_nada('desconto').replace(',', '.'))
            logging.info(f"____vlr_desconto do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'vlr_desconto' NÃO foi cadastrado por não existir no json")

        if chave_existe('totalprodutos'):
            pedido_db = Pedido.objects.create(total_produtos = valor_correto_ou_nada('totalprodutos'))
            logging.info(f"____total_produtos do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'total_produtos' NÃO foi cadastrado por não existir no json")
       
        if chave_existe('totalvenda'):
            pedido_db = Pedido.objects.create(total_venda = valor_correto_ou_nada('totalvenda'))
            logging.info(f"____total_venda do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'total_venda' NÃO foi cadastrado por não existir no json")

        # cadastro de textos
        pedido_db = Pedido.objects.create(vendedor = valor_correto_ou_nada('vendedor'))
        pedido_db = Pedido.objects.create(situacao = valor_correto_ou_nada('situacao'))

        if chave_existe('tipoIntegracao'):
            pedido_db = Pedido.objects.create(tipo_integracao = valor_correto_ou_nada('tipoIntegracao'))                
            logging.info(f"____tipo_integracao do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'tipo_integracao' NÃO foi cadastrado por não existir no json")

        pedido_db.save()
    
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
                # texto
                item_db = Item.objects.create(codigo = item['codigo'])
                if chave_existe('descricao'):
                    item_db = Item.objects.create(descricao = valor_correto_ou_nada('descricao'))
                    logging.info(f"____descricao do produto Kit {n} cadastrado")
                else:
                    logging.info(f"____O campo 'descricao' NÃO foi cadastrado por não existir no json")
                item_db = Item.objects.create(descricao = item['descricao'])
                item_db = Item.objects.create(unidade_medida = item['unidadeMedida'])

                # int
                item_db = Item.objects.create(gtin = item['gtin'])
                # float
                item_db = Item.objects.create(
                            quantidade = item['quantidade'],
                            valor_unidade = item['valorunidade'],
                            preco_custo = item['precocusto'],
                            desconto_item = item['descontoItem'],
                            peso_bruto = item['pesoBruto'],
                            largura = item['largura'],
                            altura = item['altura'],
                            profundidade = item['profundidade']
                        )
                
                if 'descricao' in item:
                    item_db = Item.objects.create(
                        descricao = item['descricao']
                    )

                item_db.save()
                print(f"- {item['descricao']}")
        else:
            pass

def main():
    paginas = 250
    for pagina in range(1, paginas):
        print("\n")
        print("#"*10)
        print(f"Página {pagina}")
        logging.info(f"Cadastrando pedidos da Página {pagina}")
        print("#"*10)
        if get_bling(modulo='pedidos', pagina=pagina):
            coloca_pedidos_no_banco(get_bling(modulo='pedidos', pagina=pagina)) 
        else:
            print(f"Página {pagina} não encontrada")
            break

if __name__ == "__main__":
    main()