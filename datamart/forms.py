# coding: utf-8

from django import forms


class EditarVendaForm(forms.Form):
    dtpedido = forms.DateTimeField(
        label='Data do Pedido',
    )

    dtenvio = forms.DateTimeField(
        label='Data do Envio',
    )

    dtrecebimento = forms.DateTimeField(
        label='Data do Recebimento',
    )

    contacliente = forms.CharField(
        label='Conta do Cliente',
        # max_length=15,
    )

    numerocartaocredito = forms.IntegerField(
        label='Número do Cartão de Crédito',
        # max_length=15,
    )

    imposto = forms.FloatField(
        label='Imposto',
    )

    codigotransportadora = forms.ChoiceField(
        label='Transportadora',
    )

    codigocliente = forms.ChoiceField(
        label='Cliente',
    )

    enderecofatura = forms.ChoiceField(
        label='Endereço da Fatura',
    )

    enderecoentrega = forms.ChoiceField(
        label='Endereço de Entrega',
    )
