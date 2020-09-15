######################################################################
######################################################################
######                                                           #####
######  Import and parse XML Files containing meccg dream cards  #####
######                                                           #####
######################################################################
######################################################################

import os
from pathlib import Path
import re
from lxml import etree
from itertools import groupby

################################
# Get XML Files for processing #
################################

XMLFiles = [file for file in os.listdir('XML Files') if re.findall('_',file) != []]

assert len(XMLFiles) > 0, "No Files in Listed Directory" 

######################################
# Dictionary of prefixes:[filepaths] #
######################################

# Setup

# Key function
def prefix(string: str):
    return string[0: string.index('_')]


# Dictionary
FilesDict = {key: list(value) for key, value in groupby(XMLFiles, prefix)}


#################
#################
### Parse XML ###
#################
#################

# 'rb' opens file as reading + binary, meaning that the bytes in the file 
# are not automatically decoded.  
# This is necessary, because we can't pass a decoded file using etree.fromstring


# del FilesDict['gw'][5]
# FilesDict

# FilesDict={'gw':['gw_char.xml'],'nec':['nec_char.xml']}

# FilesDict

# Get column names from XML
column_names = []

# for filelist in FilesDict.values():
#     for file in filelist:
#         root = etree.fromstring(open(Path(os.getcwd(),'XML Files',file),'rb').read(),parser=etree.XMLParser(encoding='ISO-8859-1'))
#         print(file,'a',root)
#         root = etree.fromstring(open(Path(os.getcwd(),'XML Files',file),'rb').read(),parser=etree.XMLParser(encoding='ascii//TRANSLIT'))
#         print(file,'b',root)

for filelist in FilesDict.values():
    for file in filelist:
        # root = etree.fromstring(open(Path(os.getcwd(),'XML Files',file),'rb').read(),parser=etree.XMLParser(encoding='ISO-8859-1'))
        root = etree.fromstring(open(Path(os.getcwd(),'XML Files',file),'rb').read(),parser=etree.XMLParser(encoding='ascii//TRANSLIT'))

        # Grab keys 
        for i in root.iterchildren():
            for j in i:
                for key in j.keys():
                    if key not in column_names:
                        column_names.append(key)

        for i in root[0].iterchildren():
            for j in i:
                if j.get("key") not in column_names:
                    column_names.append(j.get("key"))

            
# return values for multiple keys at once.
def dict_return(dict,*keys):
    values = []
    for i in keys:
        values.append(dict.get(i))
    return values


# ### Loop through xml generating list of lists where each sub-list is a card.  Values for unused attributes marked as none.

dict_sets = {prfx:[] for prfx in {prefix(i) for i in XMLFiles}}

for file in XMLFiles:
    # root = etree.fromstring(open(Path(os.getcwd(),'XML Files',file),'rb').read(),parser=etree.XMLParser(encoding='ISO-8859-1'))
    root = etree.fromstring(open(Path(os.getcwd(),'XML Files',file),'rb').read(),parser=etree.XMLParser(encoding='ascii//TRANSLIT'))
    for setkey in dict_sets:
        for i in root[0].iterchildren():
            item = []
            for key,value in zip(i.keys(),i.values()): 
                #for value in i.values():
                item.append(key)
                item.append(value)
            item = [item[i:i+2] for i in range(0, len(item), 2)] 
            for j in i.iterchildren():
                item.append((j.values()))
            #print(item)    
            dct = dict(item)
            # print(dict_return(dct,*column_names))
            # print(key)
            dict_sets[setkey].append(dict_return(dct,*column_names))

print(dict_sets)



####################################
# put list of lists into dataframe #
####################################

import pandas as pd

df_xml = pd.DataFrame(items,columns = column_names)

df_xml['Set']='Necromancer'
df_xml['GI']=None
df_xml['magic']=None
df_xml['specific']=None


# %%
df_xml['graphics']=df_xml['graphics'].str.replace('-','')
df_xml['graphics']=df_xml['graphics'].str.replace('''''','')
df_xml['graphics']=df_xml['graphics'].str.replace('\'','')

df_xml['name']=df_xml['name'].str.replace('Ã»','A')


# %%
df_xml=df_xml.fillna('')


# %%
print(df_xml[df_xml['name'].str[:1]=='B'])


# %%
df_xml[df_xml.name=='Breeder\'s Stock']


# %%



# %%
df_xml.head(5)


# %%
#for i in column_names:
#    print(i,'|',column_names.index(i))    


# %%
pd.set_option("display.max_colwidth", 10000)


# %%
print(df_xml['text'][df_xml['name']=='Mordor Rebuilt'])


# %%
print(df_xml['text'])


# %%
#df_xml_exp = df_xml[['name','Set','graphics','type','class','race']]
#For Nec
#df_xml_exp = df_xml.iloc[:,[0,29,1,3,6,14,13,12,9,10,30,7,8,16,19,11,18,31,32,15,25,22,23,24,4,2]]

#For GW
df_xml_exp = df_xml.iloc[:,[0,30,1,3,6,14,13,12,9,10,31,7,8,16,19,11,18,32,32,15,25,22,23,24,4,2]]


# %%
df_xml_exp.to_clipboard(sep='\t',index=False)


# %%
for i in list(df_xml.columns):
    print(i,'|',list(df_xml.columns).index(i))


# %%
df_xml_exp.head(1)


# %%
print(df_xml.head(10))


# %%
#import unicodedata
#for i in df_xml:
    #print(unicodedata.normalize('NFKD', i).encode('ASCII', 'ignore'))


# %%
all_char=[]

for i in df_xml['text']:
    for j in i:
        all_char.append(j)

print(set(all_char))    
    


# %%



# %%



# %%



# %%



# %%



# %%



# %%
item = []
items = []

for i in root[0].iterchildren():
    
    for j in i.iter():    
        item.extend(j.values())
    items.append(item)
    item = []
    
#print(item)
print(len(items))
#print(items)


# %%
item = []
items = []

for i in root[0].iterchildren():
    for key,value in zip(i.keys(),i.values()): 
        #for value in i.values():
        item.append(key)
        item.append(value)
    item = [item[i:i+2] for i in range(0, len(item), 2)]    
    dct = dict(item)
    items.append(dict_return(dct,*column_names))
    item=[]
    
print(items)


# %%
help(root)


# %%



# %%
print(column_names)


# %%
print(dict_return(dct,*column_names))


# %%
print(dct)


# %%
print(column_names)


# %%
help(zip)


# %%
items = [j.replace('body', 'gone') for w in items for j in w]


# %%
help(items.remove)


# %%



# %%



# %%



# %%



# %%



# %%



# %%



# %%
etree.tostring(tree.getroot())


# %%
help(root.attrib)


# %%
from lxml import etree

def parseBookXML(xmlFile):

    with open(xmlFile,'rb') as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)

    book_dict = {}
    books = []
    for book in root.getchildren():
        for elem in book.getchildren():
            if not elem.text:
                text = "None"
            else:
                text = elem.text
            print(elem.tag + " => " + text)
            book_dict[elem.tag] = text
        if book.tag == "cards":
            books.append(book_dict)
            book_dict = {}
    return books

if __name__ == "__main__":
    parseBookXML(xmlFile)
    #parseBookXML("books.xml")


# %%
for i in root[0]:
    print(i.values())


# %%
help(root.tag)


# %%
help(etree)


# %%
root[0][0].items()


# %%
for i in root[0]:
    print(i.get(i.keys))


# %%
help(root)


# %%
len(items[1])


# %%
items[1]


# %%
items = []

for i in root[0].iter():
    #print(i.values())
    items.append(i.values())

print(items)
    


# %%



# %%



# %%



# %%



# %%



# %%
from urllib.request import urlopen
from xml.etree.ElementTree import parse
# Download the RSS feed and parse it
#u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(FilePath)
# Extract and output tags of interest


# %%



# %%
for item in doc.iterfind('channel/item'):
    rarity = item.findtext('rarity')
    #date = item.findtext('pubDate')
    #link = item.findtext('link')
print(book)
#print(date)
#print(link)
#print()
#6.3


# %%
from lxml import etree
item = doc.getroot()[0]
print(item.get("game"))


# %%
from xml.etree.ElementTree import ElementTree as etree


# %%
import lxml.etree as etree


# %%
#print(etree.tostring(doc, pretty_print=True))


# %%
#test_write = etree.write(FilePath)


# %%



# %%
import os
os.getcwd()


# %%



# %%
items = []

for i in root[0].iter():
    items.extend(i.values())
        
print(items)
print(len(items))


# %%
xmlFile = r'C:\Users\Me3\Desktop\dc-master\development\nec_char.xml'.replace('\\','/')
print(xmlFile)


# %%
from lxml import etree

def parseBookXML(xmlFile):

    with open(xmlFile) as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)

    book_dict = {}
    books = []
    for book in root.getchildren():
        for elem in book.getchildren():
            if not elem.text:
                text = "None"
            else:
                text = elem.text
            print(elem.tag + " => " + text)
            book_dict[elem.tag] = text
        if book.tag == "book":
            books.append(book_dict)
            book_dict = {}
    return books

if __name__ == "__main__":
    parseBookXML("nec_char.xml")


# %%
import lxml.etree as etree

doc = etree.parse(FilePath)
print(etree.tostring(doc))#, pretty_print=True))

