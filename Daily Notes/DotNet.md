<link rel="stylesheet" href="../node_modules/bootstrap/dist/css/bootstrap.css">
<style>
    body {
        margin: 0 200px;
    }
    * {
        font-size: 16px;
    }
</style>

## `String.Format` “输入字符串格式不正确”

---

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


## `IIS“假死”`

---

IIS应用程序总是会有一段时间没有人访问，然后再打开的时候就会很慢的现象，即出现了“假死”现象  
这是因为应用程序池在一段时间的空闲之后就会被IIS自动回收，
然后再次访问的时候就需要重新启动线程，加载程序集，导致启动缓慢  
\
可以通过修改应用程序池的闲置超时时间来控制
 - 在**应用程序对应的应用程序池**上右键，选择`高级设置`
 - 高级设置页面`进程模型` --> `闲置超时（分钟）`，修改为1740

> 参考链接：<http://www.cnblogs.com/50614090/archive/2012/10/23/2735933.html>

## `Aspose.Pdf`合并PDF文件

---

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

> 参考链接  
> [Concatenate PDF Files](http://www.aspose.com/docs/display/pdfnet/Concatenate+PDF+Files)  
> [Append PDF files](http://www.aspose.com/docs/display/pdfnet/Append+PDF+files)  
> [Concatenate PDF Files with Blank PDF Using File Paths (Facades)](http://www.aspose.com/docs/display/pdfnet/Concatenate+PDF+Files+with+Blank+PDF+Using+File+Paths+%28Facades%29)  
> [PdfFileEditor Class](http://www.aspose.com/api/net/pdf/aspose.pdf.facades/pdffileeditor)  