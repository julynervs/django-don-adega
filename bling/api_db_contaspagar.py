import os
import sys

sys.path.insert(1, os.path.abspath("."))

import donadega.settings
import donadega.wsgi

from time import sleep
import logging

logging.basicConfig(
            filename='api_db_contaspagar.log', encoding='utf-8', level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

from get_bling import get_bling

def coloca_contaspagar_no_banco(retorno_get):
    from bling.models import Contato
    from bling.models import ContaPagar

    lista_contas = retorno_get['contaspagar']

    # percorre a lista de todos os contas
    for n in range(len(lista_contas)):
        conta_bling = lista_contas[n]['contapagar']
        chaves = list(lista_contas[n]['contapagar'].keys())

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

        # cadastro foreign key
        # # identifica o fornecedor que fez a conta
        # # e obtém o mesmo do banco de dados
        nome_fornecedor_bling = conta_bling['fornecedor']['nome']
        fornecedor_db = Contato.objects.filter(nome=nome_fornecedor_bling).order_by('id').first()            
        conta_db = ContaPagar.objects.create(fornecedor = fornecedor_db)

        # cadastros data
        if chave_existe('dataEmissao'):
            conta_db = ContaPagar.objects.create(data_emissao = valor_correto_ou_nada('dataEmissao'))   
            logging.info(f"____data_emissao do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'data_emissao' NÃO foi cadastrado por não existir no json")

        if chave_existe('vencimento'):
            conta_db = ContaPagar.objects.create(vencimento = valor_correto_ou_nada('vencimento'))   
            logging.info(f"____vencimento do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'vencimento' NÃO foi cadastrado por não existir no json")

        if chave_existe('competencia'):
            conta_db = ContaPagar.objects.create(competencia = valor_correto_ou_nada('competencia'))   
            logging.info(f"____competencia do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'competencia' NÃO foi cadastrado por não existir no json")

        # cadastros float
        if chave_existe('valor'):
            conta_db = ContaPagar.objects.create(valor = valor_correto_ou_nada('valor'))   
            logging.info(f"____valor do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'valor' NÃO foi cadastrado por não existir no json")
        if chave_existe('saldo'):
            conta_db = ContaPagar.objects.create(saldo = valor_correto_ou_nada('saldo'))   
            logging.info(f"____saldo do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'saldo' NÃO foi cadastrado por não existir no json")
        
        # cadastros int
        if chave_existe('id'):
            conta_db = ContaPagar.objects.create(id_bling = valor_correto_ou_nada('id'))   
            logging.info(f"____id_bling do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'id_bling' NÃO foi cadastrado por não existir no json")

        # cadastros string
        if chave_existe('situacao'):
            conta_db = ContaPagar.objects.create(situacao = valor_correto_ou_nada('situacao'))   
            logging.info(f"____situacao do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'situacao' NÃO foi cadastrado por não existir no json")

        if chave_existe('historico'):
            conta_db = ContaPagar.objects.create(historico = valor_correto_ou_nada('historico'))   
            logging.info(f"____historico do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'historico' NÃO foi cadastrado por não existir no json")

        if chave_existe('ocorrencia'):
            conta_db = ContaPagar.objects.create(ocorrencia = valor_correto_ou_nada('ocorrencia'))   
            logging.info(f"____ocorrencia do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'ocorrencia' NÃO foi cadastrado por não existir no json")

        if chave_existe('categoria'):
            conta_db = ContaPagar.objects.create(categoria = valor_correto_ou_nada('categoria'))   
            logging.info(f"____categoria do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'categoria' NÃO foi cadastrado por não existir no json")
      
        conta_db.save()
        print(f"- Conta a pagar {n} {conta_bling['historico']} cadastrada")

def main():
    paginas = 250
    for pagina in range(1, paginas):
        print("\n")
        print("#"*10)
        print(f"Página {pagina}")
        logging.info(f"Cadastrando contas a pagar da Página {pagina}")
        print("#"*10)
        if get_bling(modulo='contaspagar', pagina=pagina):
            coloca_contaspagar_no_banco(get_bling(modulo='contaspagar', pagina=pagina)) 
        else:
            print(f"Página {pagina} não encontrada")
            break
        sleep(0.4)

if __name__ == "__main__":
    main()