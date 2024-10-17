import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class LinkDatabaseInsert {
    public static void main(String[] args) throws ClassNotFoundException, SQLException {
        //1.注册数据库的驱动
        Class.forName("com.mysql.jdbc.Driver");
        //2.获取数据库连接（里面内容依次是："jdbc:mysql://主机名:端口号/数据库名","用户名","登录密码"）
        Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/BS","root","1234");
        String sql = "insert into stu(id,name,age) values(?,?,?)";
        PreparedStatement statement = connection.prepareCall(sql);
        statement.setInt(1,12);
        statement.setString(2,"小明");
        statement.setInt(3,16);

        int i = statement.executeUpdate();
        System.out.println(i);

        statement.close();
        connection.close();
    }
}