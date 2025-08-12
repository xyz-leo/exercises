from django.urls import path
from contact import views

# Namespacing the app
app_name = 'contact'

urlpatterns = [
    # Home and Search
    path('', views.home, name='home'),  # Home page
    path('search/', views.search, name='search'),  # Search contacts

    # Contact CRUD
    path('contacts/', views.contacts, name='contacts'),  # List of all contacts
    path('contact/<int:contact_id>/details/', views.single_contact, name='details'),  # Contact details
    path('contact/create/', views.create, name='create'),  # Create new contact
    path('contact/<int:contact_id>/update/', views.update, name='update'),  # Update existing contact
    path('contact/<int:contact_id>/delete/', views.delete, name='delete'),  # Delete contact

    # User management
    path('user/', views.user_view, name='user_view'),  # User dashboard/profile page
    path('user/register/', views.register, name='register'),  # User registration
    path('user/login/', views.login_view, name='login_view'),  # User login
    path('user/logout/', views.logout_view, name='logout_view'),  # User logout
    path('user/update/', views.user_update, name='user_update'),  # Update user profile

    # Categories
    path('categories/', views.category_list, name='category_list'),  # List all categories
    path('categories/<int:category_id>/contacts/', views.contacts_by_category, name='contacts_by_category'),  # Contacts by category
    path('categories/create', views.category_create, name='category_create'),  # Create new category
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),  # Category detail
    path('categories/<int:category_id>/edit', views.category_update, name='category_update'),  # Edit category
    path('categories/<int:category_id>/delete', views.category_delete, name='category_delete'),  # Delete category
]

