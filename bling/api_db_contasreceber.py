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
    from bling.models import FormaPagamento

    lista_contas = retorno_get['contasreceber']

    # percorre a lista de todos os contas
    for n in range(len(lista_contas)):
        conta_bling = lista_contas[n]['contaReceber']
        chaves = list(lista_contas[n]['contaReceber'].keys())

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

        # cadastros foreign key
        # # identifica o cliente que fez a conta
        # # e obtém o mesmo do banco de dados
        nome_cliente_bling = conta_bling['cliente']['nome']
        cliente_db = Contato.objects.filter(nome=nome_cliente_bling).order_by('id').first()            
        conta_db = ContaReceber.objects.create(cliente = cliente_db)
        
        forma_pagamento_bling = conta_bling['idFormaPagamento']
        forma_pagamento_db = FormaPagamento.objects.filter(descricao=forma_pagamento_bling).order_by('id').first()            
        conta_db = ContaReceber.objects.create(forma_pagamento = forma_pagamento_db)

        # cadastros data
        if chave_existe('dataEmissao'):
            conta_db = ContaReceber.objects.create(data_emissao = valor_correto_ou_nada('dataEmissao'))   
            logging.info(f"____data_emissao do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'data_emissao' NÃO foi cadastrado por não existir no json")

        if chave_existe('vencimento'):
            conta_db = ContaReceber.objects.create(vencimento = valor_correto_ou_nada('vencimento'))   
            logging.info(f"____vencimento do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'vencimento' NÃO foi cadastrado por não existir no json")

        if chave_existe('competencia'):
            conta_db = ContaReceber.objects.create(competencia = valor_correto_ou_nada('competencia'))   
            logging.info(f"____competencia do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'competencia' NÃO foi cadastrado por não existir no json")

        # cadastros float
        if chave_existe('valor'):
            conta_db = ContaReceber.objects.create(valor = valor_correto_ou_nada('valor'))   
            logging.info(f"____valor do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'valor' NÃO foi cadastrado por não existir no json")
        if chave_existe('saldo'):
            conta_db = ContaReceber.objects.create(saldo = valor_correto_ou_nada('saldo'))   
            logging.info(f"____saldo do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'saldo' NÃO foi cadastrado por não existir no json")
        
        # cadastros int
        if chave_existe('id'):
            conta_db = ContaReceber.objects.create(id_bling = valor_correto_ou_nada('id'))   
            logging.info(f"____id_bling do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'id_bling' NÃO foi cadastrado por não existir no json")
        
        if chave_existe('nroNoBanco'):
            conta_db = ContaReceber.objects.create(nro_banco = valor_correto_ou_nada('nroNoBanco'))   
            logging.info(f"____nro_banco do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'nro_banco' NÃO foi cadastrado por não existir no json")

        # cadastros string
        if chave_existe('situacao'):
            conta_db = ContaReceber.objects.create(situacao = valor_correto_ou_nada('situacao'))   
            logging.info(f"____situacao do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'situacao' NÃO foi cadastrado por não existir no json")

        if chave_existe('historico'):
            conta_db = ContaReceber.objects.create(historico = valor_correto_ou_nada('historico'))   
            logging.info(f"____historico do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'historico' NÃO foi cadastrado por não existir no json")

        if chave_existe('ocorrencia'):
            conta_db = ContaReceber.objects.create(ocorrencia = valor_correto_ou_nada('ocorrencia'))   
            logging.info(f"____ocorrencia do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'ocorrencia' NÃO foi cadastrado por não existir no json")

        if chave_existe('categoria'):
            conta_db = ContaReceber.objects.create(categoria = valor_correto_ou_nada('categoria'))   
            logging.info(f"____categoria do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'categoria' NÃO foi cadastrado por não existir no json")
        
        if chave_existe('vendedor'):
            conta_db = ContaReceber.objects.create(vendedor = valor_correto_ou_nada('vendedor'))   
            logging.info(f"____vendedor do pedido {n} cadastrado")
        else:
            logging.info(f"____O campo 'vendedor' NÃO foi cadastrado por não existir no json")
      
        conta_db.save()
        print(f"- Conta a receber {n} {conta_bling['historico']} cadastrada")

def main():
    paginas = 250
    for pagina in range(1, paginas):
        print("\n")
        print("#"*10)
        print(f"Página {pagina}")
        logging.info(f"Cadastrando contas a receber da Página {pagina}")
        print("#"*10)
        if get_bling(modulo='contasreceber', pagina=pagina):
            coloca_contasreceber_no_banco(get_bling(modulo='contasreceber', pagina=pagina)) 
        else:
            print(f"Página {pagina} não encontrada")
            break
        sleep(0.4)

if __name__ == "__main__":
    main()