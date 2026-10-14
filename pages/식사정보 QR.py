from pathlib import Path
import textwrap, zipfile, os

base = Path("/mnt/data")
app_code = r'''
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="아이랑 한끼",
    page_icon="🍚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# 아이랑 한끼 | 외부 API 없이 동작하는 간단한 식사 도우미
# ----------------------------
st.markdown("""
<style>
:root { color-scheme: light; }
.stApp { background: linear-gradient(180deg, #fffdf7 0%, #f7f8ef 100%); }
.block-container { max-width: 1050px; padding-top: 1.2rem; padding-bottom: 2rem; }
h1, h2, h3 { color: #203b32; }
.app-header {
  background: #ffffff; border: 1px solid #e7eadf; border-radius: 22px;
  padding: 18px 20px; margin-bottom: 14px; box-shadow: 0 4px 18px #203b320a;
}
.brand { font-size: 1.65rem; font-weight: 800; color: #163f33; }
.subbrand { color: #59685e; font-size: .93rem; margin-top: 4px; }
div.stButton > button {
  border-radius: 14px; border: 1px solid #e1e7db; min-height: 2.8rem;
  background: #fff; color: #203b32; font-weight: 650;
}
div.stButton > button:hover { border-color: #6b9d83; color: #15553e; }
div[data-testid="stMetric"] {
  background: white; border: 1px solid #e6eadf; padding: 12px;
  border-radius: 16px;
}
.menu-card {
  background: #fff; border: 1px solid #e6e9df; border-radius: 16px;
  padding: 13px 15px; margin: 8px 0;
}
.tag { display:inline-block; background:#eaf4e7; color:#285c45; padding:3px 8px;
       border-radius:999px; font-size:.76rem; margin:2px 3px 2px 0; }
.warning { background:#fff1ed; border:1px solid #f5d2c9; padding:10px 12px;
           border-radius:12px; color:#8b3428; }
.soft { color: #657168; font-size: .9rem; }
div[data-testid="stRadio"] > div { gap: .4rem; }
</style>
""", unsafe_allow_html=True)

MENUS = [
    {"name":"닭고기 채소 덮밥", "category":"든든 한 끼", "price":8500, "time":15,
     "allergens":["대두"], "tags":["단백질","한 그릇"], "desc":"닭고기와 부드러운 채소를 곁들인 덮밥"},
    {"name":"크림 버섯 파스타", "category":"든든 한 끼", "price":11000, "time":20,
     "allergens":["우유","밀"], "tags":["아이와 함께","따뜻한 메뉴"], "desc":"버섯 크림소스를 곁들인 파스타"},
    {"name":"소고기 채소 볶음밥", "category":"빠른 메뉴", "price":9000, "time":12,
     "allergens":["대두","달걀"], "tags":["단백질","한 그릇"], "desc":"남은 채소를 활용하기 좋은 볶음밥"},
    {"name":"두부 채소 비빔밥", "category":"가벼운 메뉴", "price":8000, "time":12,
     "allergens":["대두","참깨"], "tags":["식물성","간편식"], "desc":"두부와 채소를 올린 간단한 비빔밥"},
    {"name":"토마토 달걀 덮밥", "category":"빠른 메뉴", "price":7500, "time":10,
     "allergens":["달걀"], "tags":["빠른 조리","한 그릇"], "desc":"재료가 간단하고 조리 시간이 짧은 덮밥"},
    {"name":"연어 구이 도시락", "category":"든든 한 끼", "price":12500, "time":18,
     "allergens":["생선"], "tags":["단백질","도시락"], "desc":"구운 연어와 밥, 채소 구성"},
    {"name":"채소 수프와 식빵", "category":"가벼운 메뉴", "price":7000, "time":15,
     "allergens":["밀","우유"], "tags":["따뜻한 메뉴","간단식"], "desc":"채소 수프와 식빵으로 간단하게"},
    {"name":"새우 볶음밥", "category":"빠른 메뉴", "price":9500, "time":12,
     "allergens":["갑각류","대두","달걀"], "tags":["한 그릇","빠른 조리"], "desc":"새우와 채소를 넣은 볶음밥"},
]
ALLERGENS = ["우유", "달걀", "밀", "대두", "땅콩", "견과류", "생선", "갑각류", "참깨"]

def money(value):
    return f"{value:,}원"

def go(page):
    st.session_state.page = page

if "page" not in st.session_state:
    st.session_state.page = "홈"
if "profile" not in st.session_state:
    st.session_state.profile = {
        "child_age": "12~24개월", "allergies": [], "diet": "특별한 제한 없음",
        "budget": 10000, "time": 15
    }
if "settings" not in st.session_state:
    st.session_state.settings = {"alerts": True, "language": "한국어", "support": False}

profile = st.session_state.profile
settings = st.session_state.settings

st.markdown("""
<div class="app-header">
  <div class="brand">🍚 아이랑 한끼</div>
  <div class="subbrand">바쁜 육아 중에도, 우리 가족 식사를 조금 더 간편하게</div>
</div>
""", unsafe_allow_html=True)

pages = ["홈", "식사 정보 QR", "메뉴 추천", "메뉴 목록", "내 정보", "설정"]
icons = ["🏠", "▦", "✨", "🍲", "👶", "⚙️"]
nav_cols = st.columns(3)
for i, page in enumerate(pages):
    with nav_cols[i % 3]:
        if st.button(f"{icons[i]}  {page}", key=f"nav_{page}", use_container_width=True):
            go(page)

st.divider()
page = st.session_state.page

if page == "홈":
    st.title("오늘 식사, 가볍게 정해볼까요?")
    st.write("아이 돌봄으로 바쁜 날, 조리 시간과 알레르기 정보를 고려해 메뉴를 골라보세요.")
    c1, c2, c3 = st.columns(3)
    c1.metric("메뉴 아이디어", f"{len(MENUS)}개")
    c2.metric("내 조리 시간", f"{profile['time']}분 이내")
    c3.metric("예산 기준", money(profile["budget"]))
    st.subheader("무엇이 필요하세요?")
    choices = [
        ("✨ 오늘 메뉴 추천", "메뉴 추천", "시간과 예산, 알레르기 정보를 반영해 후보를 보여드려요."),
        ("🍲 메뉴 한눈에 보기", "메뉴 목록", "메뉴와 예상 가격, 조리 시간, 알레르기 정보를 확인해요."),
        ("👶 아이 정보 관리", "내 정보", "아이 연령대와 알레르기 정보를 입력하거나 수정해요."),
        ("▦ 식사 정보 QR", "식사 정보 QR", "식당에서 받은 메뉴 코드로 안내 정보를 확인해요."),
    ]
    for title, target, desc in choices:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(desc)
            if st.button("열기", key=f"home_{target}", use_container_width=True):
                go(target)
                st.rerun()
    st.info("참고: 이 앱은 식사 선택을 돕는 정보 도구입니다. 알레르기가 있거나 영유아에게 제공할 음식은 식당에 원재료와 교차접촉 가능성을 꼭 확인하세요.")

elif page == "식사 정보 QR":
    st.title("식사 정보 QR")
    st.write("식당에서 받은 QR에 연결된 메뉴 코드를 입력해 정보를 확인하는 데모 화면이에요.")
    st.caption("실제 QR 카메라 판독이나 식당 서버 연결은 포함하지 않았어요. 배포 후에도 별도 API 없이 안전하게 실행됩니다.")
    code = st.text_input("메뉴 코드", placeholder="예: BABY001", max_chars=30).strip().upper()
    if st.button("정보 확인", type="primary", use_container_width=True):
        if not code:
            st.warning("메뉴 코드를 입력해 주세요.")
        elif code in ("BABY001", "MENU001", "1234"):
            st.success("메뉴 안내 정보를 찾았어요.")
            st.markdown("### 오늘의 가족 메뉴")
            st.markdown("**닭고기 채소 덮밥** · 8,500원")
            st.write("주요 재료: 닭고기, 쌀, 당근, 애호박")
            st.write("표기 알레르기 정보: 대두(조리 소스에 포함될 수 있음)")
            st.warning("원재료와 조리 환경은 매장마다 다를 수 있으니 주문 전 직원에게 확인하세요.")
        else:
            st.error("등록된 데모 코드가 없어요. 예시 코드 **BABY001**을 입력해 보세요.")
    with st.expander("QR 기능을 실제 서비스로 확장하려면"):
        st.write("식당별 QR 코드에 메뉴 페이지 주소를 연결하거나, QR 판독 라이브러리와 검증된 메뉴 데이터 API를 추가하면 됩니다.")

elif page == "메뉴 추천":
    st.title("우리 가족 메뉴 추천")
    st.write("내 정보에 저장한 알레르기와 예산, 조리 시간을 기준으로 메뉴를 골라요.")
    allergies = set(profile["allergies"])
    budget = int(profile["budget"])
    max_time = int(profile["time"])
    candidates = [
        m for m in MENUS
        if m["price"] <= budget and m["time"] <= max_time and not allergies.intersection(m["allergens"])
    ]
    if profile["diet"] == "채식 위주":
        candidates = [m for m in candidates if any(x in m["name"] for x in ["두부", "채소", "토마토"])]
    elif profile["diet"] == "유제품 피하기":
        candidates = [m for m in candidates if "우유" not in m["allergens"]]
    st.caption(f"기준: {max_time}분 이내 · {money(budget)} 이하 · 알레르기 {len(allergies)}개 반영")
    if not candidates:
        st.warning("현재 조건에 맞는 메뉴가 없어요. 예산이나 조리 시간을 조정하거나 내 정보에서 제한 조건을 확인해 주세요.")
        if st.button("내 정보 수정하기"):
            go("내 정보")
            st.rerun()
    else:
        for m in sorted(candidates, key=lambda x: (x["time"], x["price"]))[:5]:
            with st.container(border=True):
                st.markdown(f"### 🍽️ {m['name']}")
                st.write(m["desc"])
                a, b, c = st.columns(3)
                a.metric("예상 가격", money(m["price"]))
                b.metric("조리 시간", f"{m['time']}분")
                c.metric("분류", m["category"])
                st.caption("알레르기 표기: " + (", ".join(m["allergens"]) if m["allergens"] else "등록된 항목 없음"))
    st.caption("추천 결과는 입력한 정보와 예시 데이터에 따른 참고용이며, 실제 원재료·교차접촉 여부를 보장하지 않습니다.")

elif page == "메뉴 목록":
    st.title("메뉴 목록")
    categories = ["전체", "든든 한 끼", "빠른 메뉴", "가벼운 메뉴"]
    selected_cat = st.radio("메뉴 분류", categories, horizontal=True)
    search = st.text_input("메뉴 검색", placeholder="예: 볶음밥, 파스타")
    filtered = [m for m in MENUS if (selected_cat == "전체" or m["category"] == selected_cat)
                and search.strip().lower() in m["name"].lower()]
    if not filtered:
        st.info("조건에 맞는 메뉴가 없어요. 검색어나 분류를 바꿔보세요.")
    for m in filtered:
        with st.container(border=True):
            left, right = st.columns([3, 1])
            with left:
                st.markdown(f"**🍽️ {m['name']}**")
                st.caption(m["desc"])
                st.markdown(" ".join(f'<span class="tag">{t}</span>' for t in m["tags"]), unsafe_allow_html=True)
                st.caption("알레르기 표기: " + ", ".join(m["allergens"]))
            with right:
                st.markdown(f"**{money(m['price'])}**")
                st.caption(f"⏱️ {m['time']}분")
            conflict = set(profile["allergies"]).intersection(m["allergens"])
            if conflict:
                st.markdown(f'<div class="warning">⚠️ 내 정보에 등록된 알레르기 항목과 겹쳐요: {", ".join(sorted(conflict))}</div>', unsafe_allow_html=True)

elif page == "내 정보":
    st.title("아이와 가족 정보")
    st.write("입력한 정보는 현재 브라우저 세션에서만 사용돼요. 앱을 다시 시작하면 초기화될 수 있어요.")
    with st.form("profile_form"):
        child_age = st.selectbox("아이 연령대", ["0~6개월", "7~11개월", "12~24개월", "만 2세 이상"],
                                 index=["0~6개월", "7~11개월", "12~24개월", "만 2세 이상"].index(profile["child_age"]))
        allergies = st.multiselect("확인해야 할 알레르기 항목", ALLERGENS, default=profile["allergies"])
        diet = st.selectbox("식사 선호", ["특별한 제한 없음", "채식 위주", "유제품 피하기"],
                            index=["특별한 제한 없음", "채식 위주", "유제품 피하기"].index(profile["diet"]))
        budget = st.slider("한 끼 예산", min_value=5000, max_value=20000, step=1000, value=int(profile["budget"]))
        time_limit = st.slider("가능한 조리 시간", min_value=5, max_value=60, step=5, value=int(profile["time"]))
        submitted = st.form_submit_button("정보 저장", type="primary", use_container_width=True)
    if submitted:
        st.session_state.profile = {
            "child_age": child_age, "allergies": allergies, "diet": diet,
            "budget": budget, "time": time_limit
        }
        st.success("정보를 저장했어요. 메뉴 추천에 반영됩니다.")
        st.rerun()
    if profile["allergies"]:
        st.markdown('<div class="warning">알레르기 정보는 안전과 관련이 있어요. 앱의 표기만 믿지 말고 주문 전 반드시 식당에 원재료와 교차접촉 여부를 확인하세요.</div>', unsafe_allow_html=True)
    st.caption("영유아에게 제공할 음식의 크기·질감·간은 발달 단계와 개인 상황에 맞춰 보호자가 확인해 주세요.")

elif page == "설정":
    st.title("설정")
    st.write("앱 사용 환경을 간단히 설정할 수 있어요.")
    with st.form("settings_form"):
        alerts = st.toggle
