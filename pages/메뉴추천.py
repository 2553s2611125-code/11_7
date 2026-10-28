
# -----------------------------
# 귀여운 파스텔 디자인
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;600;700&display=swap');

.stApp {
    background: #FFF9F5;
    color: #514641;
    font-family: 'Noto Sans KR', sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Jua', sans-serif !important;
    color: #75534D !important;
}

.hero {
    background: linear-gradient(135deg, #FFE6EB 0%, #FFF0D9 55%, #E5F4E8 100%);
    border: 2px solid #FFFFFF;
    border-radius: 28px;
    padding: 30px 28px;
    margin-bottom: 24px;
    box-shadow: 0 5px 18px #E8C9C333;
    position: relative;
}

.hero h1 {
    font-size: 2.35rem;
    color: #9B5969 !important;
    margin: 0 0 12px 0;
}

.hero p {
    color: #795D58;
    font-size: 0.98rem;
    line-height: 1.8;
    margin: 0;
}

.hero .sticker {
    font-size: 2.2rem;
    margin-bottom: 10px;
}

.hero .tag {
    display: inline-block;
    background: #FFFFFFB8;
    color: #A35E72;
    border-radius: 30px;
    padding: 6px 13px;
    font-size: 0.82rem;
    margin-bottom: 12px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #F4E3DD;
    border-radius: 22px;
    box-shadow: 0 4px 14px #DCC4B51A;
    padding: 8px;
}

div.stButton > button {
    border-radius: 16px;
    border: 1px solid #F0D5D9;
    background: #FFF0F2;
    color: #965C68;
    font-weight: 600;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color: #E9AAB9;
    background: #FFE1E8;
    color: #814858;
}

div.stButton > button[kind="primary"],
div.stFormSubmitButton > button {
    background: #E99BAC;
    border: none;
    color: white;
    border-radius: 16px;
    font-weight: 700;
    min-height: 46px;
}

div.stButton > button[kind="primary"]:hover,
div.stFormSubmitButton > button:hover {
    background: #D98196;
    color: white;
}

div[data-baseweb="select"] > div {
    border-radius: 13px;
    border-color: #EBD8D1;
    background: #FFFFFF;
}

div[data-testid="stTabs"] button {
    border-radius: 12px 12px 0 0;
    font-weight: 600;
}

div[data-testid="stExpander"] {
    background: #FFFAF8;
    border: 1px solid #F2E3DD;
    border-radius: 14px;
}

div[data-testid="stCaptionContainer"] {
    color: #9B8580;
}

div[data-testid="stAlert"] {
    border-radius: 16px;
}

hr {
    border-color: #F0DFD8;
}

div[data-testid="stCheckbox"] label {
    color: #795D58;
}

@media (max-width: 640px) {
    .hero {
        padding: 23px 19px;
    }
    .hero h1 {
        font-size: 1.8rem;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 귀여운 상단 배너
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="sticker">🧸 🍓 🥣</div>
    <div class="tag">♡ 육아맘 · 육아대디를 위한 레시피 ♡</div>
    <h1>오늘 뭐 먹지? 🌷</h1>
    <p>아가 돌보느라 바쁜 하루에도</p>
    <p><b>내 밥은 맛있고 간편하게!</b> 🍚</p>
    <p>냉장고 속 재료로 오늘의 메뉴를 찾아봐요.</p>
</div>
""", unsafe_allow_html=True)
