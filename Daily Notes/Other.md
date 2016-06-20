<link rel="stylesheet" href="../node_modules/bootstrap/dist/css/bootstrap.css">
<style>
    body {
        margin: 0 200px;
    }
    * {
        font-size: 16px;
    }
</style>

## `SQL Server`中`LEN`函数不包含尾随字符串

---

`SQL Server`中的`LEN`函数用于计算字符串中所含的字符数，
但是不包含尾随的空格数

```sql
LEN('1234') -- 4
LEN('1234   ') -- 4
```

## `ArcSDE缓冲区调整`

---

以下引用自南京郭局发来的SDE调优文档

> ArcSDE缓冲参数均位于其系统表`SERVER_CONFIG`中，ArcSDE数据库创建时其参
> 数来自配置文件`giomgr.defs`，该文件位于`$SDEHOME\etc`目录下。
> 不可直接修改`SERVER_CONFIG`表中内容，必须通过`$SDEHOME\bin\sdeconfig.exe`程序将该表导出，
> 用文本编辑器编辑完成后再导入。  
> \
> ArcSDE的大部分缓冲参数都已优化，需要调整的参数只有`MINBUFFSIZE`和`MAXBUFFSIZE`，
> 这两个参数决定了系统加载数据的性能。`MINBUFFSIZE`和`MAXBUFFSIZE`定义的是每一个数据流缓冲的大小，
> 每加载一个图层增加一个数据流。对于输配电应用，调整这两个参数的目的主要是加快图形背景数据的加载速度，
> 而不是电网图层的加载速度（因为电网本身的数据量和背景相比很小）。  
> \
> `MINBUFFSIZE`决定缓冲必须具备的最低限额，即低于最低限额ArcSDE服务器进程将不传送数据到客户端。
> 与此对应还有另外一个参数，`MINBUFOBJECTS`，该参数决定缓冲中的最少对象数，
> 如果缓冲中对象数没有达到`MINBUFOBJECTS` 定义的限额，ArcSDE服务器进程也不向客户端传送数据。
> 缓冲中，这两个参数的任何一个达到即可向客户端传送数据，
> 系统优先检查`MINBUFOBJECTS` 是否达到。该参数太大将增加客户端的等待时间，
> 太小将增加服务器与客户端的数据传送次数，从而提高网络数据交换时间，因此需要谨慎设置这两个参数。
> 该参数初始值为16KB。  
> \
> `MAXBUFFSIZE`决定每个数据流缓冲最大值，该值如果设置太大可能导致系统内容不足，
> 将大量数据转入虚拟内容，系统性能反而降低。如果设置值太小，将提高数据库I/O操作次数，
> 也降低系统性能。因此，该参数也必须谨慎设置。该参数初始值为64KB，
> 向SDE导入大量数据时将该参数调大可以提高数据导入速度，导入完毕后还原即可。
> `MINBUFFSIZE`和`MAXBUFFSIZE`设置的总原则为：
> ```
> `MINBUFFSIZE`< `MAXBUFFSIZE`*0.5
> ```
> 鉴于目前的输配电应用，可以将`MAXBUFFSIZE`设置为256KB，`MINBUFFSIZE`设置
> 为64KB，`MINBUFOBJECTS` 不变。

基于上述说明，结合沈阳基础地理数据量大的问题，决定将`MINBUFFSIZE`值修改为`256KB(221184)`，
`MAXBUFFSIZE`值修改为`512KB(442368)`

 1. 导出config文件
 
```
sdeconfig -o export -f serverconfig.txt -u sde -p sde
```

 这会在当前目录生成一个serverconfig.txt文件，里面包含SDE的配置参数

 2. 修改配置参数，用文本编辑器打开serverconfig.txt文件，修改参数值，如下

```
...
MINBUFFSIZE    221184
MAXBUFFSIZE    442368
...
```

 3. 导出修改后的配置

```
sdeconfig -o import -f serverconfig.txt -u sde -p sde
```

## `ArcCatalog`预览要素类`Network I/O error [SDE.GDB_UserMetaData]`

---

在ArcCatalog中预览要素类，因为要素类中的数据量太大，绘制缓慢，
此时来回切换图层，报错`Network I/O error [SDE.GDB_UserMetaData]`  
\
怀疑是数据库中的数据由问题，便将数据库中的要素类导出到本地GDB文件地理数据库中，
然后使用`数据管理工具--要素--修复几何`工具对每一个图层进行修复，会分析并修复数据问题，
如：删除图形为空的要素等；修复完成后将数据拷贝回数据库，再切换便不会报错了

## `Excel`下拉列表设置

---

 1. 选择要设置下拉列表的单元格，菜单栏中选择`数据--数据验证`

 2. 在打开的`数据验证`窗口的`设置`标签页`验证条件--允许`下拉选项选择`序列`

 3. 然后在`来源`中输入下拉列表选项，可以是如下几种形式：

     - 单击输入框后的按钮在Excel表中选择数据来源范围
     
     - 直接定义列表，形如：item1,item2,item3...

     - 输入列表名称，形如：=MyList，其中列表名称可以在`公式--名称管理器`中查看，
       可以通过在表格中选择数据来源范围，然后单击`公式--根据所选内容创建`来创建列表