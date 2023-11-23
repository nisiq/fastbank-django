from rest_framework import serializers
from core.models import Conta

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