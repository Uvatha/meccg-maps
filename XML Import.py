# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
Test Git
    ## Take list of string file paths and convert to useable paths.

    ## Great Wyrms Files
FilesList = [
            r'C:\Users\Me3\Desktop\MECCG\XML\XML\gw_char.xml',
            r'C:\Users\Me3\Desktop\MECCG\XML\XML\gw_char2.xml',
            r'C:\Users\Me3\Desktop\MECCG\XML\XML\gw_haz.xml',
            r'C:\Users\Me3\Desktop\MECCG\XML\XML\gw_rec.xml',
            r'C:\Users\Me3\Desktop\MECCG\XML\XML\gw_rec2.xml',
            r'C:\Users\Me3\Desktop\MECCG\XML\XML\gw_sites.xml'
           ]
        
from pathlib import Path

FilesDict = {'gw':[Path(i) for i in FilesList]}

    ## Necromancer Files
FilesList = [r'C:\Users\Me3\Desktop\MECCG\XML\XML\nec_char.xml',
            r'C:\Users\Me3\Desktop\MECCG\XML\XML\nec_haz.xml',
            r'C:\Users\Me3\Desktop\MECCG\XML\XML\nec_rec.xml',
            r'C:\Users\Me3\Desktop\MECCG\XML\XML\nec_sites.xml'
            ]

FilesDict['nec']=[Path(i) for i in FilesList]


    ## Parse xml

## 'rb' opens file as reading + binary, meaning that the bytes in the file are not automatically decoded.  
## This is necessary, because we can't pass a decoded file using etree.fromstring

#from lxml import etree

#root = etree.fromstring(open(xmlFile,'rb').read(),parser=etree.XMLParser(encoding='ISO-8859-1'))

# ### pull column names

from lxml import etree

column_names = []


pathx = Path(r'C:\Users\Me3\Desktop\MECCG\XML\XML\nec_char.xml')
pathstr=pathx.__str__()

parser = etree.XMLParser()
tree=etree.parse(pathstr,parser)



//node[not(@*)]
xpstr = '//cards/card//@*

tree.xpath(xpstr)

etree.tostring(tree,pretty_print=True)

#//*[contains(text(),'')]

pathx.

for file in FilesDict['nec']:
    #root = etree.fromstring(open(file,'rb').read(),parser=etree.XMLParser(encoding='ISO-8859-1'))
    root = etree.fromstring(open(file,'rb').read(),parser=etree.XMLParser(encoding='ascii//TRANSLIT'))

    ## Grab keys 
    for i in root.iterchildren():
        for j in i:
            for key in j.keys():
                if key not in column_names:
                    column_names.append(key)

    for i in root[0].iterchildren():
        for j in i:
            if j.get("key") not in column_names:
                column_names.append(j.get("key"))

            
print(column_names)          
            #print(len(i))
    #for j in i.iterchildren:
     #   print(j.values)

# ### return values for multiple keys at once.

# %%
def dict_return(dict,*keys):
    values = []
    for i in keys:
        values.append(dict.get(i))
    return values

# %% [markdown]
# ### Loop through xml generating list of lists where each sub-list is a card.  Values for unused attributes marked as none.

# %%
item = []
items = []

for file in xmlFiles:
    #root = etree.fromstring(open(file,'rb').read(),parser=etree.XMLParser(encoding='ISO-8859-1'))
    root = etree.fromstring(open(file,'rb').read(),parser=etree.XMLParser(encoding='ascii//TRANSLIT'))

    for i in root[0].iterchildren():
        for key,value in zip(i.keys(),i.values()): 
            #for value in i.values():
            item.append(key)
            item.append(value)
        item = [item[i:i+2] for i in range(0, len(item), 2)] 
        for j in i.iterchildren():
            item.append((j.values()))
        #print(item)    
        dct = dict(item)
        items.append(dict_return(dct,*column_names))
        item=[]
    
#print(items)
 

# %% [markdown]
# ### put list of lists into dataframe

# %%
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

