import sys
import re

from datetime import date, datetime
import time
sys.path.insert(0, "..")

import requests
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_modal import Modal

import pandas as pd
from util import initialize_page, url
import yaml 

initialize_page(['superadmin','pastor','welcome-team'])

with open('frontend/config.yaml', 'r') as file:
    config_data = yaml.safe_load(file)

form_inputs = {
    "이름":"new_comer_form_name",
    "생년월일":"new_comer_form_birthday",
    "전화번호":"new_comer_form_phone",
    "주소":"new_comer_form_p_address",
    "우편주소":"new_comer_form__m_address",
    "이메일":"new_comer_form_email",
    "세례여부":"new_comer_form_baptized",
    "등록일":"new_comer_form_registered_at",
}

if "new_comer_mode" not in st.session_state:
    st.session_state["new_comer_mode"] = 'list'

def delete_form_data(id):
    with st.spinner(""):
        res = requests.delete(f"{url}/api/v1/new-comers/{id}")
    if res.status_code != 200:
        st.session_state["new_comer_request_error_message"] = "죄송합니다. 지금은 삭제할 수 없습니다."
    else:
        switch_mode("list")
  

def edit_form_data(id,data):
    with st.spinner(""):
        res = requests.put(f"{url}/api/v1/new-comers/{id}", json=data)
    if res.status_code != 200:
        st.session_state["new_comer_request_error_message"] = "죄송합니다. 지금은 새신자 정보를 수정할 수 없습니다."
    else:
        switch_mode("list")

def collect_form_data():
    form_data = {
        "name": st.session_state[form_inputs["이름"]],
        "birthday":st.session_state[form_inputs["생년월일"]].isoformat(),
        "phone":st.session_state[form_inputs["전화번호"]],
        "p_address":st.session_state[form_inputs["주소"]],
        "m_address":st.session_state[form_inputs["우편주소"]],
        "email":st.session_state[form_inputs["이메일"]],
        "baptized":st.session_state[form_inputs["세례여부"]],
        "registered_at":st.session_state[form_inputs["등록일"]].isoformat()
    }

    if "new_comer_view_current_id" in st.session_state:
        form_data["id"] = st.session_state["new_comer_view_current_id"]

    return form_data

def initialize_form_data():
    for _,v in form_inputs.items():
        if v not in st.session_state:
            st.session_state[v] = ""


def clear_form_data():
    form_input_values = set([v for _,v in form_inputs.items()])
    for k in st.session_state:
        if k in form_input_values:
            st.session_state.pop(k)
        elif k == "new_comer_view_current_id":
            st.session_state.pop(k)
        if k == "new_comer_request_error_message":
            st.session_state.pop(k)
        if k == "new_comer_modify_data_loaded":
            st.session_state.pop(k)

def switch_mode(mode:str):
    st.session_state['new_comer_mode'] = mode

def view_new_comer(id:int):
    st.session_state["new_comer_mode"] = "view"
    st.session_state["new_comer_view_current_id"] = id

def update_spreadsheet_info(sheetlink, sheetname):
    with st.spinner():
        config_data["new-comer-sheet"]["link"] = sheetlink
        config_data["new-comer-sheet"]["sheet"] = sheetname
        with open('frontend/config.yaml', 'w') as file:
            yaml.safe_dump(config_data, file)

    st.info("구글시트 정보가 업데이트되었습니다")
    sheet_info_confirm_button = st.button("알겠습니다")
    if not sheet_info_confirm_button:
        st.stop()

    st.rerun()

def approve_new_comer(new_comer_data):
    res = requests.post(f"{url}/api/v1/new-comers/googleSheet", json=new_comer_data)
    if res.status_code != 201:
        st.stop()

    

        
    
    
    
    
# st.write(st.session_state)
st.title("새신자관리")

add_vertical_space()

if st.session_state["new_comer_mode"] == "list":
    clear_form_data()

    spreadsheet_info_submitted = False
    with st.form("sheet_info"):
        spreadsheet_link = st.text_input("구글시트 링크", config_data["new-comer-sheet"]["link"])
        spreadsheet_sheetname = st.text_input("구글시트 시트명", config_data["new-comer-sheet"]["sheet"])
        spreadsheet_info_submitted = st.form_submit_button("업데이트")
        
    if spreadsheet_info_submitted:
        update_spreadsheet_info(spreadsheet_link, spreadsheet_sheetname)

    with st.spinner(""):
        new_comers = requests.get(f"{url}/api/v1/new-comers")

    if new_comers.status_code != 200:
        st.error("새신자 목록을 불러 올 수 없습니다.")
        st.stop()

    add_vertical_space()
    # st.markdown("***", unsafe_allow_html=True)

    st.markdown('''
        <style>
        [data-testid="column"] {
            display: flex;
            align-items: center;
            justify-content: center;
            width: calc(20% - 1rem) !important;
            flex: 0 0 calc(20% - 1rem) !important;
            min-width: calc(20% - 1rem) !important;
            flex-wrap: wrap;
        }
        [data-testid="column"]:first-child {
            justify-content: start;
            width: calc(50% - 1rem) !important;
            flex: 0 0 calc(50% - 1rem) !important;
            min-width: calc(50% - 1rem) !important;
        }
        [data-testid="column"]:last-child {
            justify-content: end;
            width: calc(50% - 1rem) !important;
            flex: 0 0 calc(50% - 1rem) !important;
            min-width: calc(50% - 1rem) !important;
            
        }
        </style>''', unsafe_allow_html=True)
    
    new_comers_json = new_comers.json()
    register_date_new_comer_map = {}
    for new_comer_data in new_comers_json:
        register_date = new_comer_data["registered_at"]
        if register_date not in register_date_new_comer_map:
            register_date_new_comer_map[register_date] = []
        register_date_new_comer_map[register_date].append(new_comer_data)

    sorted_register_dates = sorted(register_date_new_comer_map.keys(), key=lambda date: datetime.strptime(date, "%Y-%m-%d"))

    user_index = 0

    for dt in sorted_register_dates:
        st.info(f"{dt} 등록자")
        for new_comer in register_date_new_comer_map[dt]:
            col1,col2 = st.columns(2)
            with col1:
                st.write(f'{new_comer["name"]} ({int((date.today() - date.fromisoformat(new_comer["birthday"])).days / 365.25)} 세)')
            # with col2:
            #     splited_date = str(new_comer["registered_at"]).split("-")
            #     st.write("-".join([splited_date[1], splited_date[2], splited_date[0][2:]]))
            
            with col2:
                col3,col4 = st.columns(2)
                with col3:
                    st.button(":question:", key=f"new_comer_view_key_{user_index}", on_click=view_new_comer, args=[new_comer["id"]])
                with col4:
                    st.button(":heavy_check_mark:", 
                              key=f"new_comer_approve_key_{user_index}", 
                              on_click=approve_new_comer, 
                              args=[{
                                "new_comer_id":new_comer["id"],
                                "spreadsheet_link": config_data["new-comer-sheet"]["link"],
                                "sheet":config_data["new-comer-sheet"]["sheet"]
                            }])
            user_index += 1
    # for i in range(len(new_comers_json)):
    #     new_comer = new_comers_json[i]
    #     if i != 0:
    #         add_vertical_space()
    #     col1,col2 = st.columns(2)
    #     with col1:
    #         st.write(f'{new_comer["name"]} ({int((date.today() - date.fromisoformat(new_comer["birthday"])).days / 365.25)} 세)')
    #     # with col2:
    #     #     splited_date = str(new_comer["registered_at"]).split("-")
    #     #     st.write("-".join([splited_date[1], splited_date[2], splited_date[0][2:]]))
         
    #     with col2:
    #         st.button("보기", key=f"new_comer_view_key_{i}", on_click=view_new_comer, args=[new_comer["id"]])
        
       
    #     # st.markdown("***", unsafe_allow_html=True)

elif st.session_state["new_comer_mode"] == "view":
    initialize_form_data()
    
    st.button("뒤로가기", on_click=switch_mode, args=["list"])
    current_view_id = st.session_state["new_comer_view_current_id"]

    if "new_comer_modify_data_loaded" not in st.session_state:
        curr_new_comer_res = requests.get(f"{url}/api/v1/new-comers/{current_view_id}")
        if curr_new_comer_res.status_code != 200:
            st.error("죄송합니다. 지금은 불러올 수 없습니다.")
            st.stop()

        data = curr_new_comer_res.json()
     
        st.session_state[form_inputs["이름"]] = data["name"]
        st.session_state[form_inputs["생년월일"]] = datetime.strptime(data["birthday"],"%Y-%m-%d")
        st.session_state[form_inputs["전화번호"]] = data["phone"]
        st.session_state[form_inputs["주소"]] = data["p_address"]
        st.session_state[form_inputs["우편주소"]] = data["m_address"]
        st.session_state[form_inputs["이메일"]] = data["email"]
        st.session_state[form_inputs["세례여부"]] = data["baptized"]
        st.session_state[form_inputs["등록일"]] = datetime.strptime(data["registered_at"],"%Y-%m-%d")
        st.session_state["new_comer_modify_data_loaded"] = True
    
    st.markdown("***", unsafe_allow_html=True)
    st.markdown("<h4>새신자 정보 수정</h4>", unsafe_allow_html=True)
    add_vertical_space()
    name = st.text_input("이름", key=form_inputs["이름"])
    new_comer_birthday = st.date_input("생년월일", key=form_inputs["생년월일"], min_value=date(year=1960, month=1, day=1))
    phone = st.text_input("전화번호", key=form_inputs["전화번호"])
    p_address=st.text_area("주소", key=form_inputs["주소"])
    m_address=st.text_area("우편주소", key=form_inputs["우편주소"])
    email=st.text_input("이메일", key=form_inputs["이메일"])
    baptized=st.radio("세례여부", ["세례받음", "세례 받지 않음"], index=0 if st.session_state[form_inputs["세례여부"]] == True else 1)
    st.session_state[form_inputs["세례여부"]] = True if baptized == "세례받음" else False
    registered_at = st.date_input("등록일", key=form_inputs["등록일"], min_value=date(year=1960, month=1, day=1))

    st.markdown("***", unsafe_allow_html=True)

    if "new_comer_request_error_message" in st.session_state:
        st.error(st.session_state["new_comer_request_error_message"])
    
    # st.write(collect_form_data())
    st.button("수정완료", type='primary', on_click=edit_form_data, args=[current_view_id, collect_form_data()])
    st.button("삭제", type="secondary", on_click=delete_form_data, args=[current_view_id])
    
    
    
