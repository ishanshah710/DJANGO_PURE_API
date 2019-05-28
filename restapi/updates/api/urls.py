from django.urls import path
from updates.api.views import *
from updates.views import *

urlpatterns = [
    # path('',json_example_view), # api/updates

    path('json/cbv/',JsonCBV.as_view()),
    path('json/cbv2/',JsonCBV2.as_view()),

    path('json/serialized/list',SerializedListView.as_view()),
    path('json/serialized/detail',SerializedDetailView.as_view()),

    path('json/serialized/list-manager',SerializedManagerListView.as_view()),
    path('json/serialized/detail-manager',SerializedManagerDetailView.as_view()),
    # for -manager see the tag in views.py in for both these views

    # it will from api\views
    path('',UpdateModelListAPIView.as_view()), # api/updates - list/create
    path('<int:pk>/',UpdateModelDetailAPIView.as_view()),
]
