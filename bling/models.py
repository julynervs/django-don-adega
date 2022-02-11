from django.db import models

class Contato(models.Model):
    id_bling = models.IntegerField(null=True)
    codigo = models.CharField(max_length=15, default="")
    nome = models.CharField(max_length=120, default="", null=True)
    fantasia = models.CharField(max_length=30, default="", null=True)
    tipo_pessoa = models.CharField(max_length=1, default="", null=True)
    contribuinte = models.IntegerField(null=True)
    cpf_cnpj = models.CharField(max_length=18, default="", null=True)
    ie_rg = models.CharField(max_length=18, default="", null=True)
    endereco = models.CharField(max_length=100, default="", null=True)
    numero = models.CharField(max_length=10, default="", null=True)
    complemento = models.CharField(max_length=100, default="", null=True)
    bairro = models.CharField(max_length=30, default="", null=True)
    cep = models.CharField(max_length=10, default="", null=True)
    cidade = models.CharField(max_length=30, default="", null=True)
    uf = models.CharField(max_length=2, default="", null=True)
    fone = models.CharField(max_length=40, default="", null=True)
    celular = models.CharField(max_length=40, default="", null=True)
    data_alteracao = models.CharField(max_length=30, null=True)
    data_inclusao = models.CharField(max_length=30, null=True)
    cliente_desde = models.CharField(max_length=30, null=True)
    data_nascimento = models.CharField(max_length=15, null=True)
    sexo = models.CharField(max_length=30, default="", null=True)
    site = models.CharField(max_length=80, default="", null=True)
    email = models.EmailField(max_length=100, default="", null=True)
    email_nfe = models.EmailField(max_length=100, default="", null=True)
    situacao = models.CharField(max_length=40, default="", null=True)
    informacao_contato = models.CharField(max_length=100, default="", null=True)
    limite_credito = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    def __str__(self):
        return self.nome

class TipoContato(models.Model):
    descricao = models.CharField(max_length=255)
    contato = models.ForeignKey(Contato, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.descricao

class Produto(models.Model):
    id_bling = models.IntegerField(null=True)
    codigo = models.CharField(max_length=60, default="")
    descricao = models.CharField(max_length=120, default="", null=True)
    tipo = models.CharField(max_length=1, default="", null=True)
    situacao = models.CharField(max_length=18, default="", null=True)
    descricao_curta = models.CharField(max_length=255, default="", null=True)
    unidade = models.CharField(max_length=6, default="", null=True)
    preco = models.DecimalField(max_digits=17, decimal_places=10, null=True)
    preco_custo = models.DecimalField(max_digits=17, decimal_places=10, default=0, null=True)
    peso_bruto = models.DecimalField(max_digits=11, decimal_places=3, default=0.000, null=True)
    peso_liq = models.DecimalField(max_digits=11, decimal_places=3, default=0.000, null=True)
    class_fiscal = models.CharField(max_length=10, default="", null=True)
    cest = models.CharField(max_length=7, default="", null=True)
    marca = models.CharField(max_length=40, default="", null=True)
    condicao = models.CharField(max_length=40, default="", null=True)
    frete_gratis = models.CharField(max_length=1, default="", null=True)
    linkExterno = models.CharField(max_length=100, default="", null=True)
    nome_fornecedor = models.CharField(max_length=100, default="", null=True)
    codigo_fabricante = models.CharField(max_length=255, default="", null=True)
    data_validade = models.CharField(max_length=10, default="", null=True)
    origem = models.CharField(max_length=1, default="", null=True)
    descricao_fornecedor = models.CharField(max_length=255, default="", null=True)
    id_fabricante = models.CharField(max_length=20, default="", null=True)
    largura_produto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    altura_produto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    profundidade_produto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    unidade_medida = models.CharField(max_length=20, default="", null=True)
    producao = models.CharField(max_length=1, default="", null=True)
    sped_tipo_item = models.CharField(max_length=2, default="", null=True)
    data_alteracao = models.CharField(max_length=30, null=True)
    data_inclusao = models.CharField(max_length=30, null=True)
    def __str__(self):
        return self.descricao

class ProdutoKit(models.Model):
    id_bling = models.IntegerField(null=True)
    codigo = models.CharField(max_length=60, default="")
    descricao = models.CharField(max_length=120, default="", null=True)
    tipo = models.CharField(max_length=1, default="", null=True)
    situacao = models.CharField(max_length=18, default="", null=True)
    descricao_curta = models.CharField(max_length=255, default="", null=True)
    unidade = models.CharField(max_length=6, default="", null=True)
    preco = models.DecimalField(max_digits=17, decimal_places=10, null=True)
    preco_custo = models.DecimalField(max_digits=17, decimal_places=10, default=0, null=True)
    peso_bruto = models.DecimalField(max_digits=11, decimal_places=3, default=0.000, null=True)
    peso_liq = models.DecimalField(max_digits=11, decimal_places=3, default=0.000, null=True)
    class_fiscal = models.CharField(max_length=10, default="", null=True)
    cest = models.CharField(max_length=7, default="", null=True)
    marca = models.CharField(max_length=40, default="", null=True)
    condicao = models.CharField(max_length=40, default="", null=True)
    frete_gratis = models.CharField(max_length=1, default="", null=True)
    linkExterno = models.CharField(max_length=100, default="", null=True)
    nome_fornecedor = models.CharField(max_length=100, default="", null=True)
    codigo_fabricante = models.CharField(max_length=255, default="", null=True)
    data_validade = models.CharField(max_length=10, default="", null=True)
    origem = models.CharField(max_length=1, default="", null=True)
    descricao_fornecedor = models.CharField(max_length=255, default="", null=True)
    id_fabricante = models.CharField(max_length=20, default="", null=True)
    largura_produto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    altura_produto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    profundidade_produto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    unidade_medida = models.CharField(max_length=20, default="", null=True)
    producao = models.CharField(max_length=1, default="", null=True)
    data_alteracao = models.CharField(max_length=30, null=True)
    data_inclusao = models.CharField(max_length=30, null=True)
    sped_tipo_item = models.CharField(max_length=2, default="", null=True)

class CategoriaProduto(models.Model):
    id_bling = models.PositiveIntegerField(null=True, blank=True)
    descricao = models.CharField(max_length=40, null=True, blank=True)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING, default="")

class CategoriaProdutoKit(models.Model):
    id_bling = models.PositiveIntegerField(null=True, blank=True)
    descricao = models.CharField(max_length=40, null=True, blank=True)
    produto_kit = models.ForeignKey(ProdutoKit, on_delete=models.DO_NOTHING, default="")

class Pedido(models.Model):
    data = models.DateField(null=True)
    data_saida = models.DateField(null=True)
    numero = models.CharField(max_length=10, default="", null=True)
    numero_loja = models.CharField(max_length=50, default="", null=True)
    vlr_frete = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, null=True)
    vlr_desconto = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, null=True)
    obs = models.CharField(max_length=255, default="", null=True)
    loja = models.IntegerField(default=0, null=True)
    nat_operacao = models.CharField(max_length=60, default="Venda de mercadorias", null=True)
    # cliente = models.ForeignKey(Contato, default="", on_delete=models.DO_NOTHING, null=True)
    # transporte = models.ForeignKey(Contato, default="", on_delete=models.DO_NOTHING, null=True)
    # item = models.ForeignKey(Item, default="", on_delete=models.DO_NOTHING, null=True)
    def __str__(self):
        return self.cliente

class Item(models.Model):
    codigo = models.CharField(max_length=60, default="")
    descricao = models.CharField(max_length=120, default="", null=True)
    quantidade = models.PositiveIntegerField(null=True)
    valor_unidade = models.DecimalField(max_digits=17, decimal_places=10, null=True)
    preco_custo = models.DecimalField(max_digits=17, decimal_places=10, default=0, null=True)
    desconto_item = models.DecimalField(max_digits=11, decimal_places=3, default=0.000, null=True)
    peso_bruto = models.DecimalField(max_digits=11, decimal_places=3, default=0.000, null=True)
    largura = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    altura = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    profundidade = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    unidade_medida = models.CharField(max_length=20, default="", null=True)
    gtin = models.PositiveIntegerField(null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING)