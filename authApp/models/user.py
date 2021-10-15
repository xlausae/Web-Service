from django.db                   import models
from django.contrib.auth.models  import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

#Hereda abstracción de cualquier usuario que se maneja y gestiona sus permisos
class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)#id aleatorio
    username = models.CharField('Username', max_lenght=25, unique=True)
    password = models.CharField('Password', max_lenght=256)
    name = models.CharField('Name', max_lenght=50)
    email = models.EmailField('Email', max_lenght=60)


    #Guardad el usuario para generar tokens de acceso
    def save_(self, **kwargs):#self=this #Parametros guardados como diccionario
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        #Encriptar pass enviada por el user a través del salt
        self.password = make_password(self.password, some_salt)
        #Traer método de guardar de la superclase
        super().save(**kwargs)