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


from .models import Author, Book, Book_Ph
import json
from django.core.exceptions import ObjectDoesNotExist
@api_view(['POST'])
def post_books(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        # 查询作者ID
        author_name = data['author']
        author = Author.objects.get(au_name=author_name)
        author_id = author.au_id

        # 保存书籍信息
        book_data = {
            'bo_name': data['bookName'],
            'au_id': author_id,
            'bo_type': data['type'],
            'bo_dynasty': data['dynasty'],
            'bo_introduce': data['introduction'],
            # 'bo_version': data['version']
        }
        book = Book.objects.create(**book_data)

        # 保存书籍图片信息
        images_data = data.get('images', [])
        cover_url = 'http://192.168.3.52:7791/i/2024/03/17/65f6557ec6bfd.jpg'  # 初始化 cover_url
        for image_data in images_data:
            book_photo_data = {
                'bo_id': book.bo_id,
                'bo_ph_version': data['version'],
                'bo_ph_num': image_data['page'],
                'bo_ph_url': image_data['url'],
            }
            Book_Ph.objects.create(**book_photo_data)
            # 检查页码是否为1，如果是则设为封面
            if image_data['page'] == 1:
                cover_url = image_data['url']

            # 设置封面URL
        if cover_url:
            book.bo_cover_url = cover_url
            book.save()

        return JsonResponse({'message': 'Books created successfully'}, status=201)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': f'Author "{author_name}" not found in database'}, status=400)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(['POST'])
def post_characters(request):
    try:
        data = request.data
        book_name = data.get('book_name')
        dynasty = data.get('dynasty')
        font = data.get('type')
        author_name = data.get('author_name')  # 获取书法家名
        characters = data.get('characters')

        # 根据书名查询对应的 Book 实例
        book_instance = Book.objects.get(bo_name=book_name)

        # 根据作者名查询对应的 Author 实例
        author_instance = Author.objects.get(au_name=author_name)

        for character_data in characters:
            character_sim = character_data.get('character_sim')
            character_com = character_data.get('character_com')
            photo_url = character_data.get('photo_url')
            dictionary_number = character_data.get('dictionary_number')

            # 检查汉字表中是否已存在该字
            cn_character, created = CnCharacter.objects.get_or_create(
                ch_character_sim=character_sim,
                ch_character_com=character_com
            )

            # 创建或获取字典记录
            dictionary, created = Dictionary.objects.get_or_create(
                di_character_sim=character_sim,
                di_character_com=character_com,
                ch=cn_character,  # 使用汉字对象作为外键
                bo=book_instance,  # 使用 Book 实例作为外键
                au=author_instance,  # 使用 Author 实例作为外键
                au_name=author_name,
                bo_name=book_name,
                di_dynasty=dynasty,
                di_type=font,
                di_photo_url=photo_url,
                di_number=dictionary_number
            )

        return Response({'message': 'Characters uploaded successfully!'}, status=201)

    except ObjectDoesNotExist as e:
        return Response({'error': f'Object does not exist: {str(e)}'}, status=400)

    except KeyError as e:
        return Response({'error': f'Missing key: {str(e)}'}, status=400)

    except Exception as e:
        return Response({'error': str(e)}, status=400)

from .models import Collection
@api_view(['POST'])
def post_collections(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            font = data.get('font')
            calligraphers = data.get('calligraphers')
            txt = data.get('txt')
            columns = data.get('columns')
            token = data.get('token')  # 获取 token
        except:
            return Response({'message': '解析数据失败'}, status=400)

        # 根据 token 获取用户的 us_id
        try:
            payload = serializer.loads(token)
            username = payload.get('username')
            user = Usert.objects.get(us_name=username)
            us_id = user.us_id
        except:
            return Response({'message': '获取用户信息失败'}, status=400)

        # 根据文本内容和书法家偏好搜索并保存数据
        choose_di = []
        for index,ch in enumerate(txt, start=1):  # 使用enumerate获取索引，从1开始计数
            dictionary_entry = None
            for calligrapher in calligraphers:
                try:
                    dictionary_entry = Dictionary.objects.filter(
                        di_character_sim=ch,
                        au__au_name=calligrapher,
                        di_type=font
                    ).first()  # 使用first()方法获取第一个匹配的对象
                    if dictionary_entry:
                        break
                except Dictionary.DoesNotExist:
                    pass

            if dictionary_entry:
                choose_di.append({
                    'collect_num': index,  # 使用索引作为字的序号
                    'co_ch': ch,
                    'dictionary_id': dictionary_entry.di_id
                })
            else:
                choose_di.append({
                    'collect_num': index,  # 使用索引作为字的序号
                    'co_ch': ch,
                    'dictionary_id': None
                })

        co_setting = {
            'font': font,
            'calligraphers': calligraphers,
            'columns': columns,
            'choose_di': choose_di
        }

        # 创建集字对象并保存到数据库
        try:
            collection = Collection.objects.create(
                co_title=title,
                us_id=us_id,  # 将获取到的用户ID与集字关联
                co_txt=txt,
                co_setting=co_setting
            )
            return Response({'message': '集字创建成功','co_id': collection.co_id}, status=201)
        except:
            return Response({'message': '集字创建失败'}, status=400)
    else:
        return Response({'message': '请求方法不允许'}, status=405)

from .serializers import CollectionSerializer



@api_view(['GET'])
def get_collections(request, token):
    serializer = URLSafeSerializer('vjXa$,Prd4agk5Z')
    if request.method == 'GET':
        try:
            payload = serializer.loads(token)
            username = payload.get('username')
            user = Usert.objects.get(us_name=username)
            us_id = user.us_id
        except:
            return Response({'message': '获取用户信息失败'}, status=400)

        # 获取用户的所有集字数据
        collections = Collection.objects.filter(us_id=us_id)

        # 使用序列化器序列化数据
        serializer = CollectionSerializer(collections, many=True)

        return Response(serializer.data)
    else:
        return Response({'message': '请求方法不允许'}, status=405)


from .serializers import CollectionDetailSerializer
@api_view(['GET'])
def get_collection_details(request, token, co_id):
    serializer = URLSafeSerializer('vjXa$,Prd4agk5Z')
    if request.method == 'GET':
        try:
            payload = serializer.loads(token)
            username = payload.get('username')
            user = Usert.objects.get(us_name=username)
            us_id = user.us_id
        except:
            return Response({'message': '获取用户信息失败'}, status=400)

        try:
            # 根据 co_id 获取集字详情
            collection = Collection.objects.get(pk=co_id, us_id=us_id)
        except Collection.DoesNotExist:
            return Response({'message': '集字详情不存在'}, status=404)

        # 使用序列化器序列化集字详情，包括 settings
        serializer = CollectionDetailSerializer(collection)

        return Response(serializer.data)
    else:
        return Response({'message': '请求方法不允许'}, status=405)


from django.shortcuts import get_object_or_404
@api_view(['GET'])
def get_DicCharacter(request, di_id):
    try:
        # 根据 di_id 获取对应的字典条目
        dictionary_entry = get_object_or_404(Dictionary, pk=di_id)

        # 使用序列化器序列化数据
        serializer = DictionarySerializer(dictionary_entry)

        return Response(serializer.data)
    except Exception as e:
        # 返回错误响应
        return Response({'error': str(e)}, status=500)


from django.http import JsonResponse
from rest_framework.decorators import api_view
from .util import predict_font  # 导入图像预测函数

@api_view(['POST'])
def post_predict_font_style(request):
    try:
        # 检查请求中是否包含文件
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided'}, status=400)

        # 获取上传的所有文件
        files = request.FILES.getlist('image')

        # 遍历文件列表
        for image_file in files:
            # 获取图像预测结果
            predicted_font = predict_font(image_file)

            # 打印预测结果
            print("Predicted font:", predicted_font)

        # 返回预测结果
        return JsonResponse({'predicted_font': predicted_font})

    except Exception as e:
        # 返回错误响应
        return JsonResponse({'error': str(e)}, status=500)

