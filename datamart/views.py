from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .models import Cliente, Pedido
from django.conf import settings


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
    venda = Pedido.get_by_id_as_dict(pk)
    # transportadora =

    context = {
        'venda': venda,
        # 'transportadora': transportadora,
    }
    return render(request, 'datamart/detalhes_venda.html', context)
