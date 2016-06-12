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