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

#### 空合并运算符(??)

条件运算符的一种特殊情况(?:)，`a ?? 10`就等于`a == null ? 10 : a`

#### 比较对象相等性

 1. `ReferenceEquals`静态方法，比较两个引用是否应用同一个实例（内存中的相同地址），**它认为null等于null**
 2. `Equals`虚拟方法，可以重写实现
 3. `Equals`静态方法，有两个参数表示比较的对象

     - 当两个参数都为null时，返回true
     - 当其中一个为null时，返回false
     - 当两个都不为null时，调用虚拟方法`Equals`

 4. `==`值类型比较值，引用类型比较引用，但是由于运算符重载，可以使引用类型比较值，如微软重写了String的`==`来比较字符串的值而不是引用

#### 运算符重载

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

#### 自定义强制类型转换

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