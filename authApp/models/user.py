from django.db                   import models
from django.contrib.auth.models  import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

#DAO: Gestor del modelo
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('El usuario debe tener un nickname o usuario.')
            user = self.model(username=username)
            user.set_password(password)
            user.save_(using=self._db)
            return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save_(using=self._db)
        return user


#Hereda abstracción de cualquier usuario que se maneja y gestiona sus permisos
class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)#id aleatorio
    username = models.CharField('Username', max_length=25, unique=True)
    password = models.CharField('Password', max_length=256)
    name = models.CharField('Name', max_length=50)
    email = models.EmailField('Email', max_length=60)

    #Guardad el usuario para generar tokens de acceso
    def save(self, **kwargs):#self=this #Parametros guardados como diccionario
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        #Encriptar pass enviada por el user a través del salt
        self.password = make_password(self.password, some_salt)
        #Traer método de guardar de la superclase
        super().save(**kwargs)

    objects = UserManager()
    #De User cuál es el nombre único de usuario = username
    USERNAME_FIELD = 'username'