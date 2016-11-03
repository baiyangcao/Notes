<link rel="stylesheet" href="../node_modules/bootstrap/dist/css/bootstrap.css">

## `String.Format` “输入字符串格式不正确”

```cs
string script =
    string.Format(
        "<script>if(window.parent.AfterAffixFile){ window.parent.AfterAffixFile('{0}', '{1}'); }</script>",
        result, message);
```

如上语句中报错`"输入字符串格式不正确"`，因为格式化字符串中的包含`{`和`}`，
所以在格式化时解析占位符失败，导致报错，此时应该使用`{{`和`}}`替换字符串中的`{`和`}`即可

```cs
string script =
    string.Format(
        "<script>if(window.parent.AfterAffixFile){{ window.parent.AfterAffixFile('{0}', '{1}'); }}</script>",
        result, message);
```

> 其实很多情况下特殊字符都是使用这种方式转义，如：
> 
>  - C#字符串字面量使用`@`标识时，使用`""`来表示一个双引号`"`
>  - SQL字符串常量中用`''`来表示一个单引号`'`
>  - 正则表达式中使用`$$`来表示一个`$`

<!-- -->

> 参考链接：<http://blog.csdn.net/zhl71199713/article/details/19846571>

---

## `IIS“假死”`

IIS应用程序总是会有一段时间没有人访问，然后再打开的时候就会很慢的现象，即出现了“假死”现象  
这是因为应用程序池在一段时间的空闲之后就会被IIS自动回收，
然后再次访问的时候就需要重新启动线程，加载程序集，导致启动缓慢  
\
可以通过修改应用程序池的闲置超时时间来控制
 - 在**应用程序对应的应用程序池**上右键，选择`高级设置`
 - 高级设置页面`进程模型` --> `闲置超时（分钟）`，修改为1740

> 参考链接：<http://www.cnblogs.com/50614090/archive/2012/10/23/2735933.html>

---

## `Aspose.Pdf`合并PDF文件

使用`Aspose.Pdf`类库，有很多种方法可以合并PDF文件，这里简单介绍小生见到的几种：

 - `Doucment.Pages.Add`
 - `PdfFileEditor.Append`
 - `PdfFileEditor.Concatenate`

### `Doucment.Pages.Add`

要合并几个PDF文件，实际上就是把文档里的页合并到同一个文件里面，
所以可以打开PDF文件，简单的把其他文件的页面添加即可

```cs
Doucment pdfdoc1 = new Doucment("input.pdf");
Doucment pdfdoc2 = new Doucment("input.pdf");

pdfdoc1.Pages.Add(pdfdoc2.Pages);

pdfdoc1.Save("output.pdf");
```

### `PdfFileEditor.Append`

基本思路和上面是一样的，讲一个文件的页面添加到另一个文件末尾，
但是调用这个方法需要指定输入文件，要添加的文件，以及要添加的页数范围和输出文件

```cs
PdfFileEditor.Append(input, ports, startpage, endpage, output)
```

 - `input` 输入文件，可以是`String`类型的文件路径，也可以是`Stream`类型的文件数据流

 - `ports` 要添加的文件，可以是一个文件，也可以是一个数组，类型同`input`一样可以是`String`也可以是`Stream`

 - `startpage`和`endpage` 要添加的页数范围，这个范围是指所有`ports`放在一起的页数范围
   例如：`ports`有三个文件，分别有3页，4页，5页，指定`startpage=1`和`endpage=4`，
   则会添加第一个文件的所有页面和第二个文件的第一页

 - `output` 输出文件，同`input`，可以是`String`和`Stream`类型，在`ports`维数组时也可以是`HttpResponse`类型

```cs
PdfFileEditor pdfeditor = new PdfFileEditor();

// 将input2.pdf的第一页添加到input1.pdf末尾并输出output.pdf
pdfeditor.Append("input1.pdf", "input2.pdf", 1, 1, "output.pdf");

FileStream input1 = new FileStream("input1.pdf", FileMode.Open);
FileStream input2 = new FileStream("input2.pdf", FileMode.Open);
FileStream output = new FileStream("output.pdf", FileMode.Open);
pdfeditor.Append(input1, input2, 1, 1, output);

// 将input2.pdf、input3.pdf的前6页添加到input1.pdf末尾并输出output.pdf
String[] ports = new String[]{"input2.pdf", "input3.pdf"};
pdfeditor.Append("input1.pdf", ports, 1, 6, "output.pdf");

FileStream input1 = new FileStream("input1.pdf", FileMode.Open);
FileStream[] ports = new FileStream[]{
    new FileStream("input2.pdf", FileMode.Open),
    new FileStream("input3.pdf", FileMode.Open)
};
FileStream output = new FileStream("output.pdf", FileMode.Open);
pdfeditor.Append(input1, ports, 1, 6, output);

// 将结果输出到HTTP响应
pdfeditor.Append(input1, ports, 1, 6, HttpContext.Current.Response);
```

### `PdfFileEditor.Concatenate`

`Concatenate`方法与`Append`的调用方式类似，也支持一个或多个路径`String`或数据流`Stream`输入，
输出到一个路径`String`、数据流`Stream`或HTTP请求响应`HttpResponse`，
但是并不支持合并页数的指定，会将输入文件一个接着一个的合并，其重载列表如下

```cs
// 将两个文件合并成一个输出
Concatenate(Stream, Stream, Stream)
Concatenate(String, String, String)

// 多个文件合并成一个
Concatenate(Stream[], Stream)
Concatenate(Stream[], HttpResponse)
Concatenate(String[], String)
Concatenate(String[], HttpResponse)
Concatenate(Document[], Document)

// 前方高能
Concatenate(Stream, Stream, Stream, Stream)
Concatenate(String, String, String, String)
```

其中四个参数的重载方法，允许将两个文件交叉的合并成一个文件并用指定页填充空白页，
举例来说，加入input1.pdf有6页`p1, p2, p3, p4, p5, p6`，input2.pdf有3页`p1', p2', p3'`，
再加上空白页blank.pdf，则输出为`p1, p1', p2, p2', p3, p3', p4, blank, p5, blank, p6`，
注意这里因为没有`p4', p5'`所以使用`blank`页来代替

```cs
PdfFileEditor pdfeditor = new PdfFileEditor();
pdfeditor.Concatenate("input1.pdf", "input2.pdf", "blank.pdf", "output.pdf");
```

另外，因为小生的业务需求，需要在pdf合成完毕之后删除源文件，
所以就在执行完`Concatenate`方法后直接调用`File.Delete`方法删除文件，
但是却报错了，在看了API文档之后才了解到，需要设置
`PdfFileEditor.CloseConcatenateStreams = true;`，
在合成完毕之后，关闭`Stream`。

> 参考链接  
> [Concatenate PDF Files](http://www.aspose.com/docs/display/pdfnet/Concatenate+PDF+Files)  
> [Append PDF files](http://www.aspose.com/docs/display/pdfnet/Append+PDF+files)  
> [Concatenate PDF Files with Blank PDF Using File Paths (Facades)](http://www.aspose.com/docs/display/pdfnet/Concatenate+PDF+Files+with+Blank+PDF+Using+File+Paths+%28Facades%29)  
> [PdfFileEditor Class](http://www.aspose.com/api/net/pdf/aspose.pdf.facades/pdffileeditor)

---

## `Aspose.Pdf`合并图片到PDF文件

将图片和PDF文件合成为新的PDF文件，可以先将图片转换为PDF文件，
然后[合成PDF](#aspose.pdf合并pdf文件)即可，
将图片转换成PDF文件有如下方法：

 - `Aspose.Pdf.Document`
 - `Aspose.Pdf.Generator.Pdf`

### `Aspose.Pdf.Document`

一个PDF文档包含许多页面，而每个页面又是由多个段落构成，
段落可以是文本、图片、表格、悬浮框、图表、附件等，
所以把图片转换成PDF只要用段落将图片封装起来即可  

```cs
Document doc = new Document();
Page page = doc.Pages.Add();

// 创建Image对象，命名空间是必要的，因为在别的命名空间也有Image类
Aspose.Pdf.Image image = new Aspose.Pdf.Image();

// 设置Image数据源
// 如果是本地文件或Web图片，直接设置File属性即可
image.File = @"C:\test.jpg"; // "http://localhost/test.jpg"
// 如果是Stream类型，设置ImageStream属性
// image.ImageStream = stream;

// 添加图片到页面段落
page.Paragraphs.Add(image);

doc.Save(@"C:\outputtest.pdf");
```

### `Aspose.Pdf.Generator.Pdf`

与上述方法相同，只不过使用了`Section`而不是`Page`

```cs
Aspose.Pdf.Generator.Pdf pdf = new Aspose.Pdf.Generator.Pdf();
Aspose.Pdf.Generator.Section section = new Aspose.Pdf.Generator.Section(pdf);

// 创建Image，并设置数据源
Aspose.Pdf.Generator.Image image = new Aspose.Pdf.Generator.Image(section);
// 数据源的设置方式相同，只不过这次设置的是`Image.ImageInfo.File`和`Image.ImageInfo.ImageStream`属性
image.ImageInfo.File = "http://localhost/test.jpg";

section.Paragraphs.Add(image);
pdf.Sections.Add(section);

pdf.Save(@"C:\outputtest.pdf");
```

这两种方法的输出可以是到本地文件，也可以是`Stream`对象，
在配合[合成PDF](#aspose.pdf合并pdf文件)就可以实现图片和PDF的合并了

> 参考链接：
> [Convert an Image to PDF](http://www.aspose.com/docs/display/pdfnet/Convert+an+Image+to+PDF)
> [Working with Images (Generator)](http://www.aspose.com/docs/display/pdfnet/Working+with+Images+%28Generator%29)

---

## IE8下载报错`Internet Explorer无法下载...Internet Explorer无法打开该Internet站点`

IE8打开下载链接报错，在IE11下可以正常下载，报错如下：

```
Internet Explorer无法下载XXX(来自XXX.XXX.XXX.XXX)

Internet Explorer无法打开该Internet站点。请求的站点不可用，或找不到。请以后再试。
```

### 原因

如果任何一个或多个下列条件都为真，则可能发生此问题︰

 - Internet Explorer 6.0 SP1 中选中不将加密的页存盘复选框。
 - 服务器发送的"缓存控制:: 不存储"标头(Cache-Control: no-store)。
 - 服务器发送的"缓存控制:: 无缓存"标头。

### 解决办法

1. 客户端：注册表增加下列DWORD条目BypassSSLNoCacheCheck，值设置为1，  
   **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\BypassSSLNoCacheCheck**

2. 若无法修改客户端，可以通过修改服务端返回的HTTP请求头来修复，
   HTTP response Header中的`Cache-Control`和`Pragma`不能设置为`no-cache`
   小生用的APS.NET API，做的如下修改：

```
response.Header.Add("Cache-Control", "public");
```

> 参考链接：  
> [关于IE下用HTTPS无法下载/打开文件](http://www.51testing.com/html/65/160865-209104.html)  
> [KB812935 使用 HTTPS URL 打开的 Office 文档或 PDF 文件时出现"无法下载 Internet Explorer"错误信息](https://support.microsoft.com/zh-cn/kb/812935)  
> [KB815313 禁止缓存通过 SSL 下载活动文档时](https://support.microsoft.com/zh-cn/kb/815313)  
> [KB316431 PRB：Internet Explorer 无法从 SSL Web 站点打开 Office 文档](https://support.microsoft.com/zh-cn/kb/316431)

---

## EntityFramework使用SQLite数据库

EF6可以使用`System.Data.SQLite`库连接SQLite数据库，**但是并不能支持Code First功能**  

使用nuget安装`Install-Package System.Data.SQLite`会自动安装，然后会自动在配置文件中添加一些配置，
手动在配置中加入链接字符串，注意使用`providerName="System.Data.SQLite.EF6"`，
链接字符串中的`|DataDirectory|`表示`App_Data`文件夹：

```
<connectionString>
  <add name="SqliteTest" connectionString="data source=|DataDirectory|\SqliteTest.db" providerName="System.Data.SQLite.EF6" />
</connectionString>
```

这里需要注意，直接使用默认的配置文件会报错：

```
Unable to determine the provider name for provider factory of type 'System.Data.SQLite.SQLiteFactory'. 
Make sure that the ADO.NET provider is installed or registered in the application config.
```

需要做如下修改：

  1. `DbProviderFactories`节点下的**两个**`invariantName="System.Data.SQLite"`
     改为`invariantName="System.Data.SQLite.EF6"`
  2. `provider`节点下添加如下节点：
    
    ```
    <provider invariantName="System.Data.SQLite" type="System.Data.SQLite.EF6.SQLiteProviderServices, System.Data.SQLite.EF6" />
    ```

当然即使做了这些更改还是会报错`无法加载SQLite.Interop.dll`，
其实在安装的NuGet包中就含有`SQLite.Interop.dll`文件，在packages\System.Data.SQLite.Core.1.0.94.0\build文件夹下，
我们可以在bin文件夹的x64或者x86文件夹下找到对应版本，所以可以将程序的目标平台改为x86即可运行，
或者按照Any CPU的配置发布，配置在IIS中也是可以运行的。  
  
不过EntityFramework和SQLite用起来真的是心累啊。。。

> 参考链接：  
> <https://damienbod.com/2013/11/18/using-sqlite-with-entity-framework-6-and-the-repository-pattern/>
> <http://www.csdn123.com/html/topnews201408/51/4651.htm>

## EntityFramework使用Oracle数据库

nuget安装`Oracle.ManagedDataAccess`和`Oracle.ManagedDataAccess.EntityFramework`

```
PM> Install-Package Oracle.ManagedDataAccess
PM> Install-Package Oracle.ManagedDataAccess.EntityFramework
```

安装之后app/web.config中会多出很多配置，可以在
`oracle.manageddataaccess.client/version/dataSources`
中配置TNSName，然后在链接字符串中作为数据源使用

```
<connectionStrings>
    <add name="OracleDbContext" providerName="Oracle.ManagedDataAccess.Client"
        connectionString="User Id=hr;Password=hr;Data Source=SampleDataSource"/>
</connectionStrings>
...
<oracle.manageddataaccess.client>
    <version number="*">
        <dataSources>
            <!-- Customize these connection alias settings to connect to Oracle DB -->
            <dataSource alias="SampleDataSource" descriptor="(DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=ORCL))) " />
        </dataSources>
    </version>
</oracle.manageddataaccess.client>
```

在Code First创建数据库时可能会出现数据库方案`dbo`问题，在`DbContext.OnModelCreating`
方法中设置默认方案名即可`modelBuilder.HasDefaultSchema(“Schema名”);`

> 参考链接：  
> <http://www.cnblogs.com/wlflovenet/p/4187455.html>  
> <http://docs.oracle.com/cd/E56485_01/win.121/e55744/entityCodeFirst.htm#ODPNT8314>