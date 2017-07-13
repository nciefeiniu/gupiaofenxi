'''
Created on 2017年6月11日

@author: liutao
'''
import urllib
import urllib.parse
from bs4 import BeautifulSoup
from urllib import request
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import num2date


#爬的网易的数据，新浪的太难爬。
url = r'http://quotes.money.163.com/trade/lsjysj_600052.html'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'Michael Foord',

          'location' : 'Northampton',

          'language' : 'Python' }

headers = { 'User-Agent' : user_agent }

data = urllib.parse.urlencode(values).encode(encoding='UTF8')
req = urllib.request.Request(url, data, headers)
htm = request.urlopen(req)
#创建beautifulsoup对象
soup = BeautifulSoup(htm, "html.parser")   
#提取div标签
mess = soup.find('div',attrs={'class':'area'})
#提取table标签
ta = mess.find('table',attrs={'class':'table_bg001 border_box limit_sale'})
#提取tr标签
ymd = ta.find_all('tr')
#删除列表中的空数据
del ymd[0]
daily = []  #年月日
sta = []    #开盘价
end = []    #收盘价
max = []    #最高价
min = []    #最低价
for y in ymd:
    days = y.find_all('td')
    daily.append(days[0].get_text())
    sta.append(days[1].get_text())
    max.append(days[2].get_text())
    min.append(days[3].get_text())
    end.append(days[4].get_text())
    
'''
#开始画图
#数据已经抓取完成
#保存在三个列表中daily   sta   end
#画折线图
'''

data = []
for d in daily:
    data.append(datetime.strptime(d,'%Y-%m-%d').date())
#反转列表
data = list(reversed(data))     
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=10) 
#配置横坐标
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
#横坐标间隔
plt.xticks(pd.date_range(data[0],data[-1],freq='10d'))
x = np.array(data)
y1 = np.array(sta)
y2 = np.array(end)
y3 = np.array(max)
y4 = np.array(min)

plt.figure(1)
ax1 = plt.subplot(111)
ax1.set_title("股票代码：600052  浙江广厦",fontproperties=font)
ax1.set_xlabel("时间",fontproperties=font)
ax1.set_ylabel("股价（元）",fontproperties=font)
ax1.plot(x,y1,'r')
ax1.plot(x,y2,'b')
ax1.plot(x,y3,'g')
ax1.plot(x,y4,'y')
plt.gcf().autofmt_xdate() # 自动旋转日期标记
plt.savefig('gupiao1.png',dpi=100)   


'''
#画蜡烛图
'''
#把时间转换为mdates.date2num格式，并加入二维列表中
DATA = []
for i in range(len(sta)):
    DATA.append([mdates.date2num(data[i]),float(sta[i]),float(max[i]),float(min[i]),float(end[i])])

plt.figure(2)
ax2 = plt.subplot(111) 
ax2.set_title("股票代码：600052  浙江广厦",fontproperties=font)           
ax2.set_xlabel("时间",fontproperties=font)
ax2.set_ylabel("股价（元）",fontproperties=font)
ax2.xaxis_date()
candlestick_ohlc(ax2, DATA, width=0.6, colorup='#53c156', colordown='#ff1717')    
plt.savefig('gupiao2.png',dpi=100)   
            
            
'''
合并
'''      
plt.figure(3)
ax3 = plt.subplot(211)
ax3.set_title("股票代码：600052  浙江广厦",fontproperties=font)
ax3.set_xlabel("时间",fontproperties=font)
ax3.set_ylabel("股价（元）",fontproperties=font)
ax3.plot(x,y1,'r')
ax3.plot(x,y2,'b')
ax3.plot(x,y3,'g')
ax3.plot(x,y4,'y')
plt.gcf().autofmt_xdate() # 自动旋转日期标记
ax4 = plt.subplot(212)            
ax4.set_xlabel("时间",fontproperties=font)
ax4.set_ylabel("股价（元）",fontproperties=font)
ax4.xaxis_date()
candlestick_ohlc(ax4, DATA, width=0.6, colorup='#53c156', colordown='#ff1717')    
plt.savefig('gupiao3.png',dpi=100)             
plt.show()            
            
            
            
            
            
            
            
            
