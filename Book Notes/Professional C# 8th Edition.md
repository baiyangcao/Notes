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

## 集合

---

#### 列表

```cs
List : IList, ICollection, IEnumerable, IList<T>, ICollection<T>, IEnumerable<T>
```

 - `List<T>.ForEach(Action<T> action)`

 - 删除元素使用`RemoveAt`，用索引删除比较快，而`Remove`方法先调用`IndexOf`搜索元素索引再删除

 - `FindIndex,FindLastIndex,Find,FindAll`参数类型为`Predicate<T>`，这是一个委托类型
```cs
public delegate bool Predicate<T>(T obj);
```   
   用于判断列表中的某个元素是否符合要求

 - 排序方法`Sort`使用快速排序算法对列表进行排序 
```cs
// 只有实现了IComparable接口的类可以调用无参Sort
public void Sort();
// 委托方法：public delegate int Comparison<T>(T x, T y)
public void Sort(Comparison<T>);
// 实现IComparer<T>接口，实现Compare(T, T)方法
public void Sort(IComparer<T>);
public void Sort(Int32, Int32, IComparer<T>);
```

 - `List<T>.ConvertAll<TOutput>`方法实现类型转化，参数为`Convert`委托
```cs
public sealed delegate TOutput Convert<TInput, TOutput>(TInput);
```

#### 队列

```cs
Queue<T> : ICollection, IEnumerable<T>
```

 - Enqueue: 入队
 - Dequeue: 出队，元素从队列中删除
 - Peek: 读取队列头部元素，但不删除

#### 栈

```cs
Stack<T> : ICollection, IEnumerable<T>
```

 - Push: 入栈 
 - Pop: 出栈，元素从栈中删除
 - Peek: 读取栈顶元素但不删除

#### 链表

```cs
LinkList<T>
```

 - First/Last: 链表头/尾
 - AddAfter/AddBefore/AddFirst/AddLast: 指定位置插入
 - Remove/RemoveFirst/RemoveLast: 指定位置删除
 - Find/FindLast: 从链表头/尾开始查找

```cs
LinkListNode<T>
```

 - List: LinkList<T>
 - Next/Previous: 前/后一个节点
 - Value: 当前节点

#### 字典

```cs
Dictionary<TKey, TValue>
```

作为字典中的键类型必须重写`GetHashCode`方法，满足如下要求：

 - 相同对象总是返回相同值
 - 不同对象可以返回相同值
 - 执行快，开销小
 - 不能抛出异常
 - 至少使用一个实例字段
 - 哈希值应平均分布在`int`整个数字范围内
 - 哈希值最好在对象生成周期内不变

> 字典的性能取决于`GetHashCode`方法的实现代码  
> 可以使用`string`或`int`类型的`GetHashCode`方法来获取哈希值

#### Lookup

```cs
Lookup<TKey, TElement>
```

将键值映射到集合上，只能通过`IEnumerable<T>.ToLookup(Func<TSource, TKey>)`方法来返回，
其中委托`Func<TSource, TKey>`用于筛选键值，键值相同的会放到同一个集合中，类似分组方法

#### 集

```cs
HashSet<T>, SortedSet<T> : ISet<T>, ICollection<T>
```

 - ISubSetOf/ISuperSetOf: 超集和子集验证
 - UnionWith: 合并集合

#### 可观察集合

```cs
ObservableCollection<T> : Collection<T>
```

该类中重写`SetItem`和`RemoveItem`方法，来触发`CollectionChanged`事件

#### 位数组

 - `BitArray` 可以重新设置大小，灵活
 - `BitVector32` 基于栈，速度快，但只有32位，存在一个整数中

### 并发集合

`System.Collection.Concurrent`命名空间中`IProducerConsumerCollection<T>`接口
用于实现集合线程安全访问，定义了`TryAdd`和`TryTake`方法

 - `ConcurrentDictionary<TKey, TValue>`: 提供`TryAdd/TryGetValue/TryRemove/TryUpdate`
   方法以非阻塞方式访问成员
 - `BlockCollection<T>`

     + `Add/Take(T)`: 在操作完成之前会一直阻塞线程直到完成
     + `Add/Take(T, CancellationToken)`: 可以使用令牌来取消操作
     + `TryAdd/TryTake`: 可以在方法中指定超时时间，表示调用失败之前应阻塞线程的最长时间


## LINQ

---

编译器会转换LINQ查询语句来调用方法，`System.Linq.Enumerable`类为`IEnumerable<T>`接口提供了各种扩展方法，
如`where`方法的实现代码如下：

```cs
public IEnumerable<T> Where<T>(
    this IEnumerable<T> source,
    Func<T, bool> predicate)
{
    foreach(T item in source)
    {
        if (predicate(item))
            // 返回IEnumerable类型时可以使用yield return 语句
            yield return item;
    }
}
```

LINQ查询是在对查询结果进行迭代或使用`ToArray`、`ToList`方法时才会执行，而不是在定义的时候执行

#### 查询操作符

 - `Where((item, index) => {})` 带有两个参数的扩展方法，第二个参数表示索引

 - `OfType<TResult>` 根据类型筛选，只返回`TResult`类型的元素

 - `SelectMany` 从“集合的集合”[指集合中的每一项都包含一个集合]中进行选择，定义如下

```cs
public static IEnumerable<TResult> SelectMany<TSource, TCollection, TResult>(
    this IEnumerable<TSource> source,
    // 选出“集合的集合”
    Func<TSource, IEnumerable<TCollection>> collectionselector,
    // 针对每一个“集合中的集合”来选择结果
    Func<TSource, TCollection, TResult> resultselector
);
```

 - `ThenBy/ThenByDescending` 在`OrderBy/OrderByDescending/ThenBy/ThenByDescending`
   之后调用，用于多个字段排序

 - `GroupBy` = group [item] by [item.field] into g，返回`IGourping`对象，
   使用`IGourping.Key`值来表示分组字段[item.field]值

 - 内连接 `from item1 in collection1 join item2 in collection2 on item1.field1 equals item2.field2`

 - 左外链接

```cs
from item1 in collection1
join item2 in collection2 on item1.field1 equals item2.field2 into collection3
from item3 in collection3.DefaultIfEmpty()
```

 - 组合链接

```cs
from item1 in collection1
join item2 in collection2
on new { Field1 = item1.field1, Field2 = item1.field2 }
equals new { Field1 = item2.field1, Field2 = item2.field2 }
```

 - `Distinct`去重 `Union`并集 `Intersect`交集 `Except`茶几（差集）

 - `Zip` 两个集合中一一对应合并，如果两个集合长度不同，以最小的为准

 - (`Take` => Top `Skip` 跳过) => 分页

 - 聚合函数返回一个值，`Count/Max/Min/Sum/Average/Aggregate`

 - `IEnumerable.Range/Empty/Repeat`

### 并行LINQ 

 - `IEnumerable.AsParallel` 并行执行，多个CPU，效率高

 - 手动创建分区器

```cs
System.Collection.Concurrent.Partitioner.Create(IList) // 手动创建分区器
.WithExecutionMode(ParallelExecutionMode.Default)
.WithDegreeOfParallelism(4) // 并行运行的最大任务数
.AsParallel()
```

 - 取消查询 `IList.AsParallel().WithCancellation(CancellationTokenSource.Token)`
   在想要取消查询时调用`CancellationTokenSource.Cancel`方法即可，不过查询会抛出一个
   `OperationCanceledException`异常

#### 表达式树

完全看不懂的说，大概就是说可以解析Lambda表达式吧。。。


## 动态扩展语言

---

### dynamic类型

dynamic类型可以让编译器忽略类型检查，假定dynamic对象上的任何操作都是有效的，
在编译器内部在运行期间使用`System.Runtime.ComplierServices.CallSite`类来查找操作类型，
并缓存其信息，然后调用`System.Runtime.ComplierServices.CallSiteBinder`类来绑定操作，
从`CallSite`中提取信息，生成表达式树

### DLR ScriptRuntime

可以在代码中运行别的脚本语言的脚本，如`Python`,`Ruby`,`JavaScript`

```cs
// 1. 创建脚本运行时
ScriptRuntime scriptruntime = ScriptRuntime.CreateFromConfiguration();

// 2. 获取脚本引擎
ScriptEngine pyEngine = scriptruntime.GetEngine("Python");

// 3. 创建执行作用域/命名空间
ScriptScope scope = pyEngine.CreateScope();

// 4. 创建脚本对象
ScriptSource source = pyEngine.CreateScriptSourceFromFile(path);

// 以上四步为规定动作，下面开始自选动作
// 设置变量
source.SetVariable("count", 1);
// 执行脚本
source.Execute(scope);
// 获取变量
int output = source.GetVariable("output");
```

#### DynamicObject

用于编写自己的动态类的基类，需要重写下面三个方法

```cs
// 获取字段值
public bool TryGetMember(GetMemberBinder binder, out object result);
// 设置字段值
public bool TrySetMember(SetMemberBinder binder, object value);
// 调用方法
public bool TryInvokeMember(InvokeMemberBinder binder, object[] args, out object result);
```

#### ExpandoObject

另一个创建自定义动态对象的方法就是使用`ExpandoObject`类

```cs
dynamic expobject = new ExpandoObject();
expobject.Field1 = 2;
Func<int, int, int> add = (a, b) => a + b;
expobject.Add = add;
expobject.Add(1, 2); // 3
```