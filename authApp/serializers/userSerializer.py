from authApp.models.user                     import User
from authApp.models.account                  import Account
from authApp.serializers.accountSerializer   import AccountSerializer
from rest_framework                          import serializers

class UserSerializer(serializers.ModelSerializer):
    #Objeto de tipo serializador de la clase
    account = AccountSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email', 'account']

    #Recibe info y primera cuenta y valida la data
    def create(self, validated_data):
        accountData = validated_data.pop('account')
        userInstance = User.objects.create(**validated_data)
        #Guardad en bd
        Account.objects.create(user=userInstance, **accountData)
        return userInstance

#To string - De la data del obj la imprimo
    def to_representation(self, obj):
        #Guardad obj user a partir del modelo
        user = User.objects.get(id=obj.id)
        account = Account.objects.get(user=obj.id)
        return{
            "id"        : user.id,
            "username"  : user.username,
            "name"      : user.name,
            "email"     : user.email,
            "account"   : {
                "id"                : account.id,
                "balance"           : account.balance,
                "lastChangeDate"    : account.lastChangeDate,
                "isActive"          : account.isActive
            }
        }