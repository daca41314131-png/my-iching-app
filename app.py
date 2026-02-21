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
        "unlock_benefit": "支付解鎖後，大師將為您提供：\n- 原始磁場詳細鑑定 (八星吉凶)\n- 字母轉譯深度解析\n- **命理師專屬化解建議與磁場調和碼報表**",
        "pay_btn": "💳 支付 1 USD 請大師指點迷津",
        "paid_success": "✅ 緣分已至，報告已為您開啟",
        "detail_table": "📊 原始磁場分佈解析",
        "master_voice_title": "📜 命理師的叮嚀",
        "solution_title": "🛠️ 專屬能量調和方案",
        "remedy_code": "✨ 建議開運化解碼：",
        "remedy_score": "📈 化解後預期能級：",
        "remedy_table": "📋 化解碼磁場佈局報表",
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
        counts = {"Wealth": 0, "Noble": 0, "Career": 0}
        
        # 確保輸入至少有兩個數字
        if len(nums) < 2:
            return results, total_score, counts

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
                results.append({"Section": nums[i:next_idx+1], "Star": star_name, "Score": round(final_score, 1)})
            i += 1
        return results, max(0, min(100, round(total_score, 1))), counts

    def get_star_info(self, pair):
        for name, info in self.star_config.items():
            if pair in info["pairs"]: return name, info["score"]
        return "平穩磁場", 0

    def generate_dynamic_remedy(self, original_nums, star_counts):
        # 使用原號碼作為隨機種子
        random.seed(original_nums)
        
        # 修正長度邏輯，確保足夠長度進行分析
        target_len = max(8, len(original_nums))
        if target_len > 12: target_len = 12
        
        pool_wealth = ["13", "31", "68", "86", "49", "94"]
        pool_noble = ["14", "41", "67", "76", "39", "93"]
        pool_career = ["19", "91", "78", "87", "34", "43"]
        
        min_energy = min(star_counts, key=star_counts.get)
        if min_energy == "Wealth":
            primary_pool, reason = pool_wealth, "加強財庫天醫磁場"
        elif min_energy == "Noble":
            primary_pool, reason = pool_noble, "啟動貴人生氣磁場"
        else:
            primary_pool, reason = pool_career, "固守事業延年磁場"
            
        remedy_code = ""
        # 確保 remedy_code 是偶數長度且由吉星對組成
        while len(remedy_code) < target_len:
            current_pool = primary_pool if random.random() < 0.7 else (pool_wealth + pool_noble + pool_career)
            remedy_code += random.choice(current_pool)
        
        # 截斷並確保至少有 6 碼
        remedy_code = remedy_code[:target_len]
        if len(remedy_code) % 2 != 0: remedy_code += random.choice("12346789")
        
        # 呼叫分析
        remedy_details, _, _ = self.analyze(remedy_code)
        
        final_r_score = round(96.5 + (random.random() * 3.3), 1)
        return remedy_code, final_r_score, remedy_details, reason

# --- 4. 網頁介面實作 ---
st.set_page_config(page_title="數位易經鑑定所", page_icon="🔮")
t = LANGUAGES["繁體中文"]

is_paid = st.query_params.get("pay") == "success"

st.title(t["title"])
raw_input = st.text_input(t["input_label"], placeholder="例如：0912345678")

if raw_input:
    engine = DigitalIChingPro()
    clean_nums = engine.convert_letters(raw_input)
    
    # 執行原始號碼分析
    details, score, star_counts = engine.analyze(clean_nums)
    
    st.divider()
    
    if is_paid:
        st.success(t["paid_success"])
        st.subheader(t["master_voice_title"])
        st.write(f"> 「信士您好，觀您所測之號碼 `{raw_input}`，其數位磁場中蘊含之能量與您氣運息息相關。」")
        
        st.metric(t["score_label"], f"{score} 分")
        
        if score < 60:
            st.error("❗ 此號碼磁場凶星盤據，易致財散人乏、波折重重。")
        elif score < 85:
            st.warning("⚠️ 能量尚可，然吉星力道不足，事業與財氣仍有上升空間。")
        else:
            st.success("🌟 此乃吉數！正磁場環繞，貴人相助，利於穩健發展。")

        with st.expander(t["detail_table"], expanded=True):
            if details:
                df_orig = pd.DataFrame(details).rename(columns={"Section": t["col_section"], "Star": t["col_star"], "Score": t["col_score"]})
                st.table(df_orig)
            else:
                st.write("號碼長度不足，無法生成磁場對比。")
        
        # --- 專業化解方案 (此處已加入錯誤防護) ---
        st.divider()
        st.subheader(t["solution_title"])
        
        try:
            remedy_code, r_score, r_details, reason = engine.generate_dynamic_remedy(clean_nums, star_counts)
            
            st.write(f"""
            **為何需要此化解方案？**
            宇宙萬物皆為能量共振。大師觀測您原號碼中 **{reason}** 之氣明顯不足，故特別演算此對沖陣法。
            """)
            
            col1, col2 = st.columns(2)
            col1.info(f"{t['remedy_code']}\n### **{remedy_code}**")
            col2.success(f"{t['remedy_score']}\n### **{r_score}**")
            
            st.markdown(f"#### {t['remedy_table']}")
            if r_details:
                df_rem = pd.DataFrame(r_details).rename(columns={"Section": t["col_section"], "Star": t["col_star"], "Score": t["col_score"]})
                st.table(df_rem)
            else:
                st.write("化解磁場計算中...")
        except Exception as e:
            st.error(f"能量調和計算暫時中斷，請重試。錯誤資訊: {str(e)}")
        
        if st.button("🔄 重新鑑定新號碼"):
            st.query_params.clear()
            st.rerun()
    else:
        # 付費牆邏輯
        st.warning(t["lock_msg"])
        st.info("📍 鑑定數據已演算完畢。請支付 1 USD，由大師為您親自揭開命運密碼。")
        st.link_button(t["pay_btn"], "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
        
        if st.sidebar.button("🛠️ 測試模式：直接解鎖"):
            st.query_params["pay"] = "success"
            st.rerun()

st.caption(t["footer"])