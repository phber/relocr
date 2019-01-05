from relixir.parser.hocr_preprocessor import TesseractParser
from relixir.parser.hocr_parser import HTML_Parser
from relixir.utils.visual import get_aligned_tokens

with open('data/out.html', 'r') as f:
    s = f.read()

doc = HTML_Parser().parse('test', s))
page = doc.pages[0]
res = get_aligned_tokens(page, )