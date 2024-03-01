import sys
import re

from datetime import date, datetime
sys.path.insert(0, "..")

import requests
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_modal import Modal

import pandas as pd
from util import initialize_page, url

initialize_page(['superadmin','pastor','media-team'])



form_inputs = {
    "제목":"bulletin_form_title",
    "주보날짜":"bulletin_form_date",
    "본문구절":"bulletin_form_verses",
    "찬양":"bulletin_form_praises",
    "대표기도자":"bulletin_form_praying_person",
    "공동체소식인도자":"bulletin_form_announcing_person",
    "말씀인도자":"bulletin_form_preacher",
    "말씀후찬양":"bulletin_form_postservice_praise",
    "축도":"bulletin_form_ending_person",
    "광고":"bulletin_form_announcements"

}

if "bulletin_mode" not in st.session_state:
    st.session_state["bulletin_mode"] = 'list'

def post_form_data(data):
    with st.spinner(""):
        res = requests.post(url=f"{url}/api/v1/bulletins", json=data)
    if res.status_code != 200 and res.status_code != 201:
        st.session_state["bulletin_request_error_message"] = "죄송합니다. 지금은 주보를 등록할 수 없습니다. 날짜가 겹치거나 작성하지 않은 부분이 있는지 확인해주세요."
    else:
        switch_mode("list")
        

def delete_form_data(id):
    with st.spinner(""):
        res = requests.delete(f"{url}/api/v1/bulletins/{id}")
    if res.status_code != 200:
        st.session_state["bulletin_request_error_message"] = "죄송합니다. 지금은 주보를 삭제할 수 없습니다."
    else:
        switch_mode("list")
  

def edit_form_data(id,data):
    with st.spinner(""):
        res = requests.put(f"{url}/api/v1/bulletins/{id}", json=data)
    if res.status_code != 200:
        st.session_state["bulletin_request_error_message"] = "죄송합니다. 지금은 주보를 수정할 수 없습니다."
    else:
        switch_mode("list")
    

def initialize_form_data():
    for _,v in form_inputs.items():
        if v not in st.session_state:
            if v in ["bulletin_form_praises", "bulletin_form_announcements"]:
                pass
            elif v == "bulletin_form_date":
                st.session_state[v] = date.today()
            else:
                st.session_state[v] = ""

def collect_form_data():
    announcements, _ = get_announcements()
    
    form_data = {
        "news":[{"title":st.session_state[announcement[0]], "description":st.session_state[announcement[1]]} for announcement in announcements],
        "sermon_title":st.session_state[form_inputs["제목"]],
        "sermon_content":st.session_state[form_inputs["본문구절"]],
        "sunday_date":st.session_state[form_inputs["주보날짜"]].isoformat(),
        "hymns":[],
        "representative_prayer":st.session_state[form_inputs["대표기도자"]],
        "community_news":st.session_state[form_inputs["공동체소식인도자"]],
        "message":st.session_state[form_inputs["말씀인도자"]],
        "post_message_hymn":st.session_state[form_inputs["말씀후찬양"]],
        "blessing":st.session_state[form_inputs["축도"]]
    }
    # try:
    for i in range(len(bulletin_form_praises)):
        hymn = bulletin_form_praises["찬양"].iloc[i]
        form_data["hymns"].append({"title":hymn})
    # except NameError:
    #     pass
    if "bulletin_view_current_id" in st.session_state:
        form_data["id"] = st.session_state["bulletin_view_current_id"]
    return form_data


def clear_form_data():
    form_input_values = set([v for _,v in form_inputs.items()])
    for k in st.session_state:
        if k in form_input_values:
            st.session_state.pop(k)
        elif k == "bulletin_view_current_id":
            st.session_state.pop(k)
        is_title = "bulletin_form_announcement_title" in k
        is_content = "bulletin_form_announcement_content" in k
        is_delete_button = "bulletin_form_announcement_delete" in k
        if is_title or is_content or is_delete_button:
            st.session_state.pop(k)
        if k == "bulletin_request_error_message":
            st.session_state.pop(k)
        if k == "bulletin_modify_data_loaded":
            st.session_state.pop(k)
        if k == "bulletin_hymn_titles":
            st.session_state.pop(k)


def switch_mode(mode:str):
    st.session_state['bulletin_mode'] = mode


def add_announcement(key):
    st.session_state[f"bulletin_form_announcement_title_{key}"] = ""
    st.session_state[f"bulletin_form_announcement_content_{key}"] = ""

def delete_announcement(key):
    st.session_state.pop(f"bulletin_form_announcement_title_{key}")
    st.session_state.pop(f"bulletin_form_announcement_content_{key}")
    st.session_state.pop(f"bulletin_form_announcement_delete_{key}")

def get_announcements():
    def _ending_number(s):
        match = re.search(r'\d+$', s)
        if match:
            return int(match.group())
        else:
            return None
    titles = []
    contents = []
    for k in st.session_state:
        if "bulletin_form_announcement_title" in k:
            titles.append(k)
        if "bulletin_form_announcement_content" in k:
            contents.append(k)
    titles = sorted(titles, key=lambda x: _ending_number(x))
    contents = sorted(contents, key=lambda x:_ending_number(x))
    last_key_number = _ending_number(titles[-1]) if len(titles) > 0 else 0
    return [[titles[i],contents[i],_ending_number(titles[i])] for i in range(len(titles))], last_key_number

def view_bulletin(id:int):
    st.session_state["bulletin_mode"] = "view"
    st.session_state["bulletin_view_current_id"] = id
    
# st.write(st.session_state)
st.title("주보관리")

add_vertical_space()


if st.session_state["bulletin_mode"] == "create":
    initialize_form_data()

    st.button("뒤로가기", on_click=switch_mode, args=["list"])
    st.markdown("***", unsafe_allow_html=True)
    title = st.text_input("제목", key=form_inputs["제목"])
    bulletin_date = st.date_input("주보날짜", key=form_inputs["주보날짜"])


    verses = st.text_area("본문구절", key=form_inputs["본문구절"])
   
    st.markdown("***", unsafe_allow_html=True)

    st.markdown("<p style='font-size:14px;'>찬양</p>",unsafe_allow_html=True)

    bulletin_form_praises = st.data_editor(
        data=pd.DataFrame([], columns=["찬양"], index=None),
        use_container_width=True,
        num_rows="dynamic",
        key=form_inputs["찬양"]
    )

    st.markdown("***", unsafe_allow_html=True)
    st.text_input("대표기도자", key=form_inputs["대표기도자"])
    st.text_input("공동체소식 인도자", key=form_inputs["공동체소식인도자"])
    st.text_input("말씀인도자", key=form_inputs["말씀인도자"])
    st.text_input("말씀 후 찬양", key=form_inputs["말씀후찬양"])
    st.text_input("축도", key=form_inputs["축도"])

    st.markdown("***", unsafe_allow_html=True)

    st.markdown("<p style='font-size:14px;'>광고</p>",unsafe_allow_html=True)

    announcements, last_key = get_announcements()
    st.button("광고추가", type='secondary', on_click=add_announcement, args=[last_key+1])
    for a in announcements:
        col1, col2 = st.columns([0.8,0.2])
        with col1:
            st.text_input('제목', key=a[0])
            st.text_area('내용', key=a[1])
        with col2:
            st.markdown('<p style="height:13px;"></p>', unsafe_allow_html=True)
            st.button("삭제", key=f'bulletin_form_announcement_delete_{a[2]}', on_click=delete_announcement, args=[a[2]])

    st.markdown("***", unsafe_allow_html=True)

    if "bulletin_request_error_message" in st.session_state:
        st.error(st.session_state["bulletin_request_error_message"])

    st.button("주보 등록", type='primary', on_click=post_form_data, args=[collect_form_data()])
elif st.session_state["bulletin_mode"] == "list":
    clear_form_data()
    st.button("새 주보 작성", on_click=switch_mode, args=['create'])
    
    with st.spinner(""):
        bulletins = requests.get(f"{url}/api/v1/bulletins")

    if bulletins.status_code != 200:
        st.error("주보 리스트를 불러 올 수 없습니다.")
        st.stop()

    add_vertical_space()
    st.markdown("***", unsafe_allow_html=True)

    st.markdown('''
        <style>
        [data-testid="column"] {
            display: flex;
            align-items: center;
            justify-content: center;
            width: calc(25% - 1rem) !important;
            flex: 0 0 calc(25% - 1rem) !important;
            min-width: calc(25% - 1rem) !important;
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
            width: calc(25% - 1rem) !important;
            flex: 0 0 calc(25% - 1rem) !important;
            min-width: calc(25% - 1rem) !important;
            
        }
        </style>''', unsafe_allow_html=True)
    bulletins_json = bulletins.json()

    for i in range(len(bulletins_json)):
        bulletin = bulletins_json[i]
        if i != 0:
            add_vertical_space()
        col1,col2,col3 = st.columns([5,3,2])
        with col1:
            st.write(bulletin["sermon_title"])
        with col2:
            splited_date = str(bulletin["sunday_date"]).split("-")
            st.write("-".join([splited_date[1], splited_date[2], splited_date[0][2:]]))
            # st.write("-".join(str(bulletin["sunday_date"]).split("-")))
        with col3:
            st.button("보기", key=f"bulletin_view_key_{i}", on_click=view_bulletin, args=[bulletin["id"]])
        
        
        st.markdown("***", unsafe_allow_html=True)

elif st.session_state["bulletin_mode"] == "view":
    initialize_form_data()
    
    st.button("뒤로가기", on_click=switch_mode, args=["list"])
    current_view_id = st.session_state["bulletin_view_current_id"]

    if "bulletin_modify_data_loaded" not in st.session_state:
        curr_bulletin_res = requests.get(f"{url}/api/v1/bulletins/{current_view_id}")
        if curr_bulletin_res.status_code != 200:
            st.error("죄송합니다. 지금은 불러올 수 없습니다.")
            st.stop()

        data = curr_bulletin_res.json()
     
        st.session_state[form_inputs["제목"]] = data["sermon_title"]
        st.session_state[form_inputs["주보날짜"]] = datetime.strptime(data["sunday_date"],"%Y-%m-%d")
        st.session_state[form_inputs["본문구절"]] = data["sermon_content"]
        st.session_state[form_inputs["대표기도자"]] = data["representative_prayer"]
        st.session_state[form_inputs["공동체소식인도자"]] = data["community_news"]
        st.session_state[form_inputs["말씀인도자"]] = data["message"]
        st.session_state[form_inputs["말씀후찬양"]] = data["post_message_hymn"]
        st.session_state[form_inputs["축도"]] = data["blessing"]
        hymn_titles = [hymn["title"] for hymn in data["hymns"]]
        st.session_state["bulletin_hymn_titles"] = hymn_titles
        all_news_data = data["news"]
        for i in range(len(all_news_data)):
            add_announcement(i+1)
            st.session_state[f"bulletin_form_announcement_title_{i+1}"] = all_news_data[i]["title"]
            st.session_state[f"bulletin_form_announcement_content_{i+1}"] = all_news_data[i]["description"]

        st.session_state["bulletin_modify_data_loaded"] = True
    else:
        hymn_titles = st.session_state["bulletin_hymn_titles"]

    st.markdown("***", unsafe_allow_html=True)
    st.markdown("<h4>주보 수정</h4>", unsafe_allow_html=True)
    add_vertical_space()
    title = st.text_input("제목", key=form_inputs["제목"])
    bulletin_date = st.date_input("주보날짜", key=form_inputs["주보날짜"])

    verses = st.text_area("본문구절", key=form_inputs["본문구절"])
   
    st.markdown("***", unsafe_allow_html=True)

    st.markdown("<p style='font-size:14px;'>찬양</p>",unsafe_allow_html=True)
    
    bulletin_form_praises = st.data_editor(
        data=pd.DataFrame(hymn_titles, columns=["찬양"], index=None),
        use_container_width=True,
        num_rows="dynamic",
        key=form_inputs["찬양"]
    )

    st.markdown("***", unsafe_allow_html=True)
    st.text_input("대표기도자", key=form_inputs["대표기도자"])
    st.text_input("공동체소식 인도자", key=form_inputs["공동체소식인도자"])
    st.text_input("말씀인도자", key=form_inputs["말씀인도자"])
    st.text_input("말씀 후 찬양", key=form_inputs["말씀후찬양"])
    st.text_input("축도", key=form_inputs["축도"])

    st.markdown("***", unsafe_allow_html=True)

    st.markdown("<p style='font-size:14px;'>광고</p>",unsafe_allow_html=True)

    announcements, last_key = get_announcements()
    st.button("광고추가", type='secondary', on_click=add_announcement, args=[last_key+1])
    for a in announcements:
        col1, col2 = st.columns([0.8,0.2])
        with col1:
            st.text_input('제목', key=a[0])
            st.text_area('내용', key=a[1])
        with col2:
            st.markdown('<p style="height:13px;"></p>', unsafe_allow_html=True)
            st.button("삭제", key=f'bulletin_form_announcement_delete_{a[2]}', on_click=delete_announcement, args=[a[2]])

    st.markdown("***", unsafe_allow_html=True)

    if "bulletin_request_error_message" in st.session_state:
        st.error(st.session_state["bulletin_request_error_message"])
    
    # st.write(collect_form_data())
    st.button("주보 수정", type='primary', on_click=edit_form_data, args=[current_view_id, collect_form_data()])
    st.button("주보 삭제", type="secondary", on_click=delete_form_data, args=[current_view_id])
    
    
    

    

    







