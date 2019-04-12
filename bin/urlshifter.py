#! /usr/bin/env python

from HTMLParser import HTMLParser
import argparse
import sys
import re
# from urlparse import urlparse
import ConfigParser
import csv
import os


class MyHTMLParser(HTMLParser):

    
    def __init__(self,file,inLoc,outLoc,idDict,exceptionFile):
        HTMLParser.__init__(self)
        self.outFile=file
        self.inLoc=inLoc
        self.outLoc=outLoc
        self.idDict=idDict
        self.exceptionFile=exceptionFile
        self.infilename=None

    def setInfileName(self,infilename):
        self.infilename=infilename
            
        
    def urlFiddler(self,url):
        myUrl=re.sub('&','&amp;',url)
        idRe=None
        
        
        if(re.search(self.inLoc,theTuple.netloc)):
            idRe=re.search('id=[A-Z][0-9]+',theTuple.query)
            if(idRe != None):
                id=idRe.group(0)
                inId=id.split('=')[1][1:]
                if self.idDict.has_key(inId):
                    print('{'+inId+':'+self.idDict[inId]+'}')
            else:
                self.exceptionFile.write('In: '+self.infilename+' URL: '+ url + ' Is Weird'+os.linesep)
                    
            
        return(myUrl)
    
    def handle_reftag(self,tag,attrs):
        self.outFile.write("<"+tag+' ')
        if(len(attrs) < 1):
            raise AttributeError
        for kk in attrs:
            if(None == re.match("href",kk[0])):
                self.outFile.write(kk[0]+"=")
                for sub in kk[1:]:
                    self.outFile.write('"'+sub+'"')                
            else:
               self.outFile.write("href =")
               newUrl=self.urlFiddler(kk[1])
               self.outFile.write('"'+newUrl+'"')
               self.outFile.write(">")
                                 
                                   
                
    def handle_starttag(self,tag,attrs):
        if(tag != 'a'):
            self.outFile.write(self.get_starttag_text())
        else:
            try:
               self.handle_reftag(tag,attrs)
            except AttributeError:
                print("Oops")
                self.exceptionFile.write("Oops. In file " + self.infilename + " <" + tag + "> has no href"+os.linesep)
            finally:
                self.outFile.write(">")

    def handle_decl(self,decl):
        self.outFile.write('<!'+decl+'>')

    def handle_comment(self,comment):
        self.outFile.write('<!--'+comment+'-->')
        
    def handle_entityref(self,refname):
        self.outFile.write('&'+refname+';')

    def handle_endtag(self,tag):
        self.outFile.write("</"+tag+">")
        
    def handle_data(self,data):
        self.outFile.write(data)
        

def readCsvTable(tableFN):
    idMap=dict()
    csvFile=open(tableFN,'r')
    myReader=csv.reader(csvFile,delimiter=',',quotechar='"')
    for row in myReader:
        idMap[row[1]]=row[2]
    return idMap
    

if __name__ == "__main__":
    
    my_argparser=argparse.ArgumentParser(description='Bills HTML Gizmo')
    my_argparser.add_argument('-i',type=file,dest='Infile')
    my_argparser.add_argument('-o',type=argparse.FileType('w'),dest='Outfile');
    
    args = my_argparser.parse_args()    
    myConfig = ConfigParser.ConfigParser()
    myConfig.read("urlshifter.cfg")
    tableSection='table_list'
    inPath = myConfig.get(tableSection,'inPath')
    outPath = myConfig.get(tableSection,'outPath')
    tableFN = myConfig.get(tableSection,'tableFile')
    exceptFN = myConfig.get(tableSection,'exceptFile')
    exceptMode = myConfig.get(tableSection,'exceptFileMode')
    exceptionFile=open(exceptFN,exceptMode)
    idDict = readCsvTable(tableFN)
    

    htmlData=args.Infile.read()
    theParser = MyHTMLParser(args.Outfile,inPath,outPath,idDict,exceptionFile)
    theParser.setInfileName(args.Infile.name)
    theParser.feed(htmlData)
   
