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

        # try:
        #     if Usert.objects.filter(us_name=username).exists():
        #         return JsonResponse({'message': '用户名已存在'}, status=400)
        #
        #     user = Usert.objects.create(us_name=username, us_passwd=hashed_password)
        #     user.save()
        #     return JsonResponse({'message': '注册成功'})
        # except IntegrityError as e:
        #     return JsonResponse({'message': '注册失败，用户名已存在'}, status=400)
        # except Exception as e:
        #     return JsonResponse({'message': '注册失败', 'username':username, 'password':password, 'hashed_password':hashed_password}, status=400)

    return JsonResponse({'message': '请求方法不允许'}, status=405)
