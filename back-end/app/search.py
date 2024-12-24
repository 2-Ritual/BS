from elasticsearch_dsl import Document, Text, Float, Keyword, Integer, Long, connections
from .models import Car

es = connections.create_connection(
    hosts=["http://localhost:9200"], http_auth=("elastic", "pdBKdW6xseraou6kNMNq")
)


class CarIndex(Document):
    """
    Car Elasticsearch index for storing and searching car data.
    """

    # 如有需要,可以使用中文的分词器,如ik_max_word,ik_smart,pinyin等
    name = Text()
    description = Text()
    year = Long()
    brand = Text()
    model = Text()
    price = Float()
    tags = Keyword()
    image = Text()
    url = Text()

    class Django:
        model = Car  # 指定Django模型
        fields = [
            "name",
            "description",
            "year",
            "brand",
            "model",
            "price",
            "tags",
        ]  # 指定要索引的字段

    class Index:
        name = "car"  # 索引名称
