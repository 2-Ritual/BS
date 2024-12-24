import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

from .api.Mail import mail
from .models import User
from .models import Tag
from .models import Car
from .models import Mask
from .models import MailVerify
from elasticsearch_dsl import connections
from .search import CarIndex
from .api.Crawler import Crawler
from .api.AI import AI
from elasticsearch import Elasticsearch
import schedule
import time

import threading


# Create your views here.

# 以下是使用示例
es = Elasticsearch(
    ["http://localhost:9200"], basic_auth=("elastic", "pdBKdW6xseraou6kNMNq")
)

# # 指定要删除的索引名称
# index_name = "car"
# # 删除索引
# if es.indices.exists(index=index_name):
#     es.indices.delete(index=index_name)
#     print(f"索引 '{index_name}' 已成功删除。")
# else:
#     print(f"索引 '{index_name}' 不存在。")

# if es.ping():
#     # 创建Car实例
#     tags = [
#         Tag.objects.filter(name="红色").first().tid,
#         Tag.objects.filter(name="橙色").first().tid,
#     ]
#     car = Car.objects.create(
#         name="测试用车",
#         description="测试用车",
#         url="https://www.baidu.com",
#         image="https://www.baidu.com/img/flexible/logo/pc/result.png",
#         year=2024,
#         brand="测试牌子",
#         model="测试车型",
#         price=100000.0,
#     )
#     car.tags.set(tags)
#     car.save()
#     tag_ids = [1, 2]
#     actions = []
#     for i in range(100):
#         action = {
#             "_index": "car",  # 指定索引名称
#             "_id": car.cid + i,  # 指定唯一标识
#             "_source": {
#                 "cid": car.cid + i,
#                 "name": car.name + str(i),
#                 "description": car.description + str(i),
#                 "year": car.year + i,
#                 "brand": car.brand + str(i),
#                 "model": car.model + str(i),
#                 "price": car.price + i,
#                 "url": car.url + str(i),
#                 "image": car.image + str(i),
#                 "tags": [
#                     tag.name + str(i) for tag in car.tags.filter(tid__in=tag_ids)
#                 ],  # 提取标签名称列表
#             },
#         }
#         actions.append(action)

#     # 批量插入数据
#     car_index = bulk(es, actions)
#     print(f"成功插入 {car_index} 条数据")
#     print(car_index)
#     result = es.search(
#         index="car",
#         body={"query": {"match": {"name": "测试用车"}}},
#     )
#     print(result)
#     print("Elasticsearch is connected")
# else:
#     print("Elasticsearch is not connected")

# 建立索引
CarIndex.init()


# 定时执行爬虫更新
def update_car_info_in_time():
    schedule.every().day.at("02:00").do(Crawler.update)
    while True:
        schedule.run_pending()
        time.sleep(1)


# Crawler.update(70900, 71000)

# Tag.create_tags(
#     [
#         "5万以下",
#         "5-8万",
#         "8-10万",
#         "10-15万",
#         "15-20万",
#         "20-25万",
#         "25-35万",
#         "35-50万",
#         "50-100万",
#         "100万以上",
#         "微型车",
#         "小型车",
#         "紧凑型车",
#         "中型车",
#         "中大型车",
#         "大型车",
#         "小型SUV",
#         "紧凑型SUV",
#         "中型SUV",
#         "中大型SUV",
#         "大型SUV",
#         "紧凑型MPV",
#         "中型MPV",
#         "中大型MPV",
#         "大型MPV",
#         "跑车",
#         "微面",
#         "微卡",
#         "轻客",
#         "皮卡",
#         "中国",
#         "德国",
#         "捷克",
#         "法国",
#         "英国",
#         "瑞典",
#         "意大利",
#         "日本",
#         "韩国",
#         "美国",
#         "两厢",
#         "三厢",
#         "旅行车",
#         "跨界车",
#         "掀背",
#         "硬顶敞篷车",
#         "软顶敞篷车",
#         "硬顶跑车",
#         "客车",
#         "货车",
#         "1.0L及以下",
#         "1.1-1.6L",
#         "1.7-2.0L",
#         "2.1-2.5L",
#         "2.6-3.0L",
#         "3.1-4.0L",
#         "4.0L以上",
#         "2座",
#         "4座",
#         "5座",
#         "6座",
#         "7座",
#         "7座以上",
#         "自然吸气",
#         "涡轮增压",
#         "机械增压",
#         "汽油",
#         "柴油",
#         "油电混合",
#         "天然气",
#         "汽油电驱",
#         "甲醇",
#         "纯电动",
#         "插电式混合动力",
#         "增程式",
#         "氢燃料",
#         "汽油+48V轻混系统",
#         "汽油+24V轻混系统",
#         "前驱",
#         "后驱",
#         "四驱",
#         "手动",
#         "全部自动",
#         "手自一体",
#         "无级变速",
#         "湿式双离合",
#         "干式双离合",
#         "国产",
#         "进口",
#         "全景天窗",
#         "电动天窗",
#         "电动调节座椅",
#         "车身ESP",
#         "氙气大灯",
#         "GPS导航",
#         "定速巡航",
#         "真皮座椅",
#         "倒车雷达",
#         "全自动空调",
#         "多功能方向盘",
#         "LED大灯",
#         "倒车影像",
#         "无钥匙启动",
#         "座椅加热",
#         "日间行车灯",
#         "自动泊车",
#         "蓝牙/车载电话",
#     ]
# )
# tags = Tag.objects.all()
# tags_ai = ["好看", "精致", "奢华", "快", "宽敞"]
# res = AI.analyseTags(tags_ai)
# scores = {name: 0 for name in tags.values_list("name", flat=True)}
# # for tag in tags_choosed:
# #     scores[tag] += 3
# #     for tag_ai in tags_ai:
# #         tags_relevent = res.get(tag_ai, [])
# #         if tag in tags_relevent:
# #             for each_tag in tags_relevent:
# #                 scores[each_tag] += 1
# for tag_ai in tags_ai:
#     tags_relevent = res.get(tag_ai, [])
#     for each_tag in tags_relevent:
#         scores[each_tag] += 2
# res = sorted(scores.items(), key=lambda x: x[1], reverse=True)

# print(res)


class RegisterView(APIView):
    @transaction.atomic  # 开启事务
    def get(self, request):
        req = request.query_params.dict()  # 前端给的json包数据
        print(req)
        account = req["account"]  # 提取前端传来的账号
        password = req["password"]  # 提取前端传来的密码
        email = req["email"]  # 提取前端传来的邮箱
        name = req["name"]  # 提取前端传来的姓名
        masks = ""
        if User.objects.filter(account=account).first():  # 判断账号是否存在
            res_error = {"msg": "账号已存在"}
            return Response(res_error, 400)  # 返回错误信息
        if User.objects.filter(email=email).first():  # 判断邮箱是否存在
            res_error = {"msg": "邮箱已存在"}
            return Response(res_error, 400)  # 返回错误信息
        user = User.objects.create(
            account=account, password=password, email=email, name=name, mid=masks
        )  # 创建数据
        return Response(
            200
        )  # 返回数据，这里由于提取数据表中数据直接就是jason格式所以可以直接传，其他的需要转为json格式


class LoginView(APIView):
    @transaction.atomic
    def get(self, request):
        req = request.query_params.dict()
        account = req["account"]
        password = req["password"]
        state = 0
        user = User.objects.filter(
            state=state, account=account, password=password
        ).first()
        if user:
            res = {"id": user.uid}
            user.state = 1
            user.save()
            return Response(res, 200)
        else:
            res_error = {"msg": "账号或密码错误,或者账号已经被登录"}
            return Response(res_error, 400)


class LogoutView(APIView):
    @transaction.atomic
    def get(self, request):
        req = request.query_params.dict()
        uid = req["id"]
        state = 1
        user = User.objects.filter(state=state, uid=uid).first()
        if user:
            user.state = 0
            user.save()
            return Response(200)
        else:
            res_error = {"msg": "不存在登陆状态的账号"}
            return Response(res_error, 400)


class VerifyView(APIView):

    @transaction.atomic
    def post(self, request):
        req = request.data
        email = req["email"]
        user = User.objects.filter(email=email).first()
        if not user:
            user_exist = False
        else:
            user_exist = True
        verify = MailVerify.objects.filter(email=email).first()
        if verify:
            verify.delete()
        ret, code = mail(email)  # 发送验证码

        if ret:
            verify = MailVerify.objects.create(email=email, code=code)
            if verify:
                res = {"user_exist": user_exist}
                return Response(res, 200)
        res_error = {"msg": "验证码发送失败"}
        return Response(res_error, 400)

    @transaction.atomic
    def get(self, request):
        req = request.query_params.dict()
        print(req)
        email = req["email"]
        code = req["verification"]
        verify = MailVerify.objects.filter(email=email, code=code).first()
        if verify:
            verify.delete()
            return Response(200)
        else:
            res_error = {"msg": "验证码错误或已被使用"}
            return Response(res_error, 400)


class PasswordView(APIView):
    @transaction.atomic
    def post(self, request):
        req = request.data
        email = req["email"]
        password = req["password"]
        state = 0
        user = User.objects.filter(state=state, email=email).first()
        if user:
            user.password = password
            user.save()
            return Response(200)
        else:
            res_error = {"msg": "邮箱不存在"}
            return Response(res_error, 400)


class InfoView(APIView):
    @transaction.atomic
    def get(self, request):
        req = request.query_params.dict()
        uid = req["id"]
        state = 1
        user = User.objects.filter(state=state, uid=uid).first()
        res_masks = []
        if user:
            if user.mid != "":
                print(user.mid)
                m_ids = [int(m_id_str) for m_id_str in user.mid.split(",")]
                masks = Mask.objects.filter(mid__in=m_ids)
                for mask in masks:
                    res_masks.append(
                        {
                            "id": mask.mid,
                            "name": mask.name,
                            "description": mask.description,
                            "likes": mask.likes.split(","),
                        }
                    )
            res = {
                "id": user.uid,
                "name": user.name,
                "account": user.account,
                "email": user.email,
                "masks": res_masks,
            }
            return Response(res, 200)
        else:
            res_error = {"msg": "账号不存在或未登录"}
            return Response(res_error, 400)


class ChangePasswordView(APIView):
    @transaction.atomic
    def get(self, request):
        req = request.query_params.dict()
        uid = req["id"]
        old_password = req["old_password"]
        new_password = req["new_password"]
        state = 1
        user = User.objects.filter(uid=uid, state=state, password=old_password).first()
        if user:
            user.password = new_password
            user.save()
            return Response(200)
        else:
            res_error = {"msg": "旧密码错误"}
            return Response(res_error, 400)


class UpdateInfoView(APIView):
    @transaction.atomic
    def get(self, request):
        req = request.query_params.dict()
        uid = req["id"]
        name = req["name"]
        account = req["account"]
        state = 1
        user = User.objects.filter(state=state, uid=uid).first()
        if user:
            user.name = name
            user.account = account
            user.save()
            return Response(200)
        else:
            res_error = {"msg": "账号不存在或未登录"}
            return Response(res_error, 400)


class AddMaskView(APIView):
    @transaction.atomic
    def get(self, request):
        # 因为有数组,所以不用dict()
        req = request.query_params
        name = req.get("name")
        description = req.get("description")
        id = req.get("u_id")
        likes = req.getlist("likes[]")
        dislikes = req.getlist("dislikes[]")
        state = 1
        user = User.objects.filter(state=state, uid=id).first()
        if user:
            likes_txt = ""
            if likes != []:
                for like in likes:
                    likes_txt += like + ","
                likes_txt = likes_txt[:-1]
            dislikes_txt = ""
            if dislikes != []:
                for dislike in dislikes:
                    dislikes_txt += dislike + ","
                dislikes_txt = dislikes_txt[:-1]
            mask = Mask.objects.create(
                name=name,
                description=description,
                likes=likes_txt,
                dislikes=dislikes_txt,
                user=user,
            )
            if user.mid != "":
                user.mid += "," + str(mask.mid)
            else:
                user.mid = str(mask.mid)
            user.save()
            return Response(200)
        else:
            res_error = {"msg": "账号不存在或未登录"}
            return Response(res_error, 400)


class DelMaskView(APIView):
    @transaction.atomic
    def get(self, request):
        req = request.query_params.dict()
        mid = req["id"]
        mask = Mask.objects.filter(mid=mid).first()
        if mask:
            state = 1
            user = User.objects.filter(state=state, uid=mask.user.uid).first()
            if user:
                if user.mid != "":
                    mids = user.mid.split(",")
                    mids.remove(str(mid))
                    user.mid = ",".join(mids)
                    user.save()
                mask.delete()
                return Response(200)
            else:
                res_error = {"msg": "账号不在登录状态"}
                return Response(res_error, 400)
        else:
            res_error = {"msg": "mask不存在"}
            return Response(res_error, 400)


class UpdateMaskView(APIView):
    @transaction.atomic
    def get(self, request):
        # 因为有数组,所以不用dict()
        req = request.query_params
        name = req.get("name")
        description = req.get("description")
        likes = req.getlist("likes[]")
        dislikes = req.getlist("dislikes[]")
        mid = req.get("id")
        mask = Mask.objects.filter(mid=mid).first()
        if mask:
            likes_txt = ""
            if likes != []:
                for like in likes:
                    likes_txt += like + ","
                likes_txt = likes_txt[:-1]
            dislikes_txt = ""
            if dislikes != []:
                for dislike in dislikes:
                    dislikes_txt += dislike + ","
                dislikes_txt = dislikes_txt[:-1]
            mask.name = name
            mask.description = description
            mask.likes = likes_txt
            mask.dislikes = dislikes_txt
            mask.buf = None
            mask.save()
            return Response(200)
        else:
            res_error = {"msg": "mask不存在"}
            return Response(res_error, 400)


class CommonSearchView(APIView):
    @transaction.atomic
    def get(self, request):
        # 由于一些条件可能不会存在，所以不用dict
        req = request.query_params
        name = req.get("name")
        keywords = req.get("keywords")
        brands = req.getlist("brands[]")
        models = req.getlist("models[]")
        tags = req.getlist("tags[]")
        minYear = req.get("minYear")
        maxYear = req.get("maxYear")
        minPrice = req.get("minPrice")
        maxPrice = req.get("maxPrice")
        page = int(req.get("page", 1))
        size = int(req.get("pageSize", 10))
        # minYear与maxYear的处理
        if (
            (not minYear and maxYear)
            or (minYear and not maxYear)
            or (minYear and maxYear and minYear > maxYear)
        ):
            res_error = {"msg": "minYear与maxYear不合法"}
            return Response(res_error, 400)
        # minPrice与maxPrice的处理
        if (
            (not minPrice and maxPrice)
            or (minPrice and not maxPrice)
            or (minPrice and maxPrice and minPrice > maxPrice)
        ):
            res_error = {"msg": "minPrice与maxPrice不合法"}
            return Response(res_error, 400)
        must_conditions = []  # 始终添加 name 条件
        should_conditions = []  # 将其他条件放入 should_conditions
        # 根据条件动态添加
        if name:
            must_conditions.append({"match": {"name": name}})
        if keywords:
            should_conditions.append({"match": {"description": keywords}})
        if brands:
            for brand in brands:
                should_conditions.append({"match": {"brand": brand}})
        if models:
            for model in models:
                should_conditions.append({"match": {"model": model}})
        if minYear and maxYear:
            must_conditions.append(
                {"range": {"year": {"gte": minYear, "lte": maxYear}}}
            )
        if minPrice and maxPrice:
            must_conditions.append(
                {"range": {"price": {"gte": minPrice, "lte": maxPrice}}}
            )
        if tags:
            for tag in tags:
                should_conditions.append({"term": {"tags": tag}})
        from_value = (page - 1) * size
        es = Elasticsearch(
            ["http://localhost:9200"], basic_auth=("elastic", "pdBKdW6xseraou6kNMNq")
        )
        bool = {}
        if must_conditions:
            bool["must"] = must_conditions
        if should_conditions:
            bool["should"] = should_conditions
            bool["minimum_should_match"] = 1
        if bool:
            search_body = {
                "query": {"bool": bool},
                "from": from_value,  # 添加 from 参数
                "size": size,  # 添加 size 参数
            }
        else:
            search_body = {
                "from": from_value,  # 添加 from 参数
                "size": size,  # 添加 size 参数
            }
        print(search_body)
        search_result = es.search(index="car", body=search_body)
        # 获取查询结果
        documents = search_result["hits"]["hits"]
        res = []
        res_count = search_result["hits"]["total"]["value"]
        for doc in documents:
            src = doc["_source"]
            res.append(
                {
                    "id": doc["_id"],
                    "name": src["name"],
                    "description": src["description"],
                    "year": src["year"],
                    "brand": src["brand"],
                    "model": src["model"],
                    "price": src["price"],
                    "tags": src["tags"],
                    "image": src["image"],
                    "url": src["url"],
                }
            )
        response = {"data": res, "total": res_count, "page": page, "pageSize": size}
        return Response(response, 200)


class RecommendSearchView(APIView):
    @transaction.atomic
    def get(self, request):
        # AI分析相关标签
        mask_id = request.query_params.get("mask_id")
        page = int(request.query_params.get("page", 1))
        size = int(request.query_params.get("pageSize", 10))
        mask = Mask.objects.filter(mid=mask_id).first()
        if not mask:
            res_error = {"msg": "mask不存在"}
            return Response(res_error, 400)
        # 分析相关标签
        if not mask.buf:
            tags_ai = mask.likes.split(",")
            res = AI.analyseTags(tags_ai)
            # 获取所有标签并初始化分数
            tags = Tag.objects.all()
            scores = {name: 0 for name in tags.values_list("name", flat=True)}
            # 计算分数
            for tag_ai in tags_ai:
                tags_relevent = res.get(tag_ai, [])
                print(tags_relevent)
                for each_tag in tags_relevent:
                    if each_tag in scores:
                        scores[each_tag] += 2  # 每个相关标签增加2分

            # 将分数进行排序
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            print(sorted_scores)
            # 获取最高分数
            if sorted_scores:
                max_score = sorted_scores[0][1]
                high_threshold = max_score * 0.5  # 高分阈值：最高分的50%
            else:
                high_threshold = 0

            # 按得分分级
            high_score_tags = [
                tag for tag, score in sorted_scores if score >= high_threshold
            ]
            # medium_score_tags = [
            #     tag
            #     for tag, score in sorted_scores
            #     if medium_threshold <= score < high_threshold
            # ]
            # low_score_tags = [
            #     tag for tag, score in sorted_scores if score < medium_threshold
            # ]
            # 保存标签分级结果
            mask.buf = ",".join(high_score_tags)
            mask.save()
        else:
            high_score_tags = mask.buf.split(",")
        es_results = []

        es = Elasticsearch(
            ["http://localhost:9200"], basic_auth=("elastic", "pdBKdW6xseraou6kNMNq")
        )

        from_value = (page - 1) * size
        # 只对高分标签进行 Elasticsearch 查询
        if high_score_tags:  # 如果标签列表不为空
            es_query = {
                "query": {
                    "bool": {
                        "should": [{"term": {"tags": tag}} for tag in high_score_tags]
                    }
                },
                "from": from_value,  # 添加 from 参数
                "size": size,  # 添加 size 参数
            }

            # 执行 ES 查询
            es_response = es.search(index="car", body=es_query)  # 替换索引名称为实际值

            # 将 ES 查询结果处理为需要的格式
            es_data = [
                {"id": hit["_id"], "score": hit["_score"], "data": hit["_source"]}
                for hit in es_response["hits"]["hits"]
            ]
            res_count = es_response["hits"]["total"]["value"]

            es_results.extend(es_data)
        result = []
        # 返回结果
        for src in es_results:
            result.append(
                {
                    "id": src["id"],
                    "name": src["data"]["name"],
                    "description": src["data"]["description"],
                    "year": src["data"]["year"],
                    "brand": src["data"]["brand"],
                    "model": src["data"]["model"],
                    "price": src["data"]["price"],
                    "tags": src["data"]["tags"],
                    "image": src["data"]["image"],
                    "url": src["data"]["url"],
                }
            )
        response = {"data": result, "total": res_count, "page": page, "pageSize": size}
        return Response(response, 200)


class ListTagView(APIView):
    @transaction.atomic
    def get(self, request):
        tags = Tag.objects.all()
        res = []
        for tag in tags:
            res.append(
                {"id": tag.tid, "name": tag.name, "description": tag.description}
            )
        return Response(res, 200)
