public class Product {
    private final String name;
    private final float originalPrice;
    private final float currentPrice;
    private final String imageUrl;
    private final String skuId;
    private final String[] mtest_act;

    public Product(String name, float originalPrice, float currentPrice, String imageUrl, String skuId, String[] mtestAct) {
        this.name = name;
        this.originalPrice = originalPrice;
        this.currentPrice = currentPrice;
        this.imageUrl = imageUrl;
        this.skuId = skuId;
        this.mtest_act = mtestAct;
    }

    public String getName() {
        return name;
    }
    public float getOriginalPrice() {
        return originalPrice;
    }
    public float getCurrentPrice() {
        return currentPrice;
    }
    public String getImageUrl() {
        return imageUrl;
    }
    public String[] getMtestAct() { return this.mtest_act; }
    public String getSkuId() { return skuId; }

    public void displayProductInfo() {
        System.out.println("商品名称: " + name);
        System.out.println("原价: " + originalPrice);
        System.out.println("现价: " + currentPrice);
        System.out.println("商品图片链接: " + imageUrl);
        System.out.println("SKU ID: " + skuId);
    }
}
