from django.http import JsonResponse
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt #关闭  Django 默认开启了 CSRF 保护机制
from .models import Usert
from django.db import IntegrityError
from itsdangerous import URLSafeSerializer
# 创建一个安全序列化器
serializer = URLSafeSerializer('vjXa$,Prd4agk5Z')

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
                token = serializer.dumps({'username': username})
                return JsonResponse({'message': '登录成功', 'token': token})
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
        return Response({'message': 'Book version retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
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
        return Response({'message': 'Book version photos retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # 返回错误响应
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from .serializers import DictionarySerializer, CnCharacterSerializer
from .models import Dictionary, CnCharacter

# @csrf_exempt
@api_view(['GET'])
def get_search_dictionary(request, character, font):
    try:
        # 查询 Dictionary 表中与 character 和 font 相关的数据
        queryset = Dictionary.objects.filter(di_character_sim=character, di_type=font)
        # 序列化查询结果
        serializer = DictionarySerializer(queryset, many=True)

        # 获取所有匹配的 CnCharacter 记录的 ch_id
        ch_ids = queryset.values_list('ch_id', flat=True)
        # 查询对应的 CnCharacter 表中的数据
        cn_character_queryset = CnCharacter.objects.filter(ch_id__in=ch_ids)
        # 序列化 CnCharacter 数据
        cn_character_serializer = CnCharacterSerializer(cn_character_queryset, many=True)

        # 将 CnCharacter 的数据合并到 Dictionary 的数据中
        for item in serializer.data:
            ch_id = item['ch']
            # 找到对应的 CnCharacter 数据并添加到字典中
            cn_character_data = next((ch for ch in cn_character_serializer.data if ch['ch_id'] == ch_id), None)
            if cn_character_data:
                item['ch'] = cn_character_data

        return Response({'message': 'Dictionary photos retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        # 返回错误响应
        error_response_data = {'error': str(e)}
        return Response(error_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


