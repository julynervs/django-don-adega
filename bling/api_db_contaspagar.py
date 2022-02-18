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

    lista_contas = retorno_get['contaspagar']

    # percorre a lista de todos os contas
    for n in range(len(lista_contas)):
        conta_bling = lista_contas[n]['contapagar']
        chaves = list(lista_contas[n]['contapagar'].keys())

        # filtro
        def valor_correto_ou_nada(chave):
            # filtro para existencia de um dado no JSON do Bling
            def chave_existe(chave_bling):
                if chave_bling in conta_bling.keys():
                    return True
                else:
                    return False   
            if conta_bling[chave] == '' or not chave_existe:
                logging.warning(f"____{chave} da conta {n} incorreta ou não existente, None definido no campo")
                return None
            else:
                logging.info(f"____{chave} da conta {n} cadastrada")
                return conta_bling[chave]
    
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

        conta_db.save()

        ## cadastro da tabela Pagamento
        conta_bling = conta_bling['pagamento']
        pagamento_db = Pagamento.objects.create(conta_pagar = conta_db)
        pagamento_db = Pagamento.objects.create(total_pago = valor_correto_ou_nada('totalPago')) 
        pagamento_db = Pagamento.objects.create(total_pago = valor_correto_ou_nada('totalPago'))
        pagamento_db = Pagamento.objects.create(total_pago = valor_correto_ou_nada('totalPago'))

        print(f"- Conta a pagar {n} {conta_bling['historico']} cadastrada")
        break

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
        break

if __name__ == "__main__":
    main()