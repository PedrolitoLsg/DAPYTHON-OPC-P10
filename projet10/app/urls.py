from django.conf.urls import include
from django.urls import path
from .views import (
    ProjectsView,
    ContributorsView,
    CommentsView,
    IssuesView,
    HomeView,
    UserRegistrationView,
    ContributorsDeletionView,
    SoloCommentView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('signup/', UserRegistrationView.as_view({'post': 'create'})),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('projects/', HomeView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:project_id>/', ProjectsView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('projects/<int:project_id>/users/', ContributorsView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:project_id>/users/<int:user_id>/', ContributorsDeletionView.as_view({'delete': 'destroy'})),
    path('projects/<int:project_id>/issues/', IssuesView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:project_id>/issues/<int:issue_id>/', IssuesView.as_view({'put': 'update', 'delete':'destroy'})),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', CommentsView.as_view({'post': 'create', 'get': 'list'})),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/', SoloCommentView.as_view({'get': 'retrieve', 'delete': 'destroy', "put": "update"}))
]
