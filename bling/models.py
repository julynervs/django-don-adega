from django.db import models

class Contato(models.Model):
    id_bling = models.IntegerField(unique=True)
    codigo = models.CharField(max_length=15, default="", null=True, blank=True) # string
    nome = models.CharField(max_length=120, default="", null=True, blank=False) # string
    fantasia = models.CharField(max_length=30, default="", null=True, blank=True) # string
    tipo_pessoa = models.CharField(max_length=1, default="", null=True, blank=False) # char (ex.: "J")
    contribuinte = models.IntegerField(null=True, blank=False) # inteiro (1 - Contribuinte do ICMS, 2 - Contribuinte isento do ICMS ou 9 - Não contribuinte)
    cpf_cnpj = models.CharField(max_length=18, default="", null=True, blank=True)
    ie_rg = models.CharField(max_length=18, default="", null=True, blank=True) # str
    endereco = models.CharField(max_length=100, default="", null=True, blank=True) # string
    numero = models.CharField(max_length=10, default="", null=True, blank=True)
    complemento = models.CharField(max_length=100, default="", null=True, blank=True)
    bairro = models.CharField(max_length=30, default="", null=True, blank=True)
    cep = models.CharField(max_length=10, default="", null=True, blank=True)
    cidade = models.CharField(max_length=30, default="", null=True, blank=True)
    uf = models.CharField(max_length=2, default="", null=True, blank=True)
    fone = models.CharField(max_length=40, default="", null=True, blank=True)
    celular = models.CharField(max_length=40, default="", null=True, blank=True)
    data_alteracao = models.DateTimeField(null=True, blank=True) # datetime.datetime
    data_inclusao = models.DateTimeField(null=True, blank=True) # datetime.datetime
    cliente_desde = models.DateField(null=True, blank=True) # datetime.date
    data_nascimento = models.DateField(null=True, blank=True) # datetime.date
    sexo = models.CharField(max_length=20, default="", null=True, blank=True) # string
    site = models.CharField(max_length=80, default="", null=True, blank=True) # string
    email = models.EmailField(max_length=100, default="", null=True, blank=True) # string
    email_nfe = models.EmailField(max_length=100, default="", null=True, blank=True) # string
    situacao = models.CharField(max_length=20, default="", null=True, blank=True) # string
    informacao_contato = models.CharField(max_length=100, default="", null=True, blank=True)
    limite_credito = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True) # float
    def __str__(self):
        return self.nome

class TipoContato(models.Model):
    descricao = models.CharField(max_length=255)
    contato = models.ForeignKey(Contato, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.descricao

class CategoriaProduto(models.Model):
    id_bling = models.PositiveIntegerField(unique=True)
    descricao = models.CharField(max_length=40, null=True, blank=True)
    id_categoria_pai = models.PositiveIntegerField(null=True, blank=True)
    # def save(self, *args, **kwargs):
    #     self.id_categoria_pai = 101010
    #     super(CategoriaProduto, self).save(*args, **kwargs)
    def __str__(self):
        return self.descricao

class Produto(models.Model):
    id_bling = models.IntegerField(unique=True)
    codigo = models.CharField(max_length=60, default="", unique=True, null=True, blank=True)
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.DO_NOTHING, default="")
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
    frete_gratis = models.CharField(max_length=1, default="", null=True) # S/N
    linkExterno = models.CharField(max_length=100, default="", null=True)
    nome_fornecedor = models.CharField(max_length=100, default="", null=True)
    codigo_fabricante = models.CharField(max_length=255, default="", null=True)
    data_validade = models.DateField(null=True, blank=True) # datetime.date
    origem = models.CharField(max_length=1, default="", null=True)
    descricao_fornecedor = models.CharField(max_length=255, default="", null=True)
    id_fabricante = models.CharField(max_length=20, default="", null=True)
    largura_produto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    altura_produto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    profundidade_produto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    unidade_medida = models.CharField(max_length=20, default="", null=True)
    producao = models.CharField(max_length=1, default="", null=True)
    sped_tipo_item = models.CharField(max_length=2, default="", null=True)
    data_alteracao = models.DateTimeField(null=True, blank=True) # datetime.datetime
    data_inclusao = models.DateTimeField(null=True, blank=True) # datetime.datetime
    
    def __str__(self):
        return self.descricao

class ProdutoKit(models.Model):
    id_bling = models.IntegerField(unique=True)
    codigo = models.CharField(max_length=60, default="")
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.DO_NOTHING, default="")
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
    data_alteracao = models.DateTimeField(null=True, blank=True) # datetime.datetime
    data_inclusao = models.DateTimeField(null=True, blank=True) # datetime.datetime
    sped_tipo_item = models.CharField(max_length=2, default="", null=True)

class Pedido(models.Model):
    data = models.DateField(null=True, blank=True)
    data_saida = models.DateTimeField(null=True, blank=True)
    numero = models.IntegerField(default=0, blank=True, null=True)
    vlr_frete = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, null=True)
    vlr_desconto = models.CharField(max_length=20, default="0%", null=True)
    obs = models.CharField(max_length=255, default="", null=True)
    loja = models.IntegerField(default=0, null=True, blank=True)
    vendedor = models.CharField(max_length=60, default="", null=True)
    numero_pedido_loja = models.CharField(max_length=30, blank=True, null=True)
    nat_operacao = models.CharField(max_length=60, default="Venda de mercadorias", null=True)
    situacao = models.CharField(max_length=30, default="", null=True)
    total_produtos = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, null=True)
    total_venda = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, null=True)
    tipo_integracao = models.CharField(max_length=60, default="", null=True)
    cliente = models.ForeignKey(Contato, default="", on_delete=models.DO_NOTHING, null=True)
    # transporte = models.ForeignKey(Contato, default="", on_delete=models.DO_NOTHING, null=True)
    # item = models.ForeignKey(Item, default="", on_delete=models.DO_NOTHING, null=True)
    def __str__(self):
        return self.numero

class FormaPagamento(models.Model):
    id_bling = models.IntegerField(unique=True)
    descricao = models.CharField(max_length=30, default="", null=True, blank=True)
    codigo_fiscal = models.IntegerField(null=True, blank=True)
    padrao = models.IntegerField(null=True, blank=True)
    situacao = models.IntegerField(null=True, blank=True)
    fixa = models.IntegerField(null=True, blank=True)

class ContaPagar(models.Model):
    id_bling = models.IntegerField(unique=True)
    situacao = models.CharField(max_length=30, default="", null=True, blank=True)
    data_emissao = models.DateTimeField(null=True, blank=True)
    vencimento = models.DateTimeField(null=True, blank=True)
    competencia = models.DateTimeField(null=True, blank=True)
    nro_documento = models.CharField(max_length=25, default="", null=True, blank=True)
    valor = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    saldo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    historico = models.CharField(max_length=255, default="", null=True, blank=True)
    categoria = models.CharField(max_length=255, default="", null=True, blank=True)
    portador = models.CharField(max_length=255, default="", null=True, blank=True)
    ocorrencia = models.CharField(max_length=255, default="", null=True, blank=True)
    nro_parcelas = models.IntegerField(null=True, blank=True)
    fornecedor = models.ForeignKey(Contato, on_delete=models.DO_NOTHING, null=True)

class ContaReceber(models.Model):
    id_bling = models.IntegerField(unique=True)
    situacao = models.CharField(max_length=30, default="", null=True, blank=True)
    data_emissao = models.DateTimeField(null=True, blank=True)
    vencimento = models.DateTimeField(null=True, blank=True)
    competencia = models.DateTimeField(null=True, blank=True)
    nro_documento = models.CharField(max_length=25, default="", null=True, blank=True)
    valor = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    saldo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    historico = models.CharField(max_length=255, default="", null=True, blank=True)
    categoria = models.CharField(max_length=255, default="", null=True, blank=True)
    portador = models.CharField(max_length=255, default="", null=True, blank=True)
    nro_banco = models.IntegerField(null=True)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.DO_NOTHING, null=True)
    ocorrencia = models.CharField(max_length=255, default="", null=True, blank=True)
    nro_parcelas = models.IntegerField(null=True, blank=True)
    link_boleto = models.CharField(max_length=255, default="", null=True, blank=True)
    vendedor = models.CharField(max_length=100, default="", null=True, blank=True)
    cliente = models.ForeignKey(Contato, on_delete=models.DO_NOTHING, null=True)

class Pagamento(models.Model):
    conta_pagar = models.ForeignKey(ContaPagar, on_delete=models.CASCADE, null=True)
    conta_receber = models.ForeignKey(ContaReceber, on_delete=models.CASCADE, null=True)
    total_pago = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    total_juro = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    total_desconto = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    total_acrescimo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    total_tarifa = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    data = models.DateTimeField(null=True, blank=True)

class Bordero(models.Model):
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, null=True)
    id_bling = models.IntegerField(null=True)
    conta = models.CharField(max_length=120, default="", null=True)
    data_pagamento = models.DateTimeField(null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    valor_juro = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    valor_desconto = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    valor_acrescimo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    valor_tarifa = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)

class Item(models.Model):
    codigo = models.CharField(max_length=60, default="", null=True, blank=True)
    descricao = models.CharField(max_length=120, default="", null=True)
    quantidade = models.DecimalField(max_digits=11, decimal_places=4, default=0.0000, null=True)
    valor_unidade = models.DecimalField(max_digits=17, decimal_places=10, null=True)
    preco_custo = models.DecimalField(max_digits=17, decimal_places=10, default=0, null=True)
    desconto_item = models.DecimalField(max_digits=11, decimal_places=3, default=0.000, null=True)
    peso_bruto = models.DecimalField(max_digits=11, decimal_places=3, default=0.000, null=True)
    largura = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    altura = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    profundidade = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)
    unidade_medida = models.CharField(max_length=20, default="", null=True)
    gtin = models.PositiveIntegerField(null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING, null=True)