#! /usr/bin/env python

from HTMLParser import HTMLParser
import argparse
import sys
import re
import urllib

class MyHTMLParser(HTMLParser):
    
    def handle_starttag(self,tag,attrs):
        if(tag != 'a'):
            sys.stdout.write(self.get_starttag_text())
        else:            
            sys.stdout.write("<"+tag+' ')
            sys.stdout.write(attrs[0][0]+'=')
            linkRef=re.sub('&','&amp;',attrs[0][1])
 #           linkRef=attrs[0][1]
 #           linkRef=urllib.quote(attrs[0][1])

            sys.stdout.write('"'+linkRef+'"')
            sys.stdout.write(">")

    def handle_decl(self,decl):
        sys.stdout.write('<!'+decl+'>')

    def handle_comment(self,comment):
        sys.stdout.write('<!--'+comment+'-->')
        
    def handle_entityref(self,refname):
        sys.stdout.write('&'+refname+';')

    def handle_endtag(self,tag):
        sys.stdout.write("</"+tag+">")
        
    def handle_data(self,data):
        sys.stdout.write(data)
        
   
      
         

if __name__ == "__main__":
    
    my_argparser=argparse.ArgumentParser(description='Bills HTML Gizmo')
    my_argparser.add_argument('-f',type=file,dest='Infile')
    
    args=my_argparser.parse_args()    
    
    htmlData=args.Infile.read()
    theParser = MyHTMLParser()
    
    theParser.feed(htmlData)
   
