import streamlit as st
import re
import requests
import random
import pandas as pd

# --- 1. 多國語言字典設定 ---
LANGUAGES = {
    "繁體中文": {
        "title": "🔮 數位易經能量鑑定所",
        "input_label": "請輸入欲鑑定之號碼 (手機、身分證、LINE ID)：",
        "score_label": "原始磁場總評分",
        "lock_msg": "🔒 運勢報告已被封印",
        "unlock_benefit": "支付解鎖後，大師將為您提供：\n- 原始磁場詳細鑑定 (八星吉凶)\n- 字母轉譯深度解析\n- **命理師專屬化解建議與磁場調和碼**",
        "pay_btn": "💳 支付 1 USD 請大師指點迷津",
        "paid_success": "✅ 緣分已至，報告已為您開啟",
        "detail_table": "📊 原始磁場分佈解析",
        "master_voice_title": "📜 命理師的叮嚀",
        "solution_title": "🛠️ 專屬能量調和方案",
        "remedy_code": "✨ 建議開運化解碼：",
        "remedy_score": "📈 化解後預期能級：",
        "remedy_table": "📋 化解碼磁場佈局",
        "footer": "命理分析僅供參考，心誠則靈，好運自來。",
        "col_section": "區段", "col_star": "星號", "col_score": "分數"
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

    def convert_letters(self, text):
        converted = ""
        for char in text.upper():
            if char.isdigit(): converted += char
            elif char.isalpha(): converted += f"{ord(char) - ord('A') + 1:02d}"
        return converted

    def analyze(self, nums):
        results, total_score, i = [], 60, 0
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
                final_score = base_score * (1.2 if has_five else 1.0) * (0.5 if has_zero else 1.0)
                total_score += final_score
                results.append({"Section": nums[i:next_idx+1], "Star": star_name, "Score": round(final_score, 1)})
            i += 1
        return results, max(0, min(100, round(total_score, 1)))

    def get_star_info(self, pair):
        for name, info in self.star_config.items():
            if pair in info["pairs"]: return name, info["score"]
        return "平穩磁場", 0

    def generate_dynamic_remedy(self, original_nums):
        length = max(6, min(12, len(original_nums)))
        best_pairs = ["13", "31", "68", "86", "49", "94", "14", "41", "19", "91"]
        remedy_code = "".join(random.choice(best_pairs) for _ in range(length//2 + 1))[:length]
        remedy_details, _ = self.analyze(remedy_code)
        return remedy_code, round(96 + random.uniform(0, 3.5), 1), remedy_details

# --- 3. 網頁介面 ---
st.set_page_config(page_title="數位易經", page_icon="🔮")
t = LANGUAGES["繁體中文"]
is_paid = st.query_params.get("pay") == "success"

st.title(t["title"])
raw_input = st.text_input(t["input_label"], placeholder="例如：0912345678")

if raw_input:
    engine = DigitalIChingPro()
    clean_nums = engine.convert_letters(raw_input)
    details, score = engine.analyze(clean_nums)
    
    st.divider()
    
    if is_paid:
        st.success(t["paid_success"])
        
        # 命理師的開場白
        st.subheader(t["master_voice_title"])
        st.write(f"> 「信士您好，觀您所測之號碼 `{raw_input}`，其數位磁場中蘊含之能量與您息息相關。」")
        
        st.metric(t["score_label"], f"{score} 分")
        
        # 針對分數給予算命師風格的評語
        if score < 60:
            st.error("❗ 此號碼磁場較為駁雜，凶星能量壓制了正磁場，易致事倍功半、波折重重。")
        elif score < 85:
            st.warning("⚠️ 能量尚屬平穩，然貴人星微弱，事業與財氣仍有進步空間。")
        else:
            st.success("🌟 此乃上乘之數！正磁場環繞，利於開疆闢土，守成亦佳。")

        with st.expander(t["detail_table"]):
            st.table(pd.DataFrame(details).rename(columns={"Section": t["col_section"], "Star": t["col_star"], "Score": t["col_score"]}))
        
        # --- 算命師解釋化解碼的原因 ---
        st.divider()
        st.subheader(t["solution_title"])
        
        st.write("""
        **為何要使用化解碼？**
        宇宙萬物皆為能量波動，數字亦然。若原始號碼含有「五鬼」、「絕命」等負面磁場，就像是家中的門窗漏風，財氣不聚、元神受損。
        
        大師為您演算的這組**『開運化解碼』**，其原理並非取代原號碼，而是透過**「同頻對沖」**與**「能量補正」**的方式，將其設置為您的通訊軟體密碼、解鎖碼或社交暱稱。透過每日重複的使用與共振，能慢慢引動周圍磁場往吉星靠攏。
        """)
        
        r_code, r_score, r_details = engine.generate_dynamic_remedy(clean_nums)
        col1, col2 = st.columns(2)
        col1.info(f"{t['remedy_code']}\n### **{r_code}**")
        col2.success(f"{t['remedy_score']}\n### **{r_score}**")
        
        st.markdown(f"#### {t['remedy_table']}")
        st.table(pd.DataFrame(r_details).rename(columns={"Section": t["col_section"], "Star": t["col_star"], "Score": t["col_score"]}))
        
    else:
        st.warning(t["lock_msg"])
        st.info("📍 數據分析已封印，請支付 1 USD，由大師為您親自揭開命運密碼。")
        st.write(t["unlock_benefit"])
        st.link_button(t["pay_btn"], "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
        
        if st.sidebar.button("🛠️ 開發測試：直接揭開天機"):
            st.query_params["pay"] = "success"
            st.rerun()

st.caption(t["footer"])