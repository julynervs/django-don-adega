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
        # filtro
        def valor_correto_ou_nada(chave):
            # filtro para existencia de um dado no JSON do Bling
            # se a chave existe, verifica qual o valor relativo à ela
            if chave in pedido_bling.keys():
                # se o valor relativo for '', é um valor incorreto, então retorna None
                if pedido_bling[chave] == '':
                    logging.warning(f"____{chave} da conta {n} incorreta ou não existente, None definido no campo")
                    return None
                # se o valor estiver correto, retorna o valor
                else:
                    logging.info(f"____{chave} da conta {n} cadastrada")
                    return pedido_bling[chave]
            # se a chave não existe, retorna None
            else:
                return None

        # # identifica o cliente que fez o pedido
        # # e obtém o mesmo do banco de dados
        nome_cliente_bling = pedido_bling['cliente']['nome']
        cliente_db = Contato.objects.filter(nome=nome_cliente_bling).order_by('id').first()            
        # cria objetos Pedido no banco de dados
        pedido_db = Pedido.objects.create(cliente = cliente_db)
        # cadastro de datas
        pedido_db = Pedido.objects.create(data = valor_correto_ou_nada('data'))          
        pedido_db = Pedido.objects.create(data_saida = valor_correto_ou_nada('dataSaida'))

        # cadastro de números
        ## int
        pedido_db = Pedido.objects.create(numero = valor_correto_ou_nada('numero'))
        pedido_db = Pedido.objects.create(numero_pedido_loja = valor_correto_ou_nada('numeroPedidoLoja'))
        ## float
        pedido_db = Pedido.objects.create(vlr_frete = valor_correto_ou_nada('valorfrete'))
        pedido_db = Pedido.objects.create(vlr_desconto = valor_correto_ou_nada('desconto').replace(',', '.'))
        pedido_db = Pedido.objects.create(total_produtos = valor_correto_ou_nada('totalprodutos'))
        pedido_db = Pedido.objects.create(total_venda = valor_correto_ou_nada('totalvenda'))

        # cadastro de textos
        pedido_db = Pedido.objects.create(vendedor = valor_correto_ou_nada('vendedor'))
        pedido_db = Pedido.objects.create(situacao = valor_correto_ou_nada('situacao'))
        pedido_db = Pedido.objects.create(tipo_integracao = valor_correto_ou_nada('tipoIntegracao'))                

        pedido_db.save()
        print(f"# Pedido {n} {pedido_bling['numero']}, Cliente {cliente_db.nome} cadastrado")

        # cadastro da tabela Item
        itens_bling = pedido_bling['itens']
        print("Itens:")
        for item in itens_bling:
            item = item['item']
            # cria objeto Item no banco de dados
            # texto
            item_db = Item.objects.create(codigo = valor_correto_ou_nada('codigo'))    
            item_db = Item.objects.create(descricao = valor_correto_ou_nada('descricao'))
            item_db = Item.objects.create(unidade_medida = valor_correto_ou_nada('unidadeMedida'))

            # int
            item_db = Item.objects.create(gtin = valor_correto_ou_nada('gtin'))
            # float
            item_db = Item.objects.create(
                        quantidade = valor_correto_ou_nada('quantidade'),
                        valor_unidade = valor_correto_ou_nada('valorunidade'),
                        preco_custo = valor_correto_ou_nada('precocusto'),
                        desconto_item = valor_correto_ou_nada('descontoItem'),
                        peso_bruto = valor_correto_ou_nada('pesoBruto'),
                        largura = valor_correto_ou_nada('largura'),
                        altura = valor_correto_ou_nada('altura'),
                        profundidade = valor_correto_ou_nada('profundidade')
                    )
            item_db.save()

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