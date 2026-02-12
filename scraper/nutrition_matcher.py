"""
Match Sushiro Japan calorie data (Japanese names) to Sushiro HK menu items (Chinese names).

Strategy:
1. Many items share kanji between Japanese and Chinese (e.g. サーモン=三文魚, まぐろ=吞拿魚)
2. Build a manual mapping of common Japanese→Chinese ingredient keywords
3. Use shared kanji characters for fuzzy matching
4. Output a calories lookup dict: { hk_item_title: calories }
"""
import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Manual keyword mapping: Japanese term → possible Chinese terms in HK menu
JP_TO_CN_KEYWORDS = {
    # Fish / Seafood
    'サーモン': ['三文魚', '鮭魚'],
    'まぐろ': ['吞拿魚', '鮪魚', '金槍魚'],
    'とろ': ['拖羅', '腩'],
    'えび': ['蝦', '海老'],
    'いか': ['魷魚', '花枝', '墨魚'],
    'たこ': ['章魚', '八爪魚'],
    'はまち': ['油甘魚', '鰤魚'],
    'うなぎ': ['鰻魚', '鰻'],
    'あなご': ['星鰻', '穴子'],
    'さば': ['鯖魚', '青花魚'],
    'いわし': ['沙甸魚', '鰯'],
    'かつお': ['鰹魚', '木魚'],
    'たい': ['鯛魚', '鯛'],
    '真鯛': ['真鯛'],
    'ほたて': ['帶子', '扇貝'],
    'あわび': ['鮑魚'],
    'とり貝': ['鳥貝'],
    'つぶ貝': ['螺'],
    'たらこ': ['鱈魚子', '明太子'],
    'かに': ['蟹'],
    'うに': ['海膽'],

    # Preparations
    '炙り': ['炙', '火炙'],
    '天ぷら': ['天婦羅'],
    '天': ['天婦羅'],
    'チーズ': ['芝士'],
    'アボカド': ['牛油果'],
    'マヨ': ['蛋黃醬', '美乃滋'],
    'ツナ': ['吞拿'],
    '納豆': ['納豆'],
    '玉子': ['玉子', '蛋'],
    'たまご': ['玉子', '蛋'],
    'ハム': ['火腿'],
    'バジル': ['羅勒'],
    'レモン': ['檸檬'],
    'オニオン': ['洋蔥'],

    # Dishes
    'うどん': ['烏冬'],
    'ラーメン': ['拉麵', '拉面'],
    '味噌汁': ['味噌湯'],
    '茶碗蒸し': ['茶碗蒸'],
    'パフェ': ['芭菲'],
    'アイス': ['雪糕'],
    'ケーキ': ['蛋糕'],

    # Rolls / Types
    '軍艦': ['軍艦'],
    '巻': ['卷'],
    'いなり': ['稻荷', '豆腐皮'],
    'にぎり': ['握'],
}

# Direct name mappings for items that are hard to match automatically
DIRECT_MAPPINGS = {
    # Japanese name → Chinese name (exact match from HK menu)
    # These will be populated as we discover matches
}


def load_nutrition_data():
    path = os.path.join(SCRIPT_DIR, 'nutrition_data.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_hk_menu():
    path = os.path.join(SCRIPT_DIR, 'scraped_data.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_kanji(text):
    """Extract CJK characters (shared between Japanese and Chinese)."""
    if not text:
        return ''
    return re.sub(r'[^\u4e00-\u9fff]', '', text)


def calculate_match_score(jp_name, cn_title):
    """Calculate how well a Japanese item name matches a Chinese menu title."""
    if not jp_name or not cn_title:
        return 0

    score = 0

    # 1. Check keyword mappings
    for jp_keyword, cn_keywords in JP_TO_CN_KEYWORDS.items():
        if jp_keyword in jp_name:
            for cn_kw in cn_keywords:
                if cn_kw in cn_title:
                    score += 10

    # 2. Shared kanji characters
    jp_kanji = set(extract_kanji(jp_name))
    cn_kanji = set(extract_kanji(cn_title))
    if jp_kanji and cn_kanji:
        shared = jp_kanji & cn_kanji
        if shared:
            score += len(shared) * 3

    return score


def match_nutrition_to_menu(nutrition_data, hk_menu):
    """Match nutrition items to HK menu items. Returns { title: calories }."""
    all_nutrition_items = []
    for category, items in nutrition_data.get('categories', {}).items():
        for item in items:
            all_nutrition_items.append(item)

    matches = {}
    unmatched_jp = []
    unmatched_hk = []

    for hk_item in hk_menu:
        title = hk_item.get('title', '')
        if not title:
            continue

        best_score = 0
        best_match = None

        for nut_item in all_nutrition_items:
            jp_name = nut_item['name_jp']

            # Check direct mapping first
            if jp_name in DIRECT_MAPPINGS:
                if DIRECT_MAPPINGS[jp_name] == title:
                    best_match = nut_item
                    best_score = 999
                    break

            score = calculate_match_score(jp_name, title)
            if score > best_score:
                best_score = score
                best_match = nut_item

        if best_score >= 10 and best_match:
            matches[title] = {
                'calories': best_match['calories'],
                'protein': best_match.get('protein'),
                'fat': best_match.get('fat'),
                'carbs': best_match.get('carbs'),
                'matched_jp': best_match['name_jp'],
                'score': best_score,
            }
        else:
            unmatched_hk.append(title)

    return matches, unmatched_hk


def generate_calories_lookup():
    """Generate a calories lookup dict and save it."""
    nutrition_data = load_nutrition_data()
    hk_menu = load_hk_menu()

    matches, unmatched = match_nutrition_to_menu(nutrition_data, hk_menu)

    print(f"\nMatched: {len(matches)} / {len(hk_menu)} items")
    print(f"Unmatched: {len(unmatched)} items\n")

    if matches:
        print("--- Matched Items ---")
        for title, info in sorted(matches.items(), key=lambda x: -x[1]['score']):
            print(f"  {title} → {info['matched_jp']} ({info['calories']} kcal) [score: {info['score']}]")

    if unmatched:
        print("\n--- Unmatched HK Items ---")
        for title in sorted(unmatched):
            print(f"  {title}")

    # Save lookup as JSON with full macros
    lookup = {}
    for title, info in matches.items():
        entry = {'calories': info['calories']}
        if info.get('protein') is not None:
            entry['protein'] = info['protein']
        if info.get('fat') is not None:
            entry['fat'] = info['fat']
        if info.get('carbs') is not None:
            entry['carbs'] = info['carbs']
        lookup[title] = entry

    output_path = os.path.join(SCRIPT_DIR, 'calories_lookup.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(lookup, f, indent=2, ensure_ascii=False)

    print(f"\nSaved calories_lookup.json with {len(lookup)} entries")
    return lookup


if __name__ == '__main__':
    generate_calories_lookup()
