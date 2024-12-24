from typing import List, Dict, Any, Optional
import os
import json
from pathlib import Path
import httpx
from openai import OpenAI


class AI:
    upload_flag = 0
    client = OpenAI(
        base_url="https://api.moonshot.cn/v1",
        # sk-3KN9hPPpIPPVAROVN5qwsdQgg08tKvj6BCkHVMw9zzicQTze
        # 需要添加到环境变量
        # 如果是windows的话就直接赋值
        api_key="sk-3KN9hPPpIPPVAROVN5qwsdQgg08tKvj6BCkHVMw9zzicQTze",
        # api_key=os.environ["MOONSHOT_DEMO_API_KEY"],
    )

    @staticmethod
    def analyseTags(tags: list):
        tags_str = " ".join([f"'{tag}'" for tag in tags])
        AI.upload_directory_files(
            directory="data",  # 需要修改
            cache_tag="tags",
        )
        response = AI.chat_with_cache(
            cache_tag="tags",
            user_message="读取文档中每一项下的词语，并根据词语后面的描述，用仅可能多文档中的客观标签词语，匹配主观词汇"
            + tags_str
            + "，结果去掉标签分类，去掉每个标签后面的描述，并用json的格式表示出来",
        )
        res = {}
        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                res = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
        return res

    @staticmethod
    def analyseCar(car: str):
        AI.upload_directory_files(
            directory="data/",  # 需要修改
            cache_tag="tags",
        )
        response = AI.chat_with_cache(
            cache_tag="tags",
            user_message="读取文档中每一项下的词语，并根据词语后面的描述，用尽可能多的文档中的客观标签词语，来描述这辆车："
            + car
            + "，并用json的格式表示结果。忽略尺寸与最高车速。如果有不确定的信息需要进行网络搜索",
        )
        res = {}
        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                res = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
        return res

    @staticmethod
    def upload_directory_files(
        directory: str, cache_tag: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        上传指定目录下的所有文件，并支持将文件内容缓存到 Context Cache 中。
        :param directory: 要上传文件的目录路径。
        :param cache_tag: 可选，Context Cache 的 tag 值，用于缓存文件内容。
        :return: 一个包含上传结果的 messages 列表。
        """
        messages = []
        directory_path = Path(directory)
        if not directory_path.is_dir():
            raise ValueError(f"指定的目录 '{directory}' 不存在或不是一个目录。")

        for file_path in directory_path.iterdir():
            if file_path.is_file():
                file_object = AI.client.files.create(
                    file=file_path, purpose="file-extract"
                )
                file_content = AI.client.files.content(file_id=file_object.id).text
                messages.append(
                    {
                        "role": "system",
                        "content": file_content,
                    }
                )

        if cache_tag:
            if AI.upload_flag == 0:
                r = httpx.post(
                    f"{AI.client.base_url}caching",
                    headers={
                        "Authorization": f"Bearer {AI.client.api_key}",
                    },
                    json={
                        "model": "moonshot-v1",
                        "messages": messages,
                        "ttl": 300,
                        "tags": [cache_tag],
                    },
                )
                AI.upload_flag = 1
                if r.status_code != 200:
                    raise Exception(f"创建缓存失败：{r.text}")
                return [
                    {
                        "role": "cache",
                        "content": f"tag={cache_tag};reset_ttl=600",
                    }
                ]
        return messages

    @staticmethod
    def chat_with_cache(cache_tag: str, user_message: str) -> str:
        """
        使用指定的 cache_tag 发起对话。
        :param cache_tag: Context Cache 的 tag 值，用于引用缓存的内容。
        :param user_message: 用户的问题或输入内容。
        :return: 模型的回答内容。
        """
        messages = [
            {
                "role": "cache",
                "content": f"tag={cache_tag};reset_ttl=300",
            },
            {
                "role": "system",
                "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，"
                "准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不"
                "可翻译成其他语言。",
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]

        completion = AI.client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=messages,
        )

        return completion.choices[0].message.content


if __name__ == "__main__":
    # 测试用
    response_tag = AI.analyseTags(["好看", "精致", "奢华", "快", "宽敞"])
    print(response_tag)
    print("--------------")
    car_info = '{"name": "小米SU7 2024款 830km 后驱超长续航高阶智驾Pro版", "description": "能源类型：纯电动，长*宽*高(mm)：4997*1963*1455，最高车速(km/h)：210", "year": 2024, "model": "三厢车", "price": 24.59, "image": "https://g.autoimg.cn/@img/car3/cardfs/product/g32/M07/23/9C/900x0_c42_autohomecar__Chtk2WbHO5SAL8LhAGTa9P-rdDI276.jpg", "detailed": "https://www.autohome.com.cn/spec/67500"}'
    response_car = AI.analyseCar("[" + car_info + "]")
    print(response_car)
