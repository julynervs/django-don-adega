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

        # filtro para existencia de um dado no JSON do Bling
        def valor_correto_ou_nada(chave, dict_bling=produto_bling):
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

        if 'estrutura' in chaves:
            pass
            # cadastro de campos datas
            kit_db = ProdutoKit.objects.create(data_alteracao = valor_correto_ou_nada('dataAlteracao'))
            kit_db = ProdutoKit.objects.create(data_inclusao = valor_correto_ou_nada('dataInclusao'))
            # cadastro de campos numéricos
            ## int
            kit_db = ProdutoKit.objects.create(id_bling = valor_correto_ou_nada('id'))
            ## float
            kit_db = ProdutoKit.objects.create(preco = valor_correto_ou_nada('preco'))
            kit_db = ProdutoKit.objects.create(preco_custo = valor_correto_ou_nada('precoCusto'))
            kit_db = ProdutoKit.objects.create(largura_produto = valor_correto_ou_nada('larguraProduto'))
            kit_db = ProdutoKit.objects.create(altura_produto = valor_correto_ou_nada('alturaProduto'))
            kit_db = ProdutoKit.objects.create(profundidade_produto = valor_correto_ou_nada('profundidadeProduto'))
              
            # cadastro campos texto
            kit_db = ProdutoKit.objects.create(descricao = valor_correto_ou_nada('descricao'))
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
            
            

            print(f"- ProdutoKit {n} {produto_bling['codigo']}, Categoria {categoria_bling['descricao']} cadastrado")
        else:
            ## cria um objeto (linha) da tabela produto no Django
            ## insere os dados do bling no modelo e salva
            # cadastro de campos datas
            produto_db = Produto.objects.create(data_alteracao = valor_correto_ou_nada('dataAlteracao'))
            produto_db = Produto.objects.create(data_inclusao = valor_correto_ou_nada('dataInclusao'))
            # cadastro de campos numéricos
            ## int
            produto_db = Produto.objects.create(id_bling = valor_correto_ou_nada('id'))
            ## float
            produto_db = Produto.objects.create(preco = valor_correto_ou_nada('preco'))
            produto_db = Produto.objects.create(preco_custo = valor_correto_ou_nada('precoCusto'))
            produto_db = Produto.objects.create(largura_produto = valor_correto_ou_nada('larguraProduto'))
            produto_db = Produto.objects.create(altura_produto = valor_correto_ou_nada('alturaProduto'))
            produto_db = Produto.objects.create(profundidade_produto = valor_correto_ou_nada('profundidadeProduto'))
            produto_db.save()
            
            def encontrar_ou_criar():
                # cadastros foreign key
                # # identifica o cliente que fez a conta
                # # e obtém o mesmo do banco de dados
                codigo_produto_bling = produto_bling['codigo']
                if CategoriaProduto.objects.filter(codigo=codigo_produto_bling).order_by('id').first():
                    categoria_db = CategoriaProduto.objects.filter(nome=codigo_produto_bling).order_by('id').first()            
                else:
                    categoria_db = CategoriaProduto.objects.create(id_bling = valor_correto_ou_nada('id'))
                    categoria_db = CategoriaProduto.objects.create(descricao = valor_correto_ou_nada('descricao'))
                    categoria_db = CategoriaProduto.objects.create(id_categoria_pai = valor_correto_ou_nada('id_categoria_pai'))
                    categoria_db.save()
                produto_db = Produto.objects.create(categoria = categoria_db)
                produto_db.save()
            encontrar_ou_criar()
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
            print(f"Página {pagina} não encontrada")
            break
        sleep(0.4)

if __name__ == "__main__":
    main()