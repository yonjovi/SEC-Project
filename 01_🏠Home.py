import streamlit as st
from streamlit_lottie import st_lottie
import requests


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

header = st.container()
dataset = st.container()


with header:
    st.title("Welcome!")
    st.markdown("In this project, I will help you analyse URLs, passwords, and help generate a super duper secure password "
            "or 100. Please feel free to leave a comment and/or constructive criticism via the Contact Me section.")
    st.markdown("Please note that this project is in development and is for your assistance and education purposes.")
    st.markdown("Special thanks to the Virus Total and Have I Been Pwned APIs for helping me source invaluable data.")
    st.markdown("Hope you enjoy the project.")
    st.markdown("Peace,")
    st.markdown("Yon")

    lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_Zz37yH.json")
    st_lottie(
        lottie_hello,
        speed=1,
        height=200,
        width=200,
        reverse=False,
        loop=True,
        quality="high", # medium ; high
        key=None,
    )
