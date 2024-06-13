from django import forms
from .models import Diary, Task, Schedule
from django.forms import DateTimeInput

# Taskフォーム
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'duration']

# スケジュールフォームにカテゴリの色選択を追加
CATEGORY_COLOR_CHOICES = [
    ('red', '赤'),
    ('blue', '青'),
    ('green', '緑'),
    ('pink', 'ピンク'),  # 追加
    ('yellow', '黄色'),  # 追加
    ('purple', '紫'),  # 追加
    ('black', '黒'),  # 追加
]

class ScheduleForm(forms.ModelForm):
    category_color = forms.ChoiceField(choices=CATEGORY_COLOR_CHOICES, label='カテゴリの色', required=False)

    class Meta:
        model = Schedule
        fields = ['title', 'start_datetime', 'end_datetime', 'category', 'description', 'location', 'category_color']
        labels = {
            'title': 'タイトル',
            'start_datetime': '開始日時',
            'end_datetime': '終了日時',
            'category': 'カテゴリ',
            'description': '説明',
            'location': '場所',
            'category_color': 'カテゴリの色',
        }
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

# 日記フォーム
class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'text', 'photo', 'date']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 40, 'rows': 10}),
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(),
        }