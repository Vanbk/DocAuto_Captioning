# pip install -r requirements.txt

from docxtpl import DocxTemplate
import docx2txt
import os

def extractImg(doc_path, file_name, storing_path):
    text = docx2txt.process(doc_path+file_name, storing_path)

#captions: list of strings, which are captions
def changeCaption(doc_path,file_name, img_captions):
    doc=DocxTemplate(doc_path+file_name)
    context={'caption1':""} #initialize dic
    caption=[] # to pair with generated caption
    for i in range(0,len(img_captions)):
        caption.append('caption{}'.format(i+1))
        context[caption[i]] = img_captions[i]
    doc.render(context)
    filepath = os.path.join(doc_path, "generated_test.docx")
    doc.save(filepath)
