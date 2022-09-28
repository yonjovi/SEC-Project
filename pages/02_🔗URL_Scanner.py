import requests
import time
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_lottie import st_lottie_spinner, st_lottie

API_KEY = st.secrets["API_KEY"]

def analyse_url(url):
    df = pd.read_csv("./url_results.csv")

    api_url = 'https://www.virustotal.com/vtapi/v2/url/scan'

    params = dict(apikey=API_KEY, url=url)

    response = requests.post(api_url, data=params)

    if response.status_code == 200:
        result = response.json()
        print(json.dumps(result, sort_keys=False, indent=4))

    time.sleep(15)

    url_report_api = 'https://www.virustotal.com/vtapi/v2/url/report'
    url_report_params = dict(apikey=API_KEY, resource=url, scan=0)
    url_report_response = requests.get(url_report_api, params=url_report_params)
    if url_report_response.status_code == 200:
        url_report_result = url_report_response.json()
        # print(url_report_result)
        with open('./url_data.json', 'w') as f:
            json.dump(url_report_result, f)
        # print(json.dumps(url_report_result, sort_keys=False, indent=4))
        #
        scan_result_values = []
        scan_keys = []
        for key, value in url_report_result["scans"].items():
            scan_keys.append(key)
            is_clean = value.values()
            for i in is_clean:
                if isinstance(i, str):
                    if "http" not in i:
                        scan_result_values.append(i)
                        # print(i)

    scan_results_dict = {}
    for i in range(len(scan_keys)):
        scan_results_dict[scan_keys[i]] = scan_result_values[i]
        print(f"{scan_keys[i]} : {scan_result_values[i]}")

    clean_sites = 0
    unrated_sites = 0
    malicious_sites = 0

    for i in scan_results_dict.values():
        if i == "clean site":
            clean_sites += 1
        elif i == "unrated site":
            unrated_sites += 1
        else:
            malicious_sites += 1

    df.at[1, "clean"] = clean_sites
    df.at[1, "unrated"] = unrated_sites
    df.at[1, "malicious"] = malicious_sites

    df.to_csv("./url_results_new.csv", index=False)

    url_df = pd.read_csv("./url_results_new.csv")

    verdicts = ['Clean', 'Unrated', 'Malicious']

    print(url_df.iloc[0]['clean'])

    fig = px.bar(url_df,
                 title=f"Analysis of {url}",
                 text_auto=True,
                 x=verdicts,
                 y=(url_df.iloc[0]["clean"], url_df.iloc[0]["unrated"], url_df.iloc[0]["malicious"]),
                 labels={
                     "y": "Number of records",
                     "x": "Categories"},
                 color=['clean', 'unrated', 'malicious'],
                 category_orders={'category': ['Clean', 'Unrated', 'Malicious']},
                 color_discrete_map={'clean': '#2dc937',
                                     'unrated': '#e7b416',
                                     'malicious': '#cc3232'})

    # fig.show()
    st.plotly_chart(fig, use_container_width=True)
    if malicious_sites == 0:
        st.write("This URL appears to be safe based on all rated websites 😀")
        lottie_hello = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_jbMmxR.json")
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
    elif malicious_sites == 1:
        st.warning("Uh oh, there are reports of potential malicious activity. We cannot be sure, so please proceed with caution!")
        lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_dfzh7yap.json")
        st_lottie(
            lottie_hello,
            speed=1,
            height=367,
            width=443,
            reverse=False,
            loop=True,
            quality="low",  # medium ; high
            key=None,
        )
    elif 2 <= malicious_sites < 5:
        st.warning("Several sources have reported malicious activity on this URL. Please only proceed if you are 100% sure the URL is safe!")
        lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_l9zbnyau.json")
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
    elif 5 <= malicious_sites < 10:
        st.warning("There are many reports of malicious activity ont his URL. Do not proceed to avoid risking yourself!")
        lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_vcfdbwsj.json")
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
    elif malicious_sites >= 10:
        st.warning("AVOID LIKE THE PLAGUE!!!!!!!")
        lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/private_files/lf30_ajahfhsr.json")
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


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()




header = st.container()
dataset = st.container()

with header:
    st.title('Hey legend!')
    st.text('Lets check the safety of your URL!')

with dataset:
    st.header("URL SAFETY CHECKER")
    url_test = st.text_input('Enter a URL:  ')
    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_9zddpfah.json"
    lottie_json = load_lottieurl(lottie_url)
    if url_test:
        with st_lottie_spinner(lottie_json, height=500, width=500):
            try:
                analyse_url(url_test)
            except UnboundLocalError:
                st.warning('Please enter a valid URL')
                lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_zzytykf2.json")
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
            except KeyError:
                st.warning('Please enter a valid URL')
                lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_zzytykf2.json")
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
            except TypeError:
                st.warning('Please enter a valid URL')
                lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_zzytykf2.json")
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




