import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from xml_to_dict import XMLtoDict

apikey = '614d786475776864313137776d6d514a'
startnum = 1
endnum = 1000

url = f'http://openapi.seoul.go.kr:8088/{apikey}/xml/airPolutionInfo/{startnum}/{endnum}/'

params = {
            "line" : 'line'
            ,"AREA_NM" : 'AREA_NM'
            ,"CHECKDATE" : 'CHECKDATE'
            ,"PMq" : "PMq"
          }

response = requests.get(url, params=params)
result = BeautifulSoup(response.content, 'xml')

xd = XMLtoDict()

subway = pd.DataFrame(xd.parse(response.content)['airPolutionInfo']['row'])
subway['PMq'] = subway['PMq'].astype('float')

st.title('서울 지하철 미세먼지 알리미')

option = st.selectbox(
    '몇호선이 궁금하세요?',
    ('1', '2', '3', '4', '5', '6', '7', '8'))

st.write(option, '호선')

line = subway[subway['LINE'] == option]  # 지하철 호선 설정
line.reset_index(inplace=True)
등급 = []

for i in line['PMq']:
    if i <= 15:
        등급.append('좋음')

    elif 15 < i <= 35:
        등급.append('보통')

    elif 35 < i <= 75:
        등급.append('나쁨')

    elif 75 < i:
        등급.append('매우나쁨')

등급 = pd.DataFrame(등급)
등급.columns = ['등급']

line = pd.concat([line, 등급], axis=1)

st.dataframe(line)
