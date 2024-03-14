from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['au_id', 'au_name', 'au_dynasty', 'au_photo_url', 'au_about']

from .models import Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        
        fields = ['bo_id', 'bo_name',  'bo_author_photo', 'bo_type', 'bo_dynasty', 'bo_cover_url', 'bo_introduce', 'bo_created_at', 'bo_txt']


from .models import Book_Ph
class BookPhSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book_Ph
        fields = ['bo_ph_id', 'bo_id', 'bo_ph_version', 'bo_ph_num', 'bo_ph_url', 'bo_ph_url_bu', 'bo_ph_created_at']


