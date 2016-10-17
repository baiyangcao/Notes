# argparse 使用指南

argparse是Python标准库中推荐使用的命令行解析模块，
其前身是optparse库，从Python 2.7开始，optparse库被弃用，
替代它的就是argparse库，除此之外，标准库中的getopt库也提供了相似的功能。  
  
一个命令行的工具应该满足以下几个要求：

 - 命令可以不带任何参数运行，即提供默认参数
 - 可以提供指定参数覆盖默认值
 - 提供一小段帮助文档，可以通过命令直接获取

## 基本使用

首先从一个不带任何参数的脚本开始，新建一个脚本，输入以下内容：

```python
# argtest1.py

import argparse
parser = argparse.ArgumentParser()
parser.parse_args()
```

接着来测试一下脚本

```python
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

