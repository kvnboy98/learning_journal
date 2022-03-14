import data_visual, data_hipo, data_home
import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

pages ={
    'Homepage': data_home,
    'Data Visualization': data_visual,
    'Hypothesis Testing': data_hipo
}

selected = st.sidebar.selectbox('select a page', list(pages.keys()))
page = pages[selected]

page.app()