import requests
import pandas as pd

# ==============================
# 1. 기본 설정
# ==============================

LENS_API_URL = "https://api.lens.org/scholarly/search"

API_TOKEN = "eTZyJz2Xm2rz59hMVTkz0ZB3jegploAsYH3JTurgRXV6iHgwAWTh"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# AI Semiconductor 쿼리 (수정 가능)
TECH_QUERY = '''
(semiconductor OR accelerator OR chip OR (Integrated Circuit) OR IC OR processor OR System-on-Chip OR System-on-Module OR SOC) AND (Artificial Intelligen* OR AI OR (neural network) OR neuromorphic OR (deep learning) OR (machine learning) OR inferenc* OR Decision OR Cognition OR Judgment OR Reasoning)
'''

# ==============================
# 2. 공통 함수 (재사용)
# ==============================

def get_count(query_string):
    payload = {
        "query": query_string,
        "size": 0
    }

    r = requests.post(LENS_API_URL, headers=HEADERS, json=payload)

    if r.status_code != 200:
        print("Error:", r.status_code, r.text)
        return None

    return r.json().get("total", 0)


# ==============================
# 3. 쿼리 정의
# ==============================

# 🇰🇷 한국 단독
kr_total_query = f'''
{TECH_QUERY}
AND author.affiliation.address.country_code:KR
'''
kr_international_query = f'''
{TECH_QUERY}
AND author.affiliation.address.country_code:KR
AND author.affiliation.address.country_code:*
AND NOT author.affiliation.address.country_code:KR
'''
kr_total = get_count(kr_total_query)
kr_international = get_count(kr_international_query)
kr_solo = kr_total - kr_international

# 🇰🇷-🇺🇸 한미 공동
kr_us_query = f'''
{TECH_QUERY}
AND author.affiliation.address.country_code:KR
AND author.affiliation.address.country_code:US
'''

# 🇰🇷-🇯🇵 한일 공동
kr_jp_query = f'''
{TECH_QUERY}
AND author.affiliation.address.country_code:KR
AND author.affiliation.address.country_code:JP
'''

# ==============================
# 4. 실행
# ==============================

kr_us = get_count(kr_us_query)
kr_jp = get_count(kr_jp_query)

print("한국 단독:", kr_solo)
print("한-미 공동:", kr_us)
print("한-일 공동:", kr_jp)


# ==============================
# 5. 데이터프레임 정리
# ==============================

df = pd.DataFrame({
    "구분": ["한국 단독", "한-미 공동", "한-일 공동"],
    "논문 수": [kr_solo, kr_us, kr_jp]
})

df
