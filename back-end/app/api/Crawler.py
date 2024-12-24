import requests
from bs4 import BeautifulSoup
import json
import re
from elasticsearch import Elasticsearch
from elasticsearch import helpers


def find_key(data, target_key):
    """递归查找字典或列表中指定的键"""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            result = find_key(value, target_key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, target_key)
            if result is not None:
                return result
    return None


class Crawler:
    @staticmethod
    def spec_spider(specid):
        """根据 specid 爬取车辆参数信息并返回解析后的数据"""
        url_spec = f"https://car-web-api.autohome.com.cn/car/param/getParamConf?mode=1&site=2&specid={specid}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
            ),
        }

        try:
            response = requests.get(url_spec, headers=headers)
            response.raise_for_status()
            spec_data = response.text
        except requests.RequestException as e:
            print(f"请求失败：{e}")
            return None

        try:
            data = json.loads(spec_data)
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
            return None

        title_json = find_key(data, "titlelist")
        if not title_json:
            return None

        title_data = [
            {
                title["titleid"]: title["itemname"]
                for item in title_json
                for title in item["items"]
            }
        ]

        spec_json = find_key(data, "datalist")
        if not spec_json:
            return None

        condition_json = find_key(data, "conditionlist")
        if not condition_json:
            return None
        # 收集所有 conditionlist 中的 list 中的 name
        tags = []
        for condition in condition_json:
            for item in condition["list"]:
                tags.append(item["name"])

        spec_data = []
        for spec in spec_json:
            if specid == spec["specid"]:
                one = {}
                for title in spec["paramconflist"]:
                    item_name = title.get("itemname", "")
                    if item_name:
                        one[title["titleid"]] = re.sub(
                            r"[●○\-]",
                            lambda x: {"●": "(标配)", "○": "(选配)", "-": "(无)"}[
                                x.group()
                            ],
                            item_name,
                        )
                    elif title.get("sublist"):
                        sublist_content = "".join(
                            sub["name"] + sub["value"] for sub in title["sublist"]
                        )
                        one[title["titleid"]] = re.sub(
                            r"[●○\-]",
                            lambda x: {"●": "(标配)", "○": "(选配)", "-": "(无)"}[
                                x.group()
                            ],
                            sublist_content,
                        )
                one["tags"] = ",".join(tags)
                spec_data.append(one)

        if not title_data or not spec_data:
            return None

        return {title_data[0].get(k, k): v for k, v in spec_data[0].items()}

    @staticmethod
    def getImg(specid):
        url = f"https://www.autohome.com.cn/spec/{specid}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 "
            "Safari/537.36 Edg/130.0.0.0",
        }
        response = requests.get(url, headers=headers)
        html_content = ""
        if response.status_code == 200:
            html_content = response.text
        else:
            print(f"请求失败，状态码：{response.status_code}")
        soup = BeautifulSoup(html_content, "html.parser")
        img = soup.find(
            "img",
            class_="auto-react-image-placeholder tw-size-full hover:tw-scale-110 "
            "tw-transition-transform tw-ease-in-out tw-duration-300",
        )
        if img and "src" in img.attrs:
            imgsrc = img["src"]

        return "https:" + imgsrc

    @staticmethod
    def save_to_file(file_name, data):
        """将数据保存到txt文件"""
        with open(file_name, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"数据已写入 {file_name}")

    @staticmethod
    def update(
        minid=21000, maxid=71000
    ):  # 这个范围大约是2014年左右到现在的所有车，测试的时候可以缩小范围
        """爬虫模块实现，用于更新汽车数据并存入 Elasticsearch"""
        all_data = []
        all_id = []
        all_dcar = []

        for specid in range(minid, maxid):
            spider_data = Crawler.spec_spider(specid)
            if not spider_data:
                continue
            price_filter = spider_data.get("厂商指导价(元)", "0万")
            if "万" not in price_filter:
                price_filter = "0万"

            dcar = {
                "name": spider_data.get("车型名称"),
                "description": (
                    "能源类型："
                    + spider_data.get("能源类型", "")
                    + "，长*宽*高(mm)："
                    + spider_data.get("长*宽*高(mm)", "")
                    + "，最高车速(km/h)："
                    + spider_data.get("最高车速(km/h)", "")
                ),
                "year": int(spider_data.get("上市时间", "0000")[:4]),
                "model": spider_data.get("车身结构"),
                "price": float(price_filter[:-1]),
                "brand": spider_data.get("厂商"),
                "image": Crawler.getImg(specid),
                "detailed": f"https://www.autohome.com.cn/spec/{specid}",
                "tags": spider_data.get("tags"),
            }

            all_dcar.append(dcar)
            all_data.append(spider_data)
            all_id.append(specid)

        print(f"收集完毕，共 {len(all_data)} 条车辆信息")

        es = Elasticsearch(
            "http://localhost:9200", basic_auth=("elastic", "pdBKdW6xseraou6kNMNq")
        )  # 可以增加设置的密码
        actions = [
            {"_index": "car", "_id": all_id[j], "_source": all_dcar[j]}
            for j in range(len(all_data))
        ]
        helpers.bulk(es, actions)
        print("数据已写入 Elasticsearch 索引 'car'")

        # 展示所有爬取的原数据
        # print_result()
        # 将所有爬取的原数据写入txt文档
        # txt_result()
        # 展示所有存入的数据
        # results = helpers.scan(es, index="car", query={"query": {"match_all": {}}})
        # for item in results:
        #     print(item['_id'], item['_source'])

        status = "success"
        return status
