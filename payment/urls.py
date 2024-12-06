from django.urls import path

from payment.views import cryptocloud

urlpatterns = [
    path('cryptocloud/endpoint', cryptocloud.Postback.as_view()),    

]
