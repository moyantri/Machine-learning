import sqlite3 as s
import pandas as pd
import requests
import operator
from bs4 import BeautifulSoup
from urllib.request import urlopen
from googlesearch import search

def checkyt(link):
    r=requests.get(link)
    if link.find("youtube")==-1 and r.status_code==200:
        return 1
    else:
        return 0



conn=s.connect("C:\\sqlite databases\\fake_news_data.db")
cur=conn.cursor()
r=cur.execute("select * from fake_news")
l=list(r)
l_df=pd.DataFrame(l)
new=input("Enter your news: ")
news=new.split()
count_d=[]
words=0
pos=0
percent=0
check2=[]
lcount=0
fpercent=0
flag=0
label=None
final_count=0
for i in range(1,len(l_df[1])):
    pos=int(i)
    for j in news:
        count_d.append(l_df[1][pos].count(j))
    for j in count_d:
        if j>=1:
            words=words+1
            j=1
    
    percent=((words)/len(news))*100
    
    if int(percent)>=90:
        
        body=l_df[2][i]
        for k in news:
            check2.append(body.count(k))
        for m in check2:
            if m>=1:
                final_count=final_count+1
                
        fpercent=final_count/len(news)*100
        
        if fpercent>=60:
            
            label=l_df[3][i]
            flag=1
            print("Your news exists in database!")    
        if label=="1":
            print("The news you entered is True!")
            print("Match Accuracy: ",fpercent)
        elif label=="0":
            print("The news you entered is False")
        
    
    
    words=0
    percent=0
    count_d=[]
    if flag==1:
        print("Thanks for using")
        break

if flag==0:
    print("Sorry! your news was not found in the dataset")
    print("Searching the Internet...")
    inter=[]
    inper=0
    incheck=0
    ilabel=None
    query=str(news)
    req_link=None
    for i in search(query,tld="com",num=10,start=0,stop=10,pause=2):
        a=checkyt(i)
        if a==1:
            req_link=i
            break
    if req_link==None:
        print("Unable to find results on the internet")
    else:
        print("Results found on internet!!")
        print(req_link)
        page=urlopen(req_link)
        ht=page.read().decode("utf-8")
        soup=BeautifulSoup(ht,"html.parser")
        para=soup.find_all("p")
        para_s=str(para)
        for m in news:
            if operator.contains(para_s,m)==True:
                incheck=incheck+1
        
        
        inper=(incheck/len(news))*100
        
        if inper>=90:
            print("News is True")
            print("Match Accuracy: ",inper)
            ilabel=1
        else:
            print("News is False")
            ilabel=0
            
    


cur.close()
conn.close()

