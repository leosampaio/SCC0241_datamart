from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .models import Cliente, Pedido, Transportadora, Endereco
from django.conf import settings
from .forms import EditarVendaForm


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
        pass
    venda = Pedido.get_by_id_as_dict(pk)

    transportadoras = Transportadora.get_all_as_choice()[:settings.LIMIT_QUERY]
    clientes = Cliente.get_all_as_choice()[:settings.LIMIT_QUERY]
    enderecos = Endereco.get_all_as_choice()[:settings.LIMIT_QUERY]

    if settings.LIMIT_QUERY is not None:
        transportadoras = set(transportadoras)
        transportadoras.add((venda['CODIGOTRANSPORTADORA']['CODIGO'], venda['CODIGOTRANSPORTADORA']['NOME']))

        clientes = set(clientes)
        if venda['CODIGOCLIENTE']['NOMEDOMEIO'] is not None:
            clientes.add((str(venda['CODIGOCLIENTE']['CODIGO']), ' '.join([str(venda['CODIGOCLIENTE']['PRIMEIRONOME']), str(venda['CODIGOCLIENTE']['NOMEDOMEIO']), str(venda['CODIGOCLIENTE']['SOBRENOME'])])))
        else:
            clientes.add((str(venda['CODIGOCLIENTE']['CODIGO']), ' '.join([str(venda['CODIGOCLIENTE']['PRIMEIRONOME']), str(venda['CODIGOCLIENTE']['SOBRENOME'])])))

        enderecos = set(enderecos)
        for e in ['ENDERECOFATURA', 'ENDERECOENTREGA']:
            if venda[e]['COMPLEMENTO'] is not None:
                enderecos.add((str(venda[e]['ID']), ' - '.join([str(venda[e]['LOGRADOURO']), str(venda[e]['COMPLEMENTO']), str(venda[e]['CIDADE']), str(venda[e]['ESTADO']), str(venda[e]['PAIS']), str(venda[e]['CODIGOPOSTAL'])])))
            else:
                enderecos.add((str(venda[e]['ID']), ' - '.join([str(venda[e]['LOGRADOURO']), str(venda[e]['CIDADE']), str(venda[e]['ESTADO']), str(venda[e]['PAIS']), str(venda[e]['CODIGOPOSTAL'])])))

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
