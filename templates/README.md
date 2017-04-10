## 概述

笔记记录库，包括[日常笔记](https://github.com/baiyangcao/Notes/tree/master/Daily%20Notes)，[读书笔记](https://github.com/baiyangcao/Notes/tree/master/Book%20Notes)，[学习笔记](https://github.com/baiyangcao/Notes/tree/master/Study%20Notes)等

### 日常笔记

日常工作中遇到问题及相关知识学习的锦集，包括如下几个方面：

 - [DotNet](Daily%20Notes/DotNet.md)
 - [JavaScript](Daily%20Notes/Javascript.md)
 - [Oracle](Daily%20Notes/Oracle.md)
 - [Linux](Daily%20Notes/Linux.md)
 - [其他](Daily%20Notes/Other.md)

### 读书笔记

工作生活中阅读的技术相关书籍的笔记，备忘录等

 - [C# 高级编程（第8版）](Book%20Notes/Professional%20C%23%208th%20Edition.md)
 - 利用Python进行数据分析

### 学习笔记

通过网络等相关途径自学技术的笔记

{% for note in notes %}
 - [{{ note.text }}]({{ note.url }})
{% endfor %} 