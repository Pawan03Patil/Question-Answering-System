from index import ElasticSearch
import nltk
import json
import spacy
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
from spacy import displacy
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()
from nltk.corpus import wordnet
import re, math
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
import os


#from index import ElasticSearch
def MAIN(ques):
    #es = ElasticSearch()
    ROOT_DIRECTORY = "C:\\Users\\PAWAN\\Desktop\\milestone 4\\Input files"
    es = ElasticSearch()
    for file in os.listdir(ROOT_DIRECTORY):
        filename = os.path.join(ROOT_DIRECTORY, file) 
        with open(filename, 'r',encoding='utf-8') as f:
            content = f.read()
            es.INDEX(filename, content, 'nlp1')
    filename, content = es.SEARCH('nlp1', ques)
    return(filename)




ques="When was CitiGroup Inc. created?"
path=MAIN(ques)
lemmatizer = WordNetLemmatizer()
file=open(path,'r',encoding='utf-8-sig')
file1 = file.read()

tokens = word_tokenize(file1)
# sent=sent_tokenize(file1)
doc = nlp(file1)
sent = []
for token in (doc.sents):
    sent.append(token.text)

# print(tokens)
# print(sent)
# print(lemmatizer.lemmatize("rocks"))
lema = []

for token in doc:
    lema.append(token.lemma_)

# print(lema)
pos = pos_tag(tokens)
print(pos)
nlp = spacy.load("en_core_web_sm")
sents1 = nlp(ques)
#print(sents1.to_json)

for s in sent:
    sents1=nlp(s)
    for token1 in sents1:
        print("{0}/{1} <--{2}-- {3}/{4}".format(
        token1.text, token1.tag_, token1.dep_, token1.head.text, token1.head.tag_))
    break


hyper=[]
hypo=[]
mero=[]
holo=[]

for k in tokens:
            
            bestSynonym = lesk(tokens, k)
            if bestSynonym is not None:
                for hypernym in bestSynonym.hypernyms()[:2]:
                    hyper.append(hypernym)
                for hyponym in bestSynonym.hyponyms()[:2]:
                    hypo.append(hyponym)
                for meronym in bestSynonym.part_meronyms()[:2]:
                    mero.append(meronym)
                for holonym in bestSynonym.part_holonyms()[:2]:
                    holo.append(holonym)

hypernyms=[]
hyponyms=[]
meronyms=[]
holonyms=[]

hypernyms.append(hyper)
hyponyms.append(hypo)
meronyms.append(mero)
holonyms.append(holo)



qu = ques
doc1 = nlp(ques)
customize_stop_words = ["'s", "?"]
for w in customize_stop_words:
    nlp.vocab[w].is_stop = True
G = []
s = ""
for tokens in doc1:
    G.append(tokens.lemma_)
# print(G)
s = ' '.join(G)
doc2 = nlp(s)
G = [token1.text for token1 in doc2 if not token1.is_stop]
print(G)
syn = list()
p = 0
p = pos_tag(G)
print("pos:", p)
pp = 0
for j in G:
    if ((p[pp][1] == 'NNP')):
        pp += 1
        continue
    for synset in wordnet.synsets(j):
        for lemma in synset.lemmas():
            syn.append(lemma.name())
    pp += 1
print(set(syn))
print(len(set(syn)))
count1 = len(G)
G11 = G.copy()
G9 = G.copy()
G1 = G.copy()
count = len(G)
print(count)
flag = False
doc9 = nlp(ques)
c = 0
r = 0
for y in ([(X.text, X.label_) for X in doc9.ents]):
    # print(y[1],y[0])
    e = (y[0].split())
    r = len(e)
    if ((y[1] == 'PERSON') and (r > 1)):
        flag = True
        f = e[1]
    if ((y[1] == 'ORG') and (r > 1)):
        flag = True
        c = 1
        f = e[1]
G2 = []
G3 = []
if (flag == True and c == 0):
    G.remove(e[0])
    # print(G1)
    G2 = G
    G9.remove(e[1])
    G3 = G9
if (flag == True and c == 1):
    # print(G1)
    G2 = G
    G9.remove(e[1])
    G3 = G9
# print(f)
G0 = G11 + syn
G0 = set(G0)
G6 = syn + G2
G7 = syn + G3
#print("G7:", G7)
#print("G6:", G6)
# print('Synonyms: ',G0)
c1 = 0
o1 = []
#print("g1", G0)
# print(len(G1))
'''
print(G2)
print(len(G2))
print(G3)
print(len(G3))
'''
for y in sent:
    A = []
    A += y.split()
    doc4 = nlp(y)
    lema = []
    for tokens in doc4:
        lema.append(tokens.lemma_)
    overlaps = set(lema).intersection(G0)
    length = len(overlaps)
    if (length >= (count1)):
        print(overlaps)
        o1.append(y)
        c1 += 1
print(count1)
print("for G0:", o1)
print(len(o1))
if (flag == True):
    count = len(G2)
    print("G2:", count)
    for y in sent:
        A = []
        A += y.split()
        doc = nlp(y)
        lema = []
        for tokens in doc:
            lema.append(tokens.lemma_)
        overlaps = set(lema).intersection(G6)
        length = len(overlaps)
        if (length >= (count)):
            print(overlaps)
            o1.append(y)
            c1 += 1
#print("for G6:", o1)
#print(len(o1))
if (flag == True):
    count = len(G3)
    print("G3:", count)
    for y in sent:
        A = []
        A += y.split()
        doc = nlp(y)
        lema = []
        for tokens in doc:
            lema.append(tokens.lemma_)
        overlaps = set(lema).intersection(G7)
        length = len(overlaps)
        if (length >= (count)):
            print(overlaps)
            o1.append(y)
            c1 += 1

#print("total:", o1)
#print(len(o1))

q = []
for j in o1:
    doc = nlp(j)
    # print([(X.text, X.label_) for X in doc.ents])
    for x in ([(X.text, X.label_) for X in doc.ents]):
        if ((x[1] == "LOC") or (x[1] == "GPE") or (x[1]== "DATE") or (x[1] == "PERSON")):
            q.append(j)
            break

#print(set(q))
#print(len(q))

sent_dict = {}

for each_sent in q:
    tags = each_sent.split(" ")
    ques = qu.split(" ")
    # dic={}
    uni_cval = Counter({})

    for word in tags:
        lem = lemmatizer.lemmatize(word)
        # print(lemmatizer.lemmatize("bats"))
        # print(lem)
        uni_cval[lem] += 1

    # print(uni_cval)

    # founded
    c = 0;
    prob = 1

    for i in ques:
        if c != 0 and c != (len(ques) - 1):
            lem_ques = lemmatizer.lemmatize(i)
            count_word = uni_cval[lem_ques] + 1

            doc_no = len(tags) + len(uni_cval)

            tf = count_word / doc_no
            # print(tf)
            # print(i)
            prob = prob * tf

        c = c + 1

    # print(prob)
    sent_dict[each_sent] = prob

# print(sent_dict)

maxi = -1.0000
selected = []
# print(ques)

for x in sent_dict:
    # print(x)
    # print()
    # print(sent_dict[x])
    doc = nlp(x)

    for ent in doc.ents:
        print(ent.label_)
        if ques[0] == "Who":
            if ent.label_ == "PERSON" or ent.label_ == "ORG":
                if maxi == sent_dict[x]:
                    selected.append(x)
                elif maxi < sent_dict[x]:

                    selected = []
                    selected.append(x)
                    maxi = sent_dict[x]
                    mx = maxi
                    # print(maxi)
                break

        if ques[0] == "When":
            if ent.label_ == "DATE":
                if maxi == sent_dict[x]:
                    selected.append(x)
                elif maxi < sent_dict[x]:

                    selected = []
                    selected.append(x)
                    maxi = sent_dict[x]
                    mx = maxi
                    #$print(maxi)
                break

        if ques[0] == "Where":
            if ent.label_ == "LOC" or ent.label_ == "GPE" :
                if maxi == sent_dict[x]:
                    selected.append(x)
                elif maxi < sent_dict[x]:

                    selected = []
                    selected.append(x)
                    maxi = sent_dict[x]
                    mx = maxi
                    #print(maxi)
                break

#print(selected)

doc1 = nlp(selected[0])
# print(doc1)

for ent in doc1.ents:
    # print(ent.text, ent.start_char, ent.end_char, ent.label_)
    if ques[0] == "Who":
        if ent.label_ == "PERSON":
            print("answer is:" + ent.text)
            break

    if ques[0] == "When":
        if ent.label_ == "DATE":
            print("answer is:" + ent.text)
            break

    if ques[0] == "Where":
        if ent.label_ == "LOC" or ent.label_ == "GPE":
            print("answer is:" + ent.text)
            break
      

#JSON format:
            
result={}
result["question"]=ques
result["answer"]=ent.text
result["sentence"]=selected
result["docname"]= path
z=json.dumps(result,indent=3)
print(z)

