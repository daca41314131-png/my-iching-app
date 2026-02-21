import streamlit as st
import re
import random
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 極致專業介面與 SEO 設定 (這部分會被完全隱藏) ---
# 我們將標籤內容放入一個 HTML 區塊，並加上更強力的 CSS 隱藏規則
CLEAN_INTERFACE_AND_SEO = """
<style>
    /* 1. 隱藏所有 Streamlit 標誌與按鈕 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    button[title="View source"] {display:none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    
    /* 2. 清除側邊欄多餘的裝飾 */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* 3. 調整字體與整體美感 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans TC', sans-serif;
    }
</style>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "數位易經能量鑑定所",
  "description": "專業數位磁場鑑定，透過易經八星演算提供專屬能量調和方案。",
  "areaServed": "TW",
  "provider": {
    "@type": "LocalBusiness",
    "name": "數位易經能量鑑定所",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Taipei"
    }
  }
}
</script>
"""

# 必須是 Streamlit 的第一個指令
st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")

# 關鍵：注入 CSS 與 SEO，這絕對不會在畫面上顯示任何文字代碼
st.markdown(CLEAN_INTERFACE_AND_SEO, unsafe_allow_html=True)

# --- 2. 核心邏輯類別 (修正了截圖中的解析錯誤) ---
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
        # 這是為了修復截圖中的 ValueError，確保回傳變數正確
        target_len = max(8, len(original_nums))
        if target_len > 12: target_len = 12
        pool = ["13", "31", "68", "86", "49", "94", "19", "91", "14", "41"]
        remedy_code = "".join(random.choices(pool, k=target_len//2))[:target_len]
        remedy_details, _, _ = self.analyze(remedy_code)
        explanation = "根據當下磁場感應，此數字能有效中和原本的負面震盪，建議配合清淡飲食..."
        return remedy_code, 98.5, remedy_details, explanation

# --- 3. 專業介面實作 ---
if "paid_history" not in st.session_state:
    st.session_state.paid_history = {}

st.sidebar.header("📝 鑑定資料填寫")
selected_type = st.sidebar.selectbox("選擇類型", ["手機號碼", "車牌號碼", "出生日期", "LINE ID"])
raw_input = st.sidebar.text_input("請輸入欲鑑定之號碼：", placeholder="例如：0912345678")

# 管理者區塊：將標題設為空字串，且不顯示說明文字，隱藏得更深
admin_key = st.sidebar.text_input("", type="password", placeholder="---")

ADMIN_PASSWORDS = ["master888", "admin999"] 

st.title("🔮 數位易經能量鑑定所")

if raw_input:
    engine = DigitalIChingPro()
    clean_nums = engine.convert_to_nums(raw_input)
    details, score, star_counts = engine.analyze(clean_nums)
    
    # 檢查是否已支付 (15分鐘邏輯)
    is_paid = False
    if raw_input in st.session_state.paid_history:
        if datetime.now() - st.session_state.paid_history[raw_input] < timedelta(minutes=15):
            is_paid = True

    if is_paid:
        st.success("✅ 緣分已至，報告已開啟")
        st.metric("原始磁場總評分", f"{score} 分")
        st.table(pd.DataFrame(details))
        
        st.divider()
        st.subheader("🛠️ 專屬能量調和方案")
        # 修正：確保接收 4 個變數
        r_code, r_score, r_details, r_expl = engine.generate_remedy(clean_nums, star_counts)
        st.write(r_expl)
        st.info(f"建議開運碼：{r_code} (預期能級：{r_score})")
    else:
        st.warning("🔒 鑑定報告已被封印")
        st.link_button("💳 支付 1 USD 解鎖鑑定與化解方案", "https://paypal.me/yourlink")
        
        # 只有輸入正確密鑰才會顯示這個小按鈕
        if admin_key in ADMIN_PASSWORDS:
            if st.sidebar.button("管理者解鎖"):
                st.session_state.paid_history[raw_input] = datetime.now()
                st.rerun()
else:
    st.info("👈 請於左側選單輸入您的號碼。")