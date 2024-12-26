from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)


def Crawer_main_tb(KEYWORD, pageStart, pageEnd):
    try:
        search_goods_tb(KEYWORD, pageStart, pageEnd)
    except Exception as exc:
        print('Crawer_main函数报错:', exc)


def search_goods_tb(KEYWORD, start_page, total_pages):
    try:
        driver.get('https://www.taobao.com')
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                               {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORD)
        submit.click()
        time.sleep(5)
        get_goods_tb()
        for i in range(start_page + 1, total_pages + 1):
            page_turning_tb(i)
    except TimeoutException:
        print("search_goods: error")
        return search_goods_tb(KEYWORD, start_page, total_pages)


def page_turning_tb(page_number):
    print('正在翻页: ', page_number)
    try:
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("滚动到底")
        button = driver.find_element(By.XPATH, "//button[contains(@aria-label, '下一页')]")
        print("找到按钮")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        get_goods_tb()
    except TimeoutException:
        print("page_number: error")
        page_turning_tb(page_number)


def get_goods_tb():
    time.sleep(10)
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_step = total_height // 5
    for i in range(6):
        # 计算滚动位置
        scroll_position = scroll_step * (i + 1)
        # 滚动到指定位置
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        # 等待页面内容加载
        time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content_wrapper = soup.find('div', {'id': 'content_items_wrapper'})
    if content_wrapper:
        item_divs = content_wrapper.find_all('div', class_='tbpc-col')
        for item_div in item_divs:
            item = {}

            title_span = item_div.find('span', class_='')
            if title_span:
                item['title'] = title_span.text.strip()

            price_div = item_div.find('div', class_='priceWrapper--dBtPZ2K1')
            if price_div:
                price_int = price_div.find('span', class_='priceInt--yqqZMJ5a')
                price_float = price_div.find('span', class_='priceFloat--XpixvyQ1')
                if price_int and price_float:
                    item['price'] = f"{price_int.text.strip()}{price_float.text.strip()}"

            link_tag = item_div.find('a', class_='doubleCardWrapperAdapt--mEcC7olq')
            if link_tag and 'href' in link_tag.attrs:
                item['link'] = link_tag['href']

            img_tag = item_div.find('img', class_='mainPic--Ds3X7I8z')
            if img_tag and 'src' in img_tag.attrs:
                item['image'] = img_tag['src']

            desc_spans = item_div.find_all('span', class_='text--eAiSCa_r')
            if desc_spans:
                item['description'] = [span.text.strip() for span in desc_spans]

            shop_name_span = item_div.find('span', class_='shopNameText--DmtlsDKm')
            if shop_name_span:
                item['shop'] = shop_name_span.text.strip()

            if item:
                print(f"商品 {i}:")
                print(f"标题: {item.get('title', 'N/A')}")
                print(f"价格: {item.get('price', 'N/A')}")
                print(f"链接: {item.get('link', 'N/A')}")
                print(f"图片: {item.get('image', 'N/A')}")
                print(f"描述: {item.get('description', 'N/A')}")
                print(f"店铺: {item.get('shop', 'N/A')}")
                print("-" * 50)
                # price_field_name = f"price_{current_month}"
                # product_data = {
                #     'product_name': item.get('title', 'N/A'),
                #     'product_url': item.get('link', 'N/A'),
                #     'image': item.get('image', 'N/A'),
                #     'origin': '淘宝',
                #     price_field_name: item.get('price', 'N/A')
                # }
                # Product.objects.create(**product_data)


if __name__ == "__main__":
    Crawer_main_tb("书包", 1, 1)
