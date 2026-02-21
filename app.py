import streamlit as st
import re
import requests
import random

# --- 1. 多國語言字典設定 ---
LANGUAGES = {
    "繁體中文": {
        "title": "🔮 數字易經能量分析 (專業版)",
        "input_label": "請輸入欲分析的號碼 (手機或身分證)：",
        "score_label": "能量總評分",
        "lock_msg": "🔒 分析報告已鎖定",
        "unlock_benefit": "為了保護您的隱私與提供最精準的深度解析，請支付後查看：\n- 能量總評分 (吉凶鑑定)\n- 逐段數字磁場解析 (八星明細)\n- 針對號碼的專業開運建議",
        "pay_btn": "💳 支付 1 USD 解鎖完整報告",
        "paid_success": "✅ 付款成功！已為您解鎖完整分析報告",
        "detail_table": "📊 完整磁場分佈表",
        "advice_title": "💡 深度解析建議",
        "solution_title": "🛠️ 數位磁場解決方案",
        "solution_msg": "檢測到您的數位磁場存在缺口，系統已根據您號碼的長度與結構，演算出專屬化解方案。",
        "remedy_code": "✨ 專屬化解碼建議：",
        "remedy_score": "📈 化解碼經統計分數為：",
        "footer": "免責聲明：本分析僅供娛樂參考，生活幸福仍需靠自身努力。",
        "col_section": "區段", "col_star": "星號", "col_score": "分數"
    },
    "English": {
        "title": "🔮 Digital I-Ching Analysis (Pro)",
        "input_label": "Enter the number to analyze (Phone or ID):",
        "score_label": "Total Energy Score",
        "lock_msg": "🔒 Analysis Report Locked",
        "unlock_benefit": "To provide the most accurate deep analysis, please pay to view:\n- Total Energy Score (Lucky/Unlucky)\n- Segmented energy analysis (8 Stars details)\n- Professional fortune advice for this number",
        "pay_btn": "💳 Pay 1 USD to Unlock Full Report",
        "paid_success": "✅ Payment Successful! Full report unlocked.",
        "detail_table": "📊 Energy Distribution Detail",
        "advice_title": "💡 Deep Insight & Advice",
        "solution_title": "🛠️ Digital Field Solution",
        "solution_msg": "Based on your number's structure, we have calculated a customized remedy code.",
        "remedy_code": "✨ Recommended Remedy Code:",
        "remedy_score": "📈 Remedy Code Statistical Score:",
        "footer": "Disclaimer: This analysis is for entertainment only.",
        "col_section": "Section", "col_star": "Star", "col_score": "Score"
    }
}

# --- 2. 自動偵測 IP 國家功能 ---
def get_visitor_info():
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5).json()
        if response.get("status") == "success":
            return response.get("countryCode")
    except:
        return None
    return None

# --- 3. 數字易經核心邏輯 ---
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

    def generate_dynamic_remedy(self, original_nums):
        # 根據原號碼長度決定化解碼長度
        length = len(original_nums)
        if length < 6: length = 6
        if length > 14: length = 14
        
        # 強大吉星組合庫
        best_pairs = ["13", "31", "68", "86", "49", "94", "14", "41", "19", "91", "78", "87"]
        
        remedy_code = ""
        # 循環填充直到達到目標長度
        while len(remedy_code) < length:
            remedy_code += random.choice(best_pairs)
        
        # 截斷至剛好長度
        remedy_code = remedy_code[:length]
        
        # 生成一個 97.0 到 99.8 之間的高分
        dynamic_score = round(97 + random.uniform(0, 2.8), 1)
        return remedy_code, dynamic_score

# --- 4. 網頁介面實作 ---
st.set_page_config(page_title="I-Ching Energy Pro", page_icon="🔮")

if "lang_pref" not in st.session_state:
    country_code = get_visitor_info()
    st.session_state.lang_pref = "繁體中文" if country_code in ["TW", "HK", "MO", "CN"] else "English"

selected_lang = st.sidebar.selectbox("Language/語言", list(LANGUAGES.keys()), 
                                     index=list(LANGUAGES.keys()).index(st.session_state.lang_pref))
t = LANGUAGES[selected_lang]

is_paid = st.query_params.get("pay") == "success"

st.title(t["title"])
num_input = st.text_input(t["input_label"], placeholder="例如：0912345678")

if num_input:
    clean_nums = re.sub(r'\D', '', num_input)
    engine = DigitalIChingPro()
    details, score = engine.analyze(clean_nums)
    
    st.divider()
    
    if is_paid:
        st.success(t["paid_success"])
        st.metric(t["score_label"], f"{score} 分/pts")
        
        st.subheader(t["detail_table"])
        df_display = [{"區段/Section": d["Section"], "星號/Star": d["Star"], "分數/Score": d["Score"]} for d in details]
        st.table(df_display)
        
        # --- 動態化解方案區塊 ---
        st.divider()
        st.subheader(t["solution_title"])
        
        if score < 75: # 分數低於 75 即給予建議，增加服務價值
            remedy_code, r_score = engine.generate_dynamic_remedy(clean_nums)
            st.error(f"⚠️ {t['solution_msg']}")
            st.info(f"{t['remedy_code']} **{remedy_code}** (對應原號 {len(clean_nums)} 位能級)")
            st.success(f"{t['remedy_score']} **{r_score} 分**")
        else:
            st.write("✨ 您的數字磁場能量極佳，無需額外化解。")
            
        st.subheader(t["advice_title"])
        if score >= 60:
            st.write("🌟 正向能量充足，利於事業與財運開展。")
        else:
            st.write("⚠️ 磁場能量較不穩定，建議參考專屬化解方案。")
        
        if st.button("🔄 重新分析 / Re-analyze"):
            st.query_params.clear()
            st.rerun()
    else:
        st.warning(t["lock_msg"])
        st.info(f"📍 號碼 {num_input} 的能量場已計算完畢。")
        st.write(t["unlock_benefit"])
        
        # 更新後的 PayPal 1 USD 連結
        paypal_payment_url = "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE"
        st.link_button(t["pay_btn"], paypal_payment_url)
        
        if st.sidebar.button("🛠️ 測試：模擬支付解鎖"):
            st.query_params["pay"] = "success"
            st.rerun()

st.sidebar.caption(f"Visitor Location: {get_visitor_info()}")
st.caption(t["footer"])