from authApp.models.transaction import Transaction
from authApp.models.account import Account
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'origin_account', 'destiny_account', 'amount',
            'register_date', 'note'
        ]

    def to_representation(self, obj):
        #inf basica de la transacción
        #obtener de model transacción
        #Trae obj donde llave primaria sea = a la llave primaria del objeto evaluado
        transaction = Transaction.objects.get(id=obj.id) #Select where id = id
        account_origin = Account.objects.get(id=obj.origin_account_id)#_id por llave foranea del modelo
        account_destiny = Account.objects.get(id=obj.destiny_account_id)
        
        #Serializar
        return {
            'id'            : transaction.id,
            'amount'        : transaction.amount,
            'register_date' : transaction.register_date,
            'note'          : transaction.note,
            'origin_account' : {
                'id'        : account_origin.id,
                'balance'   : account_origin.balance,
                'lastChangeDate': account_origin.lastChangeDate,
                'isActive'      : account_origin.isActive
            },
            'destiny_account' : {
                'id'        : account_destiny.id,
                'balance'   : account_destiny.balance,
                'lastChangeDate': account_destiny.lastChangeDate,
                'isActive' : account_destiny.isActive
            }
        }