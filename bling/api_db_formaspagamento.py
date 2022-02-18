import requests
import os
import sys
import re

from time import sleep

sys.path.insert(1, os.path.abspath("."))

import donadega.settings
import donadega.wsgi
import logging

logging.basicConfig(
            filename='api_db_formaspagamento.log', encoding='utf-8', level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

from get_bling import get_bling

def coloca_formaspagamento_no_banco(retorno_get):
    from bling.models import FormaPagamento

    lista_contatos = retorno_get['formaspagamento']
   
    # percorre a lista de todos os pagametos da requisição (página)
    formapagamento_db = None
    for n in range(len(lista_contatos)):
        formapagamento_bling = lista_contatos[n]['formapagamento']

        # filtro
        def valor_correto_ou_nada(chave):
            if formapagamento_bling[chave] == '':
                logging.warning(f"____{chave} da conta {n} incorreta ou não existente, None definido no campo")
                return None
            else:
                logging.info(f"____{chave} da conta {n} cadastrada")
                return formapagamento_bling[chave]

        chaves = list(lista_contatos[n]['formapagamento'].keys())

        formapagamento_db = FormaPagamento.objects.create(
                            id_bling = valor_correto_ou_nada('id'),
                            descricao = valor_correto_ou_nada('descricao'),
                            codigo_fiscal = valor_correto_ou_nada('codigoFiscal'),
                            padrao = valor_correto_ou_nada('padrao'),
                            situacao = valor_correto_ou_nada('situacao'),
                            fixa = valor_correto_ou_nada('fixa')
                        )

        formapagamento_db.save()

        print(f"- Forma de pagamento {n} {formapagamento_bling['descricao']} cadastrada")

def main():
    pagina = 1
    print("\n")
    print("#"*10)
    print(f"Página {pagina}")
    logging.info(f"Cadastrando contas a receber da Página {pagina}")
    print("#"*10)
    if get_bling(modulo='formaspagamento', pagina=pagina):
        coloca_formaspagamento_no_banco(get_bling(modulo='formaspagamento', pagina=pagina)) 
    else:
        print(f"Página {pagina} não encontrada")

if __name__ == "__main__":
    main()