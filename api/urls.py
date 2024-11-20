from django.urls import path
from accounts.views import *
from home.views import *

urlpatterns = [
    path('register/',RegisterApiView.as_view()),
    path('login/',LoginApi.as_view()),
    path('blog/',BlogApiview.as_view()),
    path('public/',PublicBlog.as_view())
    
    
]
