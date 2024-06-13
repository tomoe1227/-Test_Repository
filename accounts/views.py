from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SecurityQuestion, Cat, HealthDiet
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, CatForm, HealthDietForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('index')

class CustomSignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        self.object = form.save()
        user_email = form.cleaned_data.get('email')
        if user_email:
            send_mail(
                '登録完了のお知らせ',
                'ご登録ありがとうございます。アカウントが正常に作成されました。引き続きサービスをお楽しみください。',
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                fail_silently=False,
            )
        SecurityQuestion.objects.create(
            user=self.object,
            question=form.cleaned_data.get('security_question'),
            answer=form.cleaned_data.get('security_answer'),
        )
        return super().form_valid(form)

class CatCreateView(LoginRequiredMixin, CreateView):
    model = Cat
    form_class = CatForm
    template_name = 'accounts/cat_form.html'
    success_url = '/accounts/cat_management/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CatUpdateView(UpdateView):
    model = Cat
    form_class = CatForm
    success_url = reverse_lazy('accounts:cat_management')
    template_name = 'accounts/cat_form.html'

class CatManagementView(ListView):
    model = Cat
    template_name = 'accounts/cat_management.html'
    context_object_name = 'cats'

class HealthDietListView(LoginRequiredMixin, ListView):
    model = HealthDiet
    template_name = 'accounts/healthdiet_list.html'
    context_object_name = 'healthdiets'

    def get_queryset(self):
        return HealthDiet.objects.filter(user=self.request.user)

class HealthDietCreateView(LoginRequiredMixin, CreateView):
    model = HealthDiet
    form_class = HealthDietForm
    template_name = 'accounts/healthdiet_form.html'
    success_url = reverse_lazy('accounts:healthdiet_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HealthDietUpdateView(LoginRequiredMixin, UpdateView):
    model = HealthDiet
    form_class = HealthDietForm
    template_name = 'accounts/healthdiet_form.html'
    success_url = reverse_lazy('accounts:healthdiet_list')

class HealthDietDeleteView(LoginRequiredMixin, DeleteView):
    model = HealthDiet
    template_name = 'accounts/healthdiet_confirm_delete.html'
    success_url = reverse_lazy('accounts:healthdiet_list')