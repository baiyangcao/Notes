<link rel="stylesheet" href="../node_modules/bootstrap/dist/css/bootstrap.css">
<!--<script type="text/javascript" src="../node_modules/jquery/dist/jquery.min.js"></script>
<script type="text/javascript" src="../node_modules/bootstrap/dist/js/bootstrap.min.js"></script>-->


# Pandoc中的Markdown语法

## 概述

Pandoc中支持扩展修订版本的Markdown语法

 - 使用pandoc中支持的Markdown语法用 `-f markdown`
 - 使用标准Markdown语法用 `-f markdown_strict`

Pandoc所支持的语法各种对标准Markdown语法的扩展可以通过在格式后以`+EXTENSION`添加或`-EXTENSION`去除，如：

 - `-f markdown-footnotes` 表示识别除了footnotes扩展之外的所有pandoc Markdown语法
 - `-f markdown_strict+footnotes+pipe_tables` 表示识别标准Markdown语法加上footnotes和pipe_tables扩展语法

## 段落

段落是指一个或多个空行之后的多行文本，文本中的换行都被视作空格，
如若要输出换行，则应在行末添加两个或多个空格

> **注：** 段落之后也应加一个空行，以区分段落和其他部分，如：列表  
> 
> 如下Markdown语法
> ```
> 这是一个段落
>  - 列表项1
>  - 列表项2
> ```
> 翻译成HTML如下：
> ```
> 这是一个段落  - 列表项1  - 列表项2
> ```
> 
> 若要正确的显示列表应在段落后添加一个空行，如下：
> ```
> 这是一个段落
> 
>  - 列表项1
>  - 列表项2
> ```

#### Extension: `escaped_line_breaks`

也可以通过在行末添加一个反斜线`\`来换行，如：

```
这是第一行\
这是第二行
```

> **注：** 这是在表格单元格中添加换行的唯一形式

## 标题

Pandoc中支持两种标题语法：Setext和ATX

### Setext风格语法

setext风格标题是一行文本下跟一行`=`符号（表示一级标题）和`-`符号（表示二级标题），
文本中可以包含如*斜体*、**加粗**等行内格式

```
一级标题
=======

二级标题
-------
```

### ATX风格语法

ATX风格标题就是我们通常所用的Markdown标题语法，在行首添加一到六个`#`符号表示不同级别的标题，编译成对应的html标签`<hn>`，
如一个`#`表示一级标题，会编译成HTML标签`<h1>`，与setext风格相同，文本中可以包含如*斜体*、**加粗**等行内格式

#### Extension: `blank_before_header`

标准Markdown语法并不要求在标题前添加一个空行，但是Pandoc语法却要求标题前添加一个空行（除了文档开头）

### 标题标识符(Header identifiers)

可以通过在标题行末添加如下形式的标识符来为标题添加属性：

```
{#identifier .class .class key=value key=value}
```

`identifier`会被编译成html文档中的`id`属性，
`class`会被合并成html文档中的`class`属性

#### Extension: `auto_identifiers`

没有显示指定`identifier`的标题会根据标题内容自动分配一个唯一标识，
标题文本生成`identifier`的顺序如下：

 1. 移除格式、连接等
 2. 移除脚注(footnotes)
 3. 移除除了下划线`_`和连接符`-`之外的标点符号
 4. 用连接符`-`替换所有空格和换行符
 5. 将所有字母转换成小写
 6. `identifier`不能以数字和标点符号开头
 7. 如果文本此时为空，则取`section`做标识符

> 如果自动生成的标识符相同则根据顺序在标识符后添加`-1`、`-2`等

#### Extension: `implicit_header_references`

Pandoc默认每个标题都定义了引用链接，故对于标题`# 标题1`，
可以使用`[标题1]`或者`[标题1][]`引用，注意，引用链接是区分大小写的

## 块引用

块引用是指一个或多个段落或其他块元素（如列表或标题），每一行以一个`>`符号和一个可选的空格开头
（`>`符号并不需要在行首，但是不可缩进超过三个空格）

```
> 块引用
> 段落
> 
> 1. 列表1
> 2. 列表2 
```

块引用并不是每一行都需要以`> `符号开头，只需在每一个区域的首行添加`> `即可，
如下文本和上述的文本有相同的效果

```
> 块引用
段落

> 1. 列表1
2. 列表2 
```

> **注**
> 
> 1. 块引用可以嵌套使用
> 2. `>`后的空格作为块引用标识的一部分，若是在块引用中添加代码，
>    则需在`>`后添加五个空格

#### Extension: `blank_before_blockquote`

标准Markdown语法并不要求在块引用前添加一个空行，
但是Pandoc语法却要求在块引用前添加一个空行（除了文档开头外）

## 代码块

### 缩进式代码块

由四个空格或一个tab缩进的文本取做代码块，区块中的特殊字符、空格和换行都会被保留，
而缩进的空格和tab会在输出中移除，但在代码块中的空行不必缩进

```
    using System;

    public class Program
    {
        public static void Main() 
        {
            Console.Write('Hello World!');
        }
    }
```

### 围栏式代码块

#### Extension: `fenced_code_blocks`

除了标准的缩进式代码块之外，Pandoc还支持围栏式代码块，
代码块以三个或三个以上的`~`符号行开始，以等于或多于开始行`~`个数符号行结束，
若是代码块中含有`~`，只需使开始行和结束行中的`~`符号个数多于代码块中的即可

    ~~~~~
    ~~~~
    code here
    ~~~~
    ~~~~~~

#### Extension: `backtick_code_blocks`

与`fenced_code_blocks`相同，只不过使用反引号`` ` ``替换波浪线`~`而已

#### Extension: `fenced_code_attributes`

与标题标识符相同，在波浪线或反引号代码块的首行添加属性即可，如下：

    ~~~ { #id .cs .numberLines }
    using System;
    
    public class Program
    {
        public static void Main() 
        {
            Console.Write('Hello World!');
        }
    }
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如上代码中添加的`cs`类可以用于代码HTML和LaTex输出的代码高亮，
pandoc所支持高亮的语言可以通过在命令行中输入`pandoc --version`查看，
除了上述方式设置代码块的高亮语言，也可通过如下方式设置

    ```cs
    using System;
    
    public class Program
    {
        public static void Main() 
        {
            Console.Write('Hello World!');
        }
    }
    ```

## 行文本块

#### Extension: `line_blocks`

行文本块是指一系列由`|`和一个空格开头的行，在输出中可以保留空格和换行，
不会像段落那样将换行符转换成空格，可用于诗文和地址的排版

```
| 咏梅
| 啊！梅花
|   红
| 
|       霜
```

## 列表

### 无序列表

列表项以星号`*`、加号`+`或减号`-`开头，如下：

```
 * 列表项1
 * 列表项2
 * 列表项3
```

这样输出的列表是“紧凑”型的列表，若是要输出“宽松”型列表，
可在列表项之间添加空行即可

```
 * 列表项1

 * 列表项2

 * 列表项3
```

`四空格原则`

一个列表项里可以包含多个段落或其他块级别内容，
但是其次的段落都应该以一个空行和四个空格缩进开始

```
  * 列表项1 第一段落

    列表项1 第二段落

  * 列表项2 第一段落

        { code }
```

列表中可以嵌套列表，每一层嵌套列表都需要添加四个空格或一个tab缩进，
并且每一层应该使用不同的起始符

```
 * 1.1
     + 1.1.1
        - 1.1.1.1
        - 1.1.1.2
     + 1.1.2
 * 1.2
```

### 有序列表

有序列表项以数字、一个点`.`和一个空格开头，
并且取第一个列表项数字为基准，依次向下排，故下面两个列表是一样的

```
**列表1**

 1. 一
 2. 二
 3. 三

---

**列表2**

 1. 一
 5. 二
 9. 三

```

#### Extension: `fancy_lists`

不像标准Markdown语法只能使用阿拉伯数字作为有序列表标识，
Pandoc中还支持大小写字母、罗马数字，或用括号、右括号标识列表项，
但其后的文本需与列表标识隔开至少一个空格，
若是一个大写字母和一个点做标识，则需在其后跟两个空格  
  
`fancy_lists`扩展还支持使用`#`来代替数字

```
 #. 列表项1
 #. 列表项2
```

#### Extension: `startnum`

Pandoc支持自定义的列表起始数字，而且会在每次使用不同的列表标识便重新开始一个新列表，
如下会创建三个列表

```
 (3) 列表1项1
 (7) 列表1项2
  1. 列表2项1
  *  列表2项1 
```

### 定义列表

#### Extension: `definition_lists`

```
名词1

:    解释1
一个名词

    名词

:   解释2
```

定义列表形式如上，术语独占一行，其后可以跟一个空行，然后是一个或多个定义，
每一个定义以`:`和`~`开头，可以缩进一到两个空格  

一个术语可以包含多个定义，一个定义可以包含多个区块（段落、代码块、列表等），
而每一个区块都应以四个空格或一个tab缩进  

### 编号列表

#### Extension: `example_lists`

特殊的列表标识符`@`用于连续编号列表，整个文档中的`@`符号从`1`开始编号，
依次类推，如下的前三个`@`会分别替换为`1`, `2`, `3`

```
(@)  My first example will be numbered (1).
(@)  My second example will be numbered (2).

Explanation of examples.

(@)  My third example will be numbered (3).


(@good)  This is a good example.

As (@good) illustrates, ...
```

`@`后可以加上一个字符串来表示一个标签，用于在其他地方引用这个序号，
如上例中的`@good`会被`4`来替换

## 紧凑和宽松列表

若列表项前插入一个空行，则会将当前列表项作为段落处理（用`<p>`标签包裹），
从而输出“宽松”的列表，反之则会输出“紧凑”的列表

## 截断列表

```
 1. 列表1项1
 2. 列表1项2

 1. 列表2项1
 2. 列表2项2
```

如上想要输出两个列表，却会输出一个有四项的列表，
要想“截断”列表1，则可在两个列表之间插入一行没有缩进的行，如HTML注释

```
 1. 列表1项1
 2. 列表1项2

<!-- -->

 1. 列表2项1
 2. 列表2项2
```

## 水平线

一行由三个或三个以上`*`、`-`或`_`组成的会输出一个水平线

## 表格

Pandoc中支持`simple_tables`, `multiline_tables`, `grid_tables`和`pipe_tables`四种表格

#### Extension: `table_captions`

四种表格都可以通过在表格前或后添加一个以`Table:`（或`:`）开头的段落表示表格的表头

#### Extension: `simple_tables`

简单的表格形如下

```
  Right     Left     Center     Default
-------     ------ ----------   -------
     12     12        12            12
    123     123       123          123
      1     1          1             1

Table:  简单表格实例
```

列首行和表格中的每一行都应独占一行，
列对齐方式由列头和其下虚线行的相对位置决定：

 - 右对齐： 虚线行与列头右对齐，而左端超过列头
 - 左对齐： 虚线行与列头左对齐，而右端超过列头
 - 居中： 虚线行超出列头两端
 - 默认： 虚线行与列头两端对齐（一般情况下默认是左对齐）

表格必须以一个空行或一行虚线行加一个空行结束，
而且有时可以忽略列头行

> **注：** 中文环境不推荐使用这种方式选择对齐方式，反正小生是玩不好>_<

#### Extension: `multiline_tables`

跨行表格允许列首行和表格中的行可以分多行撰写，但是不支持单元格的跨行和跨列，
跨行表格必须以一行虚线行开始，以一行虚线行和一个空行结束，行与行之间应有一个空行

```
-------------------------------------------------------------
 Centered   Default           Right Left
  Header    Aligned         Aligned Aligned
----------- ------- --------------- -------------------------
   First    row                12.0 一个行跨
                                    多行的例子

  Second    row                 5.0 这是另一行
                                    注意表格行与行
                                    之间的空行哦~~
-------------------------------------------------------------

Table: 这个是标题
也能跨行的啦~~
```

跨行表格的列首行也可以被忽略，
也可以只包含一行，但是这一行后必须跟着一个空行

#### Extension: `grid_tables`

网格表格中列首行与其他行需要使用一行`=`隔开，但是在没有列首行的表格中可以忽略，
网格表格中的单元格可以包含任意区块（段落、代码块、列表等），
但对其方式和单元格的跨行跨列都是不支持滴~

```
: 网格表格样例

+---------------+---------------+--------------------+
| Fruit         | Price         | Advantages         |
+===============+===============+====================+
| Bananas       | $1.34         | - built-in wrapper |
|               |               | - bright color     |
+---------------+---------------+--------------------+
| Oranges       | $2.10         | - cures scurvy     |
|               |               | - tasty            |
+---------------+---------------+--------------------+
```

#### Extension: `pipe_tables`

```
| Right | Left | Default | Center |
|------:|:-----|---------|:------:|
|   12  |  12  |    12   |    12  |
|  123  |  123 |   123   |   123  |
|    1  |    1 |     1   |     1  |

  : `pipe_tables`表格样例
```

`pipe_tables`每一列之间用竖线`|`隔开，列首行和其余行之间用虚线行隔开，
虚线行中用冒号`:`来决定列的对其方式，
表格中两端的`|`竖线列可以忽略，而且`|`只是用来隔开列，而不必对齐，
但是`pipe_tables`的列首行不能忽略，要是想要生成没有列首的表格，
只要在列首行的单元格置空便可

```
 | 
-----|-----:
苹果|2.05
梨 |1.37
橘子 |3.09
```

> **注：** `pipe_tables`中的单元格不可包含如段落、列表等区块元素

## 反斜线转义符

#### Extension: `all_symbols_escapable`

除了在代码块和行内代码中，反斜线后的任何字符和空格都会按照字面输出，
Markdown语法中能被转义的字符如下

```
\`*_{}[]()>#+-.!
```

## 行内格式

### 强调

用一对`*`或`_`包裹起来的文本会被输出为斜体，
而用一对`**`或`__`包裹起来的文本会被输出为加粗

```
强调文本：这里是*斜体*,这里是**加粗**
```

若是`*`或`_`符号前后有空格，或用`\`转义，
则不会输出为斜体或加粗

```
这里 * 不会被翻译成斜体 *, 而且 \*这里也不会\*.
```

#### Extension: `intraword_underscores`

文本中的成对`_`不会被翻译成斜体，
若是想强调文本中部分的文本，可以使用`*`

### 删除线

#### Extension: `strikeout`

一对`~~`所包裹的文本会添加一条删除线

```
~~这个文本被删除了~~
```

### 上标和下标

#### Extension: `superscript`, `subscript`

上标可以通过一对`^`标识，而下标可以通过一对`~`标识，
若上下标中包含空格，可以通过`\`转义空格

```
H~2~O
2^10^ = 1024
P~a\ cat~
```

### 行内代码块

小段的行内代码块可以使用一对`` ` ``包裹，
而行内代码块中含有反引号`` ` ``，可以用双反引号包裹代码块，
但是行内代码块中的转义符`\`没有转义的作用

```
这是一个`行内代码块`
这是一个行内代码块的反引号`` ` ``
这是一个行内代码块的反斜线`\`
```

#### Extension: `inline_code_attributes`

与[代码块](#extension-fenced_code_attributes)一样，行内代码块后写可以添加属性，形式如下：

```
`行内代码块`{ #identifier .class key=value }
```

## HTML代码

#### Extension: `raw_html`

可以直接在文档中插入HTML代码（除了代码块等`<`, `>`和`&`符不会被翻译的地方之外）

#### Extension: `markdown_in_html_blocks`

使用`markdown_strict`格式的时候，HTML代码中的Markdown语法不会被翻译，
但是使用Pandoc的Markdown格式`markdown`格式时，HTML代码中的Markdown语法也会被翻译，
但是有一个例外，HTML代码`<script>`和`<style>`标签中的Markdown语法也不会被翻译

## 链接

如果用尖括号包裹一个URL或email地址，就会输出一个链接：

```
<http://google.com>
<sam@green.eggs.ham>
```

### 行内链接

行内链接文本由方括号`[]`包裹，其后跟URL链接用圆括号`()`包裹，
圆括号内的URL后可以用双引号`"`包裹一串字符串作为链接标题，

```
这是 [行内链接](链接地址), 并且这是 [一个
带有标题的行内链接](http://fsf.org "链接标题，鼠标悬停时显示")
```

Email的链接地址应该跟在`mailto`后面

```
[给我邮件哦~~](mailto:sam@green.eggs.ham)
```

### 引用链接

**显示引用链接**包含链接和链接定义两部分，
链接定义可以出现在文档其他部分，链接之前或之后皆可  
\
链接由方括号`[]`包裹的连接文本和由方括号`[]`包裹的连接标签组成

```
[链接文本1][Label1]
[链接文本2][Label2]
```

链接定义由方括号`[]`包裹的链接标签、冒号、空格和
链接地址（可以用尖括号`<>`包裹）组成，
其后还可以跟空格+链接标题，由单引号`'`, `"`或圆括号`()`包裹

```
[Label1]: http://www.baidu.com "百度一下"
[Label2]: http://www.google.com
    "谷歌一下" 
```

> **注：** 链接标签不区分大小写

**隐式引用连接**链接中的连接标签部分为空，
而链接定义中的链接标签由链接文本替换

```
详情见[官方网站][]

[官方网站]: http://guanfangwangzhan.com
```

#### Extension: `shortcut_reference_links`

隐式引用链接中的空方括号`[]`可以忽略

### 内部链接

可以使用identifier来链接到文档中的其他章节，
链接地址形如`#identifier`

```
见[标题](#标题)

见[标题]
[标题]: #标题
```

### 图片

如果链接前添加`!`，链接则会被作为图片处理，
而链接文本则会被作为图片的`alt`属性处理

```
![月亮](月亮.jpg "十五的月亮")
```

#### Extension: `implicit_figures`

若是图片作为一个独自的段落存在，则图片的连接文本会被当做标题处理

```
![这是标题](图片地址.png)
```

但若是想要将图片作为一般的行内图片处理，只需确保图片不是当前行的唯一内容即可，
比如在行末添加一个反斜线

```
![这个就不是标题了~~](图片地址.png)\
```

#### Extension: `link_attributes`

链接或图片后可以像其他元素一样添加属性
`{ #identifier .class key=value }`

```
行内图片 ![图片](地址.png){ #id .class width=20 }
和一个带属性的[引用链接]

[引用链接]: http://www.baidu.com "百度一下" { #id2 .class key=value }
```

## 脚注

#### Extension: `footnotes`

```
Here is a footnote reference,[^1] and another.[^longnote]

[^1]: Here is the footnote.

[^longnote]: Here's one with multiple blocks.

    Subsequent paragraphs are indented to show that they
belong to the previous footnote.

        { some.code }

    The whole paragraph can be indented, or just the first
    line.  In this way, multi-paragraph footnotes work like
    multi-paragraph list items.

This paragraph won't be part of the note, because it
isn't indented.
```

脚注的identifier不可包含空格，tab或换行，
在输出中脚注会按照顺序编号，如上例中的`[^longnote]`会被编号`2`，
脚注虽不必一定放在文档的末尾，但也不可以出现在其他的区块中（如列表、块引用、表格等）
