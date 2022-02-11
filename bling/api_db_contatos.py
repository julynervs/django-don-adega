"""
Este script é responsável por transferir os dados dos contatos cadastrados no Bling
para o banco de dados sqlite do Django.

"""
import requests
import os
import sys

from time import sleep

sys.path.insert(1, os.path.abspath("."))

import donadega.settings
import donadega.wsgi

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
    sleep(0.5)
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
    for n in range(len(lista_contatos)):
        contato_bling = lista_contatos[n]['contato']
        # infos do contato
        chaves = list(lista_contatos[n]['contato'].keys())

        if not 'dataNacimento' in chaves:
            contato_bling['dataNascimento'] = ""

        print(f"- Contato {n} {contato_bling['nome']} cadastrado")

        # cria um objeto (linha) da tabela Contato no Django
        # insere os dados do bling no modelo e salva
        contato_db = Contato.objects.create(
            id_bling = contato_bling['id'],
            codigo = contato_bling['codigo'],
            nome = contato_bling['nome'],
            fantasia = contato_bling['fantasia'],
            tipo_pessoa = contato_bling['tipo'],
            cpf_cnpj = contato_bling['cnpj'],
            ie_rg = contato_bling['ie_rg'],
            endereco = contato_bling['endereco'],
            numero = contato_bling['numero'],
            bairro = contato_bling['bairro'],
            cep = contato_bling['cep'],
            cidade = contato_bling['cidade'],
            complemento = contato_bling['complemento'],
            uf = contato_bling['uf'],
            fone = contato_bling['fone'],
            email = contato_bling['email'],
            situacao = contato_bling['situacao'],
            contribuinte = contato_bling['contribuinte'],
            site = contato_bling['site'],
            celular = contato_bling['celular'],
            data_alteracao = contato_bling['dataAlteracao'],
            data_inclusao = contato_bling['dataInclusao'],
            sexo = contato_bling['sexo'],
            cliente_desde = contato_bling['clienteDesde'],
            limite_credito = contato_bling['limiteCredito']
        )
        contato_db.save()
        sleep(0.2)

        # cria tabela para os tipos de contato
        # define qual contato é cliente e/ou fornecedor e/ou transportador etc
        if 'tiposContato' in chaves:
            tipo_contato_bling = lista_contatos[n]['contato']['tiposContato'][0]['tipoContato']['descricao']
            
            tipo_contato_db = TipoContato.objects.create(
                descricao=tipo_contato_bling, 
                contato=contato_db
            )
            tipo_contato_db.save()
            sleep(0.2)

def main():
    paginas = 250
    for pagina in range(paginas):
        try:
            coloca_contatos_no_banco(pagina)
        except KeyError:
            print("Não tem mais contatos para cadastrar.")
            break
        else:
            print(f"{pagina} páginas foram cadastradas.")
main()