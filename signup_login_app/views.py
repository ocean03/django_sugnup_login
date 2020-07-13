from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect

from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from signup_login_app.tokens import account_activation_token

from .forms import RegisterForm

UserModel = get_user_model()


def home_view(request):
    return render(request, 'home.html')


def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = RegisterForm()

    return render(request, 'signup.html', {'form': form})


def activation_sent_view(request):
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')


def LoginView(request):
    if request.method == 'POST':

        # AuthenticationForm_can_also_be_used__

        usermail = request.POST['email']
        password = request.POST['pwd']
        print(usermail, password)
        user = authenticate(request, email=usermail, password=password)
        if user is not None:
            form = login(request, user)
            return redirect('home')

    # form = LoginForm()
    return render(request, 'login.html')


def LogoutView(request):
    logout(request)
    return redirect("home")
