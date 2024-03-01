from datetime import date, datetime
import sys
import requests
sys.path.insert(0, "..")

import streamlit as st
from streamlit_quill import st_quill as stq
from streamlit_extras.add_vertical_space import add_vertical_space

from util import initialize_page, url

initialize_page(['superadmin','pastor'])

st.title("목장 나눔")

st.markdown("<br><br>", unsafe_allow_html=True)


form_inputs = {
    "내용":"discussion_form_html_template_data",
    "날짜":"discussion_form_date",
}

if "discussion_mode" not in st.session_state:
    st.session_state["discussion_mode"] = 'list'

def post_form_data(data):
    with st.spinner(""):
        res = requests.post(url=f"{url}/api/v1/small_group_discussions", json=data)
    if res.status_code != 200 and res.status_code != 201:
        st.session_state["discussion_request_error_message"] = "죄송합니다. 지금은 등록할 수 없습니다. 작성하지 않은 부분이 있는지 확인해주세요."
    else:
        switch_mode("list")
        

def delete_form_data(id):
    with st.spinner(""):
        res = requests.delete(f"{url}/api/v1/small_group_discussions/{id}")
    if res.status_code != 200:
        st.session_state["discussion_request_error_message"] = "죄송합니다. 지금은 삭제할 수 없습니다."
    else:
        switch_mode("list")
  

def edit_form_data(id,data):
    with st.spinner(""):
        res = requests.put(f"{url}/api/v1/small_group_discussions/{id}", json=data)
    if res.status_code != 200:
        st.session_state["discussion_request_error_message"] = "죄송합니다. 지금은 수정할 수 없습니다."
    else:
        switch_mode("list")

def initialize_form_data():
    for _,v in form_inputs.items():
        if v not in st.session_state:
            if v == "discussion_form_date":
                st.session_state[v] = date.today()
            else:
                st.session_state[v] = ""

def collect_form_data():

    form_data = {
        "html_template_data":st.session_state[form_inputs["내용"]],
        "date":st.session_state[form_inputs["날짜"]].isoformat(),
    }
    
    if "discussion_view_current_id" in st.session_state:
        form_data["id"] = st.session_state["discussion_view_current_id"]

    return form_data


def clear_form_data():
    form_input_values = set([v for _,v in form_inputs.items()])
    for k in st.session_state:
        if k in form_input_values:
            st.session_state.pop(k)
        elif k == "discussion_view_current_id":
            st.session_state.pop(k)
        elif k == "discussion_request_error_message":
            st.session_state.pop(k)
        elif k == "discussion_modify_data_loaded":
            st.session_state.pop(k)


def switch_mode(mode:str):
    st.session_state['discussion_mode'] = mode

def view_discussion(id:int):
    st.session_state["discussion_mode"] = "view"
    st.session_state["discussion_view_current_id"] = id
    

if st.session_state["discussion_mode"] == "create":
    initialize_form_data()

    st.button("뒤로가기", on_click=switch_mode, args=["list"])
    st.markdown("***", unsafe_allow_html=True)
   
    discussion_date = st.date_input("날짜", key=form_inputs["날짜"])
    content = stq(html=True,key=form_inputs["내용"])

    st.markdown("***", unsafe_allow_html=True)

    if "discussion_request_error_message" in st.session_state:
        st.error(st.session_state["discussion_request_error_message"])

    st.button("목장나눔 등록", type='primary', on_click=post_form_data, args=[collect_form_data()])

elif st.session_state["discussion_mode"] == "list":
    clear_form_data()
    st.button("새 목장나눔 작성", on_click=switch_mode, args=['create'])
    
    with st.spinner(""):
        small_group_discussions = requests.get(f"{url}/api/v1/small_group_discussions")

    if small_group_discussions.status_code != 200:
        st.error("목장나눔 리스트를 불러 올 수 없습니다.")
        st.stop()

    add_vertical_space()

    st.markdown("***", unsafe_allow_html=True)

    st.markdown('''
        <style>
        [data-testid="column"] {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
        }
        [data-testid="column"]:first-child {
            padding-left: 1em;
            justify-content: start;
            width: calc(70% - 1rem) !important;
            flex: 0 0 calc(70% - 1rem) !important;
            min-width: calc(70% - 1rem) !important;
        }
        [data-testid="column"]:last-child {
            padding-right: 1em;
            justify-content: end;
            width: calc(30% - 1rem) !important;
            flex: 0 0 calc(30% - 1rem) !important;
            min-width: calc(30% - 1rem) !important;
            
        }
        </style>''', unsafe_allow_html=True)
    small_group_discussions_json = small_group_discussions.json()
    if len(small_group_discussions_json) > 0:
        for i in range(len(small_group_discussions_json)):
            small_group_discussion = small_group_discussions_json[i]
            if i != 0:
                add_vertical_space()
            col1,col2 = st.columns(2)
            with col1:
                st.markdown(
                    f"<p><span style='margin-right:0.5em;'>{small_group_discussion['date']}</span>목장나눔</p>",
                    unsafe_allow_html=True
                )
            with col2:
                st.button("보기", key=f"discussion_view_key_{i}", on_click=view_discussion, args=[small_group_discussion["id"]])
            
            st.markdown("***", unsafe_allow_html=True)
    else:
        st.info("등록된 목장나눔이 없습니다!")

elif st.session_state["discussion_mode"] == "view":
    initialize_form_data()
    
    st.button("뒤로가기", on_click=switch_mode, args=["list"])
    current_view_id = st.session_state["discussion_view_current_id"]

    if "discussion_modify_data_loaded" not in st.session_state:
        curr_discussion_res = requests.get(f"{url}/api/v1/small_group_discussions/{current_view_id}")
        if curr_discussion_res.status_code != 200:
            st.error("죄송합니다. 지금은 불러올 수 없습니다.")
            st.stop()

        data = curr_discussion_res.json()
        

        
        st.session_state[form_inputs["날짜"]] = datetime.strptime(data["date"],"%Y-%m-%d")
        st.session_state[form_inputs["내용"]] = data["html_template_data"]
        html = str(data["html_template_data"])
        st.session_state["discussion_modify_data_loaded"] = True
    else:
        html = str(st.session_state[form_inputs["내용"]])


   

    st.markdown("***", unsafe_allow_html=True)
    st.markdown("<h4>목장 나눔 수정</h4>", unsafe_allow_html=True)
    add_vertical_space()

    discussion_date = st.date_input("날짜", key=form_inputs["날짜"])
    content = stq(html=True,key=form_inputs["내용"], value=html)

    st.markdown("***", unsafe_allow_html=True)

    if "discussion_request_error_message" in st.session_state:
        st.error(st.session_state["discussion_request_error_message"])
    
    # st.write(collect_form_data())
    st.button("목장나눔 수정", type='primary', on_click=edit_form_data, args=[current_view_id, collect_form_data()])
    st.button("목장나눔 삭제", type="secondary", on_click=delete_form_data, args=[current_view_id])
    
    
    

