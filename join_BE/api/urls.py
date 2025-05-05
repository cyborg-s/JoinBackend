from django.urls import path
from .views import task_view, task_single_view, contact_view, contact_single_view, update_or_delete_subtask, RegistrationView, UserProfileList, UserProfileDetail, CustomLoginView, CheckTokenView
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('tasks/', task_view),
    path('tasks/<int:pk>/', task_single_view),
    path('contacts/', contact_view),
    path('contacts/<int:pk>/', contact_single_view),
    path('subtasks/<int:pk>/', update_or_delete_subtask),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('users/', UserProfileList.as_view(), name='userProfiles'),
    path('users/<int:pk>/', UserProfileDetail.as_view(), name='userProfile'),
    path('api-token-auth/', CustomLoginView.as_view(), name='api_token_auth'),
    path('check-token/', CheckTokenView.as_view(), name='check-token')
]