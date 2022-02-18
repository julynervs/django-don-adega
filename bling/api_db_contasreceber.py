import os
import sys

sys.path.insert(1, os.path.abspath("."))

import donadega.settings
import donadega.wsgi

from time import sleep
import logging

logging.basicConfig(
            filename='api_db_contasreceber.log', encoding='utf-8', level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

from get_bling import get_bling

def coloca_contasreceber_no_banco(retorno_get):
    from bling.models import Contato
    from bling.models import ContaReceber

    lista_contas = retorno_get['contasreceber']

    # percorre a lista de todos os contas
    for n in range(len(lista_contas)):
        conta_bling = lista_contas[n]['contareceber']
        chaves = list(lista_contas[n]['contareceber'].keys())

        # filtro
        def valor_correto_ou_nada(chave):
            if conta_bling[chave] == '':
                logging.warning(f"____{chave} da conta {n} incorreta ou não existente, None definido no campo")
                return None
            else:
                logging.info(f"____{chave} da conta {n} cadastrada")
                return conta_bling[chave]

        # filtro para existencia de um dado no JSON do Bling
        def chave_existe(chave_bling):
            if chave_bling in conta_bling.keys():
                return True
            else:
                return False   
