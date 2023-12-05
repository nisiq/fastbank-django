from sqlite3 import IntegrityError
from rest_framework import (
    viewsets,
    status
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication as authenticationJWT
from core.models import CartaoCredito, Conta, HistoricoCartaoCredito, HistoricoSaldo

from api import serializers
import random, decimal

from rest_framework.decorators import action


class AccountViewSet(viewsets.ModelViewSet):
    "SELECT * FROM contas";
    queryset = Conta.objects.all()
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Pegar contas para usuarios autenticados """
        queryset = self.queryset
        return queryset.filter(
            user=self.request.user
        ).order_by('-created_at').distinct() #distinct evita duplicacao
    #"SELECT * FROM contas where user_id = 1"


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AccountDetailSerializer
        
        return serializers.AccountSerializer
    

    def create(self, request, *args, **kwargs):
        serializer = serializers.AccountSerializer(data=request.data)
        if serializer.is_valid():
            agencia = '0001'
            numero = ''
            # Sequencia aleatoria para o numero do seu cartao/banco
            for n in range(8):
                numero += str(random.randint(0, 9))

            conta = Conta(
                user=self.request.user,
                numero=numero,
                agencia=agencia
            )

            conta.saldo = decimal.Decimal(0)

            conta.save()

            return Response({'message':'Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def registrar_transacao(self, tipo, valor):
        conta = self.get_object()
        conta.registrar_transacao(tipo, valor)


    
    

    #REALIZAR SAQUE
    @action(methods=['POST'], detail=True, url_path='sacar')
    def sacar(self, request, pk=None):
        conta = Conta.objects.filter(id=pk).first() # Pegar a primeira conta que encontrar

        serializer_recebido = serializers.SaqueSerializer(data=request.data)

        # Se for valido e existir uma conta
        if serializer_recebido.is_valid() and conta:
                                        #pegar o valor           #pegar o dado validado 
            valor_saque = decimal.Decimal(serializer_recebido.validated_data.get('value')) #value em serializert
            # Pegar o saldo da pessoa
            saldo = decimal.Decimal(conta.saldo)

            comparacao = saldo.compare(valor_saque)
            
            if comparacao == 0 or comparacao == 1:
                print(saldo - valor_saque)
                #se o que descontar for menor ou igual a 0 = desconto - 0, 
                # se nao = saldo - saque
                novo_valor = 0 if saldo - valor_saque <= 0  else saldo - valor_saque

                conta.saldo = novo_valor
                conta.save()

                self.registrar_transacao(HistoricoSaldo.TIPO_SAQUE, valor_saque)
                return Response({"saldo": conta.saldo}, status=status.HTTP_200_OK)
            
            return Response({'message': 'Saldo Insuficiente'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer_recebido.errors, status=status.HTTP_400_BAD_REQUEST)
    

#@action = funcao nao padrao
    #DEPOSITO
    @action(methods=['POST'], detail=True, url_path='depositar')
    def depositar(self, request, pk=None):
        conta = Conta.objects.filter(id=pk).first() # Pegar a primeira conta que encontrar
        serializer_recebido = serializers.DepositoSerializer(data=request.data)

        if serializer_recebido.is_valid() and conta:
            # Pegar valor do deposito
            valor_deposito = decimal.Decimal(serializer_recebido.validated_data.get('value'))
            # Saldo da pessoa
            saldo = decimal.Decimal(conta.saldo)

            conta.saldo = saldo + valor_deposito
            conta.save()

            self.registrar_transacao(HistoricoSaldo.TIPO_DEPOSITO, valor_deposito)
            return Response({"saldo": conta.saldo}, status=status.HTTP_200_OK)

        return Response(serializer_recebido.errors, status=status.HTTP_400_BAD_REQUEST)


    # TRANSFERENCIA
    @action(methods=['POST'], detail=True, url_path='transferir')
    def transferir(self, request, pk=None):
        
        conta_origem = Conta.objects.filter(id=pk).first()

        if conta_origem:
            serializer = serializers.TransferenciaSerializer(data=request.data)

            if serializer.is_valid():
                # Obtém a conta de destino e o valor da transferência
                conta_destino = serializer.validated_data.get('conta_destino')
                valor_transferencia = decimal.Decimal(serializer.validated_data.get('valor'))

                # saldo suficiente para a transferência?
                if conta_origem.saldo >= valor_transferencia:
                    conta_origem.saldo -= valor_transferencia
                    conta_origem.save()

                    # Adiciona o valor no saldo
                    conta_destino.saldo += valor_transferencia
                    conta_destino.save()


                    self.registrar_transacao(HistoricoSaldo.TIPO_TRANSFERENCIA, valor_transferencia)
                    conta_destino.registrar_transacao(HistoricoSaldo.TIPO_TRANSFERENCIA, valor_transferencia)
                    return Response({"saldo_origem": conta_origem.saldo, "saldo_destino": conta_destino.saldo},
                            status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Saldo insuficiente para a transferência"},
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Conta de origem não encontrada"}, status=status.HTTP_404_NOT_FOUND)
    

    # solicitar cartão
    @action(methods=['POST'], detail=True, url_path='solicitar_cartao')
    def solicitar_cartao(self, request, pk=None):
        conta = Conta.objects.filter(id=pk).first()

        if conta:
            #analisa se a conta já possui um cartão de crédito associado
            if conta.cartao_credito:
                return Response({"detail": "Esta conta já possui um cartão de crédito..."},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = serializers.CreditCardSerializer(data=request.data)

            if serializer.is_valid():
                try:
                    # criando os dados do cartão
                    cartao_credito = serializer.create_credit_card_data(serializer.validated_data)

                    # associando o cartão a conta antes de salvar
                    cartao_credito.save()
                    conta.cartao_credito = cartao_credito
                    conta.save()

                    return Response({"message": "Cartão de crédito solicitado com sucesso! Iniciando com um limite de 1.000,00 :)"},
                                    status=status.HTTP_200_OK)
                except IntegrityError:
                    return Response({"detail": "Erro ao associar o cartão de crédito a conta"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Conta não encontrada"}, status=status.HTTP_404_NOT_FOUND)
    

    def calcular_valor_total_com_juros(self, valor_emprestimo, num_parcelas):
        # Aqui você pode adicionar qualquer lógica necessária para calcular o valor total com base nas parcelas e no valor do empréstimo
        # Vamos simplificar e assumir que o valor total é o valor do empréstimo por enquanto
        return valor_emprestimo, self.calcular_juros(valor_emprestimo, num_parcelas)

    def calcular_juros(self, valor_emprestimo, num_parcelas):
        # adiciona 50 reais fixo de juros fixo
        valor_fixo = decimal.Decimal('50.00')

        # Percentual de aumento por parcela
        percentual_aumento = 5  # Ajuste conforme necessário

        valor_juros = valor_fixo + (valor_emprestimo * percentual_aumento / 100 * num_parcelas)

        return valor_juros

    @action(methods=['POST'], detail=True, url_path='solicitar_emprestimo')
    def solicitar_emprestimo(self, request, pk=None):
        conta = Conta.objects.filter(id=pk).first()

        if conta:
            serializer = serializers.EmprestimoSerializer(data=request.data)

            if serializer.is_valid():
                # get valor e numero de parcelas
                valor_emprestimo = decimal.Decimal(serializer.validated_data.get('valor'))
                num_parcelas = serializer.validated_data.get('num_parcelas')

                # calcular o valor total com juros
                valor_base, valor_juros = self.calcular_valor_total_com_juros(valor_emprestimo, num_parcelas)

                # validar o valor aprov/repro
                limite_minimo = valor_emprestimo * decimal.Decimal('0.10')
                if conta.saldo >= limite_minimo:
                    
                    conta.saldo += valor_base
                    conta.save()
                
                    self.registrar_transacao(HistoricoSaldo.TIPO_EMPRESTIMO, valor_base)
                    return Response({
                    "message": "Empréstimo aprovado!",
                    "quantidade de parcelas": num_parcelas,
                    "juros": valor_juros,
                    "valor total a pagar": (valor_emprestimo + valor_juros)
                }, status=status.HTTP_200_OK)

                else:
                    return Response({"detail": "Status Financeiro insuficiente para o empréstimo. Você deve ter pelo menos 10% do valor solicitado."},
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Conta não encontrada"}, status=status.HTTP_404_NOT_FOUND)
    


    @action(methods=['POST'], detail=True, url_path='transacao_cartao')
    def transacao_cartao(self, request, pk=None):
        conta = Conta.objects.filter(id=pk).first()

        if conta and conta.cartao_credito:
            serializer = serializers.TransacaoCartaoSerializer(data=request.data)

            if serializer.is_valid():
                valor_transacao = decimal.Decimal(serializer.validated_data.get('valor'))
                local_transacao = serializer.validated_data.get('local')

                # verifica o limite do cartão
                if conta.cartao_credito.limite_disponivel >= valor_transacao:
                    # cobra da fatura
                    conta.cartao_credito.limite_disponivel -= valor_transacao
                    conta.cartao_credito.save()

                    # histórico do cartão de crédito
                    historico_transacao = HistoricoCartaoCredito.objects.create(
                        cartao_credito=conta.cartao_credito,
                        valor=-valor_transacao,
                        local=local_transacao
                    )

                    conta.registrar_transacao(HistoricoSaldo.TIPO_TRANSFERENCIA, -valor_transacao)
                    return Response({
                    "message": "Transação realizada com sucesso!",
                    "limite_disponivel": conta.cartao_credito.limite_disponivel,
                    "destinatario": local_transacao
                }, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Limite do cartão insuficiente para a transação"},
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Conta ou cartão de crédito não encontrados"},
                        status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['GET'], url_path='historico-transacoes')
    def historico_transacoes(self, request, pk=None):
        # Obtenha a conta associada ao usuário autenticado
        conta = Conta.objects.filter(id=pk, user=request.user).first()

        if conta:
            # Obtenha o histórico de transações da conta
            transacoes = HistoricoSaldo.objects.filter(conta=conta).order_by('-data_transacao')

            # Serialização e retorno da resposta
            serializer = serializers.HistoricoSaldoSerializer(transacoes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Conta não encontrada"}, status=status.HTTP_404_NOT_FOUND)
    

class HistoricoCartaoViewSet(viewsets.ReadOnlyModelViewSet):
    """ Exibe o histórico de transações no cartão de crédito """
    serializer_class = serializers.HistoricoCartaoSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cartao_credito = CartaoCredito.objects.filter(conta__user=self.request.user).first()
        if cartao_credito:
            return HistoricoCartaoCredito.objects.filter(cartao_credito=cartao_credito).order_by('-data_transacao')
        return HistoricoCartaoCredito.objects.none()


class HistoricoSaldoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoricoSaldo.objects.all()
    serializer_class = serializers.HistoricoSaldoSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # filtrar as transações por conta do usuário autenticado
        return HistoricoSaldo.objects.filter(conta__user=self.request.user).order_by('-data_transacao')
