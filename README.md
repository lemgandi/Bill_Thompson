## Crude HTML mass editor


### What Is This Stuff ?

This is a tool to move URLs in a website from one geneology site to
another.  If, for example, you have a big pile of static web pages all
pointing to pages "wc.rootsweb.ancestry.com" and you wish to move to
"wikitree.com", this program will edit all of the URLs pointing to
"wc.rootsweb.ancestry.com" to corresponding pages on
"wikitree.com". You must supply a CSV file which links the pages on
"wc.rootsweb.ancestry.com" to their corresponding pages on
"wikitree.com".

### Contents

The distribution contains three directories:

* bin/
  Contains "urlshifter.py" and "urlshifter.cfg", the actual program and configuration file
* tables/ 
  Contains the CSV tables which specify which pages correspond to what
* Shipped/
  Contains original specs, emails, and html
* html/
  Contains the html this program operates upon
  
### Usage

urlshifter.py takes two mandatory arguments and one optional one.  The
mandatory arguments are:

* -i input filename
* -o output filename

The optional argument is `-c configuration filename`.  It defaults to
"./urlshifter.cfg".

#### Configuration File

urlshifter's configuration file is a standard python "ConfigParser"
input file.  I've added comments to make it (theoretically)
self-documenting..

### Input and Output

`urlshifter.py` opens its input file read-only, and its output file
write. This means that each time you run `urlshifter.py`, it will
**destroy its output file** and replace it with new contents.  The
program produces an exceptions file in the filename specified in its
configuration file; that contains any complaints about missing input
pages, nonsensical link tags, or other confusion.

When run, the program will print its current input filename, the old
URL, and the new URL on stdout each time it changes a URL. If it finds
a link tag which it cannot understand (e.g. "<a>" or "<a href=>") it
will print "Oops" on stdout.  You can check the exceptions file to
determine which file had that trouble.

Whitespace in link tags is not preserved accurately between input and
output files..


