from django.urls import path, include
from . import views
from .views import IndexView, TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, schedule_list, ScheduleListView, ScheduleCreateView, ScheduleUpdateView, ScheduleDeleteView, ScheduleDetailView, DiaryListView, DiaryCreateView, DiaryUpdateView, DiaryDetailView, DiaryDeleteView, create_schedule, add_schedule, events, DiaryCreateCompleteView, diary_list_api

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('index/', IndexView.as_view(), name='index'),
    path('task-list/', TaskListView.as_view(), name='task-list'),
    path('tasks/add/', TaskCreateView.as_view(), name='task-add'),
    path('tasks/edit/<int:pk>/', TaskUpdateView.as_view(), name='task-edit'),
    path('tasks/delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('schedules/', ScheduleListView.as_view(), name='schedule_list'),
    path('schedules/add/', ScheduleCreateView.as_view(), name='schedule_add'),
    path('schedules/<int:pk>/edit/', ScheduleUpdateView.as_view(), name='schedule-edit'),
    path('schedules/add/', add_schedule, name='add_schedule'),
    path('schedules/<int:pk>/delete/', ScheduleDeleteView.as_view(), name='schedule-delete'),
    path('schedules/<int:pk>/detail/', ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedule/create/', create_schedule, name='create_schedule'),
    path('api/schedules/', schedule_list, name='api_schedules'),
    path('api/delete_schedule/<int:id>/', views.delete_schedule, name='delete_schedule'),
    path('events/', events, name='events'),
    path('diary-list/', DiaryListView.as_view(), name='diary-list'),
    path('diary-list/api/', diary_list_api, name='diary-list-api'),
    path('diary/add/', DiaryCreateView.as_view(), name='diary-add'),
    path('diary/edit/<int:pk>/', DiaryUpdateView.as_view(), name='diary-edit'),
    path('diary/delete/<int:pk>/', DiaryDeleteView.as_view(), name='diary-delete'),
    path('diary/<int:pk>/', DiaryDetailView.as_view(), name='diary-detail'),
    path('diary/add/complete/', DiaryCreateCompleteView.as_view(), name='diary-create-complete'),
    path('api/diaries/', diary_list_api, name='api_diaries'),
]