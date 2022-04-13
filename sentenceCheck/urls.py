from django.urls import path
from . import views

urlpatterns= [
    path('', views.topic, name='topic'),
    path('tsubques/', views.retireveSubTopicTemp, name='tsubquestemp'),
    path('questions/(<topic_name>)/',views.questionDetails,name='questions'),
    path('results/',views.verify,name='results')
]