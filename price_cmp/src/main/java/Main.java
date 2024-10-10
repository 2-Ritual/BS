import com.arronlong.httpclientutil.HttpClientUtil;
import com.arronlong.httpclientutil.common.HttpConfig;
import com.arronlong.httpclientutil.common.HttpCookies;
import com.arronlong.httpclientutil.exception.HttpProcessException;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws HttpProcessException {
//        try {
//            String url = "https://s.taobao.com/search?q=%E9%A5%BC%E5%B9%B2&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306";
//            URL realUrl = new URL(url);
//            HttpURLConnection connection = (HttpURLConnection) realUrl.openConnection();
//            connection.setRequestProperty("accept", "*/*");
//            connection.setRequestProperty("connection", "Keep-Alive");
//            connection.setRequestProperty("Referer", "https://cn.bing.com/");
//            connection.setRequestProperty("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0");
//            connection.setRequestProperty("Cookie", "t=66d96ce387a4a1b9f64747b66b62ea81; cna=7G8MHsqTrCIBASQMx4EyWnqY; thw=xx; cookie2=2ef75d0a682c6fe95646ae5d2ccce6c8; _tb_token_=ebdb631de1eee; lgc=tb6969328049; cancelledSubSites=empty; dnk=tb6969328049; tracknick=tb6969328049; _hvn_lgc_=0; wk_cookie2=1956e5630c40a438045fa2b9f7bc2cfd; wk_unb=UUpgRKVR8gcusPDPAQ%3D%3D; sn=; useNativeIM=false; mtop_partitioned_detect=1; _m_h5_tk=b7ecf633db738333840ffd04bf22d06b_1728544951660; _m_h5_tk_enc=48b9f575a9d32cdbe3cf137fc7f50fe4; _samesite_flag_=true; sgcookie=E100VBd9xuZNRigU7%2F7NuNqj1B6ud3u8ZswgmP7FBTvwDDKvepm29wZ9rntgpcKdHPAr1KRHL0wxnDZPJa3tOj9%2BYLkqYrYHU%2Bj12YZ%2BkZ31EfOjbevlRVkP8U%2FMnmboaFup; havana_lgc2_0=eyJoaWQiOjIyMTI4NTUxNTY3OTksInNnIjoiZGE3MmQxYWJhMDY0ZmQ5MzE5NjNmMzY5OTAxYjdhMTkiLCJzaXRlIjowLCJ0b2tlbiI6IjF2VjdaUzF3VWdLY3NpQTM0TmJXdEZRIn0; havana_lgc_exp=1759641753825; unb=2212855156799; uc1=cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie15=UIHiLt3xD8xYTw%3D%3D&cookie14=UoYcC%2FHbpYAnkg%3D%3D&existShop=false&pas=0&cookie21=VFC%2FuZ9ainBZ; uc3=nk2=F5RDJXMtTikXax0X&vt3=F8dD37ng4P3cGCDy5l4%3D&id2=UUpgRKVR8gcusPDPAQ%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; csg=2f9c8681; cookie17=UUpgRKVR8gcusPDPAQ%3D%3D; skt=916ee6c136a48009; existShop=MTcyODUzNzc1Mw%3D%3D; uc4=id4=0%40U2gqy1TjPO0FBCgGAmfUMaGfwyR3Pt8U&nk4=0%40FY4I5qQzfWk93S9U0S0infcAYvUPsCM%3D; _cc_=WqG3DMC9EA%3D%3D; _l_g_=Ug%3D%3D; sg=99d; _nk_=tb6969328049; cookie1=UIIq5juTlng3Hirk4qTWgM2CMe9MqnjoMVOuSIUzqKs%3D; sdkSilent=1728624153856; havana_sdkSilent=1728624153856; tfstk=g6_-M3DIA-2oGJcq8vZDxBMHkFF0mwCrET5s-pvoAtBA11kkApqPpHBh3H_kr_XxaZBt-42z46gp-ewgIP4GaQYeRRmkVykSaBAIVBMHdmMX8Aa94qaGa_ljwvNGcPDKUOxNND9CdEtX9CLBNLtIlSdp6pTBFHMjcC9Xde6IVx9X6C3Wd497Ms92Oe9IBQoJLb9KJMR-VhwSkygZ7ZdJ2pQH32ChzVxkC_9xRI7vw2J1NK3IRLuyFvCAZ83NiU7GBCXul4BOO1SBDwHbBp7AGasCgYeBgM6klLY_VjLlz_s6ANwEAOLRph_WDXg1a_92kI__tcJckLXCynNiWHYfShT5moykxUdOdaW-9261i1by0wethpSk_EOd85ippHsrgNb9oKkMBBm7MSnEY3O2cHosOr4fJDRvISfmYD-DgIpgMSnEY3O2MdVDnDoemI5..; isg=BMvLHH1SKJUss3Wjpj3gbg_6Wm-1YN_ieEHKsj3LlIphXOi-xzRzM7q-Ntyy5zfa");
//            // 建立实际的连接
//            connection.connect();
//            //请求成功
//            System.out.println("请求状态："+connection.getResponseCode());
////	        if (connection.getResponseCode() == 200) {
//            InputStream is = connection.getInputStream();
//            ByteArrayOutputStream baos = new ByteArrayOutputStream();
//            byte[] buffer = new byte[10485760]; //10MB的缓存
//            int len = 0;
//            while ((len = is.read(buffer)) != -1) {
//                baos.write(buffer, 0, len);
//            }
//            String jsonString = baos.toString();
//            System.out.println("jsonString:"+jsonString);
//            baos.close();
//            is.close();
//            //转换成json数据处理
////	        }
//        } catch (Exception e) {
//            System.out.println(e);
//        }
        HttpConfig config = HttpConfig.custom().url("https://home.jd.com/getUserVerifyRight.action")
                .inenc("utf-8").json("json字符串")
                .context(HttpCookies.custom().getContext());
        String verify = HttpClientUtil.post(config);
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter The Product:");
        String product = sc.nextLine();
        String URL = "https://search.jd.com/Search?keyword=" + product + "&wq=" + product + "&page=1&s=1&click=1";

    }
}

// https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=cab3453f2b9d428386be3dd6dd623fc8