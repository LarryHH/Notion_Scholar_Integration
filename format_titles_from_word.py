import docx

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def clean(doc):
    doc = [x for x in doc if (x and x[0] == '[')]
    doc = doc[5:]
    return doc

def write(doc, file):
    with open(file, 'w+') as f:
        f.write('\n'.join(doc))

doc = getText('Quantum inspired machine learning.docx').split('\n')
print(len(doc))
print(*doc, sep="\n")
doc = clean(doc)
write(doc, 'papers.txt')
print("DONE WRITING!")


