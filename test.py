import os, re
import requests
from epub import Epub

def get_catalog(url):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    text = response.text.replace(' class=\"empty\"', '')
    catalog_regx = '<dd><a href=\"/(.*?)\"  >(.*?)</a></dd>'
    catalog_list = re.findall(catalog_regx, text, re.DOTALL)
    intro_regx = '<div id=\"intro\">(.*?)</div>'
    intro = re.findall(intro_regx, text, re.DOTALL)

    image_regx = '<div id=\"fmimg\"><img alt=\"(.*?)\" src=\"(.*?)\" width='
    image_src = re.findall(image_regx, text, re.DOTALL)[0][1]
    img = requests.get(image_src)
    with open('cover.jpg', 'wb') as f:
        f.write(img.content)
        f.flush()

    urls = []
    title = []
    for s in catalog_list:
        if '章' in s[1] or '第' in s[1]:
            urls.append(base_url + s[0])
            title.append(s[1])

    return urls, title, intro[0]

def get_chapter(url):
    response = requests.get(url, headers=headers)
    # print(response.apparent_encoding)
    # print('utf-8' in response.text)
    # response.encoding = response.apparent_encoding
    response.encoding = 'gbk'
    regx = '<div id=\"content\">(.*?)</div>'
    content = re.findall(regx, response.text, re.DOTALL)
    content = content[0].replace('&nbsp;', '').split('<br>')
    while '' in content:
        content.remove('')

    return content

def create_epub(url_list, title_list):
    epub = Epub('世子bu凶')
    epub.set_title('世子bu凶')
    epub.add_author('关关bu公子')
    epub.add_cover('cover.jpg')
    epub.add_intro(intro)

    for i, url in enumerate(url_list):
        chaper = get_chapter(url)
        id = os.path.split(url)[1].split('.')[0]
        epub.create_chapter(id, title_list[i], chaper, False)

    epub.create()

if __name__ == "__main__":
    base_url = 'https://www.biduoxs.com/'
    book_url = 'https://www.biduoxs.com/biquge/58_58121/'
    outname = '世子很凶.epub'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50',
    }

    urls, title, intro = get_catalog(book_url)
    # print(intro)
    create_epub(urls[:10], title[:10])
    # chapter = get_chapter(urls[20])
