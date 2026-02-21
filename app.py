import streamlit as st
import re
import requests

# --- 1. 多國語言字典設定 ---
LANGUAGES = {
    "繁體中文": {
        "title": "🔮 數字易經能量分析 (專業版)",
        "input_label": "請輸入欲分析的號碼 (手機或身分證)：",
        "score_label": "能量總評分",
        "lock_msg": "🔒 深度分析報告已鎖定",
        "unlock_benefit": "目前的免費版本僅提供總分參考。支付後可解鎖：\n- 逐段數字磁場解析 (八星明細)\n- 針對號碼的專業開運建議",
        "pay_btn": "💳 支付 1 USD 解鎖完整報告",
        "paid_success": "✅ 付款成功！已為您解鎖深度詳細報告",
        "detail_table": "📊 完整磁場分佈表",
        "advice_title": "💡 深度解析建議",
        "footer": "免責聲明：本分析僅供娛樂參考，生活幸福仍需靠自身努力。",
        "col_section": "區段", "col_star": "星號", "col_score": "分數"
    },
    "English": {
        "title": "🔮 Digital I-Ching Analysis (Pro)",
        "input_label": "Enter the number to analyze (Phone or ID):",
        "score_label": "Total Energy Score",
        "lock_msg": "🔒 Detailed Analysis Locked",
        "unlock_benefit": "The free version only shows the total score. Pay to unlock:\n- Segmented energy analysis (8 Stars details)\n- Professional fortune advice for this number",
        "pay_btn": "💳 Pay 1 USD to Unlock Full Report",
        "paid_success": "✅ Payment Successful! Full report unlocked.",
        "detail_table": "📊 Energy Distribution Detail",
        "advice_title": "💡 Deep Insight & Advice",
        "footer": "Disclaimer: This analysis is for entertainment only.",
        "col_section": "Section", "col_star": "Star", "col_score": "Score"
    }
}

# --- 2. 自動偵測 IP 國家功能 ---
def get_visitor_info():
    try:
        # 使用 ip-api.com 免費介面 (每分鐘限制 45 次請求)
        response = requests.get("http://ip-api.com/json/", timeout=5).json()
        if response.get("status") == "success":
            return response.get("countryCode") # 例如 'TW', 'US'
    except:
        return None
    return None

# --- 3. 數字易經核心邏輯 ---
class DigitalIChingPro:
    def __init__(self):
        self.star_config = {
            "天醫(吉/Wealth)": {"pairs": ["13", "31", "68", "86", "49", "94", "27", "72"], "score": 20},
            "生氣(吉/Noble)": {"pairs": ["14", "41", "67", "76", "39", "93", "28", "82"], "score": 15},
            "延年(吉/Carrer)": {"pairs": ["19", "91", "78", "87", "34", "43", "26", "62"], "score": 15},
            "伏位(吉/Stable)": {"pairs": ["11", "22", "33", "44", "66", "77", "88", "99"], "score": 10},
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
            if current in '05':
                i += 1; continue
            next_idx = i + 1
            has_zero, has_five = False, False
            while next_idx < len(nums) and nums[next_idx] in '05':
                if nums[next_idx] == '0': has_zero = True
                if nums[next_idx] == '5': has_five = True
                next_idx += 1
            if next_idx < len(nums):
                pair = current + nums[next_idx]
                star_name, base_score = self.get_star_info(pair)
                # 權重修正
                final_pair_score = base_score * (1.2 if has_five else 1.0) * (0.5 if has_zero else 1.0)
                total_score += final_pair_score
                results.append({"Section": nums[i:next_idx+1], "Star": star_name, "Score": round(final_pair_score, 1)})
            i += 1
        return results, max(0, min(100, round(total_score, 1)))

    def get_star_info(self, pair):
        for name, info in self.star_config.items():
            if pair in info["pairs"]: return name, info["score"]
        return "Normal", 0

# --- 4. 網頁介面實作 ---
st.set_page_config(page_title="I-Ching Energy", page_icon="🔮")

# A. 處理語言偵測
if "lang_pref" not in st.session_state:
    country_code = get_visitor_info()
    if country_code in ["TW", "HK", "MO", "CN"]:
        st.session_state.lang_pref = "繁體中文"
    else:
        st.session_state.lang_pref = "English"

selected_lang = st.sidebar.selectbox("Language/語言", list(LANGUAGES.keys()), 
                                     index=list(LANGUAGES.keys()).index(st.session_state.lang_pref))
t = LANGUAGES[selected_lang]

# B. 檢查支付狀態
is_paid = st.query_params.get("pay") == "success"

# C. 主要內容
st.title(t["title"])
num_input = st.text_input(t["input_label"], placeholder="0912345678")

if num_input:
    clean_nums = re.sub(r'\D', '', num_input)
    engine = DigitalIChingPro()
    details, score = engine.analyze(clean_nums)
    
    st.divider()
    st.metric(t["score_label"], f"{score} 分/pts")
    
    if is_paid:
        st.success(t["paid_success"])
        st.subheader(t["detail_table"])
        # 重新格式化表格欄位名稱
        df_display = [{"區段/Section": d["Section"], "星號/Star": d["Star"], "分數/Score": d["Score"]} for d in details]
        st.table(df_display)
        
        st.subheader(t["advice_title"])
        if score >= 60:
            st.write("🌟 Positive energy detected. Suitable for expansion.")
        else:
            st.write("⚠️ Energy conflict found. Caution advised in decisions.")
    else:
        st.warning(t["lock_msg"])
        st.write(t["unlock_benefit"])
        paypal_url = f"https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE" # 請更換為你的 ID
        st.link_button(t["pay_btn"], paypal_url)
        
        # 測試用按鈕
        if st.sidebar.button("Test: Unlock Now"):
            st.query_params["pay"] = "success"
            st.rerun()

st.sidebar.caption(f"Detected Country: {get_visitor_info()}")
st.caption(t["footer"])