import datetime
import random
from rest_framework import serializers
from core.models import Conta, CartaoCredito
from datetime import datetime, timedelta


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['id', 'agencia', 'numero']
        read_only_fields = ['numero'] #Apenas leitura


class AccountDetailSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + ['id', 'saldo', 'created_at']
        read_only_fields = AccountSerializer.Meta.read_only_fields + ['id', 'saldo', 'created_at']



class DepositoSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        fields = ['value']



class SaqueSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        fields = ['value']



class TransferenciaSerializer(serializers.Serializer):
    conta_origem = serializers.PrimaryKeyRelatedField(queryset=Conta.objects.all())
    conta_destino = serializers.PrimaryKeyRelatedField(queryset=Conta.objects.all())
    valor = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        fields = ['conta_origem', 'conta_destino', 'valor']


class CreditCardSerializer(serializers.Serializer):
    # campo para a solicitação do cartão de crédito
    salario = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create_credit_card_data(self, validated_data):
        """
        Método para criar os dados do cartão de crédito
        """
        # tudo aleatorio
        numero_cartao = ''.join([str(random.randint(0, 9)) for _ in range(13)])
        cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
        
        data_vencimento = (datetime.now() + timedelta(days=3650)).strftime('%Y-%m-%d')

        # lgc para aprovar ou negar
        limite_disponivel = 1000.00 if validated_data.get('salario') > 1200.00 else 0.00

        credit_card_data = {
            'numero_cartao': numero_cartao,
            'cvv': cvv,
            'data_vencimento': data_vencimento,
            'limite_disponivel': limite_disponivel,
            'salario': validated_data.get('salario'),
        }

        # instância do modelo CartaoCredito com os dados gerados
        credit_card = CartaoCredito.objects.create(**credit_card_data)

        return credit_card

    def validate(self, data):
        """
         garantir que o salário seja fornecido
        """
        if not data.get('salario'):
            raise serializers.ValidationError("Salário é obrigatório para solicitar um cartão de crédito.")

        return data


