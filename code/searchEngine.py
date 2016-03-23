#!/usr/bin/python
import linecache
import re
from nltk.corpus import stopwords
import xml.sax
from stemming.porter2 import stem
import sys
from collections import defaultdict
from collections import Counter
import math

f22=open("N.txt","r")
ln=f22.readline()
N=int(ln)
f22.close()
cachedStopWords = []
for i in stopwords.words("english"):
	cachedStopWords.append(i.encode('utf-8'))

if (__name__ == "__main__"):
	f=open(sys.argv[1],"r")
	alpha={}
	a=f.readline().split()[0]
	i2=0
	while(a):
		if not alpha.has_key(a[0:2]):
			alpha[a[0:2]]=i2
		a=f.readline().split()[0]
		i2+=1
	while(True):
		inp=raw_input()
		cnt=cnt.encode('utf-8').lower()
		cnt=re.sub("{{.*}}",'',cnt)
		cnt=re.sub("\[.*\]",'',cnt)
		cnt=re.sub("[~`!@#$%^&*()_-]",' ',cnt) 
		cnt=re.sub("[+={}\[\]:>;]",' ',cnt) 
		cnt=re.sub("[',</?*+|\\\".]",' ',cnt)
		tf_idf=defaultdict(int)
		for word in cnt.strip().split():
			prog=re.compile("\d{4}")
			prog2=re.compile("\d{5}")
			prog3=re.compile("\d{1}")
			if word not in cachedStopWords:
				wrd = stem(word)
				let=wrd[0:2]
				ind=alpha[let]
				while(True):
					line=linecache.getline(sys.argv[1],ind).split()
					if line[0][0:2] != wrd[0:2]:
						break
					if line[0]==wrd:
						line.remove(wrd)
						line_wo=[]
						for j in line:
							line_wo.append(j[0:-1])
						c=Counter(line_wo)
						idf=math.log(N/len(c))
						for k in c.keys():
							tf_idf[k]+=idf*c[k]
						break
					ind+=1
			print tf_idf

