import streamlit as st
import re
import requests
import random
import pandas as pd

# --- 1. 多國語言與介面文字 ---
LANGUAGES = {
    "繁體中文": {
        "title": "🔮 數位易經能量鑑定所",
        "input_label": "請輸入欲鑑定之數字組合：",
        "type_options": ["手機號碼", "身分證字號", "LINE ID", "出生日期 (YYYYMMDD)", "車牌號碼"],
        "score_label": "原始磁場總評分",
        "lock_msg": "🔒 鑑定報告已被封印",
        "unlock_benefit": "此號碼尚未解鎖，支付 1 USD 即可查閱：\n- 專屬八星吉凶詳細鑑定\n- 字母/日期轉譯深度解析\n- **命理師專屬化解建議與調和碼報表**",
        "pay_btn": "💳 支付 1 USD 解鎖此號碼",
        "paid_success": "✅ 緣分已至，該號碼報告已開啟",
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
                results.append({"Section": nums[i:next_idx+1], "Star": star_name, "Score": round(final_score, 1)})
            i += 1
        return results, max(0, min(100, round(total_score, 1))), counts

    def get_star_info(self, pair):
        for name, info in self.star_config.items():
            if pair in info["pairs"]: return name, info["score"]
        return "平穩磁場", 0

    def generate_remedy(self, original_nums, star_counts):
        random.seed(original_nums)
        target_len = max(8, len(original_nums))
        if target_len > 12: target_len = 12
        pool_wealth = ["13", "31", "68", "86", "49", "94"]
        pool_noble = ["14", "41", "67", "76", "39", "93"]
        pool_career = ["19", "91", "78", "87", "34", "43"]
        min_energy = min(star_counts, key=star_counts.get)
        reason = "加強財庫天醫磁場" if min_energy == "Wealth" else ("啟動貴人生氣磁場" if min_energy == "Noble" else "固守事業延年磁場")
        primary_pool = pool_wealth if min_energy == "Wealth" else (pool_noble if min_energy == "Noble" else pool_career)
        remedy_code = ""
        while len(remedy_code) < target_len:
            pool = primary_pool if random.random() < 0.7 else (pool_wealth + pool_noble + pool_career)
            remedy_code += random.choice(pool)
        remedy_code = remedy_code[:target_len]
        remedy_details, _, _ = self.analyze(remedy_code)
        return remedy_code, round(96.5 + (random.random() * 3.3), 1), remedy_details, reason

# --- 3. 網頁介面實作 ---
st.set_page_config(page_title="數位易經鑑定所", page_icon="🔮")
t = LANGUAGES["繁體中文"]

# 用於儲存本對話 session 中已付費的號碼
if "paid_numbers" not in st.session_state:
    st.session_state.paid_numbers = set()

# 側邊欄設定
st.sidebar.header("📝 鑑定資料填寫")
selected_type = st.sidebar.selectbox("選擇類型", t["type_options"])
raw_input = st.sidebar.text_input(t["input_label"], placeholder="請輸入...")

# --- 管理者權限設定 ---
st.sidebar.divider()
admin_key = st.sidebar.text_input("🔑 管理者密鑰 (解鎖用)", type="password")

# 這裡設定兩個管理者的獨立密碼
ADMIN_PASSWORDS = ["@Daca4131911", "kayhsu1014"] 

# 檢查 PayPal 支付成功跳轉
if st.query_params.get("pay") == "success" and raw_input:
    st.session_state.paid_numbers.add(raw_input)

st.title(t["title"])

if raw_input:
    engine = DigitalIChingPro()
    clean_nums = engine.convert_to_nums(raw_input)
    details, score, star_counts = engine.analyze(clean_nums)
    is_current_paid = raw_input in st.session_state.paid_numbers
    
    if is_current_paid:
        st.success(t["paid_success"])
        st.subheader(t["master_voice_title"])
        st.write(f"> 「信士您好，觀您所測之{selected_type} `{raw_input}`，其能量與您息息相關。」")
        st.metric(t["score_label"], f"{score} 分")
        
        if score < 60: st.error("❗ 此號碼凶星壓制，易致事倍功半、波折重重。")
        elif score < 85: st.warning("⚠️ 能量尚屬平穩，然吉星微弱，仍有提升空間。")
        else: st.success("🌟 此乃上乘之數！正磁場環繞，貴人相助，利於發展。")

        with st.expander(t["detail_table"], expanded=True):
            if details:
                df_orig = pd.DataFrame(details).rename(columns={"Section": t["col_section"], "Star": t["col_star"], "Score": t["col_score"]})
                st.table(df_orig)
        
        st.divider()
        st.subheader(t["solution_title"])
        remedy_code, r_score, r_details, reason = engine.generate_remedy(clean_nums, star_counts)
        st.write(f"**為何需要此方案？**\n大師觀測您原號碼中 **{reason}** 之氣不足，故演算此對沖陣法補強。")
        c1, c2 = st.columns(2)
        c1.info(f"{t['remedy_code']}\n### **{remedy_code}**")
        c2.success(f"{t['remedy_score']}\n### **{r_score}**")
        
        st.markdown(f"#### {t['remedy_table']}")
        if r_details:
            df_rem = pd.DataFrame(r_details).rename(columns={"Section": t["col_section"], "Star": t["col_star"], "Score": t["col_score"]})
            st.table(df_rem)

        if st.sidebar.button("🔄 鑑定下一個新號碼"):
            st.query_params.clear()
            st.rerun()
    else:
        st.warning(t["lock_msg"])
        st.info(f"📍 **{selected_type}：{raw_input}** 的鑑定數據已演算完畢。")
        st.write(t["unlock_benefit"])
        st.link_button(t["pay_btn"], "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
        
        # --- 管理者權限檢查邏輯 ---
        if admin_key in ADMIN_PASSWORDS:
            st.sidebar.success("✅ 管理者身分確認")
            if st.sidebar.button("🛠️ 權限解鎖：當前號碼"):
                st.session_state.paid_numbers.add(raw_input)
                st.rerun()
        elif admin_key != "":
            st.sidebar.error("❌ 密鑰無效")

else:
    st.info("👈 請於左側選單輸入您想鑑定的號碼、生日或車牌。")

st.caption(t["footer"])