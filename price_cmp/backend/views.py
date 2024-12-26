import json
import jieba
import datetime
from crawler import crawler_all

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from backend.models import Product
from backend.models import User


current_date = datetime.datetime.now()
current_month = current_date.month
price_field_name = f"price_{current_month}"


@csrf_exempt
@require_http_methods(["POST"])
def authenticate_user(request):
    response = {}
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        # 前端完成
        # if not username or not password:
        #     response['respMsg'] = '用户名或密码不能为空'
        #     response['respCode'] = '400001'
        #     return JsonResponse(response)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            response['respMsg'] = 'no certain user'
            response['respCode'] = '400002'
            return JsonResponse(response)

        if user.password == password:
            response['respMsg'] = 'login success'
            response['respCode'] = '000000'
        else:
            response['respMsg'] = 'wrong password'
            response['respCode'] = '400003'

    except Exception as e:
        response['respMsg'] = str(e)
        response['respCode'] = '999999'

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    response = {}
    try:
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        email = data.get("email", "").strip()

        # 在前端完成检查
        # if not username or not password or not email:
        #     response['respMsg'] = '用户名、密码和邮箱不能为空'
        #     response['respCode'] = '400001'
        #     return JsonResponse(response)

        if User.objects.filter(username=username).exists():
            response['respMsg'] = 'username exists'
            response['respCode'] = '400011'
            return JsonResponse(response)

        # 检查邮箱是否已存在
        if User.objects.filter(email=email).exists():
            response['respMsg'] = 'email has been registered'
            response['respCode'] = '400012'
            return JsonResponse(response)

        # 创建新用户
        user = User(username=username, password=password, email=email)
        user.save()

        # 返回成功响应
        response['respMsg'] = 'register success'
        response['respCode'] = '000002'
        return JsonResponse(response)

    except Exception as e:
        response['respMsg'] = f"注册失败: {str(e)}"
        response['respCode'] = '999999'
        return JsonResponse(response)


@require_http_methods(["GET"])
def get_products(request):
    response = {}
    try:
        query = request.GET.get('query', '').strip()

        if query:
            keywords = list(jieba.cut_for_search(query))
            query_filter = Q()
            for keyword in keywords:
                query_filter |= Q(product_name__icontains=keyword)

            products = Product.objects.filter(query_filter)
        else:
            products = Product.objects.all()

        if not products.exists():
            crawler_all(query)
            products = Product.objects.filter(query_filter) if query else Product.objects.all()

        response['list'] = [
            {
                "product_name": product.product_name, "product_url": product.product_url,
                "image": product.image, "cur_price": getattr(product, price_field_name, None)
            }
            for product in products
        ]
        response['respMsg'] = 'success'
        response['respCode'] = '000003'
    except Exception as e:
        response['respMsg'] = str(e)
        response['respCode'] = '999999'

    return JsonResponse(response)
