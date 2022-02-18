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

from get_bling import get_bling

def coloca_contatos_no_banco(retorno_get):
    """
    Função que recebe o retorno de get_contatos(),
    faz o tratamento dos dados do JSON
    e salva essas informações no banco de dados do Django
    """
    from bling.models import Contato
    from bling.models import TipoContato

    # lista de até 100 contatos, pois é o limite de contatos por requisição do bling
    lista_contatos = retorno_get['contatos']
   
    # percorre a lista de todos os contatos da requisição (página)
    contato_db = None
    for n in range(len(lista_contatos)):
        contato_bling = lista_contatos[n]['contato']
        # infos do contato
        chaves = list(lista_contatos[n]['contato'].keys())

        print(f"- Contato {n} {contato_bling['nome']} cadastrado")

        # filtro para existencia de um dado no JSON do Bling
        def chave_existe(chave_bling):
            if chave_bling in contato_bling.keys():
                return True
            else:
                return False

        # filtro
        def valor_correto_ou_nada(chave):
            if contato_bling[chave] == '' or not chave_existe(chave):
                logging.warning(f"____{chave} do contato {contato_bling['nome']} incorreta ou não existente, None definido no campo")
                return None
            else:
                logging.info(f"____{chave} do contato {contato_bling['nome']} cadastrada")
                return contato_bling[chave]


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
        contato_db =Contato.objects.create(id_bling = valor_correto_ou_nada('id'))
        contato_db = Contato.objects.create(contribuinte = contato_bling['contribuinte'])

        ## float
        contato_db = Contato.objects.create(limite_credito = contato_bling['limiteCredito'])
        # email
        contato_db = Contato.objects.create(email = contato_bling['email'])

        # filtro para datas corretas, caso no Bling tenho um cadastro com uma data que não existe
        def data_correta_ou_nada(chave_data):
            if contato_bling[chave_data] == '0000-00-00' or contato_bling[chave_data] == '':
                logging.warning(f"____{chave_data} do contato {n} {contato_bling['nome']} incorreta ou não existente, None definido no campo")
                return None
            else:
                logging.info(f"____{chave_data} do contato {n} cadastrada")
                return contato_bling[chave_data]

        # cadastro campos de data       
        contato_db = Contato.objects.create(data_inclusao = data_correta_ou_nada('dataInclusao'))
        contato_db = Contato.objects.create(data_alteracao = data_correta_ou_nada('dataAlteracao'))
        contato_db = Contato.objects.create(cliente_desde = data_correta_ou_nada('clienteDesde'))      
        contato_db = Contato.objects.create(data_nascimento = data_correta_ou_nada('dataNascimento'))
            
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

def main():
    paginas = 250
    for pagina in range(1, paginas):
        print("\n")
        print("#"*10)
        print(f"Página {pagina}")
        logging.info(f"Cadastrando produtos da Página {pagina}")
        print("#"*10)
        if get_bling(modulo='contatos', pagina=pagina):
            coloca_contatos_no_banco(get_bling(modulo='contatos', pagina=pagina)) 
        else:
            print(f"Página {pagina} não encontrada")
            break
        sleep(0.4)

if __name__ == "__main__":
    main()