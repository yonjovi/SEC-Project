import streamlit as st
import pandas as pd
import pyphen
from string import punctuation
import requests
import hashlib
import plotly.graph_objs as go
from streamlit_lottie import st_lottie, st_lottie_spinner
import time


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

df = pd.read_csv('./password_analyticz.csv', index_col='Password')

class PasswordAnalytics:
    def vowel_counter(word):
        vowels = ["a", "e", "i", "o", "u"]
        vowel_chars = []
        vowel_count = 0
        for char in password:
            for vowel in vowels:
                if vowel.upper() in char.upper():
                    vowel_count += 1
                    vowel_chars.append(char)

        # print("Vowel count: ", vowel_count)
        # print("Vowels in password: ", vowel_chars)
        df.loc["Pass"]["num_vowels"] = vowel_count
        # df.to_csv(f'{word}_analytics.csv')
        df.to_csv('./password_analyticz.csv')

    def syllable_counter(word):
        a = pyphen.Pyphen(lang='en')
        syllables_str = a.inserted(word)
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        if syllables_str.isdigit():
            df.loc["Pass"]["num_syllables"] = 0
        else:
            split_syl = syllables_str.split("-")
            df.loc["Pass"]["num_syllables"] = len(split_syl)
        df.to_csv('./password_analyticz.csv')

    def special_char_counter(word):
        special_char_list = []
        special_chars = set(punctuation)
        for char in special_chars:
            for letter in word:
                if char == letter:
                    special_char_list.append(char)
        # print("Special Character Count: ", len(special_char_list))
        # print("Special characters in password: ", special_char_list)
        df.loc["Pass"]["num_special"] = len(special_char_list)
        # df.to_csv(f'{word}_analytics.csv')
        df.to_csv('./password_analyticz.csv')

    def pass_length(word):
        # print("Password length: ", len(word))
        df.loc["Pass"]["Length"] = len(word)
        # df.to_csv(f'{word}_analytics.csv')
        df.to_csv('./password_analyticz.csv')

    def num_counter(word):
        num_list = []
        for i in word:
            if i.isdigit():
                num_list.append(i)
        # print("Extracted numbers from the password : ", num_list)
        # print("Numbers count: ", len(num_list))
        df.loc["Pass"]["num_digits"] = len(num_list)
        # df.to_csv(f'{word}_analytics.csv')
        df.to_csv('./password_analyticz.csv')

    def character_counter(word):
        char_list = []
        for i in word:
            if not i.isdigit():
                char_list.append(i)
        # print("Character count: ", len(char_list))
        # print("Characters in password: ", char_list)
        df.loc["Pass"]["num_chars"] = len(char_list)
        # df.to_csv(f'{word}_analytics.csv')
        df.to_csv('./password_analyticz.csv')
        if df.loc["Pass"]["num_chars"] == 0:
            df.loc["Pass"]["num_syllables"] = 0

    def upper_counter(word):
        upper_list = []
        for i in word:
            if i.isupper():
                upper_list.append(i)
        # print("Upper letter count: ", len(upper_list))
        # print("Upper letters: ", upper_list)
        df.loc["Pass"]["num_upper"] = len(upper_list)
        # df.to_csv(f'{word}_analytics.csv')
        df.to_csv('./password_analyticz.csv')

    def lower_counter(word):
        lower_list = []
        for i in word:
            if i.islower():
                lower_list.append(i)
        # print("Lower letter count: ", len(lower_list))
        # print("Lower letters: ", lower_list)
        df.loc["Pass"]["num_lower"] = len(lower_list)
        # df.to_csv(f'{word}_analytics.csv')
        df.to_csv('./password_analyticz.csv')

    def is_pass_safe(password):
        # password = getpass("Please enter your password: ")

        sha_password = hashlib.sha1(password.encode()).hexdigest()
        sha_prefix = sha_password[0:5].upper()  # get first 5 characters of the password hash
        sha_postfix = sha_password[5:].upper()  # get rest of characters of the password hash

        url = "https://api.pwnedpasswords.com/range/" + sha_prefix

        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)
        pwned_dict = {}

        pwned_list = response.text.split("\r\n")
        for pwned_pass in pwned_list:
            pwned_hash = pwned_pass.split(":")
            pwned_dict[pwned_hash[0]] = pwned_hash[1]

        if sha_postfix in pwned_dict.keys():
            print("Password has been compromised {0} times".format(pwned_dict[sha_postfix]))
            compromise_count = int(pwned_dict[sha_postfix])
            formatted_count = '{:>12,.0f}'.format(compromise_count)
            st.write(f"Password has been compromised {formatted_count} times ☠️")
            # st.write("Password has been compromised {0} times ☠️".format(pwned_dict[sha_postfix]))
            lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_urgxqz4c.json")
            st_lottie(
                lottie_hello,
                speed=1,
                height=250,
                width=250,
                reverse=False,
                loop=True,
                quality="low",  # medium ; high
                key=None,
            )
            print(pwned_dict[sha_postfix])
            print('')
        else:
            # st.balloons()
            st.write("Password is safe 😸")
            lottie_hello = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_ox9RZA.json")
            st_lottie(
                lottie_hello,
                speed=1,
                height=200,
                width=200,
                reverse=False,
                loop=True,
                quality="low",  # medium ; high
                key=None,
            )
            print("Password is safe!")
            print('')


class PlotAnalytics:
    def group_bar():
        df = pd.read_csv('./password_analyticz.csv')

        w = 0.4
        x = ["Length", "Characters", "Digits", "Uppercase", "Lowercase", "Special", "Vowels", "Syllables"]

        x1 = df.loc[0]['Length']
        x2 = df.loc[0]['num_chars']
        x3 = df.loc[0]['num_digits']
        x4 = df.loc[0]['num_upper']
        x5 = df.loc[0]['num_lower']
        x6 = df.loc[0]['num_special']
        x7 = df.loc[0]['num_vowels']
        x8 = df.loc[0]['num_syllables']

        y1 = df.loc[1]['Length']
        y2 = df.loc[1]['num_chars']
        y3 = df.loc[1]['num_digits']
        y4 = df.loc[1]['num_upper']
        y5 = df.loc[1]['num_lower']
        y6 = df.loc[1]['num_special']
        y7 = df.loc[1]['num_vowels']
        y8 = df.loc[1]['num_syllables']
        y9 = df.loc[1]['Password']

        ## PLOTLY EXAMPLE ##
        average = [x1, x2, x3, x4, x5, x6, x7, x8]
        input_pass = [y1, y2, y3, y4, y5, y6, y7, y8]

        trace1 = go.Bar(
            x=x,
            y=average,
            name='Worst Passwords'
        )

        trace2 = go.Bar(
            x=x,
            y=input_pass,
            name='Your Password'
        )

        data = [trace1, trace2]
        layout = go.Layout(
            barmode='group'
        )

        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        color_discrete_sequence = ['', '#92B4EC', '#FFE69A', '#9FB4FF', '#6FB2D2', '#85C88A', '#99FFCD', '#614124',
                                   '#EEEEEE']

        fig2 = go.Figure(go.Sunburst(
            labels=["Password", "Length", "Characters", "Digits", "Uppercase", "Lowercase", "Special", "Vowels",
                    "Syllables"],
            parents=["", "Password", "Length", "Length", "Characters", "Characters", "Characters", "Characters",
                     "Characters"],
            values=[y9, y1, y2, y3, y4, y5, y6, y7, y8],
            marker=dict(colors=color_discrete_sequence)
        ))
        fig2.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        st.plotly_chart(fig2, use_container_width=True)


header = st.container()
dataset = st.container()

with header:
    st.title('Hello!')
    st.text('In this project I look into password security and analysis.')

with dataset:
    st.header('Password Analysis')
    st.text("Analyse any password! Enter one below...")
    lottie_spinner_url = "https://assets5.lottiefiles.com/packages/lf20_yha8dld0.json"
    lottie_spinner_json = load_lottieurl(lottie_spinner_url)
    password = st.text_input('Enter a password: ', type="password")
    if password:
        with st_lottie_spinner(lottie_spinner_json, height=500, width=500):
            time.sleep(1)
            PasswordAnalytics.pass_length(password)
            PasswordAnalytics.lower_counter(password)
            PasswordAnalytics.upper_counter(password)
            PasswordAnalytics.num_counter(password)
            PasswordAnalytics.character_counter(password)
            PasswordAnalytics.syllable_counter(password)
            PasswordAnalytics.vowel_counter(password)
            PasswordAnalytics.special_char_counter(password)
            PasswordAnalytics.is_pass_safe(password)

            PlotAnalytics.group_bar()
            st.write("")
            st.write("")
