import streamlit as st
import pandas as pd
import pyphen
from string import punctuation
import requests
import hashlib
import plotly.graph_objs as go
import random
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

header = st.container()
contact = st.container()


with header:
    st.title("Contact Me")

with contact:
    st.write("")
    st.write("")
    st.write('Email: yonpython@gmail.com')
    st.write("")
    st.write("")
    lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_mwzutzkk.json")
    st_lottie(
        lottie_hello,
        speed=1,
        height=400,
        width=400,
        reverse=False,
        loop=True,
        quality="high",  # medium ; high
        key=None,
    )