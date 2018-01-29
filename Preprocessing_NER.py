import os
from nltk.tokenize import RegexpTokenizer  ### for nltk word tokenization
tokenizer = RegexpTokenizer(r'\w+')
cwd = os.getcwd()
import glob

import xml.etree.ElementTree as ET
BIO_file=open("BIO_NER.txt","w")

for filename in glob.glob(os.path.join(cwd,"MADE-1.0/corpus/*")):
    print (filename.split("/")[-1])
    Annotations = open(os.path.join(cwd, "MADE-1.0/annotations/" + filename.split("/")[-1]+".bioc.xml"), "r")
    tree = ET.parse(os.path.join(cwd, "MADE-1.0/annotations/1_9.bioc.xml"))
    root = tree.getroot()

    Entity_tag = []
    Offset = []
    Ent_Length = []
    Ent_text = []
    for annot in root.iter("annotation"):
        Entity_tag.append(annot.find("infon").text)
        # Offset.append(annot.find("location").find("length").attrib)
        Ent_text.append(annot.find("text").text)
        Ent_Length.append(annot.find("location").get("length"))
        Offset.append(annot.find("location").get("offset"))

    text=""
    lines=[]
    file1=open(filename,"r")
    entity_index=0
    for line in file1:
        text += line
        line2=line.strip()
        words=tokenizer.tokenize(line2)
        if entity_index==0:  ### we have not reached our first entity
           if len(text)<Offset[entity_index]: ## which means we have not seen entities till now
              for w1 in words:
                  BIO_file.write(w1+" O" + "\n")

              BIO_file.write("\n")
           else:
              if len(tokenizer.tokenize(Ent_text[entity_index])) == 1:
                  for w1 in words:
                      if w1==Ent_text[entity_index]:
                         BIO_file.write(w1+" " + Entity_tag[entity_index]+ "\n")
                         entity_index+=1


        else:
           if len(text)>Offset[entity_index-1]: ## which means there is an entity in this sentence



    print(text[3589:3595])



file1=open(os.path.join(cwd,"MADE-1.0/corpus/1_9"),"r")
Annotations=open(os.path.join(cwd,"MADE-1.0/annotations/1_9.bioc.xml"),"r")
tree = ET.parse(os.path.join(cwd,"MADE-1.0/annotations/1_9.bioc.xml"))
root = tree.getroot()


Entity_tag=[]
Offset=[]
Ent_Length=[]
Ent_text=[]
for annot in root.iter("annotation"):
    Entity_tag.append(annot.find("infon").text)
    # Offset.append(annot.find("location").find("length").attrib)
    Ent_text.append(annot.find("text").text)
    Ent_Length.append(annot.find("location").get("length"))
    Offset.append(annot.find("location").get("offset"))



"""
BIO_file=open("BIO_NER.txt","w")
text=""
for line in file1:
    # line=line.strip()
    text+=line
print (text[3589:3595])
"""