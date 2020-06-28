#Amlan Saha Kundu, 2020

import requests,io,pdfkit,os,shutil
from bs4 import BeautifulSoup

os.mkdir("DB")
os.mkdir("TAG")
os.mkdir("DATE")

newurl = []
taglist = []
datelist = []

print("Initializing...")
initurl = "https://aspirantworld.in/category/editorialanalysis/the-hindu/"
result = requests.get(initurl)
src = result.content
soup = BeautifulSoup(src, 'lxml')
num = int(soup.find("a",{"class": "page-numbers"}).getText())
print("Start Scrapping...\nGenerating URL...")


def url_generator(num):
    url = "https://aspirantworld.in/category/editorialanalysis/the-hindu/page/"+str(num)
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    links = soup.find_all("a")
    keyword ="[Editorial Analysis]"

    for link in links:
        if keyword in link.text:
            #print(link)
            a = (link.attrs['href'])
            newurl.append(a)

def gen_html(filename,burl):
    def trim(url):
        result = requests.get(url)
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        try:
            tag = soup.find("div",{"class": "entry-tags"}).getText()
        except NoneType:
            tag = "NotDefined"
        taglist.append(tag)
        date = soup.find("li",{"class": "meta-date"}).getText()[1:]
        datelist.append(date)
        article = str(soup.find_all("article"))[1:-5925].replace("[Editorial Analysis]","")
        text = '<!DOCTYPE html><html><head> <style>body{font-size:15px; margin: 5%; font-family: "Comfortaa","CMU Serif";}.page-title{color: red; font-size: 25px;}p{color: #480d9a;}</style> </head><body>'+article
        return text

    open(filename, "w").close()
    with io.open(filename, "w",encoding="utf-8") as htmlfile:
            htmlfile.write(trim(burl))
    htmlfile.close()
    
def checkpath(path):
    return(not(os.path.isfile(path)))

def checkdir(path):
    if (not(os.path.isdir(path))):
        os.mkdir(path)
        print("DIR CREATED"+str(path))
'''
def tag(url):
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    tag = soup.find("div",{"class": "entry-tags"}).getText()
    return(tag)

def date(url):
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    date = soup.find("li",{"class": "meta-date"}).getText()[1:]
    return(date)
    

def savepdf(url,loc):
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url(url,loc, configuration=config)
'''
    
for i in range(1,(num+1)):
    print("Page: "+str(i))
    url_generator(i)

open("onlineindex.html", "w").close()
with io.open("onlineindex.html", "w",encoding="utf-8") as htmlfile:
    for i in range(0,len(newurl)):
        title = str((newurl[i][44:-1].replace("-"," ").capitalize()))
        finance = "<br><a href='"+str(newurl[i])+"'target='_blank'>"+str(i+1)+"."+title+"</a>"
        htmlfile.write(str(finance))
        htmlfn = "./DB/"+title+".html"
        url = str(newurl[i])
        if checkpath(htmlfn):
            gen_html(htmlfn,url)
            print(htmlfn)
            tag = taglist[-1]
            date = datelist[-1][:-7]
            #print(tag)
            #print(date)
            dirpathtag = "./TAG/"+str(tag)
            dirpathdate = "./DATE/"+str(date)

            checkdir(dirpathtag)
            oldpath = htmlfn
            newpath = dirpathtag+"/"+title+date+".html"
            shutil.copy(oldpath,newpath)
            
            checkdir(dirpathdate)
            newpath = dirpathdate+"/"+title+tag+".html"
            shutil.copy(oldpath,newpath)
        #savepdf(url,pdft)
        
htmlfile.close()    
#print(len(newurl))
        
