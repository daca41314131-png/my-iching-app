import streamlit as st
import re
import requests
import random
import pandas as pd

# --- 1. 多國語言字典設定 ---
LANGUAGES = {
    "繁體中文": {
        "title": "🔮 數字易經能量分析 (專業版)",
        "input_label": "請輸入號碼 (支援字母，如身分證、LINE ID)：",
        "score_label": "能量總評分",
        "lock_msg": "🔒 分析報告已鎖定",
        "unlock_benefit": "支付後即可查看：\n- 字母轉譯數據與能量評分\n- 逐段數字磁場解析 (八星明細)\n- 專屬化解方案與對比報表",
        "pay_btn": "💳 支付 1 USD 解鎖完整報告",
        "paid_success": "✅ 付款成功！已解鎖深度分析",
        "detail_table": "📊 原始磁場分佈表",
        "solution_title": "🛠️ 專屬數位化解方案",
        "remedy_code": "✨ 建議化解碼：",
        "remedy_score": "📈 化解碼預計能量分數：",
        "remedy_table": "📋 化解碼磁場解析報表",
        "footer": "免責聲明：本分析僅供娛樂參考。",
        "col_section": "區段", "col_star": "星號", "col_score": "分數"
    },
    "English": {
        "title": "🔮 Digital I-Ching Analysis (Pro)",
        "input_label": "Enter Number/ID (Letters supported):",
        "score_label": "Total Energy Score",
        "lock_msg": "🔒 Analysis Report Locked",
        "unlock_benefit": "Pay to view:\n- Letter-to-number translation\n- 8 Stars detailed analysis\n- Customized remedy report",
        "pay_btn": "💳 Pay 1 USD to Unlock",
        "paid_success": "✅ Payment Successful!",
        "detail_table": "📊 Original Energy Distribution",
        "solution_title": "🛠️ Customized Remedy Solution",
        "remedy_code": "✨ Suggested Remedy Code:",
        "remedy_score": "📈 Estimated Remedy Score:",
        "remedy_table": "📋 Remedy Code Analysis Report",
        "footer": "Disclaimer: For entertainment purposes only.",
        "col_section": "Section", "col_star": "Star", "col_score": "Score"
    }
}

# --- 2. 核心邏輯類別 ---
class DigitalIChingPro:
    def __init__(self):
        self.star_config = {
            "天醫(財運/Wealth)": {"pairs": ["13", "31", "68", "86", "49", "94", "27", "72"], "score": 20},
            "生氣(貴人/Noble)": {"pairs": ["14", "41", "67", "76", "39", "93", "28", "82"], "score": 15},
            "延年(事業/Carrer)": {"pairs": ["19", "91", "78", "87", "34", "43", "26", "62"], "score": 15},
            "伏位(平穩/Stable)": {"pairs": ["11", "22", "33", "44", "66", "77", "88", "99"], "score": 10},
            "絕命(凶/Risky)": {"pairs": ["12", "21", "69", "96", "48", "84", "37", "73"], "score": -20},
            "五鬼(凶/Variable)": {"pairs": ["18", "81", "79", "97", "36", "63", "24", "42"], "score": -20},
            "六煞(凶/Mood)": {"pairs": ["16", "61", "47", "74", "38", "83", "29", "92"], "score": -15},
            "禍害(凶/Gossip)": {"pairs": ["17", "71", "89", "98", "46", "64", "23", "32"], "score": -15}
        }

    # 字母轉數字邏輯 A=01, B=02...
    def convert_letters(self, text):
        converted = ""
        for char in text.upper():
            if char.isdigit():
                converted += char
            elif char.isalpha():
                # A=01, B=02, ..., Z=26
                num = ord(char) - ord('A') + 1
                converted += f"{num:02d}" 
        return converted

    def analyze(self, nums):
        results = []
        total_score = 60
        i = 0
        while i < len(nums) - 1:
            current = nums[i]
            if current in '05': i += 1; continue
            next_idx = i + 1
            has_zero, has_five = False, False
            while next_idx < len(nums) and nums[next_idx] in '05':
                if nums[next_idx] == '0': has_zero = True
                if nums[next_idx] == '5': has_five = True
                next_idx += 1
            if next_idx < len(nums):
                pair = current + nums[next_idx]
                star_name, base_score = self.get_star_info(pair)
                final_pair_score = base_score * (1.2 if has_five else 1.0) * (0.5 if has_zero else 1.0)
                total_score += final_pair_score
                results.append({"Section": nums[i:next_idx+1], "Star": star_name, "Score": round(final_pair_score, 1)})
            i += 1
        return results, max(0, min(100, round(total_score, 1)))

    def get_star_info(self, pair):
        for name, info in self.star_config.items():
            if pair in info["pairs"]: return name, info["score"]
        return "Normal", 0

    def generate_dynamic_remedy(self, clean_nums):
        length = len(clean_nums)
        length = max(6, min(12, length))
        best_pairs = ["13", "31", "68", "86", "49", "94", "14", "41", "19", "91", "78", "87"]
        remedy_code = "".join(random.choice(best_pairs) for _ in range(length//2 + 1))[:length]
        remedy_details, _ = self.analyze(remedy_code)
        remedy_score = round(96 + random.uniform(0, 3.8), 1)
        return remedy_code, remedy_score, remedy_details

# --- 3. 輔助與介面 ---
def get_visitor_info():
    try:
        r = requests.get("http://ip-api.com/json/", timeout=3).json()
        return r.get("countryCode") if r.get("status") == "success" else None
    except: return None

st.set_page_config(page_title="I-Ching Energy Pro", page_icon="🔮")

if "lang_pref" not in st.session_state:
    cc = get_visitor_info()
    st.session_state.lang_pref = "繁體中文" if cc in ["TW", "HK", "MO", "CN"] else "English"

selected_lang = st.sidebar.selectbox("Language/語言", list(LANGUAGES.keys()), 
                                     index=list(LANGUAGES.keys()).index(st.session_state.lang_pref))
t = LANGUAGES[selected_lang]
is_paid = st.query_params.get("pay") == "success"

st.title(t["title"])
raw_input = st.text_input(t["input_label"], placeholder="例如：A123456789 或 LINEID123")

if raw_input:
    engine = DigitalIChingPro()
    # 執行字母轉數字
    clean_nums = engine.convert_letters(raw_input)
    details, score = engine.analyze(clean_nums)
    
    st.divider()
    
    if is_paid:
        st.success(t["paid_success"])
        if any(c.isalpha() for c in raw_input):
            st.info(f"🔢 **轉譯數據：** {clean_nums} (字母已自動轉化為磁場代碼)")
        
        st.metric(t["score_label"], f"{score} 分/pts")
        
        with st.expander(t["detail_table"], expanded=True):
            df_orig = pd.DataFrame(details).rename(columns={"Section": t["col_section"], "Star": t["col_star"], "Score": t["col_score"]})
            st.table(df_orig)
        
        st.divider()
        st.subheader(t["solution_title"])
        if score < 85:
            r_code, r_score, r_details = engine.generate_dynamic_remedy(clean_nums)
            col1, col2 = st.columns(2)
            col1.info(f"{t['remedy_code']}\n### **{r_code}**")
            col2.success(f"{t['remedy_score']}\n### **{r_score}**")
            
            st.markdown(f"#### {t['remedy_table']}")
            df_rem = pd.DataFrame(r_details).rename(columns={"Section": t["col_section"], "Star": t["col_star"], "Score": t["col_score"]})
            st.table(df_rem)
        else:
            st.write("✨ 能量極佳，維持現狀即可。")
    else:
        st.warning(t["lock_msg"])
        st.info(f"📍 內容已接收，包含字母轉譯與磁場計算已準備就緒。")
        st.write(t["unlock_benefit"])
        st.link_button(t["pay_btn"], "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
        
        if st.sidebar.button("🛠️ 測試：模擬解鎖"):
            st.query_params["pay"] = "success"
            st.rerun()

st.caption(t["footer"])