"""
Este script é responsável por transferir os dados dos contatos cadastrados no Bling
para o banco de dados sqlite do Django.

"""
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
            filename='api_db_contatos.log', encoding='utf-8', level=logging.INFO,
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

def get_contatos(pagina):
    """
    Função que faz requisição GET contatos pela API do bling 
    """
    url = f"https://bling.com.br/Api/v2/contatos/page={pagina}/json/?apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19"

    payload='apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    sleep(0.4)
    return response.text

def coloca_contatos_no_banco(pagina):
    """
    Função que recebe o retorno de get_contatos(),
    faz o tratamento dos dados do JSON
    e salva essas informações no banco de dados do Django
    """
    import json
    from bling.models import Contato
    from bling.models import TipoContato

    # formata json recebido
    json = json.loads(get_contatos(pagina))
    # lista de até 100 contatos, pois é o limite de contatos por requisição do bling
    lista_contatos = json['retorno']['contatos']
   
    print("\n")
    print("#"*10)
    print(f"Página {pagina}")
    print("#"*10)

    # percorre a lista de todos os contatos da requisição (página)
    contato_db = None
    for n in range(len(lista_contatos)):
        contato_bling = lista_contatos[n]['contato']
        # infos do contato
        chaves = list(lista_contatos[n]['contato'].keys())

        print(f"- Contato {n} {contato_bling['nome']} cadastrado")
        logging.info(f"_Pag. {pagina}: Contato {n} {contato_bling['nome']} cadastrado")

        # filtro
        def valor_correto_ou_nada(chave):
            if contato_bling[chave] == '':
                logging.warning(f"____{chave} do contato {contato_bling['nome']} incorreta ou não existente, None definido no campo")
                return None
            else:
                logging.info(f"____{chave} do contato {contato_bling['nome']} cadastrada")
                return contato_bling[chave]

        # filtro para existencia de um dado no JSON do Bling
        def chave_existe(chave_bling):
            if chave_bling in contato_bling.keys():
                return True
            else:
                return False

        # cadastro campos de string
        contato_db = Contato.objects.create(codigo = valor_correto_ou_nada('codigo'))

        contato_db = Contato.objects.create(
                    nome = valor_correto_ou_nada('nome'),
                    fantasia = valor_correto_ou_nada('fantasia'),
                    tipo_pessoa = valor_correto_ou_nada('tipo'),
                    cpf_cnpj = valor_correto_ou_nada('cnpj'),
                    ie_rg = valor_correto_ou_nada('ie_rg'),
                    endereco = valor_correto_ou_nada('endereco'),
                    numero = valor_correto_ou_nada('numero'),
                    bairro = valor_correto_ou_nada('bairro'),
                    cep = valor_correto_ou_nada('cep'),
                    cidade = valor_correto_ou_nada('cidade'),
                    complemento = valor_correto_ou_nada('complemento'),
                    uf = valor_correto_ou_nada('uf'),
                    fone = valor_correto_ou_nada('fone'),
                    situacao = valor_correto_ou_nada('situacao'),
                    site = valor_correto_ou_nada('site'),
                    celular = valor_correto_ou_nada('celular'),            
                    sexo = valor_correto_ou_nada('sexo'),
        )

        # cadastro campos numéricos
        ## int
        contato_db = Contato.objects.create(id_bling = contato_bling['id'])
        logging.info(f"____id_bling do contato {n} cadastrado")
        contato_db = Contato.objects.create(contribuinte = contato_bling['contribuinte'])
        logging.info(f"____contribuinte do contato {n} cadastrado")
        ## float
        contato_db = Contato.objects.create(limite_credito = contato_bling['limiteCredito'])
        logging.info(f"____limite_credito do contato {n} cadastrado")
        # email
        contato_db = Contato.objects.create(email = contato_bling['email'])
        logging.info(f"____email do contato {n} cadastrado")

        # filtro para datas corretas, caso no Bling tenho um cadastro com uma data que não existe
        def data_correta_ou_nada(chave_data):
            if contato_bling[chave_data] == '0000-00-00' or contato_bling[chave_data] == '':
                logging.warning(f"____{chave_data} do contato {n} {contato_bling['nome']} incorreta ou não existente, None definido no campo")
                return None
            else:
                logging.info(f"____{chave_data} do contato {n} cadastrada")
                return contato_bling[chave_data]

        # cadastro campos de data
        # for chave_lista in ['dataInclusao', 'dataAlteracao', 'clienteDesde', 'dataNascimento']:
        # verifica existencia do campo
        # se o campo não existe no JSON, o dado não é cadastrado no banco de dados
        if chave_existe('dataInclusao'):
            contato_db = Contato.objects.create(data_inclusao = data_correta_ou_nada('dataInclusao'))
        else:
            logging.info(f"____O campo 'dataInclusao' não foi cadastrado por não existir no json")

        if chave_existe('dataAlteracao'):
            contato_db = Contato.objects.create(data_alteracao = data_correta_ou_nada('dataAlteracao'))
        else:
            logging.info(f"____O campo 'dataAlteracao' não foi cadastrado por não existir no json")

        if chave_existe('clienteDesde'):
            contato_db = Contato.objects.create(cliente_desde = data_correta_ou_nada('clienteDesde'))
        else:
            logging.info(f"____O campo 'clienteDesde' não foi cadastrado por não existir no json")

        if chave_existe('dataNascimento'):
            contato_db = Contato.objects.create(data_nascimento = data_correta_ou_nada('dataNascimento'))
        else:
            logging.info(f"____O campo 'dataNascimento' não foi cadastrado por não existir no json")
    
        contato_db.save()
        # sleep(0.1)

        # cria tabela para os tipos de contato
        # define qual contato é cliente e/ou fornecedor e/ou transportador etc
        if 'tiposContato' in chaves:
            tipo_contato_bling = lista_contatos[n]['contato']['tiposContato'][0]['tipoContato']['descricao']
            
            tipo_contato_db = TipoContato.objects.create(
                descricao=tipo_contato_bling, 
                contato=contato_db
            )
            tipo_contato_db.save()
            # sleep(0.1)

def main():
    paginas = 250
    for pagina in range(1, paginas):
        try:
            coloca_contatos_no_banco(pagina)
        except KeyError:
            print("Algo aconteceu ou não tem mais contatos para cadastrar.")
            logging.warning(KeyError)
            break
        except Exception as e:
            print(e)
            logging.warning(e)
            break
        else:
            print(f"{pagina} páginas foram cadastradas.")
main()