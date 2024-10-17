public class Product {
    private String name;
    private float originalPrice;
    private float currentPrice;
    private String imageUrl;
    private String skuId;
    private String[] mtest_act = new String[25];

    public Product(String name, float originalPrice, float currentPrice, String imageUrl, String skuId) {
        this.name = name;
        this.originalPrice = originalPrice;
        this.currentPrice = currentPrice;
        this.imageUrl = imageUrl;
        this.skuId = skuId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public float getOriginalPrice() {
        return originalPrice;
    }

    public void setOriginalPrice(float originalPrice) {
        this.originalPrice = originalPrice;
    }

    public float getCurrentPrice() {
        return currentPrice;
    }

    public void setCurrentPrice(float currentPrice) {
        this.currentPrice = currentPrice;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public String getSkuId() {
        return skuId;
    }

    public void setSkuId(String skuId) {
        this.skuId = skuId;
    }

    // Method to display product information
    public void displayProductInfo() {
        System.out.println("商品名称: " + name);
        System.out.println("原价: " + originalPrice);
        System.out.println("现价: " + currentPrice);
        System.out.println("商品图片链接: " + imageUrl);
        System.out.println("SKU ID: " + skuId);
    }
}
