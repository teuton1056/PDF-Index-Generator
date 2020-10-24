import json 

def order_lines_OT(lines):
    with open('OT_Order.json','r') as fp:
        order = json.load(fp)
    sorted_list = sorted(lines,key=lambda word:(int(order[word[0]]),word[1].split(':')[0],int(word[2])))
    return sorted_list

def order_lines_NT(lines):
    with open('NT_Order.json','r') as fp:
        order = json.load(fp)
    sorted_list = sorted(lines,key=lambda word:int(order[word[0]]))
    return sorted_list

def order_lines_Apocrypha(lines):
    with open('Apocrypha_Order.json','r') as fp:
        order = json.load(fp)
    sorted_list = sorted(lines,key=lambda word:int(order[word[0]]))
    return sorted_list

def order_basic(lines):
    sorted_list = sorted(lines,key=lambda word:word[0])
    return sorted_list

def main(fname="references.pidx"):
    with open(fname,'r') as fp:
        idx = fp.readlines()
    with open('OT_Order.json','r') as fp:
        OT_titles = json.load(fp)
    with open('NT_Order.json','r') as fp:
        NT_titles = json.load(fp)
    with open('Apocrypha_Order.json','r') as fp:
        Apocrypha_titles = json.load(fp)
    oti = []
    nti = []
    api = []
    idg = []
    for line in idx:
        k = line.split('|')
        if k[0] in OT_titles.keys():
            oti.append(k)
        elif k[0] in NT_titles.keys():
            nti.append(k)
        elif k[0] in Apocrypha_titles.keys():
            api.append(k)
        else:
            idg.append(k)
    otoi = order_lines_OT(oti)
    ntoi = order_lines_NT(nti)
    apoi = order_lines_Apocrypha(api)
    ind = order_basic(idg)
    fp = open("Index.tex",'w')
    fp.write("\\documentclass[12pt]{report}\n \\usepackage{fontspec}\n \\setmainfont{Times New Roman}\n \\usepackage{multicol}\n \\begin{document}\n \\begin{multicols}{3}[\\chapter*{Index}\n]")
    for line in otoi:
        fp.write(f"\\noindent {line[0]}\\ {line[1]}, {line[2]}\\par\n")
    for line in ntoi:
        fp.write(f"\\noindent {line[0]}\\ {line[1]}, {line[2]}\\par\n")
    for line in apoi:
        fp.write(f"\\noindent {line[0]}\\ {line[1]}, {line[2]}\\par\n")
    for line in ind:
        fp.write(f"\\noindent {line[0]}\\ {line[1]}, {line[2]}\\par\n")
    fp.write('\\end{multicols}\\end{document}')
    fp.close()

main()