# PDF Index Extraction
This program generates an index of Biblical references and other references common in Old/New Testament scholarship. 
## Information
### Dependencies
This program uses PyPDF2 for pulling information from the PDF and the python standard library for everything else.

### Limitations
The program pulls whatever text is embedded in the pdf. This means that if the text is not embedded, or if the text is not in the correct order, the program will not work. This is espeically true of scanned content.

### Output
The basic output is just a list of references in the correct order, by default this will appear in the base directory as "index.txt".

### Use
You can use the main.py script with arguments to change the input file. Minor modifications to the script will allow multiple input files. Also note the need to specify the base page number if the PDF is not paginated from 1. 

### Modification and Extension
Expansion of the alias files in the aliases directory will improve the behavior of the program. The program is designed to be easily modified to include additional aliases. 
I plan to improve the configruability of the formatters in the future and eventually add a .tex and possibily other outputs.
## License 
GPLv3

