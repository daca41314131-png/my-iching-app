import streamlit as st
import re
import random
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 大師解說與飲食建議庫 ---
REASON_TEMPLATES = [
    "信士可知，數字乃宇宙萬物能量之體現。您原始號碼中蘊含的氣場，如同先天之命，雖有定數，卻非不可改之侷限。目前的能量分佈顯示，某些負向磁場正潛移默化地干擾您的氣運，導致財氣不聚、元神渙散。",
    "在數位易經的觀點中，每一個號碼都是一個微型能量場。您目前的組合中，正能量吉星與負能量凶星比例失衡。這不代表您運勢不好，而是代表您的『共振頻率』偏離了繁榮的軌道。",
    "觀此號碼之相，磁場中顯現出一股駁雜之氣。在流年更迭中，若不加以調和，容易導致貴人遠去、小人近身。透過特定的數位調和，便能在無形中形成一個守護屏障。"
]

METHOD_TEMPLATES = [
    "大師為您演算的這組『專屬能量調和碼』，乃是根據您當下的氣場感應，運用『同頻對沖』與『陰陽補位』之法精確計算而成。這能為您枯竭的能量池注入活水，針對您磁場中的空缺進行標靶式的填充，讓原本凝滯的運勢重新流轉。",
    "這組數字的排列順序，暗合易經八卦之變。其原理在於每日的『重複共振』。當您頻繁輸入、看到這組數字時，您的氣場會逐漸與這些高頻能量同步，從而達成轉運、招財、避邪的效果。"
]

DIET_TEMPLATES = [
    "【靈性飲食指引】：除了數字調和，內在能量的清理亦至關重要。建議信士這段期間多食**深綠色蔬果（如菠菜、綠花椰菜）**，其木能量能助您疏肝理氣，強化『生氣』貴人場。",
    "【能量飲食建議】：觀您磁場火氣較旺，建議適度補充**根莖類食物（如地瓜、山藥）**，這類屬於『土』屬性的食物能幫助您沉穩能量、固守財庫。飲食宜清淡，避免過多紅肉。",
    "【大師食補方】：欲提升財運天醫能量，建議多攝取**黃色系食物（如玉米、南瓜、黃椒）**。此外，每日晨起飲用一杯溫開水，能啟動體內能量循環，助您事半功倍。"
]

ADVICE_TEMPLATES = [
    "【使用建議】：請將此調和碼設置為您的手機解鎖密碼或提款卡密碼。每日至少『觀想』或『觸碰』此組數字 21 次。心誠則靈，好運自來。",
    "【大師叮嚀】：此碼乃當下機緣所得。建議將其書寫於紅紙上放置於皮夾內。這組數字將成為您的能量錨點，當您感到疲憊時，注視它能助您重新匯聚正磁場。"
]

# --- 2. 核心邏輯 ---
class DigitalIChingPro:
    def __init__(self):
        self.star_config = {
            "天醫(財運)": {"pairs": ["13", "31", "68", "86", "49", "94", "27", "72"], "score": 20},
            "生氣(貴人)": {"pairs": ["14", "41", "67", "76", "39", "93", "28", "82"], "score": 15},
            "延年(事業)": {"pairs": ["19", "91", "78", "87", "34", "43", "26", "62"], "score": 15},
            "伏位(平穩)": {"pairs": ["11", "22", "33", "44", "66", "77", "88", "99"], "score": 10},
            "絕命(凶)": {"pairs": ["12", "21", "69", "96", "48", "84", "37", "73"], "score": -20},
            "五鬼(凶)": {"pairs": ["18", "81", "79", "97", "36", "63", "24", "42"], "score": -20},
            "六煞(凶)": {"pairs": ["16", "61", "47", "74", "38", "83", "29", "92"], "score": -15},
            "禍害(凶)": {"pairs": ["17", "71", "89", "98", "46", "64", "23", "32"], "score": -15}
        }

    def convert_to_nums(self, text):
        converted = ""
        for char in text.upper():
            if char.isdigit(): converted += char
            elif char.isalpha(): converted += f"{ord(char) - ord('A') + 1:02d}"
        return converted

    def analyze(self, nums):
        results, total_score, i = [], 60, 0
        counts = {"Wealth": 0, "Noble": 0, "Career": 0}
        if len(nums) < 2: return results, total_score, counts
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
                if "天醫" in star_name: counts["Wealth"] += 1
                if "生氣" in star_name: counts["Noble"] += 1
                if "延年" in star_name: counts["Career"] += 1
                final_score = base_score * (1.2 if has_five else 1.0) * (0.5 if has_zero else 1.0)
                total_score += final_score
                results.append({"區段": nums[i:next_idx+1], "星號": star_name, "分數": round(final_score, 1)})
            i += 1
        return results, max(0, min(100, round(total_score, 1))), counts

    def get_star_info(self, pair):
        for name, info in self.star_config.items():
            if pair in info["pairs"]: return name, info["score"]
        return "平穩磁場", 0

    def generate_remedy(self, original_nums, star_counts):
        target_len = max(8, len(original_nums))
        if target_len > 12: target_len = 12
        pool_wealth = ["13", "31", "68", "86", "49", "94"]
        pool_noble = ["14", "41", "67", "76", "39", "93"]
        pool_career = ["19", "91", "78", "87", "34", "43"]
        min_energy = min(star_counts, key=star_counts.get)
        primary_pool = pool_wealth if min_energy == "Wealth" else (pool_noble if min_energy == "Noble" else pool_career)
        remedy_code = ""
        while len(remedy_code) < target_len:
            pool = primary_pool if random.random() < 0.6 else (pool_wealth + pool_noble + pool_career)
            remedy_code += random.choice(pool)
        remedy_code = remedy_code[:target_len]
        remedy_details, _, _ = self.analyze(remedy_code)
        explanation = f"{random.choice(REASON_TEMPLATES)}\n\n{random.choice(METHOD_TEMPLATES)}\n\n{random.choice(DIET_TEMPLATES)}\n\n{random.choice(ADVICE_TEMPLATES)}"
        return remedy_code, round(96.5 + (random.random() * 3.3), 1), remedy_details, explanation

# --- 3. 網頁介面 ---
st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮")

if "paid_history" not in st.session_state:
    st.session_state.paid_history = {}

st.sidebar.header("📝 鑑定資料填寫")
selected_type = st.sidebar.selectbox("選擇類型", ["手機號碼", "身分證字號", "LINE ID", "出生日期", "車牌號碼"])
raw_input = st.sidebar.text_input("請輸入欲鑑定之號碼：")

st.sidebar.divider()
admin_key = st.sidebar.text_input("🔑 管理者密鑰", type="password")
ADMIN_PASSWORDS = ["@Daca4131911", "kayhsu1014"] 

# 檢查支付成功 (模擬)
if st.query_params.get("pay") == "success" and raw_input:
    st.session_state.paid_history[raw_input] = datetime.now()

st.title("🔮 數位易經能量鑑定所")

if raw_input:
    engine = DigitalIChingPro()
    clean_nums = engine.convert_to_nums(raw_input)
    details, score, star_counts = engine.analyze(clean_nums)
    
    is_current_paid = False
    if raw_input in st.session_state.paid_history:
        if datetime.now() - st.session_state.paid_history[raw_input] < timedelta(minutes=15):
            is_current_paid = True
            rem_min = 15 - (datetime.now() - st.session_state.paid_history[raw_input]).seconds // 60
        else:
            del st.session_state.paid_history[raw_input]
    
    if is_current_paid:
        st.success(f"✅ 緣分已至，報告已開啟（剩餘免費觀看時間：約 {rem_min} 分鐘）")
        st.subheader("📜 命理師的叮嚀")
        st.metric("原始磁場總評分", f"{score} 分")
        
        with st.expander("📊 原始磁場詳細解析", expanded=True):
            st.table(pd.DataFrame(details))
        
        st.divider()
        st.subheader("🛠️ 專屬能量調和方案（大師親批）")
        remedy_code, r_score, r_details, explanation = engine.generate_remedy(clean_nums, star_counts)
        st.markdown(f"### **【為何需要此數字化解與飲食調整？】**")
        st.write(explanation)
        
        st.divider()
        c1, c2 = st.columns(2)
        c1.info(f"✨ 建議開運化解碼：\n### **{remedy_code}**")
        c2.success(f"📈 化解後預期能級：\n### **{r_score}**")
        
        st.markdown("#### 📋 化解碼磁場佈局報表")
        st.table(pd.DataFrame(r_details))
        
        if st.sidebar.button("🔄 刷新當下感應方案"):
            st.rerun()
    else:
        st.warning("🔒 鑑定報告已被封印")
        st.info(f"📍 **{selected_type}：{raw_input}** 的鑑定數據已演算完畢。")
        st.link_button("💳 支付 1 USD 解鎖鑑定與化解方案", "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
        
        # --- 隱藏解鎖按鈕邏輯：只有密碼正確才會出現 ---
        if admin_key in ADMIN_PASSWORDS:
            st.sidebar.success("✅ 管理者身分確認")
            if st.sidebar.button("🛠️ 權限解鎖 (15min)"):
                st.session_state.paid_history[raw_input] = datetime.now()
                st.rerun()
else:
    st.info("👈 請於左側選單輸入您想鑑定的號碼，開啟命運之門。")

st.caption("命理分析僅供參考，心誠則靈，好運自來。")