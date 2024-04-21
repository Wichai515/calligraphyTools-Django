"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from Apps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('api/get-authors/', views.get_authors, name='get_authors'),
    path('api/get-books/', views.get_books, name='get_books'),
    path('api/get-booksphoto/', views.get_booksphoto, name='get_booksphoto'),
    path('api/get-book-photos/<int:bo_id>/', views.get_book_photos, name='get_book_photos'),
    path('api/get-book-photos/<int:bo_id>/<str:version>/', views.get_book_photos_version, name='get_book_photos_version'),
    path('api/get-search-dictionary/<str:character>/<str:font>/', views.get_search_dictionary, name='get_search_dictionary'),
    # path('api/get-search-dictionary/<str:character>/', views.get_search_dictionary, name='get_search_dictionary'),
    path('api/get-DicCharacter/<int:di_id>/', views.get_DicCharacter, name='get_DicCharacter'),
    
    path('api/get-collections/<str:token>/', views.get_collections, name='get_collections'),
    path('api/get-collection-details/<str:token>/<int:co_id>/', views.get_collection_details, name='get_collection_details'),


    path('api/post-books/', views.post_books, name='post_books'),
    path('api/post-characters/', views.post_characters, name='post_characters'),
    # path('api/post-authors/', views.post_authors, name='post_authors'),
    path('api/post-collections/', views.post_collections, name='post_collections'),

    path('api/post-predict-font-style/', views.post_predict_font_style, name='post_predict_font_style'),
]

