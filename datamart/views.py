# coding:utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cliente, Pedido, Transportadora, Endereco, Produto, DetalhesPedido, ClienteEndereco
from django.conf import settings
from .forms import EditarVendaForm, EditarProdutoForm, CadastrarClienteForm, CadastrarEnderecoForm
from wkhtmltopdf.views import PDFTemplateView
from django.db import connection


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

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        print(form.cleaned_data)

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
    if request.method == 'POST' and form.is_valid():
        print(form.cleaned_data)

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

    if request.method == 'POST' and form.is_valid():
        print(form.cleaned_data)

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

    if request.method == 'POST' and form.is_valid():
        print(form.cleaned_data)

    context = {
        'form': form,
    }
    return render(request, 'datamart/nova_venda.html', context)


def cadastrar_cliente(request):
    form = CadastrarClienteForm()
    if request.method == 'POST':
        form = CadastrarClienteForm(request.POST)
        # Salva as coisas no BD
        # Redireciona para url:incluir_enderecos param:(ID deste user)

    if request.method == 'POST' and form.is_valid():
        d = form.cleaned_data
        cliente = Cliente(
            d['sufixo'], d['nomedomeio'], d['primeironome'], d['sobrenome'], d['senha'], d['tratamento']
        )

        cliente.save()
        return redirect('cadastrar_enderecos', cliente_codigo=cliente.codigo)

    context = {
        'form': form,
    }

    return render(request, 'datamart/cadastrar_cliente.html', context)


def cadastrar_enderecos(request, cliente_codigo):
    form = CadastrarEnderecoForm()
    if request.method == 'POST':
        form = CadastrarEnderecoForm(request.POST)
        # Inclui endereco no BD

    enderecos_choice = Endereco.get_all_as_choice()[:settings.LIMIT_QUERY]
    form.fields['endereco'].choices = enderecos_choice

    if request.method == 'POST' and form.is_valid():
        print(form.cleaned_data)
        d = form.cleaned_data
        cliente_endereco = ClienteEndereco(
            cliente_codigo, d['endereco'], d['tipoendereco']
        )

        cliente_endereco.save()

    enderecos = ClienteEndereco.get_by_id_as_dict(cliente_codigo)

    context = {
        'enderecos': enderecos,
        'form': form,
    }

    return render(request, 'datamart/cadastrar_endereco.html', context)


def relatorios(request):
    return render(request, 'datamart/tela_relatorios.html')


def get_sp_clientes_gt_15_pedidos():
    cursor = connection.cursor()
    cursor.execute("SELECT (C.primeiroNome || ' ' || C.nomedoMeio || ' ' || C.sobrenome) as nomeCompleto, COUNT(*) as numeroPedidos \
FROM Cliente C \
JOIN Pedido P ON P.codigoCliente = C.codigo \
GROUP BY (C.primeiroNome || ' ' || C.nomedoMeio || ' ' || C.sobrenome) \
HAVING COUNT(*) >= 15 \
ORDER BY COUNT(*) DESC")

    querylist = cursor.fetchall()
    querylist = list(querylist)
    context = []

    for query in querylist:
        context.append({
            'NOMECOMPLETO': query[0],
            'NUMEROPEDIDOS': query[1],
        })

    return context


class SPClientes(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'pdf/clientes_gt_15_pedidos.html'
    cmd_options = {
        'margin-top': 3,
    }

    def get_context_data(self, **kwargs):
        context = super(SPClientes, self).get_context_data(**kwargs)
        context['titulo_relatorio'] = 'Clientes com mais do que 15 pedidos'
        context['clientes'] = get_sp_clientes_gt_15_pedidos()
        return context


def sp_clientes_gt_15_pedidos(request):
    return render(request, 'datamart/tela_relatorios.html')

