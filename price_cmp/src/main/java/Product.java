public class Product {
    private String name;
    private String originalPrice;
    private String currentPrice;
    private String imageUrl;
    private String skuId;

    // Constructor
    public Product(String name, String originalPrice, String currentPrice, String imageUrl, String skuId) {
        this.name = name;
        this.originalPrice = originalPrice;
        this.currentPrice = currentPrice;
        this.imageUrl = imageUrl;
        this.skuId = skuId;
    }

    // Getters and Setters
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getOriginalPrice() {
        return originalPrice;
    }

    public void setOriginalPrice(String originalPrice) {
        this.originalPrice = originalPrice;
    }

    public String getCurrentPrice() {
        return currentPrice;
    }

    public void setCurrentPrice(String currentPrice) {
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
