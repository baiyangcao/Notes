# Visual Studio Code 中利用 Task 实现Graphviz自动生成

今日在折腾使用graphviz构建脑图，使用VSCode作为编辑器，
虽然可以使用分屏达到“源码与脑图齐飞”的效果，
但是每次修改完成后必须手动执行命令生成图片，
才可以看到效果，让小生这个喜欢微调尝试的小屁孩倍感心累...   
  
故谷歌之，发现了VSCode的Task功能，于是乎，搞起来啊~~~  

## 创建task.json文件

首先`ctrl+shift+p`调出命令面板，输入`tasks`，
选择`Tasks: Confgure Task Runner`命令，在`选择任务程序`下拉列表中，
选择`Others`创建一个默认的`task.json`文件如下：

```
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "0.1.0",
    "command": "echo",
    "isShellCommand": true,
    "args": ["Hello World"],
    "showOutput": "always"
}
```

这就是一个VSCode Task的默认命令，万年不变的`Hello World`，其中:

 - `version`: 表示命令版本
 - `command`: 表示所要执行的命令，不带任何参数，并保证其可以在命令行下执行
 - `args`: 执行命令时所用的参数数组
 - `showOutput`: 命令执行结果的显示策略
    + `always`: 默认值，结果窗口总是显示
    + `never`: 从不显示结果窗口
    + `silent`: 静默状态，命令执行不报错则不显示结果窗口，反之显示

若想执行这个命令：

 - `ctrl+shift+p`调出命令面板，输入`tasks`
 - 选择`Tasks: Run Task`命令
 - 然后在弹出的下拉框中选择要执行的命令`echo`
 - 最后就可以看到弹出输出面板，显示`"Hello World"`

> 其实也可以直接在命令面板中输入`task echo`执行，注意要删除默认的`>`提示符

## 设置graphviz的生成命令

小生一般会生成png文件，使用命令：

```
> dot -Tpng [filename] -o [outputfile]
```

套用默认的`Hello World`例子的话，只要把`command`和`args`参数替换一下就可以了，
但是这里有个问题就是，命令中的源码文件`[filename]`
和输出文件`[outputfile]`应该如何设置？  
  
答案就是置换变量(Variable substitution)，使用`${var}`的格式来表示，
`${file}`表示当前打开的文件，
`${fileBasenameNoExtension}`表示当前打开文件名（不带扩展名），
如此一来我们的命令可以这样编辑：

```
{
    "version": "0.1.0",
    "command": "dot",
    "isShellCommand": true,
    "args": ["-Tpng", "${file}", "-o", "${fileBasenameNoExtension}.png"],
    "showOutput": "silent"
}
```

这样修改完成时候只要在命令面板中输入`task dot`即可以生成图片了