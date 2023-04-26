'''
Created on 3 Oct 2022

@author: Famenontsoa
'''
import fitz

class PdfTextExtractor():
    '''
    classdocs
    '''
    
    __path = ''

    def __init__(self):
        '''
        Constructor
        '''
    
    def get_path(self): return self.__path
    
    def set_path(self, path):
        if path != '' and path is not None:
            self.__path = path
        else:
            raise ValueError('Path cannot be none')
    
    # extract text from PDF
    def get_text_from_pdf(self):
        with fitz.open(self.get_path()) as doc:
            text = ''
            for page in doc:
                # print(page.get_text('text'))
                text += (page.get_text('text', flags=2))
        
        content = []
        for temp in text.split('\n'):
            content.append(temp.replace('\xa0', ' ').replace('\xad', '-').strip())
        # print(text.split('\n'))
        return content
        '''
        from pdf2image import convert_from_path
        pages = convert_from_path(self.get_path())
        for i in range(len(pages)):
            pages[i].save('page'+str(i)+'.jpg','JPEG')
        '''
        
        