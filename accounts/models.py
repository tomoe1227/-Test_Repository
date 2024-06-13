from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class SecurityQuestion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

class Cat(models.Model):
    GENDER_CHOICES = (
        ('male', 'オス'),
        ('female', 'メス'),
    )
    photo = models.ImageField(upload_to='cat_photos/', null=True, blank=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    personality = models.TextField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    food_amount = models.IntegerField(null=True, blank=True)
    health_status = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_age(self):
        today = date.today()
        if self.birthday:
            age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            months = today.month - self.birthday.month - (today.day < self.birthday.day)
            if months < 0:
                months += 12
            return f"{age}歳{months}ヶ月"
        else:
            return "不明"

class HealthDiet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    health_status = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    exercise_duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cat.name}の健康管理"