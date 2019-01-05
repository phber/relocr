from bs4 import BeautifulSoup
from relocr.models.ocr_models import Document, Page, Area, Paragraph, Line


def get_bbox(node):
    text = node.get('title')
    res = []
    for part in text.split(';'):
        part = part.strip()
        if part.startswith('bbox'):
            for p in part.split()[1:]:
                res.append(int(p))
    return res


def get_wconf(node):
    text = node.get('title')
    for part in text.split(';'):
        part = part.strip()
        if part.startswith('x_wconf'):
            return int(part.split()[1])
    return None


def get_num(node):
    return int(node.get('id').split('_')[-1])


class HTML_Parser:
    def __init__(self):
        self.wconf_min = 30  # Minimum word confidence  0 - 100 %

    def parse(self, doc_title, html_string):
        """ Returns a Document from a hOCR-string """"
        soup = BeautifulSoup(html_string, 'html.parser')
        doc = Document(doc_title)
        # Parse pages
        for page in soup.body.find_all('div', class_='ocr_page'):
            pg = Page(get_num(page), get_bbox(page))
            # Parse areas
            for area in page.find_all('div', class_='ocr_carea'):
                ar = Area(get_num(area), get_bbox(area))

                # Parse paragraphs
                for paragraph in area.find_all('p', class_='ocr_par'):
                    par = Paragraph(get_num(paragraph), get_bbox(paragraph))

                    # Parse line
                    for line in paragraph.find_all('span', class_='ocr_line'):
                        line_words = []

                        # Parse words
                        for word in line.find_all('span', class_='ocrx_word'):
                            if not word.text:
                                continue
                            if get_wconf(word) < self.wconf_min:
                                continue
                            line_words.append(word.text)
                        ln = Line(get_num(line), get_bbox(line), line_words)
                        par.lines.append(ln)
                    par.parse_sentences()
                    ar.paragraphs.append(par)
                pg.areas.append(ar)
            doc.pages.append(pg)
        return doc
