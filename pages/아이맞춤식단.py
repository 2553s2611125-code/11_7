import streamlit as st
from datetime import date, timedelta
import random
import hashlib

st.set_page_config(page_title="오늘의 꼬마식탁", page_icon="🥕", layout="wide")

# 레시피 데이터는 이 파일(app.py) 안에 저장되어 있습니다.
# allergens: 해당 메뉴에 의도적으로 들어가는 주요 알레르기 성분
# ingredient_text: 알레르기 키워드 검사에도 사용되는 재료 목록
RECIPES = [
    {"name":"닭고기 채소 덮밥","category":"한 그릇","minutes":20,"age":12,"allergens":[],"ingredients":["밥 1공기","닭고기 80g","당근 20g","애호박 20g","양파 15g","식용유 약간"],"steps":["닭고기와 채소를 아이가 먹기 좋은 크기로 잘게 썹니다.","팬에 기름을 조금 두르고 닭고기를 속까지 완전히 익힙니다.","당근, 애호박, 양파를 넣고 부드러워질 때까지 볶습니다.","밥 위에 올리고 뜨겁지 않게 식혀 제공합니다."],"tip":"고기는 속까지 완전히 익히고 큰 조각이 남지 않게 해 주세요.","image":"https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=900&q=80"},
    {"name":"소고기 채소죽","category":"죽","minutes":25,"age":7,"allergens":[],"ingredients":["밥 1/2공기","다진 소고기 40g","당근 15g","애호박 15g","물 250ml"],"steps":["채소를 아주 잘게 다집니다.","다진 소고기를 냄비에서 완전히 익힙니다.","밥, 채소, 물을 넣고 약불에서 저어 가며 끓입니다.","재료가 충분히 부드러워지면 식혀서 제공합니다."],"tip":"월령과 씹기 능력에 맞춰 입자 크기와 농도를 조절하세요.","image":"https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80"},
    {"name":"연어 채소 파스타","category":"면","minutes":25,"age":12,"allergens":["생선","밀"],"ingredients":["짧은 파스타 60g","연어 60g","브로콜리 25g","양파 15g"],"steps":["파스타를 충분히 익힙니다.","연어의 가시를 꼼꼼히 확인하고 속까지 익힌 뒤 잘게 부숩니다.","브로콜리와 양파를 부드럽게 익혀 잘게 다집니다.","재료를 섞고 먹기 좋은 크기인지 확인합니다."],"tip":"생선 가시를 반드시 확인하세요.","image":"https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=900&q=80"},
    {"name":"채소 달걀전","category":"반찬","minutes":15,"age":12,"allergens":["달걀"],"ingredients":["달걀 1개","당근 15g","애호박 15g","양파 10g"],"steps":["채소를 잘게 다집니다.","달걀을 풀고 채소를 섞습니다.","팬에 기름을 아주 조금 두르고 한입 크기로 부칩니다.","속까지 완전히 익혀 식혀서 제공합니다."],"tip":"달걀 알레르기가 있으면 선택하지 마세요.","image":"https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=900&q=80"},
    {"name":"두부 버섯 덮밥","category":"한 그릇","minutes":20,"age":12,"allergens":["대두"],"ingredients":["밥 1공기","두부 80g","표고버섯 20g","당근 15g"],"steps":["두부의 물기를 빼고 작게 자릅니다.","버섯과 당근을 잘게 썰어 충분히 익힙니다.","두부를 넣고 부드럽게 볶습니다.","밥 위에 올려 식혀서 제공합니다."],"tip":"두부는 대두 성분을 포함합니다.","image":"https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80"},
    {"name":"닭고기 감자 수프","category":"국·수프","minutes":25,"age":9,"allergens":[],"ingredients":["닭고기 60g","감자 1/2개","양파 15g","물 250ml"],"steps":["닭고기와 감자, 양파를 작게 썹니다.","냄비에 물과 재료를 넣고 충분히 익힙니다.","감자를 으깨 농도를 조절합니다.","뜨겁지 않게 식혀 제공합니다."],"tip":"닭고기는 속까지 완전히 익혀 주세요.","image":"https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=900&q=80"},
    {"name":"바나나 오트밀","category":"간식","minutes":10,"age":8,"allergens":["귀리"],"ingredients":["오트밀 25g","바나나 1/2개","물 100ml"],"steps":["바나나를 포크로 으깹니다.","오트밀과 물을 냄비에 넣고 약불에서 끓입니다.","부드러워지면 바나나를 섞습니다.","충분히 식혀 제공합니다."],"tip":"귀리 제품의 원재료와 교차접촉 표시를 확인하세요.","image":"https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=900&q=80"},
    {"name":"고구마 요거트 볼","category":"간식","minutes":15,"age":12,"allergens":["우유"],"ingredients":["고구마 1/2개","플레인 요거트 2큰술"],"steps":["고구마를 부드럽게 찌거나 삶습니다.","껍질을 벗기고 덩어리가 없게 으깹니다.","식힌 고구마에 요거트를 섞습니다.","아이에게 맞는 질감인지 확인합니다."],"tip":"요거트는 우유 성분을 포함합니다.","image":"https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=900&q=80"},
    {"name":"돼지고기 채소 볶음밥","category":"한 그릇","minutes":20,"age":12,"allergens":[],"ingredients":["밥 1공기","다진 돼지고기 60g","애호박 25g","당근 15g","양파 15g"],"steps":["채소를 잘게 다집니다.","돼지고기를 팬에서 속까지 완전히 익힙니다.","채소를 넣고 부드럽게 볶습니다.","밥을 넣어 골고루 섞고 식혀 제공합니다."],"tip":"고기는 속까지 완전히 익혀 주세요.","image":"https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=900&q=80"},
    {"name":"렌틸콩 채소 수프","category":"국·수프","minutes":30,"age":12,"allergens":[],"ingredients":["렌틸콩 40g","당근 20g","감자 1/2개","양파 15g","물 300ml"],"steps":["렌틸콩을 씻고 채소를 작게 썹니다.","냄비에 재료와 물을 넣습니다.","콩과 채소가 완전히 부드러워질 때까지 끓입니다.","필요하면 으깨 아이에게 맞는 질감으로 조절합니다."],"tip":"콩류를 처음 먹는 경우 소량으로 시작하고 반응을 살펴보세요.","image":"https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80"},
    {"name":"소고기 감자완자","category":"반찬","minutes":25,"age":12,"allergens":[],"ingredients":["다진 소고기 70g","감자 1/2개","당근 10g","양파 10g"],"steps":["감자를 삶아 으깨고 채소를 잘게 다집니다.","다진 소고기와 채소를 섞어 작은 완자 모양으로 만듭니다.","팬이나 찜기에 넣어 속까지 완전히 익힙니다.","완자를 작고 부드럽게 잘라 제공합니다."],"tip":"단단하거나 큰 완자는 질식 위험이 있으니 작고 부드럽게 준비하세요.","image":"https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80"},
    {"name":"흰살생선 감자구이","category":"반찬","minutes":20,"age":12,"allergens":["생선"],"ingredients":["대구 등 흰살생선 60g","감자 1/2개","올리브유 약간"],"steps":["생선 가시를 꼼꼼하게 확인합니다.","감자를 부드럽게 찌거나 삶아 으깹니다.","생선을 팬이나 찜기에서 속까지 익힙니다.","생선을 잘게 부수어 감자와 섞어 제공합니다."],"tip":"생선 알레르기가 있으면 제외하고 가시를 반드시 확인하세요.","image":"https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=80"},
    {"name":"치즈 브로콜리 감자","category":"반찬","minutes":15,"age":12,"allergens":["우유"],"ingredients":["감자 1개","브로콜리 30g","치즈 1/2장"],"steps":["감자와 브로콜리를 부드럽게 찌거나 삶습니다.","감자를 으깨고 브로콜리를 잘게 다집니다.","치즈를 넣어 잔열로 녹여 잘 섞습니다.","충분히 식혀 제공합니다."],"tip":"치즈는 우유 성분을 포함합니다.","image":"https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=900&q=80"},
    {"name":"사과 배 퓌레","category":"간식","minutes":12,"age":6,"allergens":[],"ingredients":["사과 1/2개","배 1/4개","물 약간"],"steps":["사과와 배의 껍질과 씨를 제거합니다.","작게 썰어 물을 조금 넣고 푹 익힙니다.","포크로 으깨거나 갈아 부드럽게 만듭니다.","충분히 식힌 뒤 월령에 맞는 질감으로 제공합니다."],"tip":"단단한 생과일 조각은 어린아이에게 질식 위험이 있을 수 있어요.","image":"https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?auto=format&fit=crop&w=900&q=80"},
    {"name":"단호박죽","category":"죽","minutes":20,"age":6,"allergens":[],"ingredients":["단호박 100g","밥 1/3공기","물 200ml"],"steps":["단호박의 씨를 제거하고 부드럽게 찝니다.","껍질을 벗기고 으깹니다.","밥과 물을 넣고 약불에서 저어 가며 끓입니다.","덩어리가 없고 충분히 식었는지 확인합니다."],"tip":"월령과 삼킴 능력에 맞게 질감을 조절하세요.","image":"https://images.unsplash.com/photo-1508747703725-719777637510?auto=format&fit=crop&w=900&q=80"},
    {"name":"병아리콩 채소볼","category":"한 그릇","minutes":20,"age":12,"allergens":[],"ingredients":["익힌 병아리콩 60g","밥 1/2공기","당근 15g","애호박 15g"],"steps":["병아리콩을 아주 부드럽게 익힙니다.","당근과 애호박을 잘게 다져 익힙니다.","병아리콩을 으깨 밥과 채소를 섞습니다.","부드럽고 작은 한입 크기로 제공합니다."],"tip":"콩을 통째로 주지 말고 충분히 으깨 주세요.","image":"https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80"},
    {"name":"시금치 감자전","category":"반찬","minutes":18,"age":12,"allergens":[],"ingredients":["감자 1개","시금치 20g","양파 10g","식용유 약간"],"steps":["감자를 곱게 갈거나 으깹니다.","시금치를 데쳐 물기를 짜고 잘게 다집니다.","감자와 시금치, 양파를 섞습니다.","팬에 얇게 펴서 속까지 익히고 식혀 제공합니다."],"tip":"바삭하고 딱딱한 부분이 생기지 않도록 조리하세요.","image":"https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=900&q=80"},
    {"name":"닭고기 당근 주먹밥","category":"한 그릇","minutes":20,"age":12,"allergens":[],"ingredients":["밥 1공기","닭고기 50g","당근 15g","김가루 약간"],"steps":["닭고기를 속까지 익혀 잘게 찢습니다.","당근을 부드럽게 익혀 잘게 다집니다.","밥과 닭고기, 당근을 섞습니다.","크고 단단하지 않게 작고 부드러운 모양으로 만듭니다."],"tip":"둥글고 단단한 큰 덩어리는 질식 위험이 있어요.","image":"https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=900&q=80"},
    {"name":"새우 채소죽","category":"죽","minutes":22,"age":12,"allergens":["새우·갑각류"],"ingredients":["밥 1/2공기","새우 30g","당근 15g","애호박 15g","물 250ml"],"steps":["새우의 껍질과 내장을 제거하고 잘게 다집니다.","냄비에 새우를 넣어 완전히 익힙니다.","밥, 채소, 물을 넣고 부드러워질 때까지 끓입니다.","뜨겁지 않게 식혀 제공합니다."],"tip":"갑각류 알레르기가 있으면 선택하지 마세요.","image":"https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80"},
    {"name":"참깨 두부무침","category":"반찬","minutes":12,"age":12,"allergens":["대두","참깨"],"ingredients":["두부 80g","참깨 1/2작은술","시금치 20g"],"steps":["두부를 충분히 익혀 물기를 뺍니다.","시금치를 데쳐 잘게 다집니다.","두부를 으깨 시금치와 섞습니다.","참깨를 넣는 경우 곱게 갈아 소량만 섞습니다."],"tip":"대두와 참깨 알레르기가 있으면 제외하세요.","image":"https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80"},
    {"name":"우유 없는 바나나 팬케이크","category":"간식","minutes":15,"age":12,"allergens":["달걀","밀"],"ingredients":["바나나 1/2개","달걀 1개","밀가루 2큰술","물 1큰술"],"steps":["바나나를 곱게 으깹니다.","달걀과 밀가루, 물을 넣고 섞습니다.","약불 팬에서 작은 크기로 앞뒤를 충분히 익힙니다.","속까지 익었는지 확인하고 식혀 제공합니다."],"tip":"달걀과 밀 성분이 포함됩니다. 해당 알레르기가 있으면 제외하세요.","image":"https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=900&q=80"},
    {"name":"메밀 채소국수","category":"면","minutes":18,"age":24,"allergens":["메밀","밀"],"ingredients":["메밀국수 50g","당근 15g","애호박 15g","물 또는 무염 육수"],"steps":["면을 제품 안내에 따라 충분히 삶습니다.","당근과 애호박을 부드럽게 익힙니다.","면을 짧게 잘라 채소와 함께 담습니다.","육수의 간과 온도를 확인해 제공합니다."],"tip":"메밀과 밀 알레르기가 있으면 제외하세요.","image":"https://images.unsplash.com/photo-1555126634-323283e090fa?auto=format&fit=crop&w=900&q=80"},
    {"name":"소고기 무국","category":"국·수프","minutes":30,"age":12,"allergens":[],"ingredients":["소고기 50g","무 40g","물 300ml","대파 조금(선택)"],"steps":["소고기와 무를 잘게 썹니다.","냄비에 소고기를 넣어 충분히 익힙니다.","무와 물을 넣고 무가 부드러워질 때까지 끓입니다.","아이용은 소금을 넣지 않거나 최소화하고 식혀 제공합니다."],"tip":"어린아이에게는 짠 양념을 최소화하세요.","image":"https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80"},
    {"name":"배추 닭고기 찜","category":"한 그릇","minutes":25,"age":12,"allergens":[],"ingredients":["닭고기 60g","배추 40g","당근 15g","물 약간"],"steps":["닭고기와 채소를 잘게 썹니다.","찜기에 배추와 당근, 닭고기를 올립니다.","닭고기가 속까지 익고 채소가 부드러워질 때까지 찝니다.","먹기 좋은 크기로 잘라 제공합니다."],"tip":"고기의 익힘 상태와 식감을 확인하세요.","image":"https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80"},
    {"name":"블루베리 바나나 스무시 볼","category":"간식","minutes":8,"age":12,"allergens":[],"ingredients":["블루베리 30g","바나나 1/2개","물 또는 무가당 식물성 음료 약간"],"steps":["블루베리를 깨끗이 씻습니다.","바나나와 블루베리를 으깨거나 갈아 부드럽게 만듭니다.","필요하면 물을 조금 넣어 농도를 조절합니다.","숟가락으로 먹기 적당한 농도로 제공합니다."],"tip":"통블루베리보다 으깨거나 잘라 제공해 질식 위험을 줄이세요.","image":"https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?auto=format&fit=crop&w=900&q=80"},
]

# 재료명에 들어가는 알레르기 관련 표현을 추가로 검사합니다.
# 이 키워드 목록은 보조 필터이며, 제품 라벨 검사를 대신하지 않습니다.
ALIASES = {
    "우유": ["우유", "요거트", "요구르트", "치즈", "버터", "크림", "유청", "분유"],
    "달걀": ["달걀", "계란", "난백", "난황"],
    "대두": ["대두", "두부", "두유", "된장", "간장", "콩기름"],
    "밀": ["밀가루", "밀", "파스타", "국수", "빵", "팬케이크"],
    "생선": ["연어", "대구", "흰살생선", "생선", "참치"],
    "땅콩": ["땅콩", "피넛"],
    "견과류": ["아몬드", "호두", "캐슈", "헤이즐넛", "피스타치오", "견과"],
    "새우·갑각류": ["새우", "게살", "게 ", "갑각류", "크릴"],
    "메밀": ["메밀"],
    "참깨": ["참깨", "깨", "참기름"],
    "귀리": ["오트밀", "귀리"],
    "돼지고기": ["돼지고기", "돼지"],
    "소고기": ["소고기", "쇠고기"],
    "닭고기": ["닭고기", "닭 "],
}

ALLERGEN_OPTIONS = ["우유", "달걀", "대두", "밀", "생선", "땅콩", "견과류", "새우·갑각류", "메밀", "참깨", "귀리", "돼지고기", "소고기", "닭고기"]

def detected_allergens(recipe):
    found = set(recipe["allergens"])
    text = " ".join(recipe["ingredients"]) + " " + recipe["name"]
    for allergen, keywords in ALIASES.items():
        if any(keyword in text for keyword in keywords):
            found.add(allergen)
    return found

def is_safe_candidate(recipe, selected_allergies, age_months, dislikes):
    if recipe["age"] > age_months:
        return False
    if selected_allergies.intersection(detected_allergens(recipe)):
        return False
    text = (recipe["name"] + " " + " ".join(recipe["ingredients"])).lower()
    if any(word.lower() in text for word in dislikes if word.strip()):
        return False
    return True

def render_recipe(recipe):
    left, right = st.columns([1, 1.25], gap="large")
    with left:
        st.image(recipe["image"], use_container_width=True)
        st.caption("{}분 · {} · 권장 월령 {}개월 이상".format(recipe["minutes"], recipe["category"], recipe["age"]))
        tags = sorted(detected_allergens(recipe))
        st.write("**등록된 알레르기 성분:** " + (", ".join(tags) if tags else "등록된 주요 성분 없음"))
    with right:
        st.markdown("**🧺 재료**")
        for ingredient in recipe["ingredients"]:
            st.write("- " + ingredient)
        st.markdown("**👩‍🍳 조리 순서**")
        for number, step in enumerate(recipe["steps"], 1):
            st.write("{}. {}".format(number, step))
        st.info("💡 " + recipe["tip"])

st.markdown("""
<style>
.stApp {background: linear-gradient(180deg, #fffaf0 0%, #fffdf8 55%, #f2faf2 100%);}
.block-container {max-width: 1180px; padding-top: 1.5rem;}
div[data-testid="stMetric"] {background: white; border: 1px solid #eee5d6; padding: 12px; border-radius: 14px;}
</style>
""", unsafe_allow_html=True)

st.title("🥕 오늘의 꼬마식탁")
st.write("아이의 나이와 보호자가 입력한 알레르기 정보를 바탕으로 메뉴를 걸러내고, 재료와 조리법을 보여줘요.")

with st.sidebar:
    st.header("👶 우리 아이 설정")
    nickname = st.text_input("아이 별명", value="꼬마")
    age_label = st.selectbox("아이 나이", ["7~11개월", "12~23개월", "2~3세", "4세 이상"], index=2)
    age_months = {"7~11개월": 11, "12~23개월": 23, "2~3세": 47, "4세 이상": 100}[age_label]
    st.markdown("**🚫 피해야 할 알레르기 성분**")
    st.caption("아래에서 아이에게 해당하는 성분을 직접 선택해 주세요. 앱이 보호자 대신 알레르기를 알아내지는 못해요.")
    selected_allergies = set(st.multiselect("알레르기 선택", ALLERGEN_OPTIONS, label_visibility="collapsed"))
    custom_allergies_text = st.text_input("목록에 없는 알레르기 성분", placeholder="예: 망고, 키위")
    custom_allergies = [x.strip() for x in custom_allergies_text.replace("，", ",").split(",") if x.strip()]
    dislikes_text = st.text_input("싫어하는 식재료 (쉼표로 구분)", placeholder="예: 버섯, 브로콜리")
    dislikes = [x.strip() for x in dislikes_text.replace("，", ",").split(",") if x.strip()]
    include_snacks = st.checkbox("간식 포함", value=True)
    st.divider()
    st.caption("알레르기가 있는 경우 제품 포장지의 원재료와 교차접촉 표시를 꼭 확인하세요.")

# 사용자가 자유 입력한 알레르기 단어는 레시피 이름과 재료명에 직접 대조합니다.
safe_recipes = []
for recipe in RECIPES:
    if not is_safe_candidate(recipe, selected_allergies, age_months, dislikes):
        continue
    text = (recipe["name"] + " " + " ".join(recipe["ingredients"])).lower()
    if any(custom.lower() in text for custom in custom_allergies):
        continue
    safe_recipes.append(recipe)

if not safe_recipes:
    st.error("현재 설정에 맞는 레시피가 없어요. 알레르기와 기피 재료 설정을 확인하거나, 전문가와 상의해 안전한 메뉴를 추가해 주세요.")
    st.stop()

seed_text = "{}|{}|{}|{}|{}".format(date.today().isoformat(), nickname, sorted(selected_allergies), custom_allergies_text, st.session_state.get("refresh_count", 0))
seed = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest(), 16) % (2**32)
rng = random.Random(seed)
st.success("{}를 위한 추천 가능 메뉴: {}개".format(nickname, len(safe_recipes)))
m1, m2, m3 = st.columns(3)
m1.metric("추천 가능한 메뉴", "{}개".format(len(safe_recipes)))
m2.metric("선택한 알레르기", "{}개".format(len(selected_allergies) + len(custom_allergies)))
m3.metric("레시피 전체", "{}개".format(len(RECIPES)))

if "refresh_count" not in st.session_state:
    st.session_state["refresh_count"] = 0
if st.button("🔄 다른 메뉴로 다시 추천받기", use_container_width=True):
    st.session_state["refresh_count"] += 1
    st.rerun()

meal_names = ["아침", "점심", "저녁"] + (["간식"] if include_snacks else [])
pool = list(safe_recipes)
rng.shuffle(pool)
today_items = [(meal, pool[index % len(pool)]) for index, meal in enumerate(meal_names)]

tab_today, tab_week, tab_all = st.tabs(["🍽️ 오늘의 식단", "📅 7일 식단표", "📚 레시피 모음"])

with tab_today:
    columns = st.columns(2)
    for index, (meal, recipe) in enumerate(today_items):
        with columns[index % len(columns)]:
            with st.container(border=True):
                st.markdown("#### " + meal)
                st.markdown("### " + recipe["name"])
                st.image(recipe["image"], use_container_width=True)
                st.caption("{}분 · {}".format(recipe["minutes"], recipe["category"]))
                if st.button("재료와 조리법 보기", key="today_" + meal):
                    st.session_state["chosen_recipe"] = recipe["name"]
    chosen_name = st.session_state.get("chosen_recipe")
    chosen_recipe = next((recipe for recipe in safe_recipes if recipe["name"] == chosen_name), None)
    if chosen_recipe:
        st.divider()
        st.subheader("상세 조리법")
        render_recipe(chosen_recipe)

with tab_week:
    st.subheader("7일 식단표")
    for offset in range(7):
        day = date.today() + timedelta(days=offset)
        day_rng = random.Random(seed + offset + 101)
        day_pool = list(safe_recipes)
        day_rng.shuffle(day_pool)
        with st.expander("{}월 {}일 ({})".format(day.month, day.day, ["월","화","수","목","금","토","일"][day.weekday()]), expanded=(offset == 0)):
            for index, meal in enumerate(meal_names):
                recipe = day_pool[index % len(day_pool)]
                st.write("**{}** — {} ({}분)".format(meal, recipe["name"], recipe["minutes"]))
    st.subheader("🛒 장보기 목록")
    ingredients = list(dict.fromkeys(item for recipe in safe_recipes for item in recipe["ingredients"]))
    for index, ingredient in enumerate(ingredients):
        st.checkbox(ingredient, key="shop_{}".format(index))
    shopping_text = "장보기 목록\n" + "\n".join("- " + item for item in ingredients)
    st.download_button("장보기 목록 다운로드", shopping_text, file_name="꼬마식탁_장보기목록.txt", mime="text/plain")

with tab_all:
    st.subheader("레시피 모음")
    category = st.selectbox("종류", ["전체"] + sorted(set(recipe["category"] for recipe in safe_recipes)))
    query = st.text_input("메뉴 또는 재료 검색", placeholder="예: 감자, 죽, 닭고기")
    for recipe in safe_recipes:
        if category != "전체" and recipe["category"] != category:
            continue
        searchable = recipe["name"] + " " + " ".join(recipe["ingredients"])
        if query.lower() not in searchable.lower():
            continue
        with st.expander("{} · {}분".format(recipe["name"], recipe["minutes"])):
            render_recipe(recipe)

st.divider()
st.caption("중요: 알레르기 필터는 앱에 등록된 레시피 정보와 키워드를 이용한 보조 기능이며 안전을 보장하지 않습니다. 제품별 숨은 성분, 제조 과정의 교차접촉, 모든 복합 원재료를 완벽히 판별할 수 없어요. 식품 라벨과 의료진 지침을 우선하고, 영아 식단은 전문가와 상의하세요.")
