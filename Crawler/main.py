import requests
from bs4 import BeautifulSoup

f = open('user-ct-test-collection-09.txt','r')
rep = {}

with open('init.sql', 'w', encoding='utf-8') as file:
    file.write("CREATE TABLE Items(Id INT, Title VARCHAR(100),Description VARCHAR(511) , Keywords VARCHAR(511), URL VARCHAR(100));")
    file.write("\n")
    file.close()

for i in range(15000):
    line = f.readline()
    
    pal = line.split("\t")
    

    dic = None
    
    for j in pal:
        if("www." in j or "http://" in j):
            try:
                page = requests.get(j.strip(), timeout=2)
            except Exception:
                print("kk")

            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')
            
                meta_item = soup.find_all('meta')
            
                dic = {"id":pal[0],"title":"NULL", "description":"NULL", "keyword":"NULL", "URL": page.url}
            
                for item in meta_item:
                    if item.get("name") and item.get("content") and 'description' in item.get('name'):
                        if dic["description"]=="NULL":
                            dic["description"]=item.get("content").strip().replace("\n"," ").replace("\r","")
                        else: 
                            pass
                    if item.get('name') and item.get("content") and 'title' in item.get('name'):
                        if dic["title"]=="NULL":
                            dic["title"]=item.get("content").strip().replace("\n"," ").replace("\r","")
                        else: 
                            pass
                    if item.get('name') and item.get("content") and 'keyword' in item.get('name'):
                        if dic["keyword"]=="NULL":
                            dic["keyword"]=item.get("content").strip().replace("\n"," ").replace("\r","")
                        else: 
                            pass
    if dic:
        print(i, dic)
        query = "INSERT INTO items(id, title, description, keyword, URL) VALUES ("+str(dic["id"])+",'"+str(dic["title"]).replace("'"," ")+"','"+str(dic["description"]).replace("'"," ")+"','"+str(dic["keyword"]).replace("'"," ")+"','"+dic["URL"]+"');"
        
        file = open('init.sql', 'r', encoding='utf-8')
        finded = False
        for l in file:
            if(query in str(l)):
                finded = True
                break

        file.close()
        
        if(not finded):
            file = open('init.sql', 'a', encoding='utf-8')
            file.write("INSERT INTO items(id, title, description, keyword, URL) VALUES ("+str(dic["id"])+",'"+str(dic["title"]).replace("'"," ")+"','"+str(dic["description"]).replace("'"," ")+"','"+str(dic["keyword"]).replace("'"," ")+"','"+dic["URL"]+"');")
            file.write("\n")
            file.close()