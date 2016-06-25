<link rel="stylesheet" href="../node_modules/bootstrap/dist/css/bootstrap.css">
<style>
    body {
        margin: 0 200px;
    }
    * {
        font-size: 16px;
    }
</style>

# C# 语言

---

## 运算符和类型强制转换

---

### 空合并运算符(??)

条件运算符的一种特殊情况(?:)，`a ?? 10`就等于`a == null ? 10 : a`

### 比较对象相等性

 1. `ReferenceEquals`静态方法，比较两个引用是否应用同一个实例（内存中的相同地址），**它认为null等于null**
 2. `Equals`虚拟方法，可以重写实现
 3. `Equals`静态方法，有两个参数表示比较的对象

     - 当两个参数都为null时，返回true
     - 当其中一个为null时，返回false
     - 当两个都不为null时，调用虚拟方法`Equals`

 4. `==`值类型比较值，引用类型比较引用，但是由于运算符重载，可以使引用类型比较值，如微软重写了String的`==`来比较字符串的值而不是引用

### 运算符重载

 1. 运算符的工作方式，编译器在遇到运算符时会根据运算符的操作数查找最佳的运算符重载方法调用，
    如果找不到，则可以通过隐式转换来查找匹配的方法，否则就会抛出异常

 2. 运算符重载形式如下：

    ```cs
    public static [ReturnType] operator + ([Type1] lhs, [Type2] rhs)
    // 运算符重载必须被声明为public static
    ```

    一般，若是[Type1]和[Type2]不是同一类型，则会再实现一个[Type1]为右操作数，[Type2]为左操作数的版本

    ```cs
    public static [ReturnType] operator + ([Type2] lhs, [Type1] rhs)
    {
        return rhs + lhs;
    }
    ```

 3. 可以重载的运算符：
     
     - 算术运算符： `+`，`-`，`*`，`/`，若重载了之后则无需重载其相应赋值运算符，如重载了`+`则编译器会自动执行对应的`+=`
     - 比较运算符：需要成对重载，共3对，`==`和`!=`，`>`和`<`，`>=`和`<=`，**在重载`==`和`!=`时还需要重载`Equals`和`GetHashCode`方法，否则会产生编译错误**
     - 按位运算符： `&`，`<<`，`>>`等

### 自定义强制类型转换

---

强制类型转换在某些情况下可以看做是运算符，其声明方式也与运算符类似

```
public static [implicit/explicit]  operator [TargetType]([SourceType] value)
```

强制类型转换必须在目标类型或源类型中定义，声明为`public static`，
若是目标类型和源类型之前存在继承关系，则不可定义强制类型转换，
派生类可以隐式的转换为基类（即是使用基类引用变量引用派生类实例），
但是基类不可以转换为派生类，若是想要达到这样效果，可以在派生类中定义一个以基类变量为参数的构造函数  

```cs
public class DerivedClass : BaseClass
{
    public DerivedClass(BaseClass bs)
    {
        // todo
    }
}
```

在类型转换时若没有直接可用的类型转换方法，则编译器会将多个强制转换方法拼接在一起来执行转换，
被称为多重影分身（当然是开玩笑的，叫多重强制转换）

## 委托、Lambda表达式和事件

---

### 委托

定义委托就是指定所要委托方法的方法签名，形式如下

```cs
delegate [ReturnType] [DelegateName]([ParameterType] [ParameterName], ... ...);
```

定义了一个委托就相当于定于了一个类，继承自`System.MulticastDelegate--System.Delegate`，
使用委托实例时，可以将方法作为参数使用new关键字调用构造函数实例化，
也可以直接将方法复制给对应的委托引用即可

```
delegate string GetString();

int x = 2;
// 以下两种写法是等价的
GetString one = new GetString(x.ToString);
GetString two = x.ToString;
```

 - `Action<T>`表示引用返回类型为void的委托，其参数列表可以至多为16个，`Action<T1, T2>`
 - `Func<T>`可以自定义至多16个传入参数和1个返回值，`Func<T1, T2, T3>`

委托可以包含多个方法，用`-`，`-=`，`+`或`+=`来为多播委托添加、删除方法，这种称为多播委托；
多播委托一般用于返回void的方法，若是包含带有返回值的方法，则在调用时只会返回最后一个方法的返回值

> **注意：**多播委托中方法的执行顺序并不固定，而且若是方法链中有一个方法执行报错抛出异常，
> 则方法链的执行就会终止，若是要避免这种问题就需要利用委托的`System.Delegate.GetInvocationList`方法，
> 获取方法链数组，逐一调用方法并处理委托
> 
> ```cs
>     public static int Main(string[] args)
>     {
>         Func<string, string> functions = One;
>         functions += Two;
> 
>         Delegate[] functionList = functions.GetInvocationList();
> 
>         foreach (Func<string, string> function in functionList)
>         {
>             System.Console.WriteLine(function("test input "));
>         }
> 
>         return 0;
>     }
> 
>     public static string One(string test)
>     {
>         return "this is test from One - " + test;
>     }
> 
>     public static string Two(string test)
>     {
>         return "this is test from Two - " + test;
>     }
> ```

### 匿名方法

匿名方法是编译器提供的一种快捷方式用来初始化委托，如下

```cs
static void Main()
{
    string second = " I love you, too. ";

    Func<string, string> anonymousDelegate = delegate(string param)
    {
        param += second;
        param += " I love you three!";
        return param;
    }

    Console.WriteLine(anonymousDelegate("I love you."));
}
```

编译器会把匿名方法转换成一个自动生成名称的方法，**并不会加快方法的执行速度**，

 - 匿名方法中可以访问方法外部的变量，但不能使用`out`和`ref`参数
 - 匿名方法中不能使用`break`，`goto`，`continue`等跳转语句跳转到方法内部

### Lambda表达式(.NET > 3.0)

Lambda表达式包含多条语句时应用`{}`和`return`

```
([ParameterName], ... ...) =>
{
    return ...
}
```

Lambda表达式也可以像匿名函数一样访问表达式外部的变量，称为闭包，
但是需要注意的是闭包的变量值是指Lambda表达式被调用时的变量值，而不是定义时，
实际上在编译器内部，是将Lambda表达式处理称为一个匿名类，
其构造函数用于传递外部变量，然后还有一个和Lambda表达式功能一样的方法，
然后在调用Lambda表达式时，实际上是用外部变量初始化了一个匿名类实例，然后调用方法

> foreach中的闭包  
> 编译器内部会将foreach语句转换为while循环，这时就需要一个循环变量指向集合中的当前项，
> 这个循环变量在C# 4中在循环外部定义，而在C# 5中在循环内部定义，
> 所以在循环体内对foreach循环中的当前项进行闭包时需要注意，
> 在C# 4中应该另外定义一个循环体内的局部变量来进行闭包，
> 否则，所有Lambda表达式中的外部变量会变成集合中的最后一项而不是闭包时的每一项

### 事件

事件定义需要有一个继承自`EventArgs`类的事件参数类，调用事件时传递相关数据

```cs
// 短记法
public event EventHandler<TEventArgs> [EventName];

// 长记法
private delegate EventHandler<TEventArgs> [delegateName];
public event EventHandler<TEventArgs> [EventName]
{
    add
    {
        [delegateName] += value;
    }
    remove
    {
        [delegateName] -= value;
    }
}
```

事件的侦听器定义时需要`object sender`和`TEventArgs e`两个变量，
一般第一个变量表示事件的发布者，第二个变量则表示相关数据  
\
发布者和侦听器之间可以通过`+=`的方法来连接，也可以通过弱事件模式进行连接，
前者的问题是当侦听器没有直接引用时，发布者仍有持有一个侦听器的引用，
除非显示的使用`-=`方法将侦听器从发布者之中移除，这就造成了垃圾回收的问题，
毕竟垃圾回收器只会回收没有任何引用的对象  
\
而通过弱事件模式的`WeakEventManager`作为连接中介就可以解决上述问题，
使用弱事件模式首先要实现一个继承自`WeakEventManager`的类，并实现

 1. 单例模式的`CurrentManager`变量

```cs
public static [TWeakEventManager] CurrentManager
{
    get
    {
        var manager = GetCurrentManager(typeof([TWeakEventManager])) as [TWeakEventManager];
        if(manager == null)
        {
            manager = new TWeakEventManager();
            SetCurrentManager(typeof([TWeakEventManager]), manager);
        }
        return manager;
    }
}
```

 2. `AddListener`和`RemoveListener`方法用于创建和移除发布者与侦听器之间的连接

```cs
public static void AddListener(object source, IWeakEventListener listener)
{
    CurrentManager.ProtectedAddListener(source, listener);
}

public static void RemoveListener(object source, IWeakEventListener listener)
{
    CurrentManager.ProtectedRemoveListener(source, listener);
}
```

 3. `StartListening`和`StopListening`方法用于设置发布者的事件变量，使用`DeliverEvent`方法

```cs
public override void StartListening(object source)
{
    (source as [Publisher]).[EventName] += DeliverEvent;
}

public override void StopListening(object source)
{
    (source as [Publisher]).[EventName] = DeliverEvent;
}
```

对于侦听器则需要实现`IWeakEventListener`接口，实现其`ReceiveWeakEvent`方法，
在方法内部调用事件处理程序，并返回`true`即可  

而在.NET 4.5中提供了泛型弱事件管理器`WeakEventManager<TEventSource, TEventArgs>`，
使用其`AddHandler`方法为发布者和侦听器建立连接即可，如下

```cs
WeakEventManager<TEventSource, TEventArgs>.AddHandler(TEventSource source,
    string eventName, Delegate eventHandler);
```

## 字符串和正则表达式

---

### 字符串

`String.IndexOfAny`和`String.LastIndexOfAny`方法可以用于一组字符串在某个指定字符串中出现的第一次和最后一次的位置  
\
`StringBuilder`可以提高追加字符串和替换单个字符的效率，删除或插入子字符串仍然效率低下，
故在拼接字符串时应该使用`StringBuilder`，
在执行`Console.WriteLine`方法格式化输出字符串时，实际上是调用了`String.Format`方法，
而`String.Format`方法先构建一个`StringBuilder`，
使用`StringBuilder.Append`方法添加格式化字符串中的固定部分，
使用`StringBuilder.AppendFormat`方法添加格式化字符串中的占位符部分(如`{0,10:E}`)  
\
格式化字符串形如：`{[index],[length]:[specifier]}`

 - `[index]`表示在后面参数数组中的位置
 - `[length]`表示字符串长度，负值左对齐，正值右对齐，少补多不切
 - `[specifier]`表示格式说明符，如`D`表示整数，`E`表示科学计数法等

也可以为自己的类指定格式化字符串，实现`IFormattable`接口，
在类中添加带有两个参数的`ToString`方法重载即可，
其中第一个参数表示格式说明符

```cs
public string ToString(string format, IFormatProvider formatProvider)
{
    // 当格式说明符为空时调用无参的ToString方法
    if (format == null)
    {
        return ToString();
    }
}
```

### 正则表达式

| 符号 | 含义 |
| ---- |:---- |
| `\s` | 任何空白字符 |
| `\S` | 任何不适空白的字符 |
| `\b` | 字边界 |
| `\B` | 任何不适字边界的字符 |

正则表达式匹配使用`Match`或`Matches`方法，结果为`Match`或`MatchCollection`对象，
每一个`Match`对象是指匹配整个正则表达式的部分，而这部分还可以在细分组，
在正则表达式中用`()`包裹的部分称为组，除了以`?:`开头的组（类似`(?: .... )`），
每个匹配中的组都存在`Match.Groups`对象中，这是一个`GroupCollection`对象，
每一个`Group`又可获取相应的捕获`Capture`  

> **注：**若是在匹配时仅仅想获得匹配的结果，而不需要相应的`GroupCollection`结果，
> 除了在组前加`?:`外，还可以在创建正则表达式时添加`RegExOption.ExplicitCaptures`方法