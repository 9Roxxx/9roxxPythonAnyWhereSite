from .models import Course, Lesson
from django.views.generic import ListView, DetailView
from django.shortcuts import render

from cloudipsp import Api, Checkout
import time
import json

secret_key = "ZuTPVQv2oWnjsheUIeoRhZ1AQIIth8hd"


class HomePage(ListView):
    model = Course
    template_name = 'courses/home.html'
    context_object_name = 'courses'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(HomePage, self).get_context_data(**kwargs)
        ctx['title'] = 'Главная страница сайта'
        return ctx


def callback_payment(request):
    if request.method == 'POST':
        data = json.load(request.POST)

        print(data)



def tarrifsPage(request):
    api = Api(merchant_id=1433491,
              secret_key=secret_key)
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": 150000,
        "order_desc": "Покупка подписки на сайте",
        "order_id": str(time.time()),
        'merchant_data': 'example@itproger.com'
    }
    url = checkout.url(data).get('checkout_url')

    return render(request, 'courses/tarrifs.html', {'title': 'Тарифы на сайте', 'url': url})


class CourseDetailPage(DetailView):
    model = Course
    template_name = 'courses/course-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CourseDetailPage, self).get_context_data(**kwargs)
        ctx['title'] = Course.objects.filter(slug=self.kwargs['slug']).first()
        ctx['lessons'] = Lesson.objects.filter(course=ctx['title']).order_by('number')
        # print(ctx['lessons'].query)
        return ctx


class LessonDetailPage(DetailView):
    model = Course
    template_name = 'courses/lessons-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(LessonDetailPage, self).get_context_data(**kwargs)

        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        lesson = list(Lesson.objects.filter(course=course).filter(slug=self.kwargs['lesson_slug']).values())

        ctx['title'] = lesson[0]['title']
        ctx['desc'] = lesson[0]['description']
        ctx['video'] = lesson[0]['video_url'].split("=")[1]
        return ctx