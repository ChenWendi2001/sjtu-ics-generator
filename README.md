# SJTU_ics_generator
SJTU课程表日历导入脚本

## 什么是ics？
`.ics`可以帮助你快速导入批量事件到系统日历。使用本脚本将对`HTML`进行解析，生成`.ics`文件，帮助你将所有课程添加至你的mac/Win系统日历,可进一步与iPhone等智能设备同步。

## 如何使用?
### Step 0
使用本脚本你需要配置好`python3`环境，最好使用`chrome`浏览器。

### Step 1
使用`chrome`或者其他`chromium`内核浏览器进入`i.sjtu.edu.cn`，选择`信息查询`->`学生课表查询`，使用`ctrl+s`（Win）或者`command+s`保存`html`或`htm`文件。确保其文件名为`学生课表查询.html`，若文件后缀为`.htm`，请更改至`.html`。

### Step 2
下载`ics_generator.py`脚本，将其放置在`学生课表查询.html`文件的同一目录中。使用命令行切换至该目录，执行以下三条命令。按照提示即可完成转换。
```
pip3 install bs4
pip3 install ics
python3 ics_generator.py
```
### Step3
双击`sjtu.ics`文件即可导入日历。