import os
from nltk.tokenize import RegexpTokenizer  ### for nltk word tokenization
tokenizer = RegexpTokenizer(r'\w+')
cwd = os.getcwd()
import glob
from nltk.tokenize import word_tokenize, sent_tokenize
import xml.etree.ElementTree as ET

count=0
incorrect_segm=0
for filename in glob.glob(os.path.join(cwd,"MADE-1.0/corpus/*")):
    count+=1
    if count%20==0:
       print(count)

    file1=open(filename,"r")
    Annotations=open(os.path.join(cwd, "MADE-1.0/annotations/" + filename.split("/")[-1]+".bioc.xml"), "r")
    tree = ET.parse(os.path.join(cwd, "MADE-1.0/annotations/" + filename.split("/")[-1]+".bioc.xml"))
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
    # print (sent_boundary)

    BIO_file=open(os.path.join(cwd,"MADE-1.0/BIO_files_doc_level_V2/" + filename.split("/")[-1] + ".txt"),"w")
    text=""
    curr_pos=0
    word_index = -1
    verification_var=[]  ## verification variable should be equal to length of Offset variable to ensure we are covering all the entities. Else, break the loop
    file1=open(filename,"r")
    for line in file1:

        # line=line.strip()
        text+=line
        line2=line.strip()
        words=tokenizer.tokenize(line2)

        for i2, w2 in enumerate(words):
            if len(w2)==2 and w2[0]=="x":
               words[i2]=w2[1]
               words.insert(i2,"x")





        for w1 in words:
            start=text.find(w1, curr_pos)
            #### segmenting sentences
            if start in sent_boundary:
               # BIO_file.write("\n")
               # print("yes we are here")
               pass
            #########

            if str(start) in Offset or str(start-1) in Offset:

               if str(start) in Offset:
                   word_index=Offset.index(str(start))
               elif str(start-1) in Offset:
                   word_index = Offset.index(str(start-1))


               verification_var.append(start)

            # entities=tokenizer.tokenize(Ent_text[word_index])
               new_line = str(start) + " " + str(start + len(w1)) + " " + w1 + " " + "B-"+Entity_tag[word_index]  +"\n"

            else:

               if word_index >=0:
                  for ind3, of3 in enumerate(Offset):
                      if int(of3)<= start and start+len(w1) <= (int(of3)+int(Ent_Length[ind3])):
                         new_line = str(start) + " " + str(start + len(w1)) + " " + w1 + " " + "I-" + Entity_tag[ind3] + "\n"
                         break
                      else:
                         new_line = str(start) + " " + str(start + len(w1)) + " " + w1 + " " + "O" + "\n"
               else:
                  new_line = str(start) + " " + str(start + len(w1)) + " " + w1 + " " + "O" + "\n"



            BIO_file.write(new_line)
            curr_pos=start+len(w1)

    if len(verification_var)!= len(set(Offset)):
       incorrect_segm+=1
       #print (verification_var)
       Offset=[int(of2) for of2 in Offset]

       #print (sorted(Offset))
       print (filename)



print(incorrect_segm)

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