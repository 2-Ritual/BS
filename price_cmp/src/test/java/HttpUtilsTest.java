import org.jsoup.nodes.Document;
import org.junit.Test;


public class HttpUtilsTest {
    private static final String TEST_URL = "http://www.google.com/";

    @Test
    public void testGetHtmlPageResponse() {
        HttpUtils httpUtils = HttpUtils.getInstance();
        httpUtils.setTimeout(30000);
        httpUtils.setWaitForBackgroundJavaScript(30000);
        try {
            String htmlPageStr = httpUtils.getHtmlPageResponse(TEST_URL);
            //TODO
            System.out.println(htmlPageStr);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Test
    public void testGetHtmlPageResponseAsDocument() {
        HttpUtils httpUtils = HttpUtils.getInstance();
        httpUtils.setTimeout(30000);
        httpUtils.setWaitForBackgroundJavaScript(30000);
        try {
            Document document = httpUtils.getHtmlPageResponseAsDocument(TEST_URL);
            //TODO
            System.out.println(document);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}