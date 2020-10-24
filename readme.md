# PDF Index Extraction
Basically, after hearing that this was something people would pay $100s of dollars for, I figured that it wouldn't be that hard to do a modest job of it, of which is this the result.

### Dependencies
This program uses PyPDF2 for pulling information from the PDF and XeLaTeX for formatting and generating a new pdf. Python is used as the main language.

### Limitations
The program pulls whatever text is embedded in the pdf, I have tested it on a number of pdfs and I've found that only ones I have downloaded from publishers seem to work. Given that this is a significant part of the purpose this limitation doesn't bother me too much.

### Output
The basic output is just a list of references in the correct order. Improvements could be made by either editing the TeX document that is produced or by improving the makeindex.py script.

### Use
Call the script text_extraction.py, pass in the path-to-file of the target pdf and the base page number from which the program will count. This program generates a references.pidx file which is read when you run makeindex.py. This function will generate a .tex file named "Index.tex" by default. 

### License 
I have released this under the GNU Public License v.3. Meaning, in short, that so long as this remains free software you may do what you like with it.
