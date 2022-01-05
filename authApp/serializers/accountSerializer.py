from authApp.models.account import Account
from rest_framework         import serializers
#Json a objeto y vis
class AccountSerializer(serializers.ModelSerializer):
    #Heredar atributos de Meta
    class Meta:
        model = Account
        fields = ['balance', 'lastChangeDate', 'isActive'] 