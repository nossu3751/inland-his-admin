import sys
import streamlit as st
sys.path.insert(0, "..")

from util import initialize_page

initialize_page(['superadmin','pastor','welcome-team'])

st.title("죄송합니다!")
st.header("준비중인 페이지입니다.")