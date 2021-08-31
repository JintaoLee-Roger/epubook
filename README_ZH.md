# Epubook

<table>
  <tr>
    <td><a href="./README.md">English</a></td>
    <td><b>中文</b></td>
  </tr>
</table>

一个创建epub格式电子书的工具，配合爬虫使用更舒适

`test.py`里面给出了一个例子，用来爬取 **世子很凶** 的前十章，并创建epub格式的电子书

> 此爬虫仅用于学习

使用方法：
```python
epub = Epub('filename') # 输入要保存的文件名，不要后缀，如: 世子bu凶

# 设置书籍名字, 可选, 默认为: 保存的文件名
epub.set_title('世子bu凶')

# 添加作者, 作者可以是多位, 可选, 默认为: "Unknow"
epub.add_author('关关bu公子')

# 添加书籍封面, 可选, 默认为无封面
epub.add_cover('cover.jpg')

# 添加书籍简介, 可选, 默认为: "No introduction"
intro = 'epubook is fine'
epub.add_intro(intro)

# 创建章节
for i, id in enumerate(id_list):
    chaper = get_chapter(i)
    epub.create_chapter(id, title_list[i], chaper, False)

# 创建
epub.create()

```