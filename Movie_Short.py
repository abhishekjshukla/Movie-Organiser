import requests
from bs4 import BeautifulSoup as bs
import re
import shutil
from pathlib import Path
import os





def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath) 
    return allFiles   





def googleSearch(query):
    with requests.session() as c:
        url = 'https://www.google.co.in/search?'
        query = {'q': query}
        urllink = requests.get(url, params=query)
        return urllink.url




path='' # Give Path of Movie Folder





lst=getListOfFiles(path)

# Create New Folders according to  Rating
dirs=['GT9','GT8','GT7.5','GT7','Garbage']
for i in dirs:
    if not os.path.exists(path+'/'+i):
        os.makedirs(path+'/'+i)





for i in lst:
    ext=["avi","mkv","mpeg","mpg","mov","mp4",'srt']
    text=i
    if text[-3:] in ext:
        text=os.path.basename(text)
        text1 = re.search('([^\\\]+)\.(avi|mkv|mpeg|mpg|mov|mp4|srt)$', text)
        if text1:
            text = text1.group(1)
        if(text not in dirs):
            text = text.replace('.', ' ').title()
        text2 = re.search('(.*?)(dvdrip|xvid| cd[0-9]|dvdscr|brrip|divx|[\{\(\[]?[0-9]{4}).*', text)
        if text2:
            text = text2.group(1)
        text3 = re.search('(.*?)\(.*\)(.*)', text)
        if text3:
            text = text3.group(1)
        print(text)
        glink=googleSearch(text+' movie rating')
        req=requests.get(glink)
        page=req.content
        soup = bs(page, 'lxml')
        doc=soup.prettify()
        rating_pattern=re.compile(r'(\d+(\.\d+)?)/10')
        try:
            mt=rating_pattern.findall(str(doc))[0][0]
            rating=float(mt)
            print(text,rating)
            new_path=os.path.dirname(i)+"/"+text+i[-4:]
            os.rename(i,new_path)
            if(rating>=9):
                shutil.move(new_path,path+'/'+'GT9')
            elif(rating<9 and rating>=8):
                shutil.move(new_path,path+'/'+'GT8')
            elif(rating<8 and rating>=7.5):
                shutil.move(new_path,path+'/'+'GT7.5')
            elif(rating<7.5 and rating>=7):
                shutil.move(new_path,path+'/'+'GT7')
            else:
                shutil.move(new_path,path+'/'+'Garbage')
        except Exception as ex:
            print(ex)



