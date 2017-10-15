# IMNU-教务系统
## 利用python爬取imnu教务系统：
获取全部成绩，计算gpa，并存入数据库

## 实际效果：

![教务系统](http://wx3.sinaimg.cn/large/a27af0cbly1fkj5tieci8j20fb0ciwf7.jpg)

## 部分代码展示
**使用模块:**```import requestsfrom bs4 import BeautifulSoupimport reimport osimport pymysql```**学绩点(gpa)计算:**```def gpa(name,kechen,xuefen,score):    n=0    bixiu = []    bxxf =[]    bxcj =[]    while n<len(kechen):        if kechen[n] =='必修':            bixiu.append(name[n]+'|'+xuefen[n]+'|'+kechen[n]+'|'+score[n])            bxxf.append(xuefen[n])            bxcj.append(score[n])            n +=1        else:            n +=1    n=0    h=0    e=0    for n in range(0,len(bxxf)):                if int(bxcj[n])<60:            g=0        if int(bxcj[n])>=60:            g=1        if int(bxcj[n])>=65:            g=1.5          if int(bxcj[n])>=70:            g=2        if int(bxcj[n])>=75:            g=2.5        if int(bxcj[n])>=80:            g=3        if int(bxcj[n])>=85:            g=3.5           if int(bxcj[n])>=90:            g=4        if int(bxcj[n])>=95:            g=4.5                h +=g*int(bxxf[n])        e +=int(bxxf[n])        g=0    gpa=h/e    gpa=round(gpa,3)    return(gpa)
```**学生名字获取:**```def index():    r = s.get('http://eip.imnu.edu.cn:80/EIP/sytsso/other.htm?appId=NEWJWXT&uuid=ff8080815742d0ba015742d54b710004')    soup = BeautifulSoup(r.text, 'lxml')    xx0 = soup.find_all("div", class_='grxxT grxxb')    xx1 = re.sub(r'\r|\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t', '',str(xx0))    p = r'<pclass="name1">(.*?)</p>'    xx =re.findall(p,str(xx1))    return(xx[0])```## 联系方式：**我的公众号：**
![公众号](http://wx4.sinaimg.cn/mw690/a27af0cbly1fbpg26dks8j2058058mxa.jpg)
-------（wx-struggler）-------
**个人微信：**（strongdreams）期待我们有共同语言！
