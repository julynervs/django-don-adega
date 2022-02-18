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
    from bling.models import Pagamento
    from bling.models import Bordero

    lista_contas = retorno_get['contaspagar']

    # percorre a lista de todos os contas
    for n in range(len(lista_contas)):
        conta_bling = lista_contas[n]['contapagar']
        chaves = list(lista_contas[n]['contapagar'].keys())

        # filtro para existencia de um dado no JSON do Bling
        def valor_correto_ou_nada(chave, dict_bling=conta_bling):
            # filtro para existencia de um dado no JSON do Bling
            # se a chave existe, verifica qual o valor relativo à ela
            if chave in dict_bling.keys():
                # se o valor relativo for '', é um valor incorreto, então retorna None
                if dict_bling[chave] == '':
                    logging.warning(f"____{chave} da conta {n} incorreta ou não existente, None definido no campo")
                    return None
                # se o valor estiver correto, retorna o valor
                else:
                    logging.info(f"____{chave} da conta {n} cadastrada")
                    return dict_bling[chave]
            # se a chave não existe, retorna None
            else:
                return None
    
        # cadastro foreign key
        # # identifica o fornecedor que fez a conta
        # # e obtém o mesmo do banco de dados
        nome_fornecedor_bling = conta_bling['fornecedor']['nome']
        fornecedor_db = Contato.objects.filter(nome=nome_fornecedor_bling).order_by('id').first()            
        conta_db = ContaPagar.objects.create(fornecedor = fornecedor_db)

        # cadastros data
        conta_db = ContaPagar.objects.create(data_emissao = valor_correto_ou_nada('dataEmissao'))   
        conta_db = ContaPagar.objects.create(vencimento = valor_correto_ou_nada('vencimento'))   
        conta_db = ContaPagar.objects.create(competencia = valor_correto_ou_nada('competencia'))   

        # cadastros float
        conta_db = ContaPagar.objects.create(valor = valor_correto_ou_nada('valor'))   
        conta_db = ContaPagar.objects.create(saldo = valor_correto_ou_nada('saldo'))   
     
        # cadastros int
        conta_db = ContaPagar.objects.create(id_bling = valor_correto_ou_nada('id'))   
        
        # cadastros string
        conta_db = ContaPagar.objects.create(situacao = valor_correto_ou_nada('situacao'))   
        conta_db = ContaPagar.objects.create(historico = valor_correto_ou_nada('historico'))   
        conta_db = ContaPagar.objects.create(ocorrencia = valor_correto_ou_nada('ocorrencia'))          
        conta_db = ContaPagar.objects.create(categoria = valor_correto_ou_nada('categoria'))   
        conta_db = ContaPagar.objects.create(portador = valor_correto_ou_nada('portador'))   
        conta_db.save()
        if 'historico' in conta_bling.keys():
            print(f"- Conta a pagar {n} {conta_bling['historico']} cadastrada")
        else:
            print(f"- Conta a pagar {n} cadastrada")

        # ## cadastro da tabela Pagamento
        conta_bling_pagamento = conta_bling['pagamento']

        pagamento_db = Pagamento.objects.create(conta_pagar = conta_db)
        pagamento_db = Pagamento.objects.create(total_pago = valor_correto_ou_nada('totalPago', dict_bling=conta_bling_pagamento)) 
        pagamento_db = Pagamento.objects.create(total_juro = valor_correto_ou_nada('totalJuro', dict_bling=conta_bling_pagamento))
        pagamento_db = Pagamento.objects.create(total_desconto = valor_correto_ou_nada('totalDesconto', dict_bling=conta_bling_pagamento))
        pagamento_db = Pagamento.objects.create(total_acrescimo = valor_correto_ou_nada('totalAcrescimo', dict_bling=conta_bling_pagamento))
        pagamento_db = Pagamento.objects.create(total_tarifa = valor_correto_ou_nada('totalTarifa', dict_bling=conta_bling_pagamento))
        pagamento_db = Pagamento.objects.create(data = valor_correto_ou_nada('data', dict_bling=conta_bling_pagamento))
        pagamento_db.save()
        print(f"- Pagamento da conta a pagar {n} cadastrado")

        # ## cadastro da tabela Bordero
        conta_bling_pagamento_borderos = conta_bling['pagamento']     
        bordero_db = Bordero.objects.create(pagamento = pagamento_db)
        bordero_db = Bordero.objects.create(id_bling = valor_correto_ou_nada('id', dict_bling=conta_bling_pagamento_borderos))
        bordero_db = Bordero.objects.create(conta = valor_correto_ou_nada('conta', dict_bling=conta_bling_pagamento_borderos))
        bordero_db = Bordero.objects.create(data_pagamento = valor_correto_ou_nada('data_pagamento', dict_bling=conta_bling_pagamento_borderos))
        bordero_db = Bordero.objects.create(valor_pago = valor_correto_ou_nada('valor_pago', dict_bling=conta_bling_pagamento_borderos))
        bordero_db = Bordero.objects.create(valor_juro = valor_correto_ou_nada('valor_juro', dict_bling=conta_bling_pagamento_borderos))
        bordero_db = Bordero.objects.create(valor_desconto = valor_correto_ou_nada('valor_desconto', dict_bling=conta_bling_pagamento_borderos))
        bordero_db = Bordero.objects.create(valor_acrescimo = valor_correto_ou_nada('valor_acrescimo', dict_bling=conta_bling_pagamento_borderos))
        bordero_db = Bordero.objects.create(valor_tarifa = valor_correto_ou_nada('valor_tarifa', dict_bling=conta_bling_pagamento_borderos))
        bordero_db.save()
        print(f"- Borderos da conta a pagar {n} cadastrados")

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