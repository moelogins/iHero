"""ihero URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_app import views as u_views
from tasks import views as t_views
urlpatterns = [
    path('learner/<int:user_id>/', u_views.learner_details, name='learner'),
    path('welcome/', u_views.heroes, name='heroes'),
    path('', u_views.indexView, name='home'),
    path('coach/<int:user_id>/', u_views.coach_details, name='coach'),
    path('admin/', admin.site.urls),
    path('addtask/', t_views.newTaskByLearner),
    path('addtotasks/', t_views.newTaskByCoach),
    path('task/<int:task_id>/', t_views.taskDetailView),
    path('markcomplete/<int:task_id>/', t_views.markTaskComplete),
    path('markincomplete/<int:task_id>/', t_views.markTaskIncomplete),
    path('coaches/', u_views.coachList),
    path('learners/', u_views.learnerList),
    path('signup/', u_views.createUser),
]
