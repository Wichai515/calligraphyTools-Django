from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['au_id', 'au_name', 'au_dynasty', 'au_photo_url', 'au_about']