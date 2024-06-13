from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings

class Task(models.Model):
    title = models.CharField('タイトル', max_length=200)
    description = models.TextField('内容')
    completed = models.BooleanField('完了', default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.DurationField('時間', null=True, blank=True)

class Diary(models.Model):
    title = models.CharField('タイトル', max_length=200)
    text = models.TextField('本文')
    date = models.DateTimeField('日付', default=timezone.now)
    photo = models.ImageField(upload_to='diary_photos/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class Schedule(models.Model):
    title = models.CharField(max_length=200)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # 場所フィールド追加
    category_color = models.CharField(max_length=7, default='#FFFFFF')  # カテゴリ色フィールド追加
    reminder = models.BooleanField(default=False)  # リマインダーフィールド追加
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='schedules')
    
    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)