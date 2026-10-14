import streamlit as st
import random
import os

# Gemini API 라이브러리 (선택적 사용)
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 Custom CSS (포근하고 깔끔한 분위기)
# -----------------------------------------------------------------------------
st.set_page_config(
