import sys

sys.path.insert(0, "..")
import streamlit as st
from util import initialize_page

initialize_page(['superadmin','pastor'])

st.title("죄송합니다!")
st.header("준비중인 페이지입니다.")