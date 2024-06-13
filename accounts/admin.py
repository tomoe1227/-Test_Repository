from django.contrib import admin
from .models import HealthDiet

@admin.register(HealthDiet)
class HealthDietAdmin(admin.ModelAdmin):
    list_display = ('user', 'cat', 'health_status', 'weight', 'exercise_duration', 'created_at')