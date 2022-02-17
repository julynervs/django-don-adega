"""
Este script é responsável por transferir os dados dos produtos cadastrados no Bling
para o banco de dados sqlite do Django.

"""
import requests
import os
import sys
from time import sleep
import json

sys.path.insert(1, os.path.abspath("."))
import donadega.settings
import donadega.wsgi
import logging

logging.basicConfig(
            filename='api_db_produtos.log', encoding='utf-8', level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

"""
## LOGGING ###
Nível  |  Quando é usando
DEBUG -> Informação detalhada, tipicamente de interesse apenas quando diagnosticando problemas.
INFO -> Confirmação de que as coisas estão funcionando como esperado.
WARNING -> Uma indicação que algo inesperado aconteceu, ou um indicativo que algum problema 
           em um futuro próximo (ex.: ‘pouco espaço em disco’). 
           O software está ainda funcionando como esperado.
ERROR -> Por conta de um problema mais grave, o software não conseguiu executar alguma função.
CRITICAL -> Um erro grave, indicando que o programa pode não conseguir continuar rodando.
"""
import get_bling

def coloca_produtos_no_banco(retorno_get):
    """
    Função que recebe o retorno de um JSON
    e salva essas informações no banco de dados do Django
    """
    from bling.models import Produto
    from bling.models import ProdutoKit
    from bling.models import CategoriaProduto
    from bling.models import CategoriaProdutoKit

    lista_produtos = retorno_get['produtos']
    # percorre a lista de todos os produtos
    for n in range(len(lista_produtos)):
        produto_bling = lista_produtos[n]['produto']
        chaves = list(lista_produtos[n]['produto'].keys())

        # filtro
        def valor_correto_ou_nada(chave):
            if produto_bling[chave] == '':
                logging.warning(f"____{chave} do produto {n} {produto_bling['descricao']} incorreta ou não existente, None definido no campo")
                return None
            else:
                logging.info(f"____{chave} do produto {n} cadastrada")
                return produto_bling[chave]
        # filtro para existencia de um dado no JSON do Bling
        def chave_existe(chave_bling):
            if chave_bling in produto_bling.keys():
                return True
            else:
                return False    

        if 'estrutura' in chaves:
            # cadastro de campos datas
            if chave_existe('dataAlteracao'):
                kit_db = ProdutoKit.objects.create(data_alteracao = valor_correto_ou_nada('dataAlteracao'))
                logging.info(f"____data_alteracao do produto Kit {n} cadastrado")
            else:
                logging.info(f"____O campo 'data_alteracao' NÃO foi cadastrado por não existir no json")
            
            if chave_existe('dataInclusao'):
                kit_db = ProdutoKit.objects.create(data_inclusao = valor_correto_ou_nada('dataInclusao'))
                logging.info(f"____data_inclusao do produto Kit {n} cadastrado")
            else:
                logging.info(f"____O campo 'data_inclusao' NÃO foi cadastrado por não existir no json")

            # cadastro de campos numéricos
            ## int
            if chave_existe('id'):
                kit_db = ProdutoKit.objects.create(id_bling = valor_correto_ou_nada('id'))
                logging.info(f"____id_bling do produto Kit {n} cadastrado")
            else:
                logging.info(f"____O campo 'id_bling' NÃO foi cadastrado por não existir no json")
            ## float
            if chave_existe('preco'):
                kit_db = ProdutoKit.objects.create(preco = valor_correto_ou_nada('preco'))
                logging.info(f"____preco do produto Kit {n} cadastrado")
            else:
                logging.info(f"____O campo 'preco' NÃO foi cadastrado por não existir no json")
            
            if chave_existe('precoCusto'):
                kit_db = ProdutoKit.objects.create(preco_custo = valor_correto_ou_nada('precoCusto'))
                logging.info(f"____preco_custo do produto Kit {n} cadastrado")
            else:
                logging.info(f"____O campo 'preco_custo' NÃO foi cadastrado por não existir no json")
            
            if chave_existe('larguraProduto'):
                kit_db = ProdutoKit.objects.create(largura_produto = valor_correto_ou_nada('larguraProduto'))
                logging.info(f"____largura_produto do produto Kit {n} cadastrado")
            else:
                logging.info(f"____O campo 'largura_produto' NÃO foi cadastrado por não existir no json")
            
            if chave_existe('alturaProduto'):
                kit_db = ProdutoKit.objects.create(altura_produto = valor_correto_ou_nada('alturaProduto'))
                logging.info(f"____altura_produto do produto Kit {n} cadastrado")
            else:
                logging.info(f"____O campo 'altura_produto' NÃO foi cadastrado por não existir no json")
            
            if chave_existe('profundidadeProduto'):
                kit_db = ProdutoKit.objects.create(profundidade_produto = valor_correto_ou_nada('profundidadeProduto'))
                logging.info(f"____profundidade_produto do produto Kit {n} cadastrado")
            else:
                logging.info(f"____O campo 'profundidade_produto' NÃO foi cadastrado por não existir no json")

            # cadastro campos texto
            kit_db = ProdutoKit.objects.create(
                descricao = valor_correto_ou_nada('descricao'))
            kit_db = ProdutoKit.objects.create(
                codigo = valor_correto_ou_nada('codigo'),
                tipo = valor_correto_ou_nada('tipo'),
                situacao = valor_correto_ou_nada('situacao'),
                unidade = valor_correto_ou_nada('unidade'),
                nome_fornecedor = valor_correto_ou_nada('nomeFornecedor'),
                codigo_fabricante  = valor_correto_ou_nada('codigoFabricante'),
                marca = valor_correto_ou_nada('marca'),
                class_fiscal = valor_correto_ou_nada('class_fiscal'),
                cest = valor_correto_ou_nada('cest'),
                origem = valor_correto_ou_nada('origem'),
                descricao_fornecedor = valor_correto_ou_nada('descricaoFornecedor'),
                id_fabricante = valor_correto_ou_nada('idFabricante'),
                unidade_medida = valor_correto_ou_nada('unidadeMedida'),
                condicao = valor_correto_ou_nada('condicao'),
                frete_gratis = valor_correto_ou_nada('freteGratis'),
                producao = valor_correto_ou_nada('producao'),
                sped_tipo_item = valor_correto_ou_nada('spedTipoItem')
            )
            kit_db.save()
            
            # # cria tabela de categoria dos kits
            categoria_bling = lista_produtos[n]['produto']['categoria']
            categoria_db = CategoriaProdutoKit.objects.create(
                id_bling = categoria_bling['id'], 
                descricao = categoria_bling['descricao'],
                produto_kit = kit_db
            )
            categoria_db.save()

            print(f"- ProdutoKit {n} {produto_bling['codigo']}, Categoria {categoria_bling['descricao']} cadastrado")
        else:
            # cria um objeto (linha) da tabela produto no Django
            # insere os dados do bling no modelo e salva
            
            # cadastro de campos datas
            if chave_existe('dataAlteracao'):
                produto_db = Produto.objects.create(data_alteracao = valor_correto_ou_nada('dataAlteracao'))
                logging.info(f"____data_alteracao do produto {n} cadastrado")
            else:
                logging.info(f"____O campo 'data_alteracao' NÃO foi cadastrado por não existir no json")
            
            if chave_existe('dataInclusao'):
                produto_db = Produto.objects.create(data_inclusao = valor_correto_ou_nada('dataInclusao'))
                logging.info(f"____data_inclusao do produto {n} cadastrado")
            else:
                logging.info(f"____O campo 'data_inclusao' NÃO foi cadastrado por não existir no json")

            # cadastro de campos numéricos
            ## int
            if chave_existe('id'):
                produto_db = Produto.objects.create(id_bling = valor_correto_ou_nada('id'))
                logging.info(f"____id_bling do produto {n} cadastrado")
            else:
                logging.info(f"____O campo 'id_bling' NÃO foi cadastrado por não existir no json")
            ## float
            if chave_existe('preco'):
                produto_db = Produto.objects.create(preco = valor_correto_ou_nada('preco'))
                logging.info(f"____preco do produto {n} cadastrado")
            else:
                logging.info(f"____O campo 'preco' NÃO foi cadastrado por não existir no json")
            
            if chave_existe('precoCusto'):
                produto_db = Produto.objects.create(preco_custo = valor_correto_ou_nada('precoCusto'))
                logging.info(f"____preco_custo do produto {n} cadastrado")
            else:
                logging.info(f"____O campo 'preco_custo' NÃO foi cadastrado por não existir no json")
            
            if chave_existe('larguraProduto'):
                produto_db = Produto.objects.create(largura_produto = valor_correto_ou_nada('larguraProduto'))
                logging.info(f"____largura_produto do produto {n} cadastrado")
            else:
                logging.info(f"____O campo 'largura_produto' NÃO foi cadastrado por não existir no json")
            
            if chave_existe('alturaProduto'):
                produto_db = Produto.objects.create(altura_produto = valor_correto_ou_nada('alturaProduto'))
                logging.info(f"____altura_produto do produto {n} cadastrado")
            else:
                logging.info(f"____O campo 'altura_produto' NÃO foi cadastrado por não existir no json")
            
            if chave_existe('profundidadeProduto'):
                produto_db = Produto.objects.create(profundidade_produto = valor_correto_ou_nada('profundidadeProduto'))
                logging.info(f"____profundidade_produto do produto {n} cadastrado")
            else:
                logging.info(f"____O campo 'profundidade_produto' NÃO foi cadastrado por não existir no json")

            produto_db.save()
            
            # # cria tabela de categoria dos produtos
            categoria_bling = lista_produtos[n]['produto']['categoria']
            categoria_db = CategoriaProduto.objects.create(
                id_bling = categoria_bling['id'], 
                descricao = categoria_bling['descricao'],
                produto = produto_db
            )
            categoria_db.save()

            print(f"- Produto {n} {produto_bling['codigo']}, Categoria {categoria_bling['descricao']} cadastrado")
            
def main():
    paginas = 250
    for pagina in range(1, paginas):
        print("\n")
        print("#"*10)
        print(f"Página {pagina}")
        logging.info(f"Cadastrando produtos da Página {pagina}")
        print("#"*10)
        if get_bling(modulo='produtos', pagina=pagina):
            coloca_produtos_no_banco(get_bling(modulo='produtos', pagina=pagina)) 
        else:
            print(f"Página {pagina} não cadastrada")
            break
        sleep(0.4)
main()


#%%%%
