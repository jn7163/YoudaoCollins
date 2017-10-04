

# 有道柯林斯
[![Code Climate](https://codeclimate.com/github/upday7/YoudaoCollins/badges/gpa.svg)](https://codeclimate.com/github/upday7/YoudaoCollins)

Anki是很适合已经学习过的知识进行复习的，作者本人使用好几个英语工具选单词，这个插件就是用来导入单词到Anki的。

本插件使用了有道的Collins数据，为了尽量是卡片和记忆数据简单明了，插件仅仅抓取柯林斯的第一个英英释义，和第一个例句以及柯林斯星级。（第一个解释是主要的）

注：作者本人学习新词的方法就是背柯林斯的英英解释 ...

## 功能

总的来说，这个插件的功能就是从文本文件导入单词信息导入到Anki，目前支持：
1. 从文本文件（*.txt）导入。
2. 从有道单词本导入。
3. 从Kindle生词本导入。

## 版本
- 仅支持Anki v2.1.X [从这里下载](https://apps.ankiweb.net)

## 安装
1. 启动Anki
2. 在菜单上一次选择 *工具 > 附加组件*，点击 /[附加组件/]， 然后输入代码 [53580332](https://ankiweb.net/shared/info/53580332)
3. 重启Anki
## 菜单
安装成功后，“有道柯林斯”菜单就会出现在菜单栏了：
<br>

![](https://raw.githubusercontent.com/upday7/YoudaoCollins/master/data/screenshots/menu.png)


### 关于Anki Deck

#### 单词查询
本插件从[有道词典](http://youdao.com)查询单词信息:
- 单词
- 音标
- 柯林斯单词评级
- 柯林斯单词Rank
- （第一条）柯林斯英英释义
- 单词发音 (默认使用[柯林斯官网](https://www.collinsdictionary.com)，
如果不可用则使用有道)
- 有道默认中文释义
- （第一条）柯林斯例句原文
- （第一条）柯林斯例句翻译

    ![](https://raw.githubusercontent.com/upday7/YoudaoCollins/master/data/screenshots/fields.png)

#### 笔记类型模板
本插件提供一套默认模板以供大家使用，当第一次导入单词后，模板会被导入。

![](https://raw.githubusercontent.com/upday7/YoudaoCollins/master/data/screenshots/card.png)

### 导入
#### ** 选择源数据
##### - 从文本文件导入
文本内容包含英语单词，用换行符分开，读取后进行查询并导入。
##### - 从有道单词本导入
插件通过提供的账号信息从[有道单词本](http://dict.youdao.com/wordbook/wordlist)仅仅抓取单词信息储存为文本文件，然后进行查询并导入。
##### - 从Kindle生词本导入

*Kindle生词本的例句(单词所在的原文引用)会被导入为一条“例句”。*

- 保证你的Kindle已经功通过USB与电脑连接。
- Kindle的盘符名字必须为“Kindle”

插件会从Kindle上的System文件夹下访问单词本信息然后转换为文本进行查并导入。

#### ** 导入到Anki
当查询完成后，插件会调用Anki的导入功能(文件->导入)进行导入:
选择
- Type = "有道柯林斯"
- 分隔符为Tab
- 勾选允许HTML

![](https://raw.githubusercontent.com/upday7/YoudaoCollins/master/data/screenshots/import.png)


## 第三方
- 模板样式 [http://leaflyer.lofter.com](http://leaflyer.lofter.com)
