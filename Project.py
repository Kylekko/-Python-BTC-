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

setBalance = 1000 # 투자금 $1000 세팅

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
                startIndex = ((startYears+1) % 2012) - 1 # 인덱스로 찾을수 있게 함
                stopIndex = startIndex + 366 # 인덱스로 찾을수 있게 함
            else:
                startIndex = ((startYears) % 2012) * 365 + 1 # 인덱스로 찾을수 있게 함
                stopIndex = startIndex + 365 # 인덱스로 찾을수 있게 함
        else:
            print('조회 범위는 2012~2021입니다')
            return settings()
        
    except ValueError: # 자료형이 다를 때
        print('숫자만 입력해주세요')
    
    dataSet = data['Price'].iloc[startIndex:stopIndex] # 투자 시작부터 1년간 차트에 출력할 열 지정
    
    plt.plot(dataSet)
    plt.xticks(np.arange(startIndex,stopIndex,31), np.arange(1,13)) # 1달간격으로 xticks 수정
    plt.title('BTC모의투자')
    plt.xlabel(str(startYears)+'년(월간)')
    plt.ylabel('달러($)')
    plt.show()
    
    try:
        selectMonth, period = map(int, input('투자 시작 월과 기간(개월)을 입력해주세요(ex. 3, 36): ').split(','))
    except UnboundLocalError: # 입력값이 지정한 형식이 아닐경우
        print(UnboundLocalError)
        print('입력 형식을 맞춰주세요')
        return settings()
    
    except ValueError: # 입력값의 자료형이 다를경우
        print(ValueError)
        print('숫자가 아닙니다')
        return settings()
    
    month = startIndex + ((selectMonth-1) * 30) # 해당 년도의 입력한 월 인덱스 지정
    setPeriod = month + (period * 30) # 투자가 끝나는 인덱스를 지정
    
    return trading(startYears, month, selectMonth, setPeriod, period)

def trading(years, month, selectMonth, selectRange, period):
    dataSet = data['Price'].iloc[month:selectRange] # 투자 기간별 차트 출력을 위한 열
    
    buy_price_per_share = data['Price'].iloc[month] # 매입금액
    sell_price_per_share = data['Price'].iloc[selectRange] # 매도금액
    
    maxPrice = df.max(dataSet) # 투자기간중 최대값 검색
    minPrice = df.min(dataSet) # 투자기간중 최소값 검색
    
    plt.plot(dataSet)
    
    if period > 20: # 기간이 20개월을 초과한다면
        plt.xticks(np.arange(month, selectRange, int(30.466*12)), np.arange(1, int((period+1)/12)+1)) # 연간 조회데이터 제공
        plt.xlabel('연간차트(1년단위)')
    else: # 기간이 19개월 이하
        plt.xticks(np.arange(month, selectRange, 30.466), np.arange(1, period+1)) # 월간 조회 데이터 제공
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
    balance = share * sell # 잔액($)
    profit = balance - setBalance # 총 수익($)
    
    if (balance / 1000) < 1:
        percentage = ((1 - (balance / setBalance)) * 100) * (-1) # 손실률 계산식
    else:
        percentage = ((balance - setBalance) / setBalance) * 100 # 수익률 계산식
    
    sleep(0.5)
    print(f'{years}년 {selectMonth}월부터 {period}개월간 투자결과\n')
    sleep(1)
    print(f'1BTC당 구매가격: USD {buy}')
    sleep(0.5)
    print(f'BTC: {share}\n')
    sleep(1.5)
    print(f'기간별최고가: USD {maxPrice}')
    sleep(0.5)
    print(f'기간별최저가: USD {minPrice}\n')
    sleep(1)
    print(f'판매가격: USD {sell}')
    sleep(0.5)
    print('누적수익: USD {:.1f}'.format(profit))
    sleep(0.5)
    print('누적수익률: {:.1f}%\n'.format(percentage))
    sleep(1)
    print('현재잔고: USD {:.1f}'.format(balance))
    print('현재잔고: KRW {:.1f}'.format(balance*1200)) # 임의 환율로 한화 환전
    print('\n==============실시간Cryto뉴스===============\n')
    return crawling()
    
def crawling():
    url = "https://www.coindeskkorea.com/news/articleList.html?sc_area=A&view_type=sm&sc_word=%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8&sc_order_by=E&sc_sdate=&sc_edate="
    res = requests.get(url) # URL Parse (HTML)
    res.raise_for_status() # 에러가 있을 시 멈추고 에러 반환

    soup = BeautifulSoup(res.text, 'html.parser') # HTML을 text형식으로 바꾸고 parsing한다

    for i in range(1,4):
        headline = soup.select_one('#user-container > div.float-center.custom-m.mobile.template.list.max-width-1250 > div.user-content > section > article > div.article-list > section > div:nth-child({}) > div.text-block > div.list-titles > a > strong'.format(i)).string
        writter = soup.select_one('#user-container > div.float-center.custom-m.mobile.template.list.max-width-1250 > div.user-content > section > article > div.article-list > section > div:nth-child({}) > div.text-block > div.list-dated > strong'.format(i)).string
        print('헤드라인:'+headline)
        print('작성자:'+writter+'\n')
        sleep(0.5)
        
    return restart()

def restart(): # 재시작 함수
    yn = input('다시 하려면 \'y\'를 입력하세요: ')
    if yn == 'y':
        notice()
    else:
        print('종료합니다')
        
if __name__ == '__main__':
    notice()