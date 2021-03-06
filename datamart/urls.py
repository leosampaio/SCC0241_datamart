from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^conta/$', views.conta, name='conta'),
    url(r'^nova-venda/$', views.nova_venda, name='nova_venda'),

    url(r'^cadastrar-cliente/$', views.cadastrar_cliente, name='cadastrar_cliente'),
    url(r'^cadastrar-cliente/(?P<cliente_codigo>\d+)/enderecos/$', views.cadastrar_enderecos, name='cadastrar_enderecos'),

    url(r'^listar-vendas/$', views.listar_vendas, name='listar_vendas'),
    url(r'^listar-vendas/detalhes/(\d+)/$', views.detalhes_venda, name='detalhes_venda'),
    url(r'^listar-vendas/delete/(\d+)/$', views.delete_venda, name='delete_venda'),
    url(r'^listar-vendas/detalhes/(?P<codigopedido>\d+)/produtos/$', views.detalhes_produto, name='detalhes_produto'),
    url(r'^listar-vendas/detalhes/(\d+)/produtos/editar/([A-Za-z0-9_\-]+)/$', views.alterar_produto, name='alterar_produto'),

    url(r'^relatorios/$', views.relatorios, name='relatorios'),
    url(r'^relatorios/sp-clientes-gt-15-pedidos/$', views.sp_clientes_gt_15_pedidos, name='sp_clientes_gt_15_pedidos'),
    url(r'^relatorios/sp-clientes-gt-15-pedidos/pdf/$', views.SPClientes.as_view(), name='sp_clientes_gt_15_pedidos_pdf'),
    url(r'^relatorios/relatorio2/$', views.relatorio2_html, name='relatorio2_html'),
    url(r'^relatorios/relatorio2/pdf/$', views.relatorio2.as_view(), name='relatorio2_pdf'),
]
