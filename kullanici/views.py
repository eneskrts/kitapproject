
from .models import User
from django.views.generic import TemplateView,FormView
from .forms import RegisterForm,LoginForm,ProfilUpdateForm
from time import time
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from kitapproje.send_mail import mail_gonder
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from kitapproje.utils import generate_token
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect

# form invalid design
def border_form_input(form):
        for field in form:
            if field.errors:
                form.fields[field.name].widget.attrs["class"]+=" is-invalid"
                #form.fields[field.name].widget.attrs["style"]+="border:10px solid green"
            else:
                form.fields[field.name].widget.attrs["class"]+=" is-valid"
        return form

def KayitView(request):
    form = RegisterForm(data=request.POST or None)
    if request.method == 'POST':
      
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            try:
                user.save()
            except Exception as e:
                messages.success(request,
                              "Bu mail adresi sistemimizde Kayıtlı",
                              extra_tags="danger")
                return render(request, "kullanici/register.html", context={'form': form})


            messages.info(request,"Mail Adresinize Aktivasyon Linki Gönderilmiştir. Üyeliğinizin Tamamlanması İçin Lütfen Onaylayınız",extra_tags="info")
            form = RegisterForm()

        else:

            #print("yok buraya ")
            #print([field.errors for field in form])
            form = border_form_input(form)     

    return render(request,"kullanici/register.html",context={'form':form})



class ActivateView(TemplateView):
    def get(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            #success message
            # home ekranına yönlendirme !!!
            messages.success(request,"Üyelik Aktivasyonu Başarıyla Sağlandı",extra_tags="success")
            return redirect('register')

        return render(request,'kullanici/activate_failed.html',status=401)


def LoginView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        # print("Buraaaa")
        # print(form)
        if form.is_valid():

            #messages.success(request,"Başarıyla Giriş Yaptınız. Anasayfaya Yönlendiriliyorsunuz.")
            mail = request.POST.get("email")
            user = User.objects.get(email=mail)
            if not user.is_active:
                messages.success(request,"Mail adresinizi lütfen aktifleştiirin",extra_tags="info")
                return render(request, "kullanici/login.html", context={'form': form})
            else:
                login(request,user)
                messages.success(request,"Giriş Yaptığınız İçin Teşekkürler %s"%(user.first_name),extra_tags="success")
                return render(request,"kullanici/login.html",context={'form':form})

        messages.success(request, "Kullanıcı Adı veya Parola Hatalı.", extra_tags="danger")
        return render(request, "kullanici/login.html", context={'form': form})
    else:

        form = LoginForm()
        return render(request,"kullanici/login.html",context={'form':form})

def LogoutView(request):
    isim = request.user.first_name
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yapıldı %s"%isim,extra_tags="success")
    return HttpResponseRedirect(reverse('login'))


def password_reset_request(request):
    
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        print("FORM",password_reset_form)
        if password_reset_form.is_valid():
            
            data = password_reset_form.cleaned_data["email"]
            user = None
            try:
                user = User.objects.get(email=data)
            except:
                messages.success(request, "Bu mail adresi sistemimizde kayıtlı değil", extra_tags="danger")

            #print("DATA",data)
            if user:
                mail_gonder(user,body="Şifrenizi aşağıdaki bağlantıdan sıfırlayabilirsiniz.",url_name="password_reset_confirm")
                messages.success(request,"Şifre Sıfırlama Bağlantısı Mail Adresinize Gönderildi.",extra_tags="success")

            return render(request=request, template_name="kullanici/recovery_password_mail.html", context={"password_reset_form":password_reset_form})


    password_reset_form = PasswordResetForm()
           

    return render(request=request, template_name="kullanici/recovery_password_mail.html", context={"password_reset_form":password_reset_form})


def ProfileView(request):
    if request.method == "GET":
        user = User.objects.get(username=request.user.username)
        initial = {'first_name': user.first_name, 'last_name': user.last_name,
                   'email': user.email, 'phone': user.phone}
        form = ProfilUpdateForm(initial=initial,data=request.POST or None, files=request.FILES or None)
        return render(request, "kullanici/profile/profile.html", {'form': form})
    if request.method == "POST":
        print(request.POST)
        form = ProfilUpdateForm(data=request.POST or None, files=request.FILES or None,instance=request.user)
        if form.is_valid():
            user = form.save(commit=True)
            image = form.cleaned_data.get("image")
            print(type(image))
        else:
            form = border_form_input(form)

    return render(request,"kullanici/profile/profile.html",{"form":form})




