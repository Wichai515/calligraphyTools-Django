from django.http import JsonResponse
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt #关闭  Django 默认开启了 CSRF 保护机制
from .models import Usert
from django.db import IntegrityError

@csrf_exempt
def login(request):
    # if request.method == "POST":
    #     return JsonResponse({'code': 200, 'msg': 'success'})
    if request.method == 'POST':
        # print(request)
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Usert.objects.get(us_name=username)
            if check_password(password, user.us_passwd):
            #if password == user.us_passwd:
                # 登录成功
                return JsonResponse({'message': '登录成功'})
            else:
                # 密码错误
                return JsonResponse({'message': '密码错误'}, status=400)
        except Usert.DoesNotExist:
            # 用户不存在
            return JsonResponse({'message': '用户不存在'}, status=400)

    # 如果不是POST请求，返回错误信息
    return JsonResponse({'message': '请求方法不允许'}, status=405)

@csrf_exempt
def register(request):
    # if request.method == "POST":
    #     return JsonResponse({'code': 200, 'msg': 'success'})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        hashed_password = make_password(password)

        try:
            if Usert.objects.filter(us_name=username).exists():
                return JsonResponse({'message': '用户名已存在'}, status=400)

            user = Usert.objects.create(us_name=username, us_passwd=hashed_password)
            user.save()
            return JsonResponse({'message': '注册成功'})
        except IntegrityError as e:
            return JsonResponse({'message': '注册失败，用户名已存在', 'error': str(e), 'username':username}, status=400)
        except Exception as e:
            return JsonResponse({'message': '注册失败', 'error': str(e),'hashed_password':hashed_password}, status=400)

        #test
    return JsonResponse({'message': '请求方法不允许'}, status=405)


from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Author
from .serializers import AuthorSerializer
from rest_framework import status


@api_view(['GET'])
def get_authors(request):
    try:
        # 获取所有的书法家数据
        authors = Author.objects.all()
        # 序列化数据
        serializer = AuthorSerializer(authors, many=True)
        # 返回成功响应
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # 返回错误响应
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from .models import Book
from .serializers import BookSerializer

# import logging
#
# logger = logging.getLogger(__name__)
@api_view(['GET'])
def get_books(request):
    try:
        # 获取所有的书籍数据
        books = Book.objects.all()
        # logger.info("Books retrieved successfully: %s", books)
        # 序列化数据
        serializer = BookSerializer(books, many=True)
        # 返回成功响应
        return Response({'message': 'Books retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # 返回错误响应
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from .models import Book_Ph
from .serializers import BookPhSerializer

@api_view(['GET'])
def get_booksphoto(request):
    try:
        # 获取所有的书籍照片数据
        book_photos = Book_Ph.objects.all()
        # 序列化数据
        serializer = BookPhSerializer(book_photos, many=True)
        # 返回成功响应
        return Response({'message': 'Book photos retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # 返回错误响应
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 通过书籍 ID 获取书籍版本+照片
from rest_framework.renderers import JSONRenderer
@api_view(['GET'])
def get_book_photos(request, bo_id):
    try:
        # 获取指定 bo_id 和 bo_ph_num=1 的数据
        book_photos = Book_Ph.objects.filter(bo_id=bo_id, bo_ph_num=1)
        # 序列化数据
        serializer = BookPhSerializer(book_photos, many=True)
        # 返回成功响应
        return Response({'message': 'Book version photos retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # 返回错误响应
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_book_photos_version(request, bo_id, version):
    try:
        # 获取指定 bo_id和版本的数据
        book_photos = Book_Ph.objects.filter(bo_id=bo_id, bo_ph_version=version)
        # 序列化数据
        serializer = BookPhSerializer(book_photos, many=True)
        # 返回成功响应
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # 返回错误响应
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

