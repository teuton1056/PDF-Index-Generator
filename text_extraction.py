import PyPDF2
import json
import re
import sys

# NT and OT json files originally from https://github.com/TehShrike/books-of-the-bible
# some alterations have been made to the original files, but the core design and much content remains the same.
    
def extract_references(text,index_file='index_files.json',index_directory="aliases"):
    # this is a deprecated function which is retained in the code because it may prove useful in future.
    garbage = """[]{}(),.;':-_\\|"`~<>/?ﬁ"""
    words = text.split(' ')
    clean_words = []
    references = []
    for word in words:
        clean_words.append(word.strip(garbage).lstrip(garbage))
    with open(index_file,'r') as fp:
        index_files = json.load(fp)
    for index in index_files:
        with open(f"{index_directory}/{index}",'r') as fp:
            idx = json.load(fp)
        for item in idx:
            #print(item)
            for word in clean_words:
                if word == item:
                    references.append({'reference':word,'catch':item})
                else:
                    for alias in item['aliases']:
                        if word == alias:
                            references.append({'reference':word,'catch':alias})
    print(references)
    return references

def get_idx_for_page(text,page_number,index_file='index_files.json',index_directory="aliases"):
    #latex: f"\\indexentry{{{match}}}{{{page_number}}}\n"
    idx_text = ""
    with open(index_file,'r') as fp:
        index_files = json.load(fp)
    for index in index_files:
        with open(f"{index_directory}/{index}",'r') as fp:
            idx = json.load(fp)
        # idx contains a list of dicts where "name" is the regular name and "aliases" are the valid abbreviations.
        for item in idx:
            for alias in item['aliases']:
                # use a regex to find the referecnes
                matches = re.findall(f"{alias}" + r"\.?\s\d{1,3}\.?:?\d{0,3}-?\d{0,3}", text)
                for m in matches:
                    # we are only interested in the numerical part of the match.
                    match = m.strip('.:;,').lstrip()[len(alias):]
                    idx_text += f"{item['name']}|{match}|{page_number}\n"
    return idx_text

def create_idx(fname,base_number=1):
    # creating a pdf file object
    pdfFileObj = open(fname, 'rb')  
    # creating a pdf reader object  
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
    # printing number of pages in pdf file  
    #print(pdfReader.numPages)  
    number_of_pages = pdfReader.numPages
    document = []
    # creating a page object  
    for number in range(number_of_pages):
        pageObj = pdfReader.getPage(number)  
        # extracting text from page  
        text = pageObj.extractText()
        #with open(f'out_{number}.txt','w',encoding='utf-8') as fp:
        #    fp.write(text)
        page = {'Relative_Number':int(number) + base_number,'raw_text':text}
        document.append(page)
    # closing the pdf file object  
    pdfFileObj.close()
    # lets make an index!
    index = ""
    for page in document:
        index += get_idx_for_page(page['raw_text'],page['Relative_Number'])
    with open('references.pidx','w') as fp:
        fp.write(index)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception(f"Too few arguments. Excepted 2, recieved {len(sys.argv) - 1}")
    fname = sys.argv[1]
    base_page = int(sys.argv[2])
    create_idx(fname,base_page)
    #create_idx('VT_Article.pdf',617)