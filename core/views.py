from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from .forms import TaskForm, ScheduleForm, DiaryForm
from .models import Task, Diary, Schedule
from django.db.models import F, Sum
from django.db import models  # ここを追加
from typing import Dict
import json
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import timedelta, localtime
from django.utils.dateparse import parse_datetime
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

class IndexView(TemplateView):
    template_name = 'index.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'core/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_duration = Task.objects.filter(owner=self.request.user).aggregate(
            total_duration=Sum(F('duration'))
        )
        context['total_duration'] = self.convert_duration(total_duration['total_duration'])
        return context

    def convert_duration(self, duration):
        if duration:
            total_seconds = duration.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}時間{int(minutes)}分"
        return "0時間0分"

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'core/task_form.html'
    success_url = reverse_lazy('core:task-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'core/task_form.html'
    success_url = reverse_lazy('core:task-list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'core/task_confirm_delete.html'
    success_url = reverse_lazy('core:task-list')

class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'core/schedule_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedules = Schedule.objects.all()
        context['schedule_data'] = serialize('json', schedules, fields=('title', 'start_datetime', 'end_datetime'))
        return context

class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'core/schedule_form.html'
    success_url = reverse_lazy('core:schedule_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'core/schedule_form.html'
    success_url = reverse_lazy('core:schedule_list')

class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Schedule
    success_url = reverse_lazy('core:schedule_list')

class ScheduleDetailView(LoginRequiredMixin, DetailView):
    model = Schedule
    template_name = 'core/schedule_detail.html'

def schedule_list(request):
    schedules = Schedule.objects.all()
    data = [
        {
            'title': schedule.title,
            'start': schedule.start_datetime.isoformat(),
            'end': schedule.end_datetime.isoformat(),
            'extendedProps': {
                'description': schedule.description,
                'location': schedule.location
            }
        } for schedule in schedules
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.owner = request.user
            schedule.save()
            return JsonResponse({'status': 'success', 'schedule_id': schedule.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)
    return JsonResponse({'status': 'error', 'method': 'GET not allowed'}, status=405)

def add_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'core/schedule_form.html', {'form': form})

@require_http_methods(["DELETE"])
def delete_schedule(request, id):
    try:
        print(f"Received delete request for schedule id: {id}")  # デバッグ用の出力
        schedule = Schedule.objects.get(id=id, owner=request.user)
        schedule.delete()
        print(f"Schedule id {id} deleted successfully.")  # デバッグ用の出力
        return JsonResponse({'status': 'success'})
    except Schedule.DoesNotExist:
        print(f"Schedule id {id} not found.")  # デバッグ用の出力
        return JsonResponse({'status': 'error', 'message': 'Schedule not found'}, status=404)

def events(request):
    events = Schedule.objects.all()
    events_data = [
        {
            'title': event.title,
            'start': event.start_datetime.isoformat(),
            'end': event.end_datetime.isoformat(),
        } for event in events
    ]
    return JsonResponse(events_data, safe=False)

class DiaryListView(LoginRequiredMixin, ListView):
    model = Diary
    context_object_name = 'diaries'
    template_name = 'core/diary_list.html'

    def get_queryset(self):
        return Diary.objects.filter(owner=self.request.user).order_by('-date')

class DiaryCreateView(LoginRequiredMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'core/diary_form.html'
    success_url = reverse_lazy('core:diary-create-complete')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'core/diary_form.html'
    success_url = reverse_lazy('core:diary-list')

class DiaryDetailView(LoginRequiredMixin, DetailView):
    model = Diary
    template_name = 'core/diary_detail.html'

class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    model = Diary
    template_name = 'core/diary_confirm_delete.html'
    success_url = reverse_lazy('core:diary-list')

class DiaryCreateCompleteView(TemplateView):
    template_name = 'core/diary_create_complete.html'

def diary_list_api(request):
    diaries = Diary.objects.filter(owner=request.user)
    data = [
        {
            'title': diary.title,
            'start': localtime(diary.date).date().isoformat(),  # 日付のみに変更
            'description': diary.text,
            'url': reverse('core:diary-detail', args=[diary.id]),
        } for diary in diaries
    ]
    return JsonResponse(data, safe=False)