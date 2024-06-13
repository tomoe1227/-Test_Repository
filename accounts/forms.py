from django import forms
from .models import Cat, HealthDiet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    security_question = forms.CharField(required=True)
    security_answer = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "security_question", "security_answer")

class SignUpForm(UserCreationForm):
    security_question = forms.ChoiceField(choices=[
        ('question1', '母親の旧姓'),
        ('question2', '卒業した小学校の名前'),
        ('question3', '自身の出身地')
    ])
    security_answer = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "security_question", "security_answer")

class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['photo', 'name', 'birthday', 'gender', 'personality', 'weight', 'food_amount', 'health_status']
        labels = {
            'photo': '写真',
            'name': '名前',
            'birthday': '誕生日',
            'gender': '性別',
            'personality': '性格',
            'weight': '体重(kg)',
            'food_amount': '食事量(g)',
            'health_status': '健康状態',
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'weight': forms.NumberInput(attrs={'step': "0.01"}),
        }

class HealthDietForm(forms.ModelForm):
    class Meta:
        model = HealthDiet
        fields = ['health_status', 'weight', 'exercise_duration']
        labels = {
            'health_status': '健康状態',
            'weight': '体重(kg)',
            'exercise_duration': '運動時間(分)',
        }