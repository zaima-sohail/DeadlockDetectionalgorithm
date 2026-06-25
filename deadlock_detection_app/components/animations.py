import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_hero_animation():
    lottie_url = "https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json"
    lottie_json = load_lottieurl(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, height=300, key="hero")
        
def show_success_animation():
    lottie_url = "https://assets1.lottiefiles.com/packages/lf20_jbrw3hcz.json"
    lottie_json = load_lottieurl(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, height=150, key="success")

def show_error_animation():
    lottie_url = "https://assets10.lottiefiles.com/packages/lf20_g1mqub4f.json"
    lottie_json = load_lottieurl(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, height=150, key="error")
