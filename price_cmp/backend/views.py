import json
import jieba
import datetime

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from backend.crawler import crawler_all
from backend.models import Product, EmailVerification
from backend.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view
import random
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


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


@api_view(['POST'])
def send_verification_code(request):
    email = request.data.get('email')
    print(email)
    if not email:
        return JsonResponse({"success": False, "error": "Email is required"})

    verification_code = random.randint(100000, 999999)
    print(verification_code)

    try:
        verification = EmailVerification.objects.get(email=email)
        verification.verification_code = verification_code
        verification.created_at = timezone.now()
        verification.save()
    except ObjectDoesNotExist:
        verification = EmailVerification.objects.create(
            email=email,
            verification_code=verification_code,
        )

    send_mail(
        '验证码',
        f'您的验证码是：{verification_code}',
        '3011371796@qq.com',
        [email],
        fail_silently=False,
    )

    return JsonResponse({"success": True, "respCode": '400041'}, status=200)


# 验证验证码的接口
@api_view(['POST'])
def verify_verification_code(request):
    email = request.data.get('email')
    verification_code = request.data.get('verification_code')

    if not email or not verification_code:
        return Response({"error": "邮箱和验证码不能为空", "respCode": "400031"})

    try:
        verification = EmailVerification.objects.get(email=email)

        if not verification.is_valid():
            return Response({"error": "验证码已过期", "respCode": "400032"})

        if str(verification.verification_code) != str(verification_code):
            return Response({"error": "验证码不正确", "respCode": "400033"})

        verification.delete()
        return Response({"success": True, "respCode": "000007"}, status=200)
    except ObjectDoesNotExist:
        return Response({"error": "验证码记录不存在", "respCode": "400034"})


@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    response = {}
    try:
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        email = data.get("email", "").strip()

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
            return JsonResponse({'respCode': '999999', 'message': []}, status=500)

        if not products.exists():
            crawler_all(query)
            if query:
                products = Product.objects.filter(query_filter)

        response['list'] = [
            {
                "product_name": product.product_name, "product_url": product.product_url,
                "image": product.image, "cur_price": getattr(product, price_field_name, None),
                "origin": product.origin, "product_id": product.id
            }
            for product in products
        ]
        response['respMsg'] = 'success'
        response['respCode'] = '000003'
    except Exception as e:
        response['respMsg'] = str(e)
        response['respCode'] = '999999'

    return JsonResponse(response)


@require_http_methods(["GET"])
def get_reminder(request):
    username = request.GET.get('username')
    response = {}

    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)

    try:
        user = User.objects.filter(username=username).first()
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    reminder_ids = [
        user.reminder_1,
        user.reminder_2,
        user.reminder_3,
        user.reminder_4,
        user.reminder_5
    ]
    reminder_ids = [id for id in reminder_ids if id != 0]

    if not reminder_ids:
        return JsonResponse({'error': 'No reminders found for this user'}, status=404)

    products = Product.objects.filter(id__in=reminder_ids)

    if not products:
        return JsonResponse({'error': 'No matching products found'}, status=404)

    response['list'] = [
        {
            "product_name": product.product_name, "product_url": product.product_url,
            "image": product.image, "cur_price": getattr(product, price_field_name, None),
            "origin": product.origin, "product_id": product.id
        }
        for product in products
    ]
    response['respMsg'] = 'success'
    response['respCode'] = '000006'

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def add_reminder(request):
    try:
        data = json.loads(request.body)
        product_id = data['product_id']
        username = data.get("username", "").strip()
        user = User.objects.filter(username=username).first()

        if not user:
            return JsonResponse({'respCode': '400001', 'message': '用户不存在'})

        reminders = [user.reminder_1, user.reminder_2, user.reminder_3, user.reminder_4, user.reminder_5]
        for i in range(5):
            if reminders[i] == product_id:
                return JsonResponse({'respCode': '400022', 'message': '该商品已在提醒队列中'})
            if reminders[i] == 0:
                if i == 0:
                    user.reminder_1 = product_id
                elif i == 1:
                    user.reminder_2 = product_id
                elif i == 2:
                    user.reminder_3 = product_id
                elif i == 3:
                    user.reminder_4 = product_id
                elif i == 4:
                    user.reminder_5 = product_id

                user.save()
                return JsonResponse({'respCode': '000004', 'message': 'Reminder added successfully'})
        return JsonResponse({'respCode': '400021', 'message': '没有可以添加的提醒项'})

    except Exception as e:
        return JsonResponse({'respCode': '999999', 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def delete_reminder(request):
    try:
        data = json.loads(request.body)
        product_id = data['product_id']
        username = data.get("username", "").strip()
        user = User.objects.filter(username=username).first()

        if not user:
            return JsonResponse({'respCode': '400001', 'message': '用户不存在'})

        reminders = [user.reminder_1, user.reminder_2, user.reminder_3, user.reminder_4, user.reminder_5]
        updated = False

        for i in range(5):
            if reminders[i] == product_id:
                if i == 0:
                    user.reminder_1 = 0
                elif i == 1:
                    user.reminder_2 = 0
                elif i == 2:
                    user.reminder_3 = 0
                elif i == 3:
                    user.reminder_4 = 0
                elif i == 4:
                    user.reminder_5 = 0

                updated = True

        if updated:
            user.save()
            return JsonResponse({'respCode': '000005', 'message': 'delete reminder success'})

        return JsonResponse({'respCode': '400022', 'message': '没有找到匹配的提醒项'})

    except Exception as e:
        return JsonResponse({'respCode': '999999', 'message': str(e)}, status=500)


@require_http_methods(["GET"])
def detail_info(request):
    product_id = request.GET.get('query')
    if not product_id:
        return JsonResponse({'error': 'Product ID is required'}, status=400)

    try:
        product_id = int(product_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid Product ID'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    return JsonResponse({
        'product_id': product.id,
        'product_name': product.product_name,
        'price_1': product.price_1,
        'price_2': product.price_2,
        'price_3': product.price_3,
        'price_4': product.price_4,
        'price_5': product.price_5,
        'price_6': product.price_6,
        'price_7': product.price_7,
        'price_8': product.price_8,
        'price_9': product.price_9,
        'price_10': product.price_10,
        'price_11': product.price_11,
        'price_12': product.price_12,
        'image': product.image,
        'origin': product.origin
    })
