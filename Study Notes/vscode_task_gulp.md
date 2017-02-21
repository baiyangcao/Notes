# VSCode 中利用 Task 和 Gulp 实现保存时自动生成Graphviz

在上一个文章[# Visual Studio Code 中利用 Task 实现Graphviz自动生成](vscode_task.md)
中，实现了在Visual Studio Code中`ctrl+shift+B`构建后自动生成脑图图片的功能，
但是，小生又开始犯懒了，`ctrl+S`后`ctrl+shift+B`...如果能直接`ctrl+S`改多好，
于是乎，折腾之路再一次启程了，解决方案如下：

使用Gulp的监视功能来实现生成命令的执行；在`task.json`中配置构建时执行Gulp，
然后在Gulp中配置相应的生成命令和监视任务，用来监视`*.gv`文件的保存，
接着调用生成任务来生成Graphviz图片，以上。

## 安装Gulp/-spawn

安装Gulp和Gulp-spawn，其中Gulp-spawn用来执行生成命令：

```
npm install -g gulp
npm install gulp gulp-spawn
```

## 创建监视执行任务

在根目录下新建`gulpfile.js`文件，内容如下：

```
var gulp  = require('gulp')
var spawn = require('gulp-spawn')

// 生成图片任务
gulp.task('dot', function() {
	return gulp.src('*.gv')
		.pipe(spawn({
			cmd: 'dot'
			, args: ['-Tpng']
			, filename: function(base, ext) {
				return base+'.png'
			}
		}))
		.pipe(gulp.dest('.'))
})

// 文件监视任务
gulp.task('watch', function() {
	gulp.watch('*.gv', ['dot'])
})
```

## 设置VSCode任务

在`task.json`脚本中配置对应的构建任务：

```
{
    "version": "0.1.0",
    "command": "gulp",
    "isShellCommand": true,
    "tasks": [
        {
            "taskName": "watch",
            "isBuildCommand": true,
            "showOutput": "always",
            "isBackground": true
        }
    ]
}
```

其中`isBuildCommand`会在构建后执行gulp脚本启动监视程序，
`isBackground`保证任务会在后台运行，
如果不想每次保存都弹出输出的话，`showOutput`可以设置为`silent`

最后，就可以在`ctrl+shift+B`之后无限保存来生成Graphviz图片了~~~

> 参考链接:  
> <https://code.visualstudio.com/docs/editor/tasks>  
> <https://code.visualstudio.com/docs/languages/markdown#_automating-markdown-compilation>
> <https://gist.github.com/ukabu/9114366>