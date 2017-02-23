from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm

from member.models import MyUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=40, required=False)
    # gender = forms.ChoiceField(choices=MyUser.CHOICES_GENDER)
    # gender = forms.CharField(max_length=1, widget=forms.Select(choices=CHOICES_GENDER))
    # 라디오 버튼으로하기
    gender = forms.ChoiceField(choices=MyUser.CHOICES_GENDER, widget=forms.RadioSelect())

    def clean_username(self):
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError('username already exists!')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        validate_password(password1)
        if password1 != password2:
            raise forms.ValidationError('Password1 and Password2 not equal')
        return password2

    def create_user(self):
        username = self.cleaned_data['username']
        # password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        email = self.cleaned_data['email']
        gender = self.cleaned_data['gender']
        nickname = self.cleaned_data['nickname']

        # if MyUser.objects.filter(username=username).exists():
        #     form.add_error('username', 'username already exists')
        # if password1 != password2:
        #     form.add_error('password1', 'Password1 and Password2 not equal')
        # else:

        user = MyUser.objects.create_user(
            username=username,
            password=password2
        )
        user.email = email
        user.gender = gender
        user.nickname = nickname
        user.save()
        return user


class ProfileImageForm(forms.Form):
    image = forms.ImageField()


class ProfileImageModelForm(ModelForm):
    class Meta:
        model = MyUser
        fields = (
            'img_profile',
        )


class SignUpModelForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'gender',
            'nickname',
        )
