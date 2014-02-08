from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice 
from pdfminer.converter import TextConverter 
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import StringIO
import urllib2
import sys

def getText(url):
    data = urllib2.urlopen(url).read()
    fp = StringIO.StringIO() 
    fp.write(data) 
    fp.seek(0) 
    outfp = StringIO.StringIO() 
    
    srcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(srcmgr, outfp, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(srcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    t = outfp.getvalue() 
    outfp.close() 
    fp.close() 
    return t

if __name__ == "__main__":
    print getPdf(sys.argv[1])
