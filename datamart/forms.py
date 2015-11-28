# coding: utf-8

from django import forms


class EditarVendaForm(forms.Form):
    codigocliente = forms.ChoiceField(
        label='Cliente',
    )

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

    enderecofatura = forms.ChoiceField(
        label='Endereço da Fatura',
    )

    enderecoentrega = forms.ChoiceField(
        label='Endereço de Entrega',
    )


class EditarProdutoForm(forms.Form):
    codigoproduto = forms.ChoiceField(
        label='Produto',
    )

    quantidade = forms.IntegerField(
        label='Quantidade',
        min_value=0,
    )

    desconto = forms.FloatField(
        label='Desconto',
        max_value=1.0,
        min_value=0.0,
    )


class CadastrarClienteForm(forms.Form):
    tratamento = forms.CharField(
        label='Tratamento',
        max_length=8,
    )

    primeironome = forms.CharField(
        label='Primeiro Nome',
        max_length=50,
    )

    nomedomeio = forms.CharField(
        label='Nome do Meio',
        max_length=50,
    )

    sobrenome = forms.CharField(
        label='Sobrenome',
        max_length=50,
    )

    sufixo = forms.CharField(
        label='Sufixo',
        max_length=10,
    )

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'required': True})
    )


class CadastrarEnderecoForm(forms.Form):
    tipoendereco = forms.CharField(
        label='Tipo de Endereço',
        max_length=50,
    )

    endereco = forms.ChoiceField(
        label='Endereço',
    )
