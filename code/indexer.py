#!/usr/bin/python

from nltk.corpus import stopwords
import xml.sax
from stemming.porter2 import stem
from collections import Counter
import re
from collections import defaultdict
import os
import sys


cachedStopWords = []
for i in stopwords.words("english"):
	cachedStopWords.append(i.encode('utf-8'))
wordCount={}
wordCountLst=[]
chnks=0
ddWrdCount=defaultdict(list)
N=0

def merge(n):
	for i in range(n/2):
		f1=open("chunk"+str(2*i+1),"r")
		f2=open("chunk"+str(2*i+2),"r")
		a=f1.readline().split()
		b=f2.readline().split()
		a1=a[0]
		b1=b[0]
		a.remove(a1)
		b.remove(b1)
		F=open("CHUNK"+str(i),"w")
		while(True):
			if a1==b1:
				F.write(a1+" ")
				for j in a:
					F.write(j+" ")
				for j in b:
					F.write(j+" ")
				F.write("\n")
				a=f1.readline().split()
				b=f2.readline().split()
				if a:
					a1=a[0]
					a.remove(a1)
				if b:
					b1=b[0]
					b.remove(b1)
				if not a or not b:
					break
			elif a1<b1:
				F.write(a1+" ")
				for j in a:
					F.write(j+" ")
				F.write("\n")
				a=f1.readline().split()
				if a:
					a1=a[0]
					a.remove(a1)
				else:
					break
			else:
				F.write(b1+" ")
				for j in b:
					F.write(j+" ")
				F.write("\n")
				b=f2.readline().split()
				if b:
					b1=b[0]
					b.remove(b1)
				else:
					break
		if(a):
			while(True):
				F.write(a1+" ")
				for j in a:
					F.write(j+" ")
				F.write("\n")
				a=f1.readline().split()
				if a:
					a1=a[0]
					a.remove(a1)
				else:
					break
		if(b):
			while(True):
				F.write(b1+" ")
				for j in b:
					F.write(j+" ")
				F.write("\n")
				b=f2.readline().split()
				if b:
					b1=b[0]
					b.remove(b1)
				else:
					break
		os.system("rm chunk"+str(2*i+1))
		os.system("rm chunk"+str(2*i+2))
		os.system("mv CHUNK"+str(i)+" chunk"+str(i+1))
	if n%2==1:
		os.system("mv chunk"+str(n)+" chunk"+str(n/2+1))


class wikiReader( xml.sax.ContentHandler ):
	def __init__(self):
		self.CurrentData = ""
		self.title = ""
		self.text = ""
		self.id=0
		self.prevTitle=""

	def startElement(self,tag,attributes):
		self.CurrentData = tag
	
	def endElement(self, tag):
		self.CurrentData=""

	def characters(self, content):
		if self.CurrentData == "title":
			#f.write("\nDocument - "+str(self.id)+"\n")
			#f.write("Title: "+self.prevTitle.encode('utf-8')+"\n")
			#self.prevTitle=content
			self.id+=1
			global N
			N=self.id
			#print title
			#f.write(str(wordCount)+"\n")
			#wordCount.clear()
			cnt=content.encode('utf-8').lower()
			cnt=re.sub("{{.*}}",'',cnt)
			cnt=re.sub("\[.*\]",'',cnt)
			cnt=re.sub("[~`!@#$%^&*()_-]",' ',cnt) 
			cnt=re.sub("[+={}\[\]:>;]",' ',cnt) 
			cnt=re.sub("[',</?*+|\\\".]",' ',cnt)
			for word in cnt.strip().split():
				prog=re.compile("\d{4}")
				prog2=re.compile("\d{5}")
				prog3=re.compile("\d{1}")
				if word not in cachedStopWords:
					wrd = stem(word)
					#wordCountLst.append( (wrd,self.id) )
					#f.write(wrd+"\n")
					#wordCount.append(word)
					#f.write(wrd+" ")
					ddWrdCount[wrd].append(str(self.id)+'t')
					"""if wrd not in wordCount.keys():
						wordCount[wrd]=1
					else:
						wordCount[wrd]+=1"""
		if self.CurrentData=="text":
			cnt=content.encode('utf-8').lower()
			cnt=re.sub("{{.*}}",'',cnt)
			cnt=re.sub("\[.*\]",'',cnt)
			cnt=re.sub("[~`!@#$%^&*()_-]",' ',cnt) 
			cnt=re.sub("[+={}\[\]:>;]",' ',cnt) 
			cnt=re.sub("[',</?*+|\\\".]",' ',cnt)
			for word in cnt.strip().split():
				prog=re.compile("\d{4}")
				prog2=re.compile("\d{5}")
				prog3=re.compile("\d{1}")
				if prog3.match(word):
					if not ( prog.match(word) and not prog2.match(word)):
						continue
				#prog=re.compile("\w*\\\w*")
				#if prog.match(word):
				#	continue
				if word not in cachedStopWords:
					wrd = stem(word)
					#print wrd
					#wordCountLst.append( (wrd,self.id) )
					#f.write(wrd+"\n")
					#wordCount.append(word)
					#f.write(wrd+" ")
					ddWrdCount[wrd].append(str(self.id)+'b')
					"""if wrd not in wordCount.keys():
						wordCount[wrd]=1
					else:
						wordCount[wrd]+=1"""
		if len(ddWrdCount)>100000:
			global chnks
			chnks+=1
			f1=open("chunk"+str(chnks),"w")
			lst = ddWrdCount.keys()
			lst.sort()
			for i in  lst:
				f1.write(i+" ")
				for j in ddWrdCount[i]:
					f1.write(str(j)+" ")
				f1.write("\n")
			f1.close()
			ddWrdCount.clear()

if (__name__ == "__main__"):
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	Handler = wikiReader()
	parser.setContentHandler( Handler )
	parser.parse(sys.argv[1])
	#print Counter(wordCount)
	#print wordCount
	#f.write(str(wordCount))
	#print ddWrdCount
	#print "Sorting"
	#wordCountLst.sort()
	#prevWrd=""
	"""for i in wordCountLst:
		if i[0] == prevWrd:
			wordCount[prevWrd].append(i[1])
		else:
			prevWrd=i[0]
			wordCount[prevWrd]=[ i[1] ]"""
	print "merging"
	n=chnks
	while(True):
		if n==1:
			break
		merge(n)
		if(n%2==0):
			n=n/2
		else:
			n=n/2+1
	os.system("mv chunk1 "+sys.argv[2])
	f=open("N.txt","w")
	f.write(str(N))
	f.close()
	#f.write(str(ddWrdCount))
	#lst = ddWrdCount.keys()
	#lst.sort()
	#lst=sorted(ddWrdCount.keys())
	#f.write(str(lst))
	#for i in  lst:
	#	f.write(i+" "+str(ddWrdCount[i])+"\n")
