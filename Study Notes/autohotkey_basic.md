# AutoHotKey 快速入门

AutoHotKey 是一个免费的键盘宏程序，可以用于配置键盘快捷键、鼠标事件
以及摇杆事件，还可以在输入文本的时候对文本进行扩展（自动补全）

## 第一个脚本

新建文件`test.ahk`并输入以下内容：

```
^!n::
  Run, notepad
Return
```

保存文件，双击执行，可以在右下角看到脚本执行的图标，
然后按下`Ctrl`+`Alt`+`N`就可以打开记事本程序。  
  
AutoHotKey 快捷键命令大概可以分为三个部分：

 - `::`左边的部分表示需要按下的快捷键，`^`表示`Ctrl`，`!`表示`Alt`
 - `::`右边部分表示需要执行的命令
 - 最后`Return`表示结束命令

另外除了快捷键(HotKey)配置， AutoHotKey 还可以配置 HotStrings，
相当于我们平时使用的 IDE 中的文本自动补全功能  
  
在电脑右下角的脚本执行图标上右键，单击“编辑脚本”，
会弹出一个记事本程序来编辑当前运行的脚本，加入如下内容：

```
::hw::Hello World!
```

保存文件，关闭编辑器，在右下角脚本图标上右键，单击“重新加载脚本”，
然后来测试一下脚本功能，首先`Ctrl`+`Alt`+`N`打开记事本，
输入`hw`，按下`Enter`或`Tab`就会进行自动补全，用`Hello World!`替换`hw`。  

## 特殊符号

像`^`表示`Ctrl`这种快捷键中的特殊符号，意义如下：

| 符号 | 意义 |
| ---- | ---- |
| # | Win（键盘上有Windows图标的键） |
| ! | Alt |
| ^ | Ctrl |
| + | Shift |

我们除了可以像上面的一样定义全局快捷键之外，
另外还有一些用于Windows的特殊命令，可以用于定义特定窗口的快捷键，如:

 - `#IfWinActive`表示窗口是否处于激活状态，可以用于指定在特定窗口下可用的快捷键，
   如下脚本表示在`Untitled - Notepad`窗口中按下`Win+P`按键会弹出窗口
   提示“你按下了Win+P”
   
   ```
   #IfWinActive Untitled - Notepad
   #space::
     MsgBox, 你按下了Win+P
   Return
   #IfWinActive
   ```

 - `#IfWinExist`表示窗口是否存在

## 发送按键 - `一键当千`

快捷键后的命令部分除了执行命令运行程序之外，还可以向电脑发送按键单击事件，
就相当于 AutoHotKey 帮你去按下按键，从而获取按下一个快捷键相当于一堆按键。  
  
```
LCtrl::
  Send, AutoHotKey
Return
```

上述命令表示按下左边`Ctrl`按键时会发送按键，依次按下`AutoHotKey`，
对于键盘上的一些特殊按键，如`Ctrl`等都有对应的表示，如：`^`表示`Ctrl`，
`!`表示`Alt`等等，除了这种类似快捷键特殊符号的表示，还可以使用`{...}`的方式来
表示，如：`{lAlt}`表示左边的`Alt`键，`{F1}-{F24}`表示键盘上的`F1`到`F24`键等。  
  
```
; 按下Win+H就等于按下Ctrl+Alt+HOME键
#h::
  Send, ^!{HOME}
Return
```

其实，除了`^`、`!`、`+`、`#`可以表示组合键之外，
其他的`{...}`形式的符号都只是按顺序敲击键盘罢了，
比如：`^{HOME}`表示按下`Ctrl`的同时按下`HOME`键，
而`{Ctrl}{HOME}`则表示按下`Ctrl`松开，然后按下`HOME`键。  
  
若是想要实现组合键的功能，可以使用`{Ctrl Down}`和`{Ctrl Up}`这种组合，
表示按下和松开`{Ctrl}`键，在这两个之间的符号都会在**按住**`Ctrl`的情况下执行。
也就是说：`^{HOME}` = `{Ctrl Down}{HOME}{Ctrl Up}` != `{Ctrl}{HOME}`

> 注：支持的Send键列表见[官方文档](https://autohotkey.com/docs/commands/Send.htm)，
> 但是要注意的是除了官方文档提供的按键可以使用`{...}`形式，
> 其他的按键都不可以使用，如`{a}`就是一种错误的表达方式

另外，Send后的部分可以分多行以便于阅读，只要用括号括起来就可以：

```
^j::
  Send,
    (
      Line 1
      Line 2
      A dobe
    )
Return
```

> 参考链接：  
> <https://autohotkey.com/docs/Tutorial.htm>