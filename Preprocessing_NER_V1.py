import os
from nltk.tokenize import RegexpTokenizer  ### for nltk word tokenization
tokenizer = RegexpTokenizer(r'\w+')
cwd = os.getcwd()
import glob
from nltk.tokenize import sent_tokenize
import xml.etree.ElementTree as ET



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

###### finding sentence boundaries
text=""
for line1 in file1:
    text+=line1

sent_boundary = []
sentences = sent_tokenize(text)
for sent in sentences:
    sent_boundary.append(text.find(sent))

########
print (sent_boundary)

BIO_file=open(os.path.join(cwd,"MADE-1.0/BIO_files/BIO_NER_V1.txt"),"w")
text=""
curr_pos=0
word_index = -1
file1=open(os.path.join(cwd,"MADE-1.0/corpus/1_9"),"r")
for line in file1:

    # line=line.strip()
    text+=line
    line2=line.strip()
    words=tokenizer.tokenize(line2)

    for w1 in words:
        start=text.find(w1, curr_pos)
        #### segmenting sentences
        if start in sent_boundary:
           BIO_file.write("\n")
           print("yes we are here")
        #########

        if str(start) in Offset:
           word_index=Offset.index(str(start))

        # entities=tokenizer.tokenize(Ent_text[word_index])
           new_line = str(start) + " " + str(start + len(w1)) + " " + w1 + " " + "B-"+Entity_tag[word_index]  +"\n"

        else:
           if word_index >=0:
              if int(Offset[word_index])+int(Ent_Length[word_index])>= start+len(w1):
                 new_line = str(start) + " " + str(start + len(w1)) + " " + w1 + " " + "I-" + Entity_tag[word_index] + "\n"
              else:
                 new_line = str(start) + " " + str(start + len(w1)) + " " + w1 + " " + "O" + "\n"
           else:
              new_line = str(start) + " " + str(start + len(w1)) + " " + w1 + " " + "O" + "\n"



        BIO_file.write(new_line)
        curr_pos=start+len(w1)




"""
# print (text[3589:3595])
print (len(text))
sentences=sent_tokenize(text)

char_len=0
for sent in sentences:
    char_len+=(len(sent))
    char_len+=1
    # print (sent.replace("\n",""))

print (char_len)

"""