#! /usr/bin/env python
###########################################################################################################
#   Copyright (c) Charles Shapiro April 2019
#
#   This file is part of urlshifter.
#   urlshifter is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   urlshifter is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with urlshifter.  If not, see <http://www.gnu.org/licenses/>.
#
###########################################################################################################


# Parse HTML and alter URLs as necessary.
from HTMLParser import HTMLParser
import argparse
import sys
import re
# from urlparse import urlparse Thought about this but decided it was unnecessary.
import ConfigParser
import csv
import os


class MyHTMLParser(HTMLParser):

    # Paste in all my data..
    def __init__(self,file,inLoc,outLoc,idDict,exceptionFile,idREList):
        HTMLParser.__init__(self)
        self.outFile=file
        self.inLoc=inLoc
        self.outLoc=outLoc
        self.idDict=idDict
        self.exceptionFile=exceptionFile
        self.infilename=None
        self.idREList=idREList
        
    # Set filename for each run
    def setInfileName(self,infilename):
        self.infilename=infilename
        
    # Find an ID inside a URL.  Use the succession of REs I got from the config file to sequentially
    # search for it.
    def find_id_in_url(self,url):
        retVal=""
        Success=True
        reListNum=1
        
        idRE=re.search(self.idREList[0],url)
        if(None == idRE):
            self.exceptionFile.write('In: ' + self.infilename + ' URL: ' + url + ' Is Weird'+os.linesep)
            Success=False
        else:
            newSearchString=idRE.group(0)
        while((True == Success) and (reListNum <= len(self.idREList[1:])) ):
            idRE=re.search(self.idREList[reListNum],newSearchString)
            if(None == idRE):
                self.exceptionFile.write("In: [%s] URL: [%s] is Missing a list key" % (self.infilename,url) + os.linesep)
            else:
                newSearchString=idRE.group(0)
            reListNum = reListNum+1
        if(True == Success):
            return newSearchString
        else:
            return ""
        
    # Does this URL match the one given in the configuration file? If so, substitute a new one.    
    def urlFiddler(self,url):
        myUrl=re.sub('&','&amp;',url)
        originalURL=myUrl
        if(re.match(self.inLoc,url)):
            inId=self.find_id_in_url(url)
            if((self.idDict.has_key(inId)) and (len(self.idDict[inId]) > 0)):
               myUrl=self.outLoc % (self.idDict[inId])
               print("File: [%s] URL: [%s] changed to: [%s]" % (self.infilename,originalURL,myUrl))
            else:
               self.exceptionFile.write('In: %s URL: %s [%s] not found in id list' % (self.infilename,url,inId) + os.linesep)
               myUrl=originalURL
        return(myUrl)

    # Handle "<a" tags.  The parser gets really confused if reftags are malformed, e.g. "<a>" or "<a href=>". So in
    # that case I throw an "AttributeError" exception which is caught in the calling routine to prevent an abend.
    def handle_reftag(self,tag,attrs):
        self.outFile.write("<"+tag+' ')
        if(len(attrs) < 1):
            raise AttributeError
        for kk in attrs:
            if(len(kk) < 2):
                raise AttributeError        
            if(None == re.match("href",kk[0])):
                self.outFile.write(kk[0]+"=")
                for sub in kk[1:]:
                    if(None == sub):
                        raise AttributeError
                    else:
                        self.outFile.write('"'+sub+'"')                
            else:
               self.outFile.write("href =")
               newUrl=self.urlFiddler(kk[1])
               self.outFile.write('"'+newUrl+'"')
               self.outFile.write(">")
                                 
                                   
    # Determine if my start tag is link.  If so, work on it. If not, just dump it out.
    def handle_starttag(self,tag,attrs):
        if(tag != 'a'):
            self.outFile.write(self.get_starttag_text())
        else:
            try:
                self.handle_reftag(tag,attrs)
            except AttributeError:
                print("Oops")
                self.exceptionFile.write("Oops. In file %s <%s> has no href" % (self.infilename,tag) + os.linesep)
            finally:
                self.outFile.write(">")
                
    # Dump these out with no alteration.
    def handle_decl(self,decl):
        self.outFile.write('<!'+decl+'>'
        )
    # Dump these out with no alteration.
    def handle_comment(self,comment):
        self.outFile.write('<!--'+comment+'-->')
        
    # Dump these out with no alteration.        
    def handle_entityref(self,refname):
        self.outFile.write('&'+refname+';')
        
    # Dump these out with no alteration.
    def handle_endtag(self,tag):
        self.outFile.write("</"+tag+">")
        
    # Dump these out with no alteration.        
    def handle_data(self,data):
        self.outFile.write(data)
        
# Read the csv table of input and output ids. The first field is a name; I ignore it.
def readCsvTable(tableFN):
    idMap=dict()
    csvFile=open(tableFN,'r')
    myReader=csv.reader(csvFile,delimiter=',',quotechar='"')
    for row in myReader:
        idMap[row[1]]=row[2]
    del idMap[''] # No null string keys!    
    return idMap
    
# Main Line -- handle command line, read config table, instantiate and run html parser.
if __name__ == "__main__":

    cfgName="./urlshifter.cfg"
    my_argparser=argparse.ArgumentParser(description='A program to rewrite URLs in an HTML file')
    my_argparser.add_argument('-i',type=file,required=True,
                              help="Input HTML file (must exist)",dest='Infile')
    my_argparser.add_argument('-o',type=argparse.FileType('w'),required=True,
                              help="Output HTML file (opened write)",dest='Outfile');
    my_argparser.add_argument('-c',type=str,default=cfgName,required=False,
                              help="Configuration file name, defaults to %s" % (cfgName),dest="ConfigFileName")

    args = my_argparser.parse_args()    
    myConfig = ConfigParser.ConfigParser()
    myConfig.read(args.ConfigFileName)
    
    tableSection='urlshifter'
    
    inPath = myConfig.get(tableSection,'inPath')
    outPath = myConfig.get(tableSection,'outPath')
    tableFN = myConfig.get(tableSection,'tableFile')
    exceptFN = myConfig.get(tableSection,'exceptFile')
    exceptMode = myConfig.get(tableSection,'exceptFileMode')
    exceptionFile=open(exceptFN,exceptMode)
    
    # Read the list of regular expressions we use to isolate the input id from
    # the input URL.
    moreREs=True
    reNum=0
    searchREs=[]
    while(True == moreREs):
        optName="inptRE%d" % (reNum)
        if(myConfig.has_option(tableSection,optName)):
           searchREs.append(myConfig.get(tableSection,optName))
           reNum=reNum+1
        else:
           moreREs=False
    
    idDict = readCsvTable(tableFN)
    
    htmlData=args.Infile.read()
    theParser = MyHTMLParser(args.Outfile,inPath,outPath,idDict,exceptionFile,searchREs)
    theParser.setInfileName(args.Infile.name)
    theParser.feed(htmlData)
   
