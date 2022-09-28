import streamlit as st
from string import punctuation
import requests
import random
from streamlit_lottie import st_lottie


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def generate_pass(password_length, password_amount):
    uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase_letters = uppercase_letters.lower()
    digits = "01234567890"
    symz = list(set(punctuation))
    symbols = ""
    for i in symz:
        symbols += i
    # print(symbols)

    upper, lower, nums, syms = True, True, True, True

    all = ""

    if upper:
        all += uppercase_letters
    if lower:
        all += lowercase_letters
    if nums:
        all += digits
    if syms:
        all += symbols

    length = password_length
    amount = password_amount

    for x in range(amount):
        gen_password = "".join(random.sample(all, length))
        st.write(x+1, ". ", gen_password)
        print(gen_password)


header = st.container()
dataset = st.container()

with header:
    st.title("Password Generator")
    st.text("Generate a secure password below!")

with dataset:
    st.header('Password Generator')
    st.text('Use the sliders below to generate as many passwords as you like!')
    pass_length = st.slider('Choose password length:', 1, 50, 6)
    st.write("Password length: ", pass_length, ".")
    pass_amount = st.slider('Choose how many passwords you would like to generate:', 1, 100, 1)
    st.write("Passwords to be generated: ", pass_amount, ".")
    st.button("Generate Again!", on_click=generate_pass(pass_length, pass_amount))
    st.write("")
    st.write("")
    lottie_hello = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_fhcjkhtv.json")
    st_lottie(
        lottie_hello,
        speed=1,
        height=400,
        width=400,
        reverse=False,
        loop=True,
        quality="low",  # medium ; high
        key=None,
    )