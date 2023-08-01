import os, glob, re
import shutil, zipfile
from typing import List
from utils import EpubBase


class Epub(EpubBase):

    def __init__(self, path: str, resume=False):
        super(Epub, self).__init__(path)
        self.catalog = {}  # {id:title}
        if resume:
            self.resume()

    def resume(self) -> None:
        """ 
        resume from an existed dir, obtain chapters' id and title,
        fill self.catalog
        """
        l = glob.glob(os.path.join(self.path, 'chapter_*.xhtml'))
        l = sorted(l, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        for f in l:
            cid = int(f.split('_')[-1].split('.')[0])
            with open(f, 'r') as _f:
                title = re.findall('<title>(.*?)</title>', _f.read())[0]
            self.catalog[cid] = title

    def create_chapter(self,
                       cid: int,
                       title: str,
                       text: str or List[str],
                       html: bool = True,
                       full: bool = False) -> None:
        ''' create a chapter from text.
        
        The text can be \n
        (1) normal content text, i.e. a full chapter in string, set html=False;\n 
        (2) a string list, each element is a paragraph of a chapter;\n
        (3) xhtml text, it can be text from a completed XHTML file (set html=True, full=True),
        or text without XHTML head, meta, just keep body, such as 
        "<p>para1</p><p>para2<\p>" (html=True, full=False, default settings)

        Args:
            cid: chapter id in opf file, ncx file
            title: chapter name
            text: content
            html: if True, text in html format, default is True
            full: if True, text can be created a full XHTML file
        '''
        self.catalog[cid] = title
        chapter = EpubChapter(title)

        if isinstance(text, list) or not html:
            content = chapter.from_text(text)
        else:
            content = chapter.from_html_text(text, full)

        with open(os.path.join(self.path, f'chapter_{cid}.xhtml'),
                  'w',
                  encoding='utf-8') as f:
            f.write(content)

    def chapter_from_file(self, cid: str, title: str, filename: str) -> None:
        ''' create a chapter from a XHTML file

        Args:
            cid: chapter id in opf file, ncx file
            title: chapter name
            filename: XHTML file path
        '''
        if not os.path.exists(filename):
            print(f'File: {filename} not exists!')
            exit(1)
        self.catalog[cid] = title
        shutil.copy(filename, os.path.join(self.path, f'chapter_{cid}.xhtml'))

    def create(self, clean: bool = True) -> None:
        ''' create a epub file

        Args:
            clean: if True, delete temp file (unzip epub file can obtain it), default True
        '''
        self.write_META_INF()
        self.write_opf()
        self.write_page()
        self.write_catalog()
        self.write_mimetype()
        self.write_stylesheet()
        self.write_toc()
        self.compression(clean)

    def compression(self, clean: bool = True) -> None:
        file_list = os.listdir(self.path)
        z = zipfile.ZipFile(self.path + '.epub', 'w', zipfile.ZIP_DEFLATED)
        z.write(os.path.join(self.path, 'mimetype'),
                'mimetype',
                compress_type=zipfile.ZIP_STORED)
        file_list.remove('mimetype')
        for f in file_list:
            if not os.path.isdir(os.path.join(self.path, f)):
                z.write(os.path.join(self.path, f), f)
            else:
                fs = os.listdir(os.path.join(self.path, f))
                z.write(os.path.join(self.path, f, fs[0]),
                        os.path.join(f, fs[0]))
        if clean:
            shutil.rmtree(self.path)

    def write_opf(self) -> None:
        ''' write content.opf file'''
        self.write_opf_head()
        cont1 = '    <item href=\"catalog.xhtml\" id=\"catalog\" media-type=\"application/xhtml+xml\"/>\n' + \
            '    <item href=\"stylesheet.css\" id=\"css\" media-type=\"text/css\"/>\n' + \
            '    <item href=\"page.xhtml\" id=\"page\" media-type=\"application/xhtml+xml\"/>\n' + \
            '    <item href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\" id=\"ncx\"/>\n' + \
            '</manifest>\n' + \
            '\n' + \
            '<spine toc=\"ncx\">\n' + \
            '    <itemref idref=\"page\"/>\n' + \
            '    <itemref idref=\"catalog\"/>\n'
        with open(os.path.join(self.path, 'content.opf'),
                  'a',
                  encoding='utf-8') as f:
            for cid in self.catalog.keys():
                f.write(
                    f'    <item href=\"chapter_{cid}.xhtml\" id=\"{cid}\" media-type=\"application/xhtml+xml\"/>\n'
                )
            if self.cover_img_path is not None:
                f.write(
                    f'    <item id="cover-image" href="cover.{self.suffix}" media-type="image/{self.media_type}"/>\n'
                )
            f.write(cont1)
            for cid in self.catalog.keys():
                f.write(f'    <itemref idref=\"{cid}\"/>\n')
            f.write('</spine>\n')
            f.write('<guide>\n')
            f.write(
                '    <reference href=\"catalog.xhtml\" type=\"toc\" title=\"目录\"/>\n'
            )
            f.write('</guide>\n')
            f.write('</package>\n')

    def write_catalog(self) -> None:
        '''write catalog.xhtml file'''
        self.write_catalog_head()
        with open(os.path.join(self.path, 'catalog.xhtml'),
                  'a',
                  encoding='utf-8') as f:
            for cid, title in self.catalog.items():
                f.write(
                    f'        <li class=\"catalog\"><a href=\"chapter_{cid}.xhtml\">{title}</a></li>\n'
                )
            f.write(
                '    </ul>\n    <div class=\"mbppagebreak\"></div>\n</body>\n</html>'
            )

    def write_toc(self) -> None:
        '''write toc.ncx file'''
        self.write_toc_head()
        with open(os.path.join(self.path, 'toc.ncx'), 'a',
                  encoding='utf-8') as f:
            idx = 1
            for cid, title in self.catalog.items():
                f.write(
                    f'<navPoint id=\"{cid}\" playOrder=\"{idx}\"><navLabel><text>{title}</text></navLabel><content src=\"chapter_{cid}.xhtml\"/></navPoint>\n'
                )
                idx += 1
            f.write('</navMap>\n')
            f.write('</ncx>')


class EpubChapter():

    def __init__(self, title=''):
        self.chapter_title = title
        self.chapter = ''
        self.head = '<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"no\"?>\n' + \
            '<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\" \"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">\n' + \
            '<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"zh-CN\">\n' + \
            '<head>\n' + \
            f'    <title>{title}</title>\n' + \
            '    <link href=\"stylesheet.css\" type=\"text/css\" rel=\"stylesheet\"/>\n' + \
            '    <style type=\"text/css\">\n' + \
            '        @page { margin-bottom: 5.000000pt; margin-top: 5.000000pt; }\n' + \
            '    </style>\n' + \
            '</head>\n' + \
            '<body>\n' + \
            f'    <h2><span style=\"border-bottom:1px solid\">{title}</span></h2>\n'
        self.tail = '    <div class=\"mbppagebreak\"></div>\n</body>\n</html>'

    def from_html_text(self, html_text: str, full: bool = False) -> str:
        if full:
            self.chapter = html_text
        else:
            self.chapter = self.head + html_text + self.tail

        return self.chapter

    def from_text(self, text: str or List[str]) -> str:
        if not isinstance(text, List):
            text = text.split('\n')
        html_text = '    <p>' + '</p>\n    <p>'.join(text) + '</p>\n'
        self.chapter = self.head + html_text + self.tail

        return self.chapter