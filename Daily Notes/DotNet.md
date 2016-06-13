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