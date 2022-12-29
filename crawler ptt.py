import requests
from bs4 import BeautifulSoup
import numpy as np
new_url = "https://www.ptt.cc/bbs/Football/index"
totalgood=0
totalgreat=0
totalbad=0
dic = {}
count = 0
headers = {"cookie": "over18=1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35"}
warticle = open('article.csv',"w+",newline="",encoding="utf-8-sig")
wcomment = open('comment.csv',"w+",newline="",encoding="utf-8-sig")
wcomment_a = open('commend_a.csv',"w+",newline="",encoding="utf-8-sig")
for i in range(102,103):
    
    
    url1  = new_url + str(i) + ".html"
    
    r = requests.get(url1)
    soup = BeautifulSoup(r.text,"lxml")
    titles = soup.find_all(class_='title')
    for j, title in enumerate(titles):
        try:
            link = title.find('a')['href']        
            if ('https' not in link):
                link = f'https://www.ptt.cc/{link}'
                
               
                r = requests.get(link)
                r.encoding = "utf8"
                
                soup = BeautifulSoup(r.text,"lxml")
                
                tag_div = soup.findAll(class_ = "article-meta-value") # 作者 標題 時間
                author = tag_div[0].text
                autitle = tag_div[2].text.replace(',','')
                autime = tag_div[3].text 
                ym = autime[20:24]+autime[4:7]
                if ym in dic.keys():
                    dic[ym] += 1
                else:
                    dic[ym]=1 

                count +=1
                count1 = ("A"+str(count).zfill(5))

                #---------------------
                content_of_web = soup.find(id='main-content') # 內文
                
                content_of_web = content_of_web.text
                content_of_web = content_of_web.split('\n')
                content_of_web = content_of_web[1:]
                content_of_target = []
                
                for i, content in enumerate(content_of_web):
                    
                    if (content == ''):
                        continue
                    if (content == '--'):  
                            break
                    content_of_target.append(content.replace(",","，"))
                content_of_target = ("".join(content_of_target))
                content_of_target = content_of_target.replace("  ","" ).replace(" ","").replace("   ","").replace("    ","")
                warticle.write(count1+","+author+","+autitle+","+autime+","+content_of_target+"\n")
               
                #---------------------
                
                tag_push  = soup.findAll(class_ = "push") # → 推 噓 總和
                good = 0 
                great = 0
                bad = 0
                c2=[]
                for push in  tag_push:
                    c2.append(push.text[0]+",")
                    if (push.text[0] == "→"):
                        good+=1
                        totalgood+=1
                    elif(push.text[0] == "推"):
                        great+=1
                        totalgreat+=1
                    else:
                        bad +=1
                        totalbad+=1
                       
               # print("→總共有"+str(good)+"次") 
               #print("噓總共有"+str(bad)+"次")          
                #print("推總共有"+str(great)+"次")
                allcomment = good+bad+great
                #print("此文章評論共有"+str(allcomment)+"個")
                gor = round(good/allcomment,2)
                grr = round(great/allcomment,2)
                bar = round(bad/allcomment,2)
                
               
                ta =  ""
                ta = f"{count1},{good},{great},{bad},{allcomment},{gor},{grr},{bar}\n"
                wcomment_a.write(ta)
                #print(ta)
                #---------------------    
                c3=[]
                c4=[]
                c5=[]    
                tag_userid = soup.findAll(class_ = "f3 hl push-userid") 
                for user in tag_userid:
                    c3.append(user.text+",")
                    
                
                tag_content = soup.findAll(class_ = "f3 push-content")
                for content1 in tag_content:
                    c4.append(content1.text[1:].replace(",","，")+",")
                
                tag_ipdatetime = soup.findAll(class_ = "push-ipdatetime")
                for ipdatetime in tag_ipdatetime:
                    c5.append(ipdatetime.text)
                
                for a in range(np.size(c2)):
                    t=""
                    t=(count1+","+c2[a]+c3[a]+c4[a]+c5[a])
                    wcomment.write(t)
             
                #---------------------

        except:
            link = '文章已被刪除'
       # finally:
            #print("------------------------")
        
warticle.close()
wcomment.close()
wcomment_a.close()
print(dic)
print("→總共有"+str(totalgood)+"次") 
print("噓總共有"+str(totalbad)+"次")          
print("推總共有"+str(totalgreat)+"次")