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
    from bling.models import Pagamento
    from bling.models import Bordero

    lista_contas = retorno_get['contasreceber']

    # percorre a lista de todos os contas
    for n in range(len(lista_contas)):
        conta_bling = lista_contas[n]['contaReceber']
        chaves = list(lista_contas[n]['contaReceber'].keys())

        # filtro
        def valor_correto_ou_nada(chave):
            # filtro para existencia de um dado no JSON do Bling
            # se a chave existe, verifica qual o valor relativo à ela
            if chave in conta_bling.keys():
                # se o valor relativo for '', é um valor incorreto, então retorna None
                if conta_bling[chave] == '':
                    logging.warning(f"____{chave} da conta {n} incorreta ou não existente, None definido no campo")
                    return None
                # se o valor estiver correto, retorna o valor
                else:
                    logging.info(f"____{chave} da conta {n} cadastrada")
                    return conta_bling[chave]
            # se a chave não existe, retorna None
            else:
                return None

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
        conta_db = ContaReceber.objects.create(data_emissao = valor_correto_ou_nada('dataEmissao'))   
        conta_db = ContaReceber.objects.create(vencimento = valor_correto_ou_nada('vencimento'))   
        conta_db = ContaReceber.objects.create(competencia = valor_correto_ou_nada('competencia'))   
    
        # cadastros float
        conta_db = ContaReceber.objects.create(valor = valor_correto_ou_nada('valor'))   
        conta_db = ContaReceber.objects.create(saldo = valor_correto_ou_nada('saldo'))   
    
        # cadastros int
        conta_db = ContaReceber.objects.create(id_bling = valor_correto_ou_nada('id'))   
        conta_db = ContaReceber.objects.create(nro_banco = valor_correto_ou_nada('nroNoBanco'))   
     
        # cadastros string  
        conta_db = ContaReceber.objects.create(situacao = valor_correto_ou_nada('situacao'))   
        conta_db = ContaReceber.objects.create(historico = valor_correto_ou_nada('historico'))       
        conta_db = ContaReceber.objects.create(vendedor = valor_correto_ou_nada('vendedor'))   
      
        conta_db.save()
        print(f"- Conta a receber {n} {conta_bling['historico']} cadastrada")

        # ## cadastro da tabela Pagamento
        conta_bling_pagamento = conta_bling['pagamento']

        pagamento_db = Pagamento.objects.create(conta_receber = conta_db)
        pagamento_db = Pagamento.objects.create(total_pago = valor_correto_ou_nada('totalPago', dict_bling=conta_bling_pagamento)) 
        pagamento_db = Pagamento.objects.create(total_juro = valor_correto_ou_nada('totalJuro', dict_bling=conta_bling_pagamento))
        pagamento_db = Pagamento.objects.create(total_desconto = valor_correto_ou_nada('totalDesconto', dict_bling=conta_bling_pagamento))
        pagamento_db = Pagamento.objects.create(total_acrescimo = valor_correto_ou_nada('totalAcrescimo', dict_bling=conta_bling_pagamento))
        pagamento_db = Pagamento.objects.create(total_tarifa = valor_correto_ou_nada('totalTarifa', dict_bling=conta_bling_pagamento))
        pagamento_db = Pagamento.objects.create(data = valor_correto_ou_nada('data', dict_bling=conta_bling_pagamento))
        pagamento_db.save()
        print(f"- Pagamento da conta a receber {n} cadastrado")

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
        print(f"- Borderos da conta a receber {n} cadastrados")

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