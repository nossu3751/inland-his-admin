import sys

sys.path.insert(0, "..")

import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.add_vertical_space import add_vertical_space

import pandas as pd
from util import initialize_page, url

authenticator, config = initialize_page()

import yaml

if st.session_state["authentication_status"]:
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Password modified successfully')
            with open('frontend/config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
        
    except Exception as e:
        st.error(e)



