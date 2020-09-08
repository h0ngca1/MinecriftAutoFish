#!/usr/bin/env python
# coding: utf-8

# In[7]:


import time
import pyautogui
import cv2
from playsound import playsound


# In[8]:


#等待用户切屏到游戏
playsound("audios\\switchtogame.mp3")


# In[ ]:


#取屏幕尺寸
(l_x, l_y) = pyautogui.size() 
#计算截屏范围
#钓鱼要求:鱼钩在准星到底部的中间即65%-85%高度
l_left = l_x * 0.49
l_top = l_y * 0.65
l_width = l_x * 0.02
l_height = l_y * 0.2


# In[ ]:


#甩钩
pyautogui.click(button='right')
playsound("audios\\startfishing.mp3")

#等待鱼钩稳定下来
time.sleep(2)

#截图:未上钩
pyautogui.screenshot("initialhook.png",region = (l_left, l_top, l_width, l_height))

#读取图片
img = cv2.imread("initialhook.png")
#灰度化
grayimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#二值化
ret, binary = cv2.threshold(grayimg,100,255,cv2.THRESH_BINARY)
#识别轮廓
contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#框出来
# cv2.drawContours(img,contours,-1,(0,0,255),1)
# cv2.imshow("img", img)
# cv2.waitKey()
# cv2.destroyAllWindows()


# In[ ]:


#计算鱼钩中心及鱼钩高度
hooktop = 9999
hookbottom = 0
ysumfinal = 0
cts = len(contours)
    
for contour in contours:
    ysum = 0
    pts = len(contour)
    for i in range(0,pts):
        ysum += contour[i,0,1]
        hooktop = min(hooktop,contour[i,0,1])
        hookbottom = max(hookbottom,contour[i,0,1])
    ycenter = ysum / pts
    ysumfinal += ycenter
hookheight = hookbottom - hooktop
ycenterfinal = ysumfinal / cts
print("------------")
print("鱼钩位置=",ycenterfinal)
print("鱼钩高度=",hookheight)

#计算上钩位置
yhooklimit = ycenterfinal + hookheight * 1.5
print("上钩位置>",yhooklimit)


# In[ ]:


while 1 == 1:
    #每0.3秒截屏并判断一次
    time.sleep(0.3)
    
    #截图:未上钩
    pyautogui.screenshot("checkhook.png",region = (l_left, l_top, l_width, l_height))

    #读取图片
    img = cv2.imread("checkhook.png")
    #灰度化
    grayimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #二值化
    ret, binary = cv2.threshold(grayimg,100,255,cv2.THRESH_BINARY)
    #识别轮廓
    contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cts = len(contours)
    
    #如果没有轮廓:上钩/不在钓鱼状态
    if cts == 0:
        #拉钩或甩钩
        pyautogui.click(button='right')
        print("鱼钩不见了,拉钩或甩钩！")
        time.sleep(2)
        continue
    
    #计算鱼钩高度
    ysumfinal = 0
    for contour in contours:
        ysum = 0
        pts = len(contour)
        for i in range(0,pts):
            ysum += contour[i,0,1]
        ycenter = ysum / pts
        ysumfinal += ycenter
    ycenterfinal = ysumfinal / cts
    
    #判断是否上钩
    if ycenterfinal >= yhooklimit:
        #拉钩
        pyautogui.click(button='right')
        print("上钩！鱼钩高度=",ycenterfinal,">",yhooklimit)
        #再甩钩
        pyautogui.click(button='right')
        print("甩钩！")
        time.sleep(2)
#     else:
#         print("等待中...鱼钩高度=",ycenterfinal)


# In[ ]:




