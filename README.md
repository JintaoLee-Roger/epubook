# Epubook

<table>
  <tr>
    <td><b>English</b></td>
    <td><a href="./README_ZH.md">中文</a></td>
  </tr>
</table>

A tool with python to create ebook in **EPUB** format.

`test.py` is an example to obtain the first ten chapters by web crawler, then 
create an ebook in EPUB format.

> This example is for learning purposes only.

### Usage
```python
epub = Epub('filename') # the file name to save without suffix, such as mybook

# set book's name, optional, default: the saved file name
epub.set_title('my book name')

# add an author, if there are two or more author, call this 
# function multiple times, optional, default: "Unknow"
epub.add_author('Roger')

# add book's cover image (input file's path), optional, default: No cover
epub.add_cover('cover.jpg')

# add book's introduction, optional, default: "No introduction"
intro = 'epubook is fine'
epub.add_intro(intro)

# create chapters
for i, id in enumerate(id_list):
    chaper = get_chapter(i)
    epub.create_chapter(id, title_list[i], chaper, False)

# create ebook in epub format
epub.create()

```