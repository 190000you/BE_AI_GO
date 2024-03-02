import streamlit as st
from langchain_openai import ChatOpenAI
from streamlit_folium import folium_static
import folium
import re
import pandas as pd

#df = pd.read_csv("C:\Langchain\poat\langchain\관광지_대구광역시0.csv", encoding='cp949')

llm = ChatOpenAI(openai_api_key = "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")

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 사람들에게 대구 관광지를 추천해주는 대구 여행 전문가야. 항상 적합한 여행지 5개와 적합한 맛집 5개와 적합한 숙소 5개를 (위도: xx.xxxx, 경도: yy.yyyy) 형식의 표현과 함께 추천 해줘야해"),
    ("user", "{input}")
])


from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

st.balloons()
st.title('가볼까?')
st.caption('대구여행은 _:blue[가볼까?]_ 와 함께 :sunglasses:')
user_input = st.text_input('어떤 여행을 떠나시나요?')
st.caption('예) 친구들과 1박 2일동안 대구를 여행할 계획이야')
st.caption('예) 부모님과 하루 정도 대구를 여행할 계획이야. 사람들이 많이 없는 조용하고 한적한 곳으로 알려줘.')
if st.button('여행지 추천받기'):
    with st.spinner('골똘히 고민 중...'):
        result = chain.invoke({"input" : user_input})
    st.write(result)
    
    #여기 안에 관광지 추천 알고리즘 탑제
    #matching_rows = df[df["name"] == user_input]
    #if not matching_rows.empty:
       # st.write("여기 몇 가지 추천 여행지가 있어요:")
        #for index, row in matching_rows.iterrows():
           # st.write(f"- {row['name']}: {row['street_name_adress']}: {row['parking']}: {row['info']}: {row['call']}")

    text = result
    #여기 안에 맛집 추천 알고리즘 탑제

    #여기 안에 숙소 추천 알고리즘 탑제 

    pattern = r"(.+?)\(위도: (\d+\.\d+), 경도: (\d+\.\d+)\)"
    matches = re.findall(pattern, text)
    coordinates = [(match[0].strip(), float(match[1]), float(match[2])) for match in matches]


    #folium 예시
    m = folium.Map(location = [35.864592, 128.593334], zoom_start= 14)
        
    for coordinate in coordinates:
        name, latitude, longitude = coordinate
        folium.Marker(
            location=[latitude, longitude],
            popup=name,
            tooltip="추천 장소"
        ).add_to(m)

    st_data = folium_static(m, width = 725)