from datetime import date, datetime
import sys
import requests
sys.path.insert(0, "..")

import streamlit as st
from streamlit_quill import st_quill as stq
from streamlit_extras.add_vertical_space import add_vertical_space

from util import initialize_page, url

initialize_page(['superadmin'])

st.title("패치노트")

st.markdown("<br><br>", unsafe_allow_html=True)


form_inputs = {
    "내용":"patch_note_descriptions",
}

if "patch_note_mode" not in st.session_state:
    st.session_state["patch_note_mode"] = 'list'

def post_form_data(data):
    with st.spinner(""):
        res = requests.post(url=f"{url}/api/v1/app_patches", json=data)
    if res.status_code != 200 and res.status_code != 201:
        st.session_state["app_patch_error_message"] = "죄송합니다. 지금은 등록할 수 없습니다. 작성하지 않은 부분이 있는지 확인해주세요."
    else:
        switch_mode("list")

def initialize_form_data():
    for _,v in form_inputs.items():
        if v not in st.session_state:
            st.session_state[v] = ""

def collect_form_data():

    form_data = {
        "description":st.session_state[form_inputs["내용"]],
        "date":date.today().isoformat(),
    }
    
    return form_data


def clear_form_data():
    form_input_values = set([v for _,v in form_inputs.items()])
    for k in st.session_state:
        if k in form_input_values:
            st.session_state.pop(k)
        elif k == "app_patch_error_message":
            st.session_state.pop(k)


def switch_mode(mode:str):
    st.session_state['patch_note_mode'] = mode


if st.session_state["patch_note_mode"] == "create":
    initialize_form_data()

    st.button("뒤로가기", on_click=switch_mode, args=["list"])
    st.markdown("***", unsafe_allow_html=True)
   
    content = stq(html=True,key=form_inputs["내용"])

    st.markdown("***", unsafe_allow_html=True)

    if "app_patch_error_message" in st.session_state:
        st.error(st.session_state["app_patch_error_message"])

    st.button("패치노트 등록", type='primary', on_click=post_form_data, args=[collect_form_data()])

elif st.session_state["patch_note_mode"] == "list":
    clear_form_data()
    st.button("새 패치노트 작성", on_click=switch_mode, args=['create'])
    
    with st.spinner(""):
        app_patches = requests.get(f"{url}/api/v1/app_patches")

    if app_patches.status_code != 200:
        st.error("패치노트를 불러 올 수 없습니다.")
        st.stop()

    add_vertical_space()

    st.markdown("***", unsafe_allow_html=True)

    
    app_patches_json = app_patches.json()
    if len(app_patches_json) > 0:
        for i in range(len(app_patches_json)):
            app_patch = app_patches_json[i]
            if i != 0:
                add_vertical_space()
        
            
            st.markdown(
                f"<p><span style='margin-right:0.5em;'>{app_patch['date']}</span>패치노트</p>",
                unsafe_allow_html=True
            )

            st.markdown(
                app_patch['description'],
                unsafe_allow_html=True
            )
           
            
            st.markdown("***", unsafe_allow_html=True)
    else:
        st.info("등록된 패치노트가 없습니다!")

