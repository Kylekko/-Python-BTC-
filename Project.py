import numpy as np
import pandas as pd
from pandas import DataFrame as df
import matplotlib.pyplot as plt

import requests
from bs4 import BeautifulSoup

from time import sleep

import matplotlib as mpl
import matplotlib.font_manager as fm
from matplotlib import rc

#다음 3줄의 코드는 한글을 그래프에 출력하기 위함이다. 
mpl.rcParams['axes.unicode_minus'] = False
font_name = fm.FontProperties(fname="c:/windows/fonts/malgun.ttf").get_name()
rc('font', family=font_name)

setBalance = 1000

data = pd.read_csv('./BTC 2012-2021.csv')
data = data[::-1] # 데이터 거꾸로 읽어오기
data = data.reset_index(drop=True) # 인덱스 재정렬

def notice():
    title = 'BTC Trading Simulator'
    
    for i in title:
        print(i, end='')
        sleep(0.1)
    print()
    sleep(0.5)
    print('==================::Notice::==================')
    sleep(0.5)
    print('설명에 따라 투자시점과 매도시점을 입력하시면됩니다')
    sleep(0.5)
    print('*모의투자 금액: 1000$(약120만원)')
    sleep(0.5)
    print('*투자가능 기간: 2012-01-01 ~ 2021-12-31')
    sleep(0.5)
    print('==============================================')
    sleep(0.5)
    
    return settings()
    
def settings():
    try:
        startYears = int(input('투자 시작 연도를 입력해주세요(ex. 2012): '))
        if startYears > 2011 or startYears < 2022:
            if startYears == 2012:
                startIndex = ((startYears+1) % 2012) - 1 # 데이터 정규화
                stopIndex = startIndex + 366 # 데이터 정규화
            else:
                startIndex = ((startYears) % 2012) * 365 + 1 # 데이터 정규화
                stopIndex = startIndex + 365 # 데이터 정규화 
        else:
            print('조회 범위는 2012~2021입니다')
            return settings()
    except ValueError:
        print('숫자만 입력해주세요')
    
    dataSet = data['Price'].iloc[startIndex:stopIndex]
    
    plt.plot(dataSet)
    plt.xticks(np.arange(startIndex,stopIndex,31), np.arange(1,13))
    plt.title('BTC모의투자')
    plt.xlabel(str(startYears)+'년(월간)')
    plt.ylabel('달러($)')
    plt.show()
    
    try:
        selectMonth, period = map(int, input('투자 시작 월과 기간(개월)을 입력해주세요(ex. 3, 36): ').split(','))
    except UnboundLocalError:
        print(UnboundLocalError)
        print('입력 형식을 맞춰주세요')
        return settings()
    except ValueError:
        print(ValueError)
        print('숫자가 아닙니다')
        return settings()
    
    month = startIndex + ((selectMonth-1) * 30)
    setPeriod = month + (period * 30)  
    
    return trading(startYears, month, selectMonth, setPeriod, period)

def trading(years, month, selectMonth, selectRange, period):
    dataSet = data['Price'].iloc[month:selectRange]
    
    buy_price_per_share = data['Price'].iloc[month]
    sell_price_per_share = data['Price'].iloc[selectRange]
    
    maxPrice = df.max(dataSet)
    minPrice = df.min(dataSet)
    
    plt.plot(dataSet)
    
    if period > 20:
        plt.xticks(np.arange(month, selectRange, 30*12), np.arange(1, int((period+1)/12)+2))
        plt.xlabel('연간차트(1년단위)')
    else:
        plt.xticks(np.arange(month, selectRange, 31), np.arange(1, period+1))
        plt.xlabel('월간차트(월)')
    plt.title('BTC모의투자')
    plt.ylabel('달러($)')
    
    print('\n===설정기간 동안의 가격변화 차트를 출력합니다===')
    sleep(0.5)
    plt.show()
    
    return balance(years
                   , selectMonth
                   , period
                   , buy_price_per_share
                   , sell_price_per_share
                   , maxPrice
                   , minPrice)
    
def balance(years, selectMonth, period, buy, sell, maxPrice, minPrice):
    share = setBalance / buy # BTC개수
    balance = share * sell # 잔액
    profit = balance - setBalance # 수익
    
    if (balance / 1000) < 1:
        percentage = ((1 - (balance / setBalance)) * 100) * (-1) # 손실률 계산
    else:
        percentage = ((balance - setBalance) / setBalance) * 100 # 수익률 계산
    
    sleep(0.5)
    print('{}년 {}월부터 {}개월간 투자결과\n'.format(years, selectMonth, period))
    sleep(1)
    print('1BTC당 구매가격: USD {}'.format(buy))
    sleep(0.5)
    print('BTC: {}\n'.format(share))
    sleep(1.5)
    print('기간별최고가: USD {}'.format(maxPrice))
    sleep(0.5)
    print('기간별최저가: USD {}\n'.format(minPrice))
    sleep(1)
    print('판매가격: USD {}'.format(sell))
    sleep(0.5)
    print('누적수익: USD {:.1f}'.format(profit))
    sleep(0.5)
    print('누적수익률: {:.1f}%\n'.format(percentage))
    sleep(1)
    print('현재잔고: USD {:.1f}'.format(balance))
    print('현재잔고: KRW {:.1f}'.format(balance*1200))
    print('\n==============실시간Cryto뉴스===============\n')
    return crawling()
    
def crawling():
    url = "https://www.coindeskkorea.com/news/articleList.html?sc_area=A&view_type=sm&sc_word=%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8&sc_order_by=E&sc_sdate=&sc_edate="
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')

    for i in range(1,4):
        headline = soup.select_one('#user-container > div.float-center.custom-m.mobile.template.list.max-width-1250 > div.user-content > section > article > div.article-list > section > div:nth-child({}) > div.text-block > div.list-titles > a > strong'.format(i)).string
        writter = soup.select_one('#user-container > div.float-center.custom-m.mobile.template.list.max-width-1250 > div.user-content > section > article > div.article-list > section > div:nth-child({}) > div.text-block > div.list-dated > strong'.format(i)).string
        print('헤드라인:'+headline)
        print('작성자:'+writter+'\n')
        sleep(0.5)
        
    return restart()

def restart():
    yn = input('다시 하려면 \'y\'를 입력하세요: ')
    if yn == 'y':
        notice()
    else:
        print('종료합니다')
        
        
notice()