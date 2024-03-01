
import streamlit as st
from PIL import Image
from streamlit_extras.add_vertical_space import add_vertical_space
from util import initialize_page

initialize_page()

st.title("인랜드 히즈 관리자 페이지")

add_vertical_space()
add_vertical_space()

st.write('''인랜드 히즈 관리자 페이지에 오신 것을 환영합니다.
         이 페이지는 히즈청년부 목사님, 전도사님 및 사역자들만 접속할 수 있습니다.
         만약 사역과 관련이 없는 분이시라면 돌아가주시길 바랍니다. ''')

add_vertical_space()

st.write('''좌측 상단의 아이콘을 눌러 메뉴를 확인해주세요.''')

st.write('''히즈앱 및 히즈홈페이지 내 각 데이터를 관리할 수 있습니다.''')