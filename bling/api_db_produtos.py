"""
Este script é responsável por transferir os dados dos produtos cadastrados no Bling
para o banco de dados sqlite do Django.

"""
import requests
import os
import sys
from time import sleep

sys.path.insert(1, os.path.abspath("."))
import donadega.settings
import donadega.wsgi
import logging

logging.basicConfig(
            filename='api_db_produtos.log', encoding='utf-8', level=logging.INFO,
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


def get_produtos(pagina):
    url = f"https://bling.com.br/Api/v2/produtos/page={pagina}/json/?apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19"
    payload='apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    sleep(0.5)
    return response.text

def coloca_produtos_no_banco(pagina):
    """
    Função que recebe o retorno de get_produtos(),
    faz o tratamento dos dados do JSON
    e salva essas informações no banco de dados do Django
    """
    import json
    from bling.models import Produto
    from bling.models import ProdutoKit
    from bling.models import CategoriaProduto
    from bling.models import CategoriaProdutoKit

    # get_mais_produtos(pagina)
    # formata json recebido
    json = json.loads(get_produtos(pagina))
    lista_produtos = json['retorno']['produtos']

    print("\n")
    print("#"*10)
    print(f"Página {pagina}")
    print("#"*10)

    # percorre a lista de todos os produtos
    for n in range(len(lista_produtos)):
        produto_bling = lista_produtos[n]['produto']
        chaves = list(lista_produtos[n]['produto'].keys())

        for chave, valor in produto_bling.items():
            if valor == '':
                produto_bling[chave] = None
            
        if 'estrutura' in chaves:
            kit_db = ProdutoKit.objects.create(
                id_bling = produto_bling['id'],
                codigo = produto_bling['codigo'],
                descricao = produto_bling['descricao'],
                tipo = produto_bling['tipo'],
                situacao = produto_bling['situacao'],
                unidade = produto_bling['unidade'],
                preco = produto_bling['preco'],
                preco_custo = produto_bling['precoCusto'],
                data_alteracao = produto_bling['dataAlteracao'],
                data_inclusao = produto_bling['dataInclusao'],
                nome_fornecedor = produto_bling['nomeFornecedor'],
                codigo_fabricante  = produto_bling['codigoFabricante'],
                marca = produto_bling['marca'],
                class_fiscal = produto_bling['class_fiscal'],
                cest = produto_bling['cest'],
                origem = produto_bling['origem'],
                descricao_fornecedor = produto_bling['descricaoFornecedor'],
                id_fabricante = produto_bling['idFabricante'],
                largura_produto = produto_bling['larguraProduto'],
                altura_produto = produto_bling['alturaProduto'],
                profundidade_produto = produto_bling['profundidadeProduto'],
                unidade_medida = produto_bling['unidadeMedida'],
                condicao = produto_bling['condicao'],
                frete_gratis = produto_bling['freteGratis'],
                producao = produto_bling['producao'],
                sped_tipo_item = produto_bling['spedTipoItem']
            )
            kit_db.save()
            sleep(0.1)
            
            # # cria tabela de categoria dos kits
            categoria_bling = lista_produtos[n]['produto']['categoria']
            categoria_db = CategoriaProdutoKit.objects.create(
                id_bling = categoria_bling['id'], 
                descricao = categoria_bling['descricao'],
                produto_kit = kit_db
            )
            categoria_db.save()
            sleep(0.1)
            logging.info(f"Página {pagina}: Produto {n} {produto_bling['codigo']} cadastrado")
            print(f"- Produto {n} {produto_bling['codigo']}, Categoria {categoria_bling['descricao']} cadastrado")
        else:
            # cria um objeto (linha) da tabela produto no Django
            # insere os dados do bling no modelo e salva
            produto_db = Produto.objects.create(
                id_bling = produto_bling['id'],
                codigo = produto_bling['codigo'],
                descricao = produto_bling['descricao'],
                tipo = produto_bling['tipo'],
                situacao = produto_bling['situacao'],
                unidade = produto_bling['unidade'],
                preco = produto_bling['preco'],
                preco_custo = produto_bling['precoCusto'],
                data_alteracao = produto_bling['dataAlteracao'],
                data_inclusao = produto_bling['dataInclusao'],
                nome_fornecedor = produto_bling['nomeFornecedor'],
                codigo_fabricante  = produto_bling['codigoFabricante'],
                marca = produto_bling['marca'],
                class_fiscal = produto_bling['class_fiscal'],
                cest = produto_bling['cest'],
                origem = produto_bling['origem'],
                descricao_fornecedor = produto_bling['descricaoFornecedor'],
                id_fabricante = produto_bling['idFabricante'],
                largura_produto = produto_bling['larguraProduto'],
                altura_produto = produto_bling['alturaProduto'],
                profundidade_produto = produto_bling['profundidadeProduto'],
                unidade_medida = produto_bling['unidadeMedida'],
                condicao = produto_bling['condicao'],
                frete_gratis = produto_bling['freteGratis'],
                producao = produto_bling['producao'],
                sped_tipo_item = produto_bling['spedTipoItem']
            )
            produto_db.save()
            sleep(0.1)
            
            # # cria tabela de categoria dos produtos
            categoria_bling = lista_produtos[n]['produto']['categoria']
            categoria_db = CategoriaProduto.objects.create(
                id_bling = categoria_bling['id'], 
                descricao = categoria_bling['descricao'],
                produto = produto_db
            )
            categoria_db.save()
            sleep(0.1)
            logging.info(f"Página {pagina}: Produto {n} {produto_bling['codigo']} cadastrado")
            print(f"- Produto {n} {produto_bling['codigo']}, Categoria {categoria_bling['descricao']} cadastrado")
            
def main():
    paginas = 250
    for pagina in range(1, paginas):
        try:
            coloca_produtos_no_banco(pagina)
        except KeyError:
            print("Não tem mais produtos para cadastrar.")
            logging.error("Chave não encontrada no json. Sem produtos para cadastrar.")
        else:
            logging.info(f"{pagina} páginas foram cadastradas.")
main()
