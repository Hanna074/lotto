from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='이메일',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일 주소'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': '아이디'})
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': '비밀번호'})
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': '비밀번호 확인'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
