import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.nodes.Entities;
import org.jsoup.select.Elements;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter The Product:");
        String input_product = sc.nextLine();
        String URL = "https://search.jd.com/Search?keyword=" + input_product + "&wq=" + input_product + "&page=1&s=1&click=1";

        ChromeOptions options = new ChromeOptions();
        options.setBinary("C:/Program Files/Google/Chrome/Application/chrome.exe");
        options.addArguments("--headless","--disable-gpu");
        System.setProperty("webdriver.chrome.driver", "L:/BS/chromedriver-win64/chromedriver.exe");
        WebDriver driver = new ChromeDriver(options);

        driver.get(URL);
        Thread.sleep(5000);
        String html = driver.getPageSource();
        System.out.println("The testing page title is: " + driver.getTitle());
        driver.quit();
        Document doc =  Jsoup.parse(html);
//        System.out.println(doc);

        Elements productElements = doc.select(".gl-item");

        // 创建一个列表保存 Product 对象
        List<Product> productList = new ArrayList<>();

        // 遍历每个商品项，提取信息并创建 Product 对象
        for (Element productElement : productElements) {
            // 提取商品名称、原价、现价、图片链接和SKU ID
            String name = productElement.select(".p-name a em").text();
            String dataBuried = productElement.attr("data-buried");
            String decodedDataBuried = Entities.unescape(dataBuried);
            System.out.println(decodedDataBuried);
            String originalPrice = productElement.attr("").split("\"ori_price\":\"")[1].split("\"")[0];
            String currentPrice = productElement.attr("data-buried").split("\"price\":\"")[1].split("\"")[0];
            String imageUrl = productElement.select(".p-img img").attr("src");
            String skuId = productElement.attr("data-sku");

            Product product = new Product(name, originalPrice, currentPrice, imageUrl, skuId);
            productList.add(product);
        }



    }
}

// https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=cab3453f2b9d428386be3dd6dd623fc8