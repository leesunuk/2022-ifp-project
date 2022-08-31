from contextlib import AbstractContextManager
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class Post(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    title = models.CharField('TITLE', max_length=50)
    material = models.ManyToManyField('Material')
    image = models.ImageField('IMAGE', upload_to='coffee/%Y/%m', blank=True, null=True)
    content = models.TextField('CONTENT')
    create_dt = models.DateTimeField('CREATE DT', auto_now_add=True)
    update_dt = models.DateTimeField('UPDATE DT', auto_now=True)
    bookmark_user = models.ManyToManyField(get_user_model(), blank=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('update_dt',)
        
    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Material(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class UserManager(BaseUserManager): #유저 생성시 사용하는 Helper class
    def create_user(self, email, date_of_birth, password=None):
        if not email: 
            raise ValueError('Users must have an email address')
         #django에서 제공해주는 user모델을 보면 email 파라메터 자리에 username이 있음,
         # 하지만 필자는 email을 이용해 로그인을 구현할 것임으로 다음과 같이 수정
        # email을 입력하지 않는 경우 ValueError를 return
        user = self.model(
            email = self.normalize_email(email),
            date_of_birth=date_of_birth,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, date_of_birth, password):
        #위와 같은 사유로 email로 치환
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser): # 실제 user 모델
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
        
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin