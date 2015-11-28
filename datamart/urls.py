from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^conta/$', views.conta, name='conta'),
    url(r'^listar-vendas/$', views.listar_vendas, name='listar_vendas'),
    url(r'^listar-vendas/detalhes/(\d+)/$', views.detalhes_venda, name='detalhes_venda'),
    url(r'^listar-vendas/detalhes/(\d+)/produtos/$', views.detalhes_produto, name='detalhes_produto'),
    url(r'^listar-vendas/detalhes/(\d+)/produtos/editar/([A-Za-z0-9_\-]+)/$', views.alterar_produto, name='alterar_produto'),
]
