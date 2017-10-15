import requests
from bs4 import BeautifulSoup
import re
import os
import pymysql


s = requests.Session()
db = pymysql.connect(host='localhost',port=3307,user='root',passwd='usbw',db='score',charset='utf8')
cursor = db.cursor()

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }

def index_post(name,password):
    data = {
    'username': str(name),
    'password': str(password),
   
    'verification':'',
    }
    
    r = s.post('http://eip.imnu.edu.cn/EIP/syt/login/Login.htm', data,headers=header)
    
def index():
    r = s.get('http://eip.imnu.edu.cn:80/EIP/sytsso/other.htm?appId=NEWJWXT&uuid=ff8080815742d0ba015742d54b710004')
    soup = BeautifulSoup(r.text, 'lxml')
    xx0 = soup.find_all("div", class_='grxxT grxxb')
    xx1 = re.sub(r'\r|\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t', '',str(xx0))
    p = r'<pclass="name1">(.*?)</p>'
    xx =re.findall(p,str(xx1))
    return(xx[0])
    
def get_score():
    r = s.get('http://210.31.186.11/qbcj',headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    divs = soup.find_all("tr", class_='odd gradeX')
    value1 = re.sub(r'<font color="red">|</font>|\r|\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t', '',str(divs))
    p = r'<td>(.*?)</td>'
    value = re.findall(p,str(value1))
    return(value)
#-----------------gpa的计算方式在这里哦----------------
def gpa(name,kechen,xuefen,score):
    n=0
    bixiu = []
    bxxf =[]
    bxcj =[]
    while n<len(kechen):
        if kechen[n] =='必修':
            bixiu.append(name[n]+'|'+xuefen[n]+'|'+kechen[n]+'|'+score[n])
            bxxf.append(xuefen[n])
            bxcj.append(score[n])
            n +=1
        else:
            n +=1
    n=0
    h=0
    e=0
    for n in range(0,len(bxxf)):
        
        if int(bxcj[n])<60:
            g=0
        if int(bxcj[n])>=60:
            g=1
        if int(bxcj[n])>=65:
            g=1.5  
        if int(bxcj[n])>=70:
            g=2
        if int(bxcj[n])>=75:
            g=2.5
        if int(bxcj[n])>=80:
            g=3
        if int(bxcj[n])>=85:
            g=3.5   
        if int(bxcj[n])>=90:
            g=4
        if int(bxcj[n])>=95:
            g=4.5
        
        h +=g*int(bxxf[n])
        e +=int(bxxf[n])
        g=0
    gpa=h/e
    gpa=round(gpa,3)
    return(gpa)

def main():
    stu_id=input('请输入您的学号')  
    stu_password=input('请输入您的密码')
    index_post(stu_id,stu_password)
    print('%s同学你好\r\n下面是你近几年的成绩以及gpa:\r\n'%index())
    value=get_score()
    len1=len(value)
    #print(len1)  判断数组长度
    print('课程名|'+'学分|'+'课程属性|'+'成绩')
    num=1
    name = []
    xuefen = []
    kechen = []
    score = []
    grade = []
    while num<len1-1:
       
        name.append(value[num])
        xuefen.append(value[num+3])
        kechen.append(value[num+4])
        score.append(value[num+5])
        if int(value[num+5])<60:
            grade.append(value[num]+'|'+value[num+3]+'|'+value[num+4]+'|'+value[num+5]+'(不好意思同学你这门挂了！)')
            
        else:
            grade.append(value[num]+'|'+value[num+3]+'|'+value[num+4]+'|'+value[num+5])
        num +=8
       
    n=0    
    for n in range(0,len(grade)):
        print(grade[n])#入库操作
        sql = "insert into score(student_id,name,k_name,k_xuefen,k_kechen,k_score) values('{}','{}','{}','{}','{}','{}') ".format(stu_id,index(),name[n],xuefen[n],kechen[n],score[n])
        cursor.execute(sql)#执行sql语句
        db.commit()
     
    gpa_=gpa(name,kechen,xuefen,score)    
    print('你的gpa为:%s'%gpa_) 
    
#-------------------------------------优化优化---------------------------#
if __name__=='__main__':
    main()
    db.close()
    os.system("pause>nul")
