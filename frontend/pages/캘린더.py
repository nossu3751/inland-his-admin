import sys

sys.path.insert(0, "..")

from datetime import datetime

import streamlit as st
from util import initialize_page, calendar_options, calendar_css

initialize_page(['superadmin','pastor','welcome-team','media-team','praise-team'])

st.title("죄송합니다!")
st.header("준비중인 페이지입니다.")

# from streamlit_calendar import calendar

# def switch_mode(mode:str):
#     st.session_state['calendar_mode'] = mode

# def get_clicked_date(event):
#     if "callback" in event:
#         event_type = event["callback"]
#         if event_type == "dateClick":
#             selected_date = event[event_type]["date"]
#         elif event_type == "eventClick":
#             selected_date = event[event_type]["event"]["start"]
#         else:
#             st.error("죄송합니다. 날짜를 선택할 수 없습니다.")
#             st.stop()
#         dt_obj = datetime.fromisoformat(selected_date)
#         selected_date = dt_obj.strftime("%Y-%m-%d")
#         st.session_state["calendar_modify_selected_date"] = selected_date
#         switch_mode("view")
#         return selected_date
#     else:
#         st.error("죄송합니다. 날짜를 선택할 수 없습니다.")
#         st.stop()


# def clear_form_data():
#     form_input_values = set([v for _,v in form_inputs.items()])
#     for k in st.session_state:
#         if k in form_input_values:
#             st.session_state.pop(k)
#         elif k == "calendar_modify_selected_date":
#             st.session_state.pop(k)
#         elif k == "calendar_request_error_message":
#             st.session_state.pop(k)

    
# calendar_events = [
#     {
#         "title": "Event 1",
#         "start": "2024-03-01T08:30:00",
#         "end": "2023-07-31T10:30:00",
#         "resourceId": "a",
#     },
#     {
#         "title": "Event 2",
#         "start": "2024-03-02T07:30:00",
#         "end": "2023-07-31T10:30:00",
#         "resourceId": "b",
#     },
#     {
#         "title": "Event 3",
#         "start": "2024-02-29T10:40:00",
#         "end": "2023-07-31T12:30:00",
#         "resourceId": "a",
#     }
# ]

# form_inputs = {
#     "내용":"discussion_form_html_template_data",
#     "날짜":"discussion_form_date",
# }


# if "calendar_mode" not in st.session_state:
#     st.session_state["calendar_mode"] = 'list'

# if st.session_state["calendar_mode"] == "list":
#     # clear_form_data()

#     st.button("새 이벤트 등록", on_click=switch_mode, args=['create'])

#     st.markdown("***", unsafe_allow_html=True)

#     cal = calendar(events=calendar_events, options=calendar_options, custom_css=calendar_css)
#     st.write(cal)
# elif st.session_state["calendar_mode"] == "view":
#     st.button("뒤로가기", on_click=switch_mode, args=["list"])
#     st.write(st.session_state["calendar_modify_selected_date"])

# st.session_state