import os
import base64
from typing import Iterable
from PIL import Image
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.app_logo import add_logo

import yaml
from yaml.loader import SafeLoader

flask_env = os.getenv("INLAND_HIS_ENV")

if flask_env == "development":
    url = 'http://localhost:5001'
else:
    url = 'https://admin.inlandhis.com/proxy/'

def initialize_page(required_roles:Iterable=[]):
    set_page_config()
    hide_streamlit_style()
    topbar()
    authenticate_result = authenticate()
    if authenticate_result != None:
        role, authenticator, config = authenticate_result
        authorize(required_roles, role)
        return authenticator, config
    return None,None
    

def set_page_config():
    favicon = Image.open("frontend/assets/images/favicon.ico")
    st.set_page_config("히즈관리자", initial_sidebar_state='collapsed', page_icon=favicon)

def hide_streamlit_style():
    hide_streamlit_style = """
        <style>
        # .stApp {
            
        # }
        html, body {
            max-width: 100%;
            overflow-x: hidden;
        }
        div[data-testid="stToolbar"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
        }
        div[data-testid="stDecoration"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
        }
        div[data-testid="stStatusWidget"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
        }
        div[data-testid="stToolbarNoPadding"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
        }
        div[data-testid="stDecorationNoPadding"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
        }
        div[data-testid="stStatusWidgetNoPadding"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
        }
        div[data-testid="collapseControl"] {
        z-index:1000000 !important;
        }
        div.block-container {
            padding: 2rem !important;
        }
        [data-testid="stSidebarNav"]::before {
                content: "히즈관리앱";
                margin-left: 20px;
                margin-bottom: 50px;
                font-size: 30px;
                position: relative;
                top: 30px;
                font-weight: bolder;
                color: #3e3053;
                background-color: #F4F3F7;
            }
        button[data-testid="baseButton-header"] {
        z-index:1000000 !important;
        position: relative;
        }
        button[data-testid="baseButton-headerNoPadding"] {
        z-index:1000000 !important;
        position: relative;
        }
        #MainMenu {
        visibility: hidden;
        height: 0%;
        }
        header {
        visibility: hidden;
        height: 0%;
        }
        footer {
        visibility: hidden;
        height: 0%;
        }
        div.stButton > button:first-child {
            background-color: #735f90;
            border: 1.5px solid #735f90;
            color:#ffffff;
        }
        div.stButton > button:hover {
            background-color: #9F90B6;
            color:#ddd;
            }
        div.stButton > button[data-testid="baseButton-secondary"]:first-child {
            background-color:#ffffff;
            border: 1.5px solid #735f90;
            color:#735f90;
        }
        div.stButton > button[data-testid="baseButton-secondary"]:hover {
            background-color: #9F90B6;
            color:#ddd;
            }
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    

def topbar():
    logo_url = image_url("./frontend/assets/images/his logo white.png")
    st.markdown(
        f'''
            <style>
                .reportview-container {{
                    margin-top: -2em;
                }}
                
                .topbar {{
                    background-color:#ffffff; 
                    height: 50px; 
                    width: 100vw;
                    position: fixed;
                    top: 0;
                    left: 0;
                    z-index: 1;
                    display: flex;
                    align-items: center;
                    border-bottom: solid 1px #ccc;
                    justify-content: center;
                }}
                .logo-img {{
                    display: inline-flex;
                    height: 36px;
                    width: 36px;
                    filter: brightness(0) saturate(100%) invert(40%) sepia(4%) saturate(3177%) hue-rotate(222deg) brightness(100%) contrast(96%);
                }}
            </style>
            <div class="topbar">
                <img src="data:image/png;base64,{logo_url}" alt="" class="logo-img">
            </div> 
        '''
    , unsafe_allow_html=True)

def image_url(image):
    file_ = open(image, "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    return data_url

def logo():
    add_logo("./frontend/assets/images/his logo white.png")

def authorize(required_roles:list, current_role:str):
    if len(required_roles) > 0 and current_role not in required_roles:
        st.error("해당 계정으로 접속할 수 없는 페이지입니다.")
        st.stop()


def authenticate():
    with open('./frontend/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    authenticator.login()

    if st.session_state["authentication_status"]:
        st.write("logged in")
        with st.sidebar:
            authenticator.logout()
            try:
                role = config['credentials']['usernames'][st.session_state["username"]]['role']
                return role, authenticator, config
            except KeyError:
                return None


    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
        st.stop()
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
        st.stop()

    

calendar_options = {
    "editable": "true",
    "selectable": "true",
    "headerToolbar": {
        "left": "prev",
        "center": "title",
        "right": "next"
    },

    "initialView": "dayGridMonth",
    "height": "auto"
    
}

calendar_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 1.2rem;
    }
    .fc-timeline-event {
    overflow: hidden;
    }
    .fc-event {
        white-space: nowrap;
        text-overflow: ellipsis;
    }
    .fc-event-time {
        display:none;
    }
    .fc-daygrid-event-dot {
        border: 2px solid rgb(114, 83, 148) !important;
    }
"""