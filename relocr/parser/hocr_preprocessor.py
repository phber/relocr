import os
import shutil
from tempfile import mkdtemp
import subprocess
import tempfile
import os
import errno
import pytesseract
import six
import cv2


class ShellParser(object):
    def run(self, args):
        """Run ``command`` and return the subsequent ``stdout`` and ``stderr``
        as a tuple. If the command is not successful, this raises a
        :exc:`textract.exceptions.ShellError`.
        """

        # run a subprocess and put the stdout and stderr on the pipe object
        try:
            pipe = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        except OSError as e:
            if e.errno == errno.ENOENT:
                # File not found. This is equivalent to getting exitcode 127 from sh
                raise Exception(' '.join(args), 127, '', '')

        # pipe.wait() ends up hanging on large files. using
        # pipe.communicate appears to avoid this issue
        stdout, stderr = pipe.communicate()

        # if pipe is busted, raise an error (unlike Fabric)
        if pipe.returncode != 0:
            raise Exception(' '.join(args), pipe.returncode, stdout, stderr)

        return stdout, stderr


class TesseractParser(ShellParser):
    """Extract text from various image file formats using tesseract-ocr"""

    def _extract_ppm(self, path_list):
        args = ['tesseract', path_list, 'stdout', 'hocr']
        stdout, _ = self.run(args)
        return stdout

    def extract(self, filename, lang=None):
        """Extract text from pdfs using tesseract (per-page OCR)."""
        temp_dir = mkdtemp()
        base = os.path.join(temp_dir, 'conv')
        try:
            self.run(['pdftoppm', filename, base])
            res = ''
            for page_path in sorted(os.listdir(temp_dir)):
                page_path = os.path.join(temp_dir, page_path)
                res += f'{page_path}\n'
            
            list_path = os.path.join(temp_dir, 'path_list.txt')
            with open(list_path, 'w') as f:
                f.write(res)
            page_content = self._extract_ppm(list_path)
            return page_content.decode("utf-8")
        finally:
            shutil.rmtree(temp_dir)

