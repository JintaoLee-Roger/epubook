import os, shutil


class EpubBase():

    def __init__(self, path: str) -> None:
        self.title = os.path.split(path)[1].split('.')[0]
        self.author = []
        self.lang = 'zh-cn'
        self.intro = 'No introduction'
        self.cover_img_path = None

        self.path = path
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.meta_path = os.path.join(self.path, 'META-INF')
        if not os.path.exists(self.meta_path):
            os.mkdir(self.meta_path)
        # self.ops_path = os.path.join(self.path, 'OPS')
        # if not os.path.exists(self.ops_path):
        #     os.mkdir(self.ops_path)

    def set_title(self, title: str) -> None:
        self.title = title

    def add_author(self, author: str) -> None:
        self.author.append(author)

    def set_language(self, lang: str) -> None:
        self.lang = lang

    def add_intro(self, intro: str) -> None:
        ''' add introduction in page.xhtml file'''
        self.intro = intro

    def add_cover(self, img_name: str) -> None:
        if not os.path.exists(img_name):
            print(f"Image: {img_name} not exists!")
            exit(1)
        self.suffix = img_name.split('.')[1]
        self.cover_img_path = os.path.join(self.path, f'cover.{self.suffix}')
        shutil.copy(img_name, self.cover_img_path)
        if self.suffix == 'jpg':
            self.media_type = 'jpeg'
        elif self.suffix == 'svg':
            self.media_type = 'svg+xml'
        else:
            self.media_type = self.suffix

    def write_META_INF(self) -> None:
        content = '<?xml version=\"1.0\"?>\n' + \
            '<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">\n' + \
            '   <rootfiles>\n' + \
            '      <rootfile full-path=\"content.opf\" media-type=\"application/oebps-package+xml\"/>\n' + \
            '   </rootfiles>\n' + \
            '</container>'

        with open(os.path.join(self.meta_path, 'container.xml'),
                  'w',
                  encoding='utf-8') as f:
            f.write(content)

    def write_mimetype(self) -> None:
        content = 'application/epub+zip'
        with open(os.path.join(self.path, 'mimetype'), 'w',
                  encoding='utf-8') as f:
            f.write(content)

    def write_stylesheet(self) -> None:
        content = 'body{\n' + \
            '    margin:10px;\n' + \
            '    font-size: 1.0em;\n' + \
            '}\n' + \
            'ul,li{list-style-type:none;margin:0;padding:0;}\n' + \
            '\n' + \
            'p{text-indent:2em; line-height:1.5em; margin-top:0; margin-bottom:1.5em;}\n' + \
            '\n' + \
            '.catalog{line-height:2.5em;font-size: 0.8em;}\n' + \
            'li{border-bottom: 1px solid #D5D5D5;}\n' + \
            'h1{font-size:1.6em; font-weight:bold;}\n' + \
            '\n' + \
            'h2 {\n' + \
            '    display: block;\n' + \
            '    font-size: 1.2em;\n' + \
            '    font-weight: bold;\n' + \
            '    margin-bottom: 0.83em;\n' + \
            '    margin-left: 0;\n' + \
            '    margin-right: 0;\n' + \
            '    margin-top: 1em;\n' + \
            '}\n' + \
            '\n' + \
            '.mbppagebreak {\n' + \
            '    display: block;\n' + \
            '    margin-bottom: 0;\n' + \
            '    margin-left: 0;\n' + \
            '    margin-right: 0;\n' + \
            '    margin-top: 0 }\n' + \
            'a {\n' + \
            '    color: inherit;\n' + \
            '    text-decoration: none;\n' + \
            '    cursor: default\n' + \
            '    }\n' + \
            'a[href] {\n' + \
            '    color: blue;\n' + \
            '    text-decoration: none;\n' + \
            '    cursor: pointer\n' + \
            '    }\n' + \
            '\n' + \
            '.italic {\n' + \
            '    font-style: italic\n' + \
            '    }'
        with open(os.path.join(self.path, 'stylesheet.css'),
                  'w',
                  encoding='utf-8') as f:
            f.write(content)

    def write_page(self) -> None:
        authors = ", ".join(self.author) if self.author != [] else 'Unknow'
        content = '<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"no\"?>\n' + \
            '<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\" \"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">\n' + \
            '<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"zh-CN\">\n' + \
            '    <head>\n' + \
            '        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>\n' + \
            '        <title>书籍信息</title>\n' + \
            '        <style type=\"text/css\" title=\"override_css\">\n' + \
            '            @page {padding: 0pt; margin:0pt}\n' + \
            '            body { text-align: left; padding:0pt; margin: 0pt;font-size: 1.0em}\n' + \
            '            ul,li{list-style-type:none;margin:0;padding:0;line-height: 1.5em;font-size: 1.0em}\n' + \
            '            h1{font-size:1.5em}\n' + \
            '            h2 {font-size: 1.2em}\n' + \
            '		.copyright{color:#646464}\n' + \
            '        </style>\n' + \
            '    </head>\n' + \
            '    <body>\n' + \
            '        <div>\n' + \
            f'            <h1>{self.title}</h1>\n' + \
            f'            <h2>作者：{authors}</h2>\n' + \
            '        <ul><li><b>内容简介：</b></li>\n' + \
            f'            <li>{self.intro}</li>\n' + \
            '            <li><br/></li>\n' + \
            '            <li class=\"copyright\">Epub is created by <b>epubook</b></li>\n' + \
            '            <li class=\"copyright\">github: [<b><a href=\"https://github.com/JintaoLee-Roger/epubook\" target=\"_blank\">JintaoLee-Roger/crawler</a></b>]</li>\n' + \
            '        </ul>\n' + \
            '        </div>\n' + \
            '    </body>\n' + \
            '</html>'
        with open(os.path.join(self.path, 'page.xhtml'), 'w',
                  encoding='utf-8') as f:
            f.write(content)

    def write_toc_head(self) -> None:
        authors = ", ".join(self.author) if self.author != [] else 'Unknow'
        content = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n' + \
            '<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">\n' + \
            '<head>\n' + \
            '    <meta content=\"epubook:000000\" name=\"dtb:uid\"/>\n' + \
            '    <meta content=\"2\" name=\"dtb:depth\"/>\n' + \
            '    <meta content=\"epubook [https://github.com/JintaoLee-Roger/crawler]\" name=\"dtb:generator\"/>\n' + \
            '    <meta content=\"0\" name=\"dtb:totalPageCount\"/>\n' + \
            '    <meta content=\"0\" name=\"dtb:maxPageNumber\"/>\n' + \
            '</head>\n' + \
            '<docTitle>\n' + \
            f'    <text>{self.title}</text>\n' + \
            '</docTitle>\n' + \
            '<docAuthor>\n' + \
            f'    <text>{authors}</text>\n' + \
            '</docAuthor>\n' + \
            '<navMap>\n'
        with open(os.path.join(self.path, 'toc.ncx'), 'w',
                  encoding='utf-8') as f:
            f.write(content)

    def write_catalog_head(self) -> None:
        content = '<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"no\"?>\n' + \
            '<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\" \"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">\n' + \
            '<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"zh-CN\">\n' + \
            '<head>\n' + \
            '    <title>目录</title>\n' + \
            '    <link href=\"stylesheet.css\" type=\"text/css\" rel=\"stylesheet\"/>\n' + \
            '    <style type=\"text/css\">\n' + \
            '        @page { margin-bottom: 5.000000pt; margin-top: 5.000000pt; }\n' + \
            '    </style>\n' + \
            '</head>\n' + \
            '<body>\n' + \
            '    <h1>目录<br/>Content</h1>\n' + \
            '    <ul>\n'
        with open(os.path.join(self.path, 'catalog.xhtml'),
                  'w',
                  encoding='utf-8') as f:
            f.write(content)

    def write_opf_head(self) -> None:
        authors = ", ".join(self.author) if self.author != [] else 'Unknow'
        content = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n' + \
            '<package xmlns=\"http://www.idpf.org/2007/opf\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" unique-identifier=\"bookid\" version=\"2.0\">\n' + \
            '<metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:opf=\"http://www.idpf.org/2007/opf\">\n' + \
            f'    <dc:title>{self.title}</dc:title>\n' + \
            f'    <dc:creator>{authors}</dc:creator>\n' + \
            f'    <dc:description>{self.title}</dc:description>\n' + \
            '    <dc:language>zh-cn</dc:language>\n' + \
            '    <dc:date>2020-05-14T12:42:30+08:00</dc:date>\n' + \
            '    <dc:contributor>Roger Lee</dc:contributor>\n' + \
            '    <dc:publisher>epubook</dc:publisher>\n' + \
            '    <dc:identifier id=\"bookid\">epubook:000000</dc:identifier>\n'

        if self.cover_img_path is not None:
            content = content + '    <meta name=\"cover\" content=\"cover-image\"/>\n'
        content = content + '</metadata>\n' + \
            '\n' + \
            '<manifest>\n'

        with open(os.path.join(self.path, 'content.opf'),
                  'w',
                  encoding='utf-8') as f:
            f.write(content)


if __name__ == "__main__":
    EpubBase('.').write_page('Test', ['svlier'], 'testetstetse hdhsd 但是')
