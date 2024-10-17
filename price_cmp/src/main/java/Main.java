import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
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
//        options.setBinary("C:/Users/2_Ritual/AppData/Local/Google/Chrome/Application/chrome.exe"); // old
        options.setBinary("C:/Program Files/Google/Chrome/Application/chrome.exe"); // new
        options.addArguments("--headless","--disable-gpu");
        System.setProperty("webdriver.chrome.driver", "L:/BS/chromedriver-win64/chromedriver.exe");
        WebDriver driver = new ChromeDriver(options);

        driver.get(URL);
        Thread.sleep(5000);
        String html = driver.getPageSource();
        System.out.println("The testing page title is: " + driver.getTitle());
        driver.quit();
        Document doc =  Jsoup.parse(html);
        System.out.println(doc);

        Elements productElements = doc.select(".gl-item");
        List<Product> productList = new ArrayList<>();

        for (Element productElement : productElements) {
            String name = productElement.select(".p-name a em").text();
            String img_src = productElement.select(".p-img a img").attr("src");
            if (img_src.isEmpty()) img_src = productElement.select(".p-img a img").attr("data-lazy-img");
            Elements element = productElement.select("div[data-buried]");

            String formattedData = element.attr("data-buried");

            try {
                JsonElement jsonElement = JsonParser.parseString(formattedData);
                JsonObject jsonObject = jsonElement.getAsJsonObject();

                float price = Float.parseFloat(jsonObject.get("price").getAsString());
                float oriPrice = Float.parseFloat(jsonObject.get("ori_price").getAsString());
                String skuId = jsonObject.get("skuid").getAsString();

                String mtestActString = jsonObject.get("mtest_act").getAsString();
                String[] mtestAct = mtestActString.split(",");

                productList.add(new Product(name, price, oriPrice, img_src, skuId, mtestAct));
                productList.getLast().displayProductInfo();
                System.out.println();

            } catch (Exception e) {
                e.printStackTrace();
            }

        }

//        System.out.println("\n是否退出程序：Y/N");
//        Scanner input = new Scanner(System.in);
//        String Y_N = input.nextLine();
//        if(Y_N.equals('Y')||Y_N.equals('y')){
//            System.exit(0);
//        }
    }
}