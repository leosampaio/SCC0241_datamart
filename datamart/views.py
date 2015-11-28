from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Pedido, Transportadora, Endereco, Produto, DetalhesPedido, ClienteEndereco
from django.conf import settings
from .forms import EditarVendaForm, EditarProdutoForm, CadastrarClienteForm, CadastrarEnderecoForm
from .pdf import hello
from reportlab.pdfgen import canvas


def clients_index(request):
    clientes = Cliente.all()
    return HttpResponse(clientes)


def index(request):
    return render(request, 'datamart/index.html')


def conta(request):
    return render(request, 'datamart/conta.html')


def listar_vendas(request):
    lista_de_vendas = Pedido.dictfetchall()[:settings.LIMIT_QUERY]

    context = {
        'vendas': lista_de_vendas,
    }
    return render(request, 'datamart/listar_vendas.html', context)


def detalhes_venda(request, pk):
    form = EditarVendaForm()
    if request.method == 'POST':
        form = EditarVendaForm(request.POST)
    venda = Pedido.get_by_id_as_dict(pk)

    transportadoras = Transportadora.get_all_as_choice()[:settings.LIMIT_QUERY]
    clientes = Cliente.get_all_as_choice()[:settings.LIMIT_QUERY]
    enderecos = Endereco.get_all_as_choice()[:settings.LIMIT_QUERY]

    if settings.LIMIT_QUERY is not None:
        transportadoras = set(transportadoras)
        transportadoras.add((venda['CODIGOTRANSPORTADORA']['CODIGO'], venda['CODIGOTRANSPORTADORA']['NOME']))

        clientes = set(clientes)
        clientes.add((str(venda['CODIGOCLIENTE']['CODIGO']), venda['CODIGOCLIENTE']['NOMECONCATENADO']))

        enderecos = set(enderecos)
        for e in ['ENDERECOFATURA', 'ENDERECOENTREGA']:
            enderecos.add((str(venda[e]['ID']), venda[e]['ENDERECOCONCATENADO']))

    form.fields['dtpedido'].initial = venda['DTPEDIDO']
    form.fields['dtenvio'].initial = venda['DTENVIO']
    form.fields['dtrecebimento'].initial = venda['DTRECEBIMENTO']
    form.fields['contacliente'].initial = venda['CONTACLIENTE']
    form.fields['numerocartaocredito'].initial = venda['NUMEROCARTAOCREDITO']
    form.fields['imposto'].initial = venda['IMPOSTO']

    form.fields['codigotransportadora'].choices = transportadoras
    form.fields['codigotransportadora'].initial = venda['CODIGOTRANSPORTADORA']['CODIGO']

    form.fields['codigocliente'].choices = clientes
    form.fields['codigocliente'].initial = venda['CODIGOCLIENTE']['CODIGO']

    form.fields['enderecofatura'].choices = enderecos
    form.fields['enderecofatura'].initial = venda['ENDERECOFATURA']['ID']

    form.fields['enderecoentrega'].choices = enderecos
    form.fields['enderecoentrega'].initial = venda['ENDERECOENTREGA']['ID']

    context = {
        'venda': venda,
        'form': form,
    }
    return render(request, 'datamart/detalhes_venda.html', context)


def detalhes_produto(request, pk):
    form = EditarProdutoForm()
    if request.method == 'POST':
        form = EditarProdutoForm(request.POST)

    produtos_venda = DetalhesPedido.get_by_id_as_dict(pk)
    produtos_choice = Produto.get_all_as_choice()[:settings.LIMIT_QUERY]
    produtos_precos = Produto.get_all_as_pricelist()[:settings.LIMIT_QUERY]

    form.fields['codigoproduto'].choices = produtos_choice

    # form.fields['desconto'].initial = 0

    context = {
        'venda_id': pk,
        'produtos_venda': produtos_venda,
        'produtos_precos': produtos_precos,
        'form': form,
    }

    return render(request, 'datamart/detalhes_produto.html', context)


def alterar_produto(request, venda_pk, produto_codigo):
    form = EditarProdutoForm()
    if request.method == 'POST':
        form = EditarProdutoForm(request.POST)

    produto_atual = DetalhesPedido.get_by_pk_as_dict(venda_pk, produto_codigo)
    produtos_choice = Produto.get_all_as_choice()[:settings.LIMIT_QUERY]
    produtos_precos = Produto.get_all_as_pricelist()[:settings.LIMIT_QUERY]

    if settings.LIMIT_QUERY is not None:
        produtos_choice = set(produtos_choice)
        produtos_precos = set(produtos_precos)
        produtos_choice.add((produto_atual['CODIGOPRODUTO']['CODIGO'], produto_atual['CODIGOPRODUTO']['NOMECONCATENADO']))
        produtos_precos.add((produto_atual['CODIGOPRODUTO']['CODIGO'], produto_atual['CODIGOPRODUTO']['PRECO']))

    form.fields['codigoproduto'].choices = produtos_choice
    form.fields['codigoproduto'].initial = produto_atual['CODIGOPRODUTO']['CODIGO']
    form.fields['desconto'].initial = produto_atual['DESCONTO']
    form.fields['quantidade'].initial = produto_atual['QUANTIDADE']

    context = {
        'venda_id': venda_pk,
        'produtos_precos': produtos_precos,
        'form': form,
    }

    return render(request, 'datamart/alterar_produto.html', context)


def nova_venda(request):
    form = EditarVendaForm()
    if request.method == 'POST':
        form = EditarVendaForm(request.POST)
        # Salva as coisas no BD
        # Redireciona para url:alterar_produto param:(ID desta venda)

    transportadoras = Transportadora.get_all_as_choice()[:settings.LIMIT_QUERY]
    clientes = Cliente.get_all_as_choice()[:settings.LIMIT_QUERY]
    enderecos = Endereco.get_all_as_choice()[:settings.LIMIT_QUERY]

    form.fields['codigotransportadora'].choices = transportadoras
    form.fields['codigocliente'].choices = clientes
    form.fields['enderecofatura'].choices = enderecos
    form.fields['enderecoentrega'].choices = enderecos

    context = {
        'form': form,
    }
    return render(request, 'datamart/nova_venda.html', context)


def cadastrar_cliente(request):
    form = CadastrarClienteForm()
    if request.method == 'POST':
        form = EditarVendaForm(request.POST)
        # Salva as coisas no BD
        # Redireciona para url:incluir_enderecos param:(ID deste user)

    context = {
        'form': form,
    }

    return render(request, 'datamart/cadastrar_cliente.html', context)


def cadastrar_enderecos(request, cliete_codigo):
    form = CadastrarEnderecoForm()
    enderecos = ClienteEndereco.get_by_id_as_dict(cliete_codigo)
    if request.method == 'POST':
        form = CadastrarEnderecoForm(request.POST)
        # Inclui endereço no BD

    enderecos_choice = Endereco.get_all_as_choice()[:settings.LIMIT_QUERY]
    form.fields['endereco'].choices = enderecos_choice

    context = {
        'enderecos': enderecos,
        'form': form,
    }

    return render(request, 'datamart/cadastrar_endereco.html', context)


def relatorios(request):
    return render(request, 'datamart/tela_relatorios.html')


def sp_clientes_gt_15_pedidos(request):
    c = canvas.Canvas("hello.pdf")
    hello(c)
    c.showPage()
    c.save()
    return render(request, 'datamart/tela_relatorios.html')
