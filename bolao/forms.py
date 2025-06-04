from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import AccessToken

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    access_token = forms.CharField(
        required=True,
        help_text="Digite o token de acesso fornecido para participar do bolão."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "access_token")

    def clean_access_token(self):
        token = self.cleaned_data.get('access_token')
        try:
            access_token = AccessToken.objects.get(token=token)
            if not access_token.is_valid():
                raise ValidationError("Este token de acesso é inválido ou expirou.")
            return token
        except AccessToken.DoesNotExist:
            raise ValidationError("Token de acesso inválido.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
            # Use the access token
            token = AccessToken.objects.get(token=self.cleaned_data['access_token'])
            token.use()
            
        return user

class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='Nome de usuário ou E-mail',
        widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário ou E-mail'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'})
    )

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            # Tenta autenticar com username
            user = authenticate(username=username_or_email, password=password)
            
            # Se não funcionou com username, tenta com email
            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if not user:
                raise ValidationError('Nome de usuário/E-mail ou senha inválidos.')
            
            self.user_cache = user
        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None) 