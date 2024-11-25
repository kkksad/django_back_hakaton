from django.urls import path
from .views import RegisterView, LoginView, AddFamilyMemberView, ListFamilyMembersView, DeleteUserView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('add_family_member/', AddFamilyMemberView.as_view(), name='add_family_member'),
    path('list_family_members/', ListFamilyMembersView.as_view(), name='list_family_members'),
    path('delete_family_member/', DeleteUserView.as_view(), name='delete_family_member'),
]


