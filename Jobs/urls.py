
from django.urls import path
from .views import JobView,JobCategoryViews


urlpatterns = [
    path('',JobView.as_view()),
    path('<uuid:job_id>',JobView.as_view()),
    path('job_category',JobCategoryViews.as_view()), 
]
