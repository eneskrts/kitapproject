from django.db import models

from django import forms
# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from kitapproje.send_mail import mail_gonder
from django.templatetags.static import static
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.password_validation import validate_password
from time import time
import re
def name_validator(value):
    if not value.isalpha():
        raise ValidationError("Bu Alan Sadece harflerden oluşmalıdır")
def pass_validator(value):
    #validate_password(value)
    if len(value) < 8 or len(value) > 100:
        raise ValidationError("Şifreniz 8 karakterden uzun 100 karakterden kısa olamaz")

    if re.search('[0-9]', value) is None:
        raise ValidationError("Şifrenizde En Az Bir Sayı Bulunmalıdır")

    if re.search('[A-Z]', value) is None:
        raise ValidationError("Şifrenizde En Az Bir Büyük Harf Bulunmalıdır")

    else:
        pass
def il_ilce_validator(value):
    p = static('js/kullanici/il-ilce.txt')
    if "i" in value:
        value = value.replace("i","İ")
    value = value.upper()
    #value = value.replace("I","İ")

    print(value)
    #content = p.readlines()
    with open(p[1:],"r",encoding="utf-8") as f:
        data = f.read()

        if value in data:
            return value
        else:
            raise ValidationError("Lütfen Doğru Seçim Yapınız")
def phone_validator(value):
    if value is None or len(value.replace("-","")) != 10 or not value.replace("-","").isnumeric():
        #self.add_error("phone", "Numara Formatı Doğru Değil")
        raise ValidationError("Numara Formatı Doğru Değil")

        raise ValidationError("")
def email_validator(value):
    validate_email(value)



class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150, blank=True,validators=[name_validator])
    last_name = models.CharField(_('last name'), max_length=150, blank=True,validators=[name_validator])
    email = models.EmailField(_('email address'), blank=True,validators=[email_validator])
    password = models.CharField(_('password'), max_length=128,validators=[pass_validator])
    #password2 = models.CharField(_('password again'), max_length=128, validators=[pass_validator])
    adres = models.TextField(max_length=500, blank=False)
    il = models.CharField(max_length=40, blank=False,validators=[il_ilce_validator])
    ilce = models.CharField(max_length=40, blank=False,validators=[il_ilce_validator])
    phone = models.CharField( max_length=12,validators=[phone_validator])
    def save(self, *args, **kwargs):
        print("test")
        super(User, self).save(*args,**kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField()
def add_username(sender,instance,created,**kwargs):
    print(instance,created)
    if created:
        user = User.objects.get(id=instance.id)
        if not user.is_superuser:
            user.username = user.first_name+user.last_name+str(int(time()))
            #profil de oluşturacağız.
            user.save()
            mail_gonder(user, body="Üyelik onayınız için aşağıdaki linke tıklamanız gerekmektedir.")

# def user_check_mail_exists(sender,instance,**kwargs):
#     if instance.id is None:
#         # yani user modeli daha oluşturulmadıysa
#         value = instance.email
#         email = value.lower()
#         if User.objects.filter(email=email).exists():
#             raise ValidationError("Email Sistemde Kayıtlı.")


post_save.connect(add_username,sender=User)
#pre_save.connect(user_check_mail_exists,sender = User)



