# 软工管SCS后端



# 12.6更新（by：张皓翔）

除开搜索的算法与elastic的使用，前端接口已经全部实现，并通过测试

## 关于ElasticSearch的使用

下载ElasticSearch，启动，设置密码并关闭ssl认证。具体可以看这篇文章：

[ElasticSearch：下载、启动和账号密码登录_elasticsearch账号密码在哪看-CSDN博客](https://blog.csdn.net/weixin_44384273/article/details/137816331)

下载python与django连接ElasticSearch的库

```bash
pip install elasticsearch django-elasticsearch-dsl      
```

索引与数据表的关联已经在app/search.py写好

```python
from elasticsearch_dsl import Document, Text, Float, Integer, Long, connections
from .models import Car
connections.create_connection(
    hosts=['http://localhost:9200'], http_auth=('elastic', '你设置的密码')
)
class CarIndex(Document):
    """
    Car Elasticsearch index for storing and searching car data.
    """

    name = Text()
    description = Text()
    year = Long()
    brand = Text()
    model = Text()
    price = Float()
    tags = Text(multi=True)  # 标签可以使用Keyword存储

    class Django:
        model = Car  # 指定Django模型
        fields = ['name', 'description', 'year', 'brand', 'model', 'price']  # 指定要索引的字段

    def save(self, **kwargs):
        """
        Save the document in Elasticsearch.
        """
        tags_list = list(self.tags)  # 获取标签的实际值
        self.tags = tags_list  # 设置标签为列表
        super().save(**kwargs)  # 调用父类的save方法
    class Index:
        name = 'car'  # 索引名称
```

像下面的示例使用即可

```python
es = Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'pdBKdW6xseraou6kNMNq'))
CarIndex.init()
if es.ping():
    # 创建Car实例
    tags=[Tag.objects.filter(name="红色").first().tid, Tag.objects.filter(name="橙色").first().tid]
    car = Car.objects.create(
        name="测试用车",
        description="测试用车",
        year=2024,
        brand="测试牌子",
        model="测试车型",
        price=100000,
    )
    car.tags.set(tags)
    car.save()
    tag_ids = [1,2]
    # 创建和保存到Elasticsearch
    car_index = CarIndex(
        meta={'id': car.cid},  # 没有cid的情况下使用其他唯一标识
        name=car.name,
        description=car.description,
        year=car.year,
        brand=car.brand,
        model=car.model,
        price=car.price,
        tags=[tag.name for tag in car.tags.filter(tid__in=tag_ids)]  # 提取标签名称列表
    )
    print(car_index)
    car_index.save()  # 保存到Elasticsearch
    result = es.search(index="car", body={"query": {"match": {"name":"测试用车"}}},)
    print(result)
    print('Elasticsearch is connected')
else:
    print('Elasticsearch is not connected')
```





