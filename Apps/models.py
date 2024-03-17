from django.db import models


class Usert(models.Model):
    us_id = models.AutoField(primary_key=True)
    us_po = models.CharField(max_length=10, default='user')
    us_name = models.CharField(max_length=100, unique=True)
    us_email = models.EmailField(unique=False, blank=True, null=True)
    us_telephone = models.CharField(max_length=11, unique=True, blank=True, null=True)
    us_passwd = models.CharField(max_length=128)

    # 如果需要显示用户头像，请添加以下字段
    # us_headphoto = models.ImageField(upload_to='user_photos/', null=True, blank=True)

    class Meta:
        db_table = 'User'

class Author(models.Model):
    au_id = models.AutoField(primary_key=True)
    au_name = models.CharField(max_length=255)
    au_dynasty = models.CharField(max_length=50)
    au_photo_url = models.CharField(max_length=255, default=None, blank=True, null=True)
    au_about = models.TextField(default=None, blank=True, null=True)

    class Meta:
        db_table = 'Author'

class Book(models.Model):
    bo_id = models.AutoField(primary_key=True)
    bo_name = models.CharField(max_length=255)
    au = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, related_name='books', db_column='au_id')
    bo_author_photo = models.CharField(max_length=255, default=None, blank=True, null=True)
    bo_type = models.CharField(max_length=50)
    bo_dynasty = models.CharField(max_length=50)
    bo_cover_url = models.CharField(max_length=255, default=None, blank=True, null=True)
    bo_introduce = models.TextField(default=None, blank=True, null=True)
    bo_created_at = models.DateTimeField(auto_now_add=True)
    bo_txt = models.TextField(default=None, blank=True, null=True)

    class Meta:
        db_table = 'Book'

class Book_Ph(models.Model):
    bo_ph_id = models.BigAutoField(primary_key=True)
    bo = models.ForeignKey(Book, on_delete=models.CASCADE, default=None, related_name='bookphoto', db_column='bo_id')
    bo_ph_version = models.CharField(max_length=100)
    bo_ph_num = models.IntegerField()
    bo_ph_url = models.CharField(max_length=255)
    bo_ph_url_bu = models.CharField(max_length=255, default=None, blank=True, null=True)
    bo_ph_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Book_Ph'


class CnCharacter(models.Model):
    ch_id = models.BigAutoField(primary_key=True)
    ch_character_sim = models.CharField(max_length=1)
    ch_character_com = models.CharField(max_length=1)
    ch_explain = models.CharField(max_length=255, default=None, null=True)

    class Meta:
        db_table = 'CnCharacter'

class Dictionary(models.Model):
    di_id = models.BigAutoField(primary_key=True)
    di_character_sim = models.CharField(max_length=1)
    di_character_com = models.CharField(max_length=1)
    ch = models.ForeignKey(CnCharacter, on_delete=models.CASCADE, default=None, db_column='ch_id', related_name='cn_character')
    au = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, db_column='au_id', related_name='author')
    bo = models.ForeignKey(Book, on_delete=models.CASCADE, default=None, db_column='bo_id', related_name='book')
    au_name = models.CharField(max_length=255)
    bo_name = models.CharField(max_length=255)
    di_dynasty = models.CharField(max_length=100)
    di_type = models.CharField(max_length=100)
    di_photo_url = models.CharField(max_length=255)
    di_number = models.IntegerField()
    di_ph_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Dictionary'

class Collection(models.Model):
    co_id = models.AutoField(primary_key=True)
    co_title = models.CharField(max_length=255)
    us = models.ForeignKey(Usert, on_delete=models.CASCADE, default=None, db_column='us_id', related_name='collections')
    co_txt = models.TextField()
    co_setting = models.JSONField(default=None, null=True)
    co_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Collection'
