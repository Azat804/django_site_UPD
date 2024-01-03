from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class AddReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mark'].choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 200:
            raise ValidationError('Длина превышает 200 символов')
 
        return comment
     

    class Meta:
        model=Review
        fields=['comment','mark']
        #hidden_fields=['user_name','film']
        widgets={'comment':forms.Textarea(attrs={'cols': 60, 'rows': 10,'class':'form-input','placeholder':'Напишите свой отзыв'}),'mark':forms.RadioSelect(attrs={'class':'form-radio'})}
        #comment = forms.CharField(label='Рецензия', help_text='Напишите свой отзыв',max_length=1000, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
        #mark = forms.ChoiceField(label='Оценка',help_text='Поставьте оценку',choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], initial=('5','5') ,widget=forms.RadioSelect)
        #help_texts={'comment':('hjhj'),}

class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    first_name=forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class':'form-input'}))
    last_name=forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class':'form-input'}), required=False)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class':'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-input'}))
    captcha = CaptchaField(label='')
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'password1', 'password2']

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))
    


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class':'form-input'}), max_length=255)
    surname = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class':'form-input'}), max_length=255)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-input'}))
    content = forms.CharField(label='Content',widget=forms.Textarea(attrs={'cols': 40, 'rows': 10, 'class':'form-input','placeholder':'Напишите свою проблему'}))
    captcha = CaptchaField(label='')

    