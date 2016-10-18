# argparse 使用指南

argparse是Python标准库中推荐使用的命令行解析模块，
其前身是optparse库，从Python 2.7开始，optparse库被弃用，
替代它的就是argparse库，除此之外，标准库中的getopt库也提供了相似的功能。  
  
一个命令行的工具应该满足以下几个要求：

 - 命令可以不带任何可选参数运行，即提供默认可选参数
 - 可以提供指定可选参数覆盖默认值
 - 提供一小段帮助文档，可以通过命令直接获取

## 基本使用

首先从一个不带任何参数的脚本开始，新建一个脚本，输入以下内容：

```python
# argtest1.py

import argparse
parser = argparse.ArgumentParser()
parser.parse_args()

# ----------------
# 测试脚本
# ----------------

# 直接执行命令没有任何作用
$ python argtest1.py

# --help参数显示基本用法
$ python argtest1.py --help
usage: argtest1.py [-h]

optional arguments:
  -h, --help  show this help message and exit

# 提供错误的可选参数
$ python argtest1.py --verbose
usage: argtest1.py [-h]
argtest1.py: error: unrecognized arguments: --verbose

# 提供错误的位置参数
$ python argtest1 foo
usage: argtest1.py [-h]
argtest1.py: error: unrecognized arguments: foo
```

从上面可以看出，argparse模块提供了两个个基本功能：

 - `--help`或`-h`参数显示基本用法
 - 对于错误的位置参数或可选参数给出提示

> 注：这里的位置参数就相当于函数中的位置参数和关键字参数

## 参数添加

为命令行工具添加参数可以使用`ArgumentParser.add_argument`方法，
然后可以在脚本中调用`ArgumentParser.parse_args`方法获取脚本执行时设置的参数值

```python
ArgumentParser.add_argument(name or flags...
  [, action][, nargs][, const][, default][, type]
  [, choices][, required][, help][, metavar][, dest]) 
```

函数原型如上，参数含义分别为（其中加粗的参数为将会涉及到的）：

 - **`name or flags`**: 位置参数的名称（如：*foo*）或可选参数的标识（如：*-f, --foo*）
 - **`action`**: 参数出现在命令行中所要执行的操作类型，可以理解为如何读取参数
 - `nargs`: 当前参数可以从命令行中读取几个参数值，如为一个参数指定多个值
 - **`const`**: `action`或`nargs`所使用的一个常量值
 - **`default`**: 当参数在命令行中不存在时的默认值，**注意，这里是不存在时的默认值，而不是没有指定值时的默认值**
 - **`type`**: 参数的数据类型，可以用来对命令行参数进行数据检查，默认读取的参数值都是字符串
 - **`choices`**: 参数的可选值列表
 - `required`: 参数是否必须，对于位置参数来说，默认为True，而可选参数默认值为False
 - **`help`**: 参数简介，会在`-h/--help`指令下显示出来
 - `metavar`: 在用法简介帮助信息里的参数名称
 - `dest`: 参数在`ArgumentParser.parse_args`方法返回值中的属性名

接下来就来分别看一下位置参数与可选参数的使用方法

### 位置参数

```python
# argtest2.py

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('square', help='计算给定值的平方值', type=int)
args = parser.parse_args()
print(args.square**2)

# ----------------
# 测试脚本
# ----------------

$ python argtest2.py -h
usage: argtest2.py [-h] square

positional arguments:
  square      计算给定值的平方值

optional arguments:
  -h, --help  show this help message and exit

$ python argtest2.py 4
16

# 给出错误类型的参数
$ python argtest2.py four
usage: argtest2.py [-h] square
argtest2.py: error: argument square: invalid int value: 'four'
```

### 可选参数

```python
# argtest3.py

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', 
  help='控制输出的可见性', action='store_true')
args = parser.parse_args()
if args.verbose:
  print('可见性打开')

# ----------------
# 测试脚本
# ----------------
$ python argtest3.py -v
可见性打开

$ python argtest3.py
```

 - 添加可选参数的时候，可以提供一个短参数选项(-v)和一个长参数选项(--verbose)，也可以省略短参数
 - `action='store_true`表示参数值储存为True，即在命令行中提供参数时`parser.parse_args`获取的参数值为True，否则为False

### 同时使用位置参数、可选参数

```python
# argtest4.py

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('square', type=int, help="计算给定值的平方值")
parser.add_argument('-v', '--verbose', type=int, choices=[0, 1, 2], 
  default=0, help="如何显示输出结果")
args = parser.parse_args()
answer = args.square**2

if args.verbose >= 2:
  print('{}的平方值是{}'.format(args.square, answer))
elif args.verbose >=1:
  print('{}^2 = {}'.format(args.square, answer))
else:
  print(answer)

# ----------------
# 测试脚本
# ----------------

$ python argtest4.py --help
usage: argtest4.py [-h] [-v {0,1,2}] square

positional arguments:
  square                计算给定值的平方值

optional arguments:
  -h, --help            show this help message and exit
  -v {0,1,2}, --verbose {0,1,2}
                        如何显示输出结果

$ python argtest4.py -v 0 4
16

$ python argtest4.py 4
16

$ python argtest4.py -v 1 4
4^2 = 16

$ python argtest4.py -v 2 4
4的平方值是16
```

## 冲突选项

有些选项的作用相反，不可以同时使用，为了加上这样的限制，
可以使用`ArgumentParser.add_mutually_exclusive_group`方法

```python
# argtest5.py

import argparse

parser = argparse.ArgumentParser(description='计算给定基数的幂')
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', action='store_true')
group.add_argument('-q', '--quiet', action='store_true')
parser.add_argument('x', type=int, help='基数')
parser.add_argument('y', type=int, help='幂数')
args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print('{}的{}次幂等于{}'.format(args.x, args.y, answer))
else:
    print('{}^{} = {}'.format(args.x, args.y, answer))

# ----------------
# 测试脚本
# ----------------

$ python argtest5.py -h
usage: argtest5.py [-h] [-v | -q] x y

计算给定基数的幂

positional arguments:
  x              基数
  y              幂数

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
  -q, --quiet

$ python argtest5.py 4 2
16

$ python argtest5.py 4 2 -q
16

$ python argtest5.py 4 2 -v
4的2次幂等于16

$ python argtest5.py 4 2 -qv
usage: argtest5.py [-h] [-v | -q] x y
argtest5.py: error: argument -v/--verbose: not allowed with argument -q/--quiet
```

> 参考链接： <https://docs.python.org/3/howto/argparse.html>