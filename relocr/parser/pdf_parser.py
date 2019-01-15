import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLineHorizontal, LTText
from unidecode import unidecode
import logging
from relocr.models.data_model import Document, Page, TextBox


logging.getLogger("pdfminer").setLevel(logging.ERROR)


class PDF_Extractor:
    def __init__(self):
        self.rsrcmgr = PDFResourceManager()

    def extract_dir(self, d):
        """Extract BBOX from path data"""
        res = []
        for path in os.listdir(d):
            if not path.endswith('.pdf'):
                continue
            path = os.path.join(d, path)
            logging.info(f"Extracting data from {path} ...")
            try:
                res.append(self.extract(path))
            except Exception as e:
                logging.error(f"Extraction failed, {e}")
        return res

    def extract(self, path, max_pages=50):
        title = os.path.basename(path).split('.')[0]  # Use filename as doc title
        doc = Document(title)
        with open(path, 'rb') as fp:
            parser = PDFParser(fp)
            document = PDFDocument(parser)
            device = PDFPageAggregator(self.rsrcmgr, laparams=LAParams())
            interpreter = PDFPageInterpreter(self.rsrcmgr, device)
            for num, page in enumerate(PDFPage.create_pages(document), 1):
                if num > max_pages:
                    break
                new_page = Page(num, page.mediabox)
                interpreter.process_page(page)
                layout = device.get_result()
                self.parse_page(new_page, layout)
                doc.pages.append(new_page)
        return doc

    def parse_page(self, new_page, layout, min_len=3, ignore_digits=True):
        """ Parse the PDF layout. """
        for lt in layout:
            if isinstance(lt, LTTextBox):
                text = lt.get_text().replace('\n', ' ').strip()
                if len(text) < min_len:
                    continue
                if ignore_digits and text.isdigit():
                    continue
                text.replace('-', ' ')
                text = ' '.join(text.split())
                text = unidecode(text)
                new_box = TextBox(lt.index, lt.bbox, text)
                new_page.boxes.append(new_box)
