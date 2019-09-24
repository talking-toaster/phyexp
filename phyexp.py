from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import date
import random


#学号
username='021800000'
#登录密码
passward='xxxxxxxxxxxxxx'
#填写课程的序号
toChoseCourse=[
   59,61,63,1,66,
]
#填写上课时间，第一位代表星期（1-7），第二位代表时间段（1-5），对应8,10,12,14,19点的课程
toChoseTime=[
    [2,3],
    [2,4],
    [3,3],
    [4,2],
    [4,4],
    [5,2],
    [5,3],
]

baseUrl = 'http://phyexp.nuaa.edu.cn/wechat'
couseIDList=[
    ['62','必修-用电位差计校准毫安表（理116南，考试型实验，详见微信公众号实验课件中的实验须知）','1'],#0
    ['59','必修-分光计的调节（理118）','1'],#1
    ['61', '必修-超声声速的测量（理103）','1'],#2
    ['63','必修-迈克耳孙干涉仪 （理101）','1'],#3
    ['60','必修-用分光计测量棱镜材料折射率（理118）','1'],#4
    ['65', '选修-全息照相 （理107）','0'],#5
    ['101','选修-表面张力测量（理110）','0'],#6  
    ['64','选修- 霍耳效应法测磁场 （理112）','0'],#7 
    ['92','选修-热电效应（120）','0'],#8 
    ['1','选修—牛顿环(理106) ','0'],#9
    ['0','选修-动态法测量金属的杨氏模量 （理116北）','0'],#10 
    ['66','选修- 铁磁材料磁化特性研究（理214）','0']#11
]
timeExpList = ['08','10','14','16','19']


def initWebdriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation']) 
    options.add_argument('--headless')
    driver = webdriver.Chrome( options=options) 
    driver.get(baseUrl)
    return driver

def login(driver,username,password):
    inputName = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[1]/div[2]/input')
    inputPassword = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/input')
    btLogin = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/button')
    inputName.click()
    time.sleep(random.random())
    inputName.send_keys(username)
    time.sleep(random.random())
    inputPassword.click()
    inputPassword.send_keys(password[0:3])
    time.sleep(0.13)
    inputPassword.send_keys(password[3:len(password)+1])
    time.sleep(0.17)
    btLogin.click()

def findTime(driver):
    timeList = []
    for i in range(20):
        try:
            textLable = driver.find_element_by_xpath(f'//*[@id="vux_view_box_body"]/div[2]/div[{i}]/div/div[2]/p/lable')
            timeList.append(textLable.text)
        except:
            continue
    return timeList
def findChoseBt(driver):
    choseBtList = []
    for i in range(20):
        try:
            choseBt = driver.find_element_by_xpath(f'//*[@id="vux_view_box_body"]/div[2]/div[{i}]/div/div[2]/span/div/div[2]/button')
        except:
            continue
        time = driver.find_element_by_xpath(f'//*[@id="vux_view_box_body"]/div[2]/div[{i}]/div/div[2]/p/label')
        choseBtList.append([time.text,i])
    return choseBtList
def main():
    driver = initWebdriver()
    login(driver,username,password)
    time.sleep(random.random())
    for couse in toChoseCourse:
        url = baseUrl+f'/experiment/{couse}/lessons'
        driver.get(url)
        choseBtList = findChoseBt(driver)
        for choseBt in choseBtList:
            for choseTime in toChoseTime:
                if date(int(choseBt[0][0:4]),int(choseBt[0][5:7]),int(choseBt[0][8:10])).isoweekday() == choseTime[0] \
                            and choseBt[0][11:13] == timeExpList[choseTime[1]-1] :
                    if date(int(choseBt[0][0:4]),int(choseBt[0][5:7]),int(choseBt[0][8:10])).__sub__(date.today()).days>1:
                        print('可选择'+str(couse)+' '+choseBt[0])
                        driver.execute_script(f'document.querySelector("#vux_view_box_body > div.router-view > div:nth-child({choseBt[1]}) > div > div.vux-cell-bd.vux-cell-primary > span > div > div.action-wrapper > button").click()')
                        time.sleep(3)        
                        #driver.execute_script(f'document.querySelector("body > div:nth-child(9) > div > div > div.weui-dialog > div.weui-dialog__ft > a.weui-dialog__btn.weui-dialog__btn_default").click()')
                        driver.execute_script(f'document.querySelector("body > div:nth-child(9) > div > div > div.weui-dialog > div.weui-dialog__ft > a.weui-dialog__btn.weui-dialog__btn_primary").click()')
                        return True
        driver.close()
        return False
if __name__ == "__main__":
    gotCourse = False
    while(not gotCourse):
        minsTo1200 = abs(time.localtime().tm_hour*60+time.localtime().tm_min-720)
        if  minsTo1200 <2:
            try:
                main()
                time.sleep(random.uniform(2.7,3.5))
            except:
                print('在一次刷新中出错')
            
        elif minsTo1200 <5:
            try:
                main()
                time.sleep(random.randint(18,23))
            except:
                print('在一次刷新中出错')
            
        elif time.localtime().tm_hour in range(7,20):
            try:
                main()
                time.sleep(random.randint(60*10,60*12))
            except:
                print('在一次刷新中出错')
            
        else:
            try:
                main()
                time.sleep(random.randint(60*25,60*28))
            except:
                print('在一次刷新中出错')
            
                




