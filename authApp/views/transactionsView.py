from django.conf                        import settings
from rest_framework                     import generics, status
from rest_framework.response            import Response
from rest_framework.permissions         import IsAuthenticated
from rest_framework_simplejwt.backends  import TokenBackend

from authApp.models.account                     import Account
from authApp.models.transaction                 import Transaction
from authApp.serializers.transactionSerializer  import TransactionSerializer


class TransactionDetailView(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()

    def get(self, request, *args, **kwargs):
        token           = request.META.get('HTTP_AUTHORIZATION')[7:]
        token_backend   = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data      = token_backend.decode(token, verify=False)

        if valid_data['user_id'] != kwargs['user']:
            string_response = {'detail':'No tiene acceso autorizado.'}
            return Response(string_response, status=status.HTTP_401_UNAUTHORIZED)
        
        return super().get(request, *args, **kwargs)

class TransactionsAccountView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Transaction.objects.all()

    def get_queryset(self):
        token           = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        token_backend   = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data      = token_backend.decode(token, verify=False)

        if valid_data['user_id'] != self.kwargs['user']:
            string_response = {'detail':'No tiene acceso autorizado.'}
            return Response(string_response, status=status.HTTP_401_UNAUTHORIZED)
        
        #Select * from transaction where origin_account_id = '2'
        queryset = Transaction.objects.filter(origin_account_id=self.kwargs['account'])
        return queryset

class TransactionCreateView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        token           = request.META.get('HTTP_AUTHORIZATION')[7:]
        token_backend   = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data      = token_backend.decode(token, verify=False)

        if valid_data['user_id'] != request.data['user_id']:
            string_response = {'detail':'No tiene acceso autorizado.'}
            return Response(string_response, status=status.HTTP_401_UNAUTHORIZED)
       
        origin_account = Account.objects.get(id=request.data['transaction_data']['origin_account'])
        if origin_account.balance < request.data['transaction_data']['amount']:
            string_response = {'detail':'Saldo Insuficiente'}
            return Response(string_response, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        serializer = TransactionSerializer(data=request.data['transaction_data'])
        serializer.is_valid(raise_exception=True)
        serializer.save()

        origin_account.balance -= request.data['transaction_data']['amount']
        origin_account.save()
        
        destiny_account = Account.objects.get(id=request.data['transaction_data']['destiny_account'])
        destiny_account.balance += request.data['transaction_data']['amount']
        destiny_account.save()
        
        return Response("Transacción exitosa", status=status.HTTP_201_CREATED)

class TransactionUpdateView(generics.UpdateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Transaction.objects.all()

    def put(self, request, *args, **kwargs):
        token           = request.META.get('HTTP_AUTHORIZATION')[7:]
        token_backend   = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data      = token_backend.decode(token, verify=False)

        if valid_data['user_id'] != kwargs['user']:
            string_response = {'detail':'No tiene acceso autorizado.'}
            return Response(string_response, status=status.HTTP_401_UNAUTHORIZED)
        
        return super().update(request, *args, **kwargs)

class TransactionDeleteView(generics.DestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Transaction.objects.all()

    def delete(self, request, *args, **kwargs):
        token           = request.META.get('HTTP_AUTHORIZATION')[7:]
        token_backend   = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data      = token_backend.decode(token, verify=False)

        if valid_data['user_id'] != kwargs['user']:
            string_response = {'detail':'No tiene acceso autorizado.'}
            return Response(string_response, status=status.HTTP_401_UNAUTHORIZED)
        
        return super().destroy(request, *args, **kwargs)
