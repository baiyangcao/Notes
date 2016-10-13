# Anaconda使用入门

## 简介

 - `Conda`是一个开源的包、环境管理器，可以用于在同一个机器上安装不同版本的软件包及其依赖，并能够在不同的环境之间切换
 - `Anaconda`包括`Conda`、`Python`以及一大堆安装好的工具包，比如：`numpy`、`pandas`等
 - `Miniconda`包括`Conda`、`Python`  
  
一般我们下载使用的就是`Anaconda`，包括了基本的一些工具包，
`conda`就是用于管理包和环境的命令行工具，下面介绍一下其基本用法
  
  
## `conda`管理

```
# 确认conda已安装
conda --version

# 更新conda版本
conda update conda
```
其中更新命令不仅仅会更新conda的版本，同时会自动更新相关的包

## 环境管理

这里的环境指的是不同的软件版本及其依赖所构成的环境，
环境之间“绝缘”，相同软件包的不同版本可以存在于同一机器下  
  
```
# 创建新环境
conda create --name snowflakes biopython
```
其中snowflakes代指环境的名称，biopython指要在新环境中添加的软件包，
这里并没有指定新的环境所要使用的Python版本，所以会使用当前环境使用的Python版本

```
# 查看当前环境
conda info --envs
# conda environments:
#
# root                  *  C:\Program Files\Anaconda3
# snowflakes               C:\Program Files\Anaconda3\envs\snowflakes
```
上述命令会列出当前所有可用的环境及其路径，并在当前使用的环境前添加`*`  
  
root是在安装Anaconda时自动创建的环境名称，
其Python版本根据选择的Anaconda版本而定

```
# 创建环境时指定Python版本
conda create --name bunnies python=3 astroid babel
```
在创建环境指定软件包时，可以使用`package_name=version_number`
的方式来指定要使用的软件版本

```
# 切换环境
# Linux, OSX: 
# source activate snowflakes
#
# Windows:
activate snowflakes

# 切换回默认环境(root)
# Linux, OSX: 
# source deactivate
#
# Windows:
deactivate
```

其实，还可以复制一个和指定环境完全相同的环境，
只要在创建时添加`--clone`参数指定相应的环境名称即可

```
# 复制环境
conda create --name flowers --clone snowflakes
```

## 软件包管理

```
# 查看所有已安装的软件包
conda list
```
可用的完整软件包列表可以在<http://docs.continuum.io/anaconda/pkg-docs.html>中查找，
所有的软件包都按照Python的版本进行了分类  
  
当我们想要安装某个软件包时，可以直接在命令行中进行查找并安装

```
# 查找软件包
# 罗列出所有可用的版本并在已经安装的版本前加*
conda search beautifulsoup4

# 安装软件包
conda install --name beautifulsoup4=4.5.1
```

另外，也可以<http://anaconda.org>网站上搜索想要的软件包，
根据页面上的提示执行相应的命令即可安装  
  
最后，同样的可以使用`pip`命令来安装软件包

```
pip install XXX
```

## `python`管理

对于`conda`来说，其实python也是一个软件包，
所以，`python`的管理基本和软件包管理相同

```
# 查找可用python版本
conda search --full-name python
```
查找名称完全匹配python的软件包，而不是名称还有python的软件包，
可以在创建环境时指定python版本
```
conda create -n snakes python=3.4
```

## 卸载包、环境

```
# 卸载包
# 删除指定环境中的指定包
conda remove --name snowflakes biopython

# 卸载环境
# --all参数表示移除环境中的所有软件包，即删除整个环境
conda remove --name snakes --all
```


> 参考链接：<http://conda.pydata.org/docs/test-drive.html>