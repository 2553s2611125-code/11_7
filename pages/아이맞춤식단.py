import streamlit as st
from datetime import date, timedelta
import random
import hashlib
import json
import re

st.set_page_config(page_title="오늘의 꼬마식탁", page_icon="🥕", layout="wide")

# ----------------------------
# 앱 내장 레시피 데이터
# allergens는 식품 알레르기 표시용 주요 성분 태그입니다.
# 실제 제품/양념의 교차오염 가능성은 별도로 확인해야 합니다.
# ----------------------------
RECIPES = [
    {
        "id": "rice_bowl", "name": "닭고기 채소 덮밥", "category": "한 그릇", "age_min": 12,
        "time": 20, "difficulty": "쉬워요", "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["밥 1공기", "닭고기 80g", "당근 20g", "애호박 20g", "양파 15g", "식용유 약간"],
        "allergens": [], "avoid_tags": ["닭고기"],
        "steps": ["닭고기와 채소를 아이가 먹기 좋은 작은 크기로 썰어요.", "팬에 식용유를 아주 조금 두르고 닭고기를 완전히 익혀요.", "당근, 애호박, 양파를 넣고 부드러워질 때까지 볶아요.", "밥 위에 올리고 재료가 너무 뜨겁지 않은지 확인해 주세요."],
        "tips": "돌 이후 아이는 질기거나 큰 조각이 없도록 잘게 잘라 주세요."
    },
    {
        "id": "beef_porridge", "name": "소고기 채소죽", "category": "죽", "age_min": 7,
        "time": 25, "difficulty": "쉬워요", "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["밥 1/2공기", "다진 소고기 40g", "당근 15g", "애호박 15g", "물 250ml"],
        "allergens": [], "avoid_tags": ["소고기"],
        "steps": ["당근과 애호박을 아주 잘게 다져요.", "냄비에 소고기를 넣고 색이 변할 때까지 볶아요.", "밥과 채소, 물을 넣고 약불에서 저어 가며 끓여요.", "재료가 충분히 부드러워지고 고기가 완전히 익으면 식혀서 주세요."],
        "tips": "월령과 씹기 능력에 맞춰 물의 양과 입자 크기를 조절하세요."
    },
    {
        "id": "salmon_pasta", "name": "연어 채소 파스타", "category": "면", "age_min": 12,
        "time": 25, "difficulty": "보통", "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["짧은 파스타 60g", "연어 60g", "브로콜리 25g", "양파 15g", "올리브유 약간"],
        "allergens": ["생선", "밀"], "avoid_tags": ["생선"],
        "steps": ["파스타를 제품 안내에 따라 충분히 익혀요.", "연어의 가시를 꼼꼼히 확인하고 완전히 익힌 뒤 잘게 부숴요.", "브로콜리와 양파를 부드럽게 익혀 잘게 다져요.", "모든 재료를 섞고 필요하면 면수를 조금 넣어 부드럽게 마무리해요."],
        "tips": "생선 가시와 면의 길이·탄력에 주의하고 아이가 먹기 좋은 크기로 준비하세요."
    },
    {
        "id": "egg_pancake", "name": "채소 달걀전", "category": "반찬", "age_min": 12,
        "time": 15, "difficulty": "쉬워요", "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["달걀 1개", "당근 15g", "애호박 15g", "양파 10g", "식용유 약간"],
        "allergens": ["달걀"], "avoid_tags": [],
        "steps": ["채소를 아주 잘게 다져요.", "달걀을 풀고 다진 채소를 섞어요.", "달군 팬에 기름을 아주 조금 바르고 한입 크기로 부쳐요.", "속까지 완전히 익힌 뒤 충분히 식혀서 제공해요."],
        "tips": "달걀 알레르기가 있으면 이 레시피는 선택하지 마세요."
    },
    {
        "id": "tofu_rice", "name": "두부 버섯 비빔밥", "category": "한 그릇", "age_min": 12,
        "time": 20, "difficulty": "쉬워요", "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["밥 1공기", "두부 80g", "표고버섯 20g", "당근 15g", "참기름 몇 방울"],
        "allergens": ["대두"], "avoid_tags": [],
        "steps": ["두부의 물기를 빼고 작은 큐브로 썰어요.", "버섯과 당근을 잘게 다져 충분히 익혀요.", "두부를 넣고 부서지지 않게 볶아요.", "밥 위에 올리고 참기름을 아주 조금 더해 섞어 주세요."],
        "tips": "두부는 대두 성분을 포함해요. 대두 알레르기가 있으면 제외하세요."
    },
    {
        "id": "chicken_soup", "name": "닭고기 감자 수프", "category": "국·수프", "age_min": 9,
        "time": 25, "difficulty": "쉬워요", "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["닭고기 60g", "감자 1/2개", "양파 15g", "물 250ml", "우유 50ml(선택)"],
        "allergens": ["우유"], "avoid_tags": ["닭고기"],
        "steps": ["닭고기와 감자, 양파를 작은 크기로 썰어요.", "냄비에 물과 재료를 넣고 속까지 완전히 익혀요.", "감자가 부드러워지면 숟가락으로 으깨 농도를 조절해요.", "우유를 사용할 경우 우유 알레르기가 없는지 확인하고 한 번 더 데워요."],
        "tips": "우유를 빼고 물로 조리하면 우유 성분을 줄일 수 있지만, 다른 재료의 교차접촉은 별도로 확인해야 해요."
    },
    {
        "id": "banana_oat", "name": "바나나 오트밀", "category": "간식", "age_min": 8,
        "time": 10, "difficulty": "쉬워요", "image": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["오트밀 25g", "바나나 1/2개", "물 또는 우유 100ml"],
        "allergens": ["귀리", "우유(우유 사용 시)"], "avoid_tags": [],
        "steps": ["바나나를 포크로 충분히 으깨요.", "오트밀과 물을 냄비에 넣고 약불에서 부드러워질 때까지 끓여요.", "으깬 바나나를 섞고 충분히 식혀요.", "우유를 사용할 경우 알레르기 여부를 확인하고 물로 대체할 수 있어요."],
        "tips": "귀리 제품은 제조 시설의 밀 등 교차접촉 표시도 확인하세요."
    },
    {
        "id": "sweet_potato", "name": "고구마 요거트 볼", "category": "간식", "age_min": 12,
        "time": 15, "difficulty": "쉬워요", "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["고구마 1/2개", "플레인 요거트 2큰술"],
        "allergens": ["우유"], "avoid_tags": [],
        "steps": ["고구마를 찌거나 삶아 속까지 부드럽게 익혀요.", "껍질을 벗기고 덩어리가 없도록 으깨요.", "충분히 식힌 뒤 플레인 요거트를 섞어요.", "아이의 씹기 능력에 맞는 농도로 조절해 주세요."],
        "tips": "우유 알레르기가 있으면 요거트를 넣지 말고, 대체 제품 성분표를 확인하세요."
    },
    {
        "id": "pork_rice", "name": "돼지고기 애호박 볶음밥", "category": "한 그릇", "age_min": 12,
        "time": 20, "difficulty": "쉬워요", "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["밥 1공기", "다진 돼지고기 60g", "애호박 25g", "당근 15g", "양파 15g"],
        "allergens": [], "avoid_tags": ["돼지고기"],
        "steps": ["채소를 잘게 다져요.", "다진 돼지고기를 팬에서 완전히 익혀요.", "채소를 넣고 부드러워질 때까지 볶아요.", "밥을 넣고 골고루 섞어 충분히 데운 뒤 식혀 주세요."],
        "tips": "고기는 속까지 완전히 익히고 큰 덩어리가 남지 않도록 해 주세요."
    },
    {
        "id": "rice_ball", "name": "김가루 채소 주먹밥", "category": "간식·한 끼", "age_min": 12,
        "time": 15, "difficulty": "쉬워요", "image": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["밥 1공기", "당근 15g", "시금치 15g", "김가루 1작은술", "참기름 몇 방울"],
        "allergens": [], "avoid_tags": [],
        "steps": ["당근과 시금치를 부드럽게 익혀 잘게 다져요.", "밥에 채소와 김가루, 참기름을 섞어요.", "아이의 씹기 능력에 맞는 작고 부드러운 크기로 뭉쳐요.", "목에 걸리지 않도록 질거나 딱딱하지 않은지 확인하며 보호자와 함께 먹어요."],
        "tips": "둥글고 단단한 큰 주먹밥은 질식 위험이 있어 작고 부드럽게 준비하세요."
    },
    {
        "id": "lentil_soup", "name": "렌틸콩 채소 수프", "category": "국·수프", "age_min": 12,
        "time": 30, "difficulty": "보통", "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["렌틸콩 40g", "당근 20g", "감자 1/2개", "양파 15g", "물 300ml"],
        "allergens": [], "avoid_tags": [],
        "steps": ["렌틸콩을 씻고 채소를 작게 썰어요.", "냄비에 모든 재료와 물을 넣어요.", "약불에서 렌틸콩과 채소가 완전히 부드러워질 때까지 끓여요.", "필요하면 으깨거나 갈아 아이에게 맞는 질감으로 조절해요."],
        "tips": "콩류를 처음 먹는 경우 소량으로 시작하고 반응을 살펴보세요."
    },
    {
        "id": "cheese_broccoli", "name": "브로콜리 치즈 감자", "category": "반찬", "age_min": 12,
        "time": 15, "difficulty": "쉬워요", "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=1000&q=80",
        "ingredients": ["감자 1개", "브로콜리 30g", "치즈 1/2장"],
        "allergens": ["우유"], "avoid_tags": [],
        "steps": ["감자와 브로콜리를 부드럽게 찌거나 삶아요.", "감자를 포크로 으깨고 브로콜리를 잘게 다져요.", "치즈를 넣어 잔열로 녹이고 잘 섞어요.", "너무 뜨겁지 않게 식혀 제공해요."],
        "tips": "치즈는 우유 성분이 들어 있어 우유 알레르기가 있으면 제외하세요."
    },
]

ALLERGEN_OPTIONS = ["우유", "달걀", "대두", "밀", "생선", "땅콩", "견과류", "새우·갑각류", "메밀", "참깨", "귀리", "돼지고기", "소고기", "닭고기"]
ALLERGEN_ALIASES = {
    "우유": ["우유", "요거트", "치즈", "버터", "크림", "유청", "분유"],
    "달걀": ["달걀", "계란", "난백", "난황"],
    "대두": ["대두", "두부", "콩", "간장", "두유", "된장"],
    "밀": ["밀", "파스타", "면", "빵", "밀가루", "간장"],
    "생선": ["생선", "연어", "참치", "대구"],
    "땅콩": ["땅콩", "피넛"],
    "견과류": ["견과", "아몬드", "호두", "캐슈", "헤이즐넛", "피스타치오"],
    "새우·갑각류": ["새우", "게", "갑각류", "크릴"],
    "메밀": ["메밀"],
    "참깨": ["참깨", "참기름", "깨"],
    "귀리": ["귀리", "오트밀"],
    "돼지고기": ["돼지고기", "돼지"],
    "소고기": ["소고기", "쇠고기"],
