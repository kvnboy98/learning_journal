from matplotlib import image
import streamlit as st
from PIL import Image
def app():
    st.markdown("<h1 style='text-align: center; color: black;'> WELCOME TO THE LANDING PAGE </h1>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns([0.15,1,0.1])
    col2.image('https://image.shutterstock.com/image-vector/winter-mountain-forest-landscape-background-260nw-322188917.jpg')

    st.write('''<h1 style='text-align: center; color: black; font-size:20px'> This project was created in order 
    to complete Milestone 1 held by Hacktiv8 </h1>''', unsafe_allow_html=True)

    with st.expander('About Author'):
        st.write('''<h1 style='text-align: center; color: black; font-size:13px; font-family:verdana'> Created by Kevin Boy Gunawan </h1>''', unsafe_allow_html=True)
        st.write('''<h1 style='text-align: center; color: black; font-size:13px; font-family:verdana'> March 3, 2022 </h1>''', unsafe_allow_html=True)