import streamlit as st
import re
import random
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 極致專業介面與 SEO 設定 (完全隱藏在背景) ---
CLEAN_MARKUP = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    button[title="View source"] {display:none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    /* 隱藏側邊欄頂部裝飾 */
    [data-testid="stSidebarNav"] {display: none;}
</style>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "數位易經能量鑑定所",
  "description": "專業數位磁場鑑定與能量調和方案",
  "areaServed": "TW"
}
</script>
"""

st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")
# 注入隱藏標籤
st.markdown(CLEAN_MARKUP, unsafe_allow_html=True)

# --- 2. 大師解說庫 (找回您的專業度) ---
REASONS = [
    "信士可知，數字乃宇宙能量之顯化。您原始號碼中的氣場如同先天之命，雖有定數，卻非不可改之侷限。目前的能量分佈顯示，某些負向磁場正潛移默化地干擾您的氣運，導致財氣不聚、元神渙散。",
    "在易經數位磁場中，每一個組合都是一個微型能量場。您目前的組合中，正負能量比例失衡，這代表您的『共振頻率』偏離了繁榮的軌道。這就像是一個人穿了不合腳的鞋，走得再快也會感到疲憊。"
]

DIETS = [
    "【靈性能量指引】：除了數字調和，內在能量的清理亦至關重要。建議信士這段期間多食**深綠色蔬果（如菠菜、綠花椰菜）**，其木能量能助您疏肝理氣，強化『生氣』貴人場。",
    "【能量飲食建議】：觀您磁場火氣較旺，建議補充**根莖類食物（如地瓜、山藥）**，這類屬於『土』屬性的食物能幫助您沉穩能量、固守財庫。飲食宜清淡，避免過多紅肉。"
]

ADVICES = [
    "【開運法門】：請將此調和碼設置為手機解鎖密碼。每日至少『觀想』此組數字 21 次。心誠則靈，好運自來。",
    "【大師叮嚀】：此碼乃當下機緣所得。建議將其書寫於紅紙上放置於皮夾內，它將成為您的能量錨點，助您重新匯聚正磁場。"
]

# --- 3. 核心運算引擎 ---
class DigitalIChingPro:
    def __init__(self):
        self.star_config = {
            "天醫(財運)": {"pairs": ["13", "31", "68", "86", "49", "94", "27", "72"], "score": 20},
            "生氣(貴人)": {"pairs": ["14", "41", "67", "76", "39", "93", "28", "82"], "score": 15},
            "延年(事業)": {"pairs": ["19", "91", "78", "87", "34", "43", "26", "62"], "score": 15},
            "絕命(凶)": {"pairs": ["12", "21", "69", "96", "48", "84", "37", "73"], "score": -20},
            "五鬼(凶)": {"pairs": ["18", "81", "79", "97", "36", "63", "24", "42"], "score": -20},
            "六煞(凶)": {"pairs": ["16", "61", "47", "74", "38", "83", "29", "92"], "score": -15},
            "禍害(凶)": {"pairs": ["17", "71", "89", "98", "46", "64", "23", "32"], "score": -15}
        }

    def convert_to_nums(self, text):
        return "".join(re.findall(r'\d+', text))

    def analyze(self, nums):
        results, total_score, i = [], 60, 0
        if len(nums) < 2: return results, total_score
        while i < len(nums) - 1:
            pair = nums[i:i+2]
            star_name = "平穩磁場"; star_score = 0
            for name, info in self.star_config.items():
                if pair in info["pairs"]: star_name = name; star_score = info["score"]; break
            total_score += star_score
            results.append({"區段": pair, "星號": star_name, "分數": star_score})
            i += 1
        return results, max(0, min(100, total_score))

    def generate_dynamic_remedy(self, original_nums):
        # 移除固定種子，確保每次化解碼都不同
        target_len = 8
        pool = ["13", "31", "68", "86", "41", "14", "19", "91"]
        remedy_code = "".join(random.choices(pool, k=4))
        remedy_details, _ = self.analyze(remedy_code)
        
        # 拼接長篇專業解說
        explanation = f"{random.choice(REASONS)}\n\n{random.choice(DIETS)}\n\n{random.choice(ADVICES)}"
        
        # 回傳 4 個變數，徹底解決 ValueError
        return remedy_code, round(97.0 + random.random()*2, 1), remedy_details, explanation

# --- 4. 介面呈現 ---
if "paid_history" not in st.session_state:
    st.session_state.paid_history = {}

st.sidebar.header("📝 鑑定資料填寫")
selected_type = st.sidebar.selectbox("選擇類型", ["手機號碼", "車牌號碼", "出生日期", "LINE ID"])
raw_input = st.sidebar.text_input("請輸入欲鑑定之號碼：", placeholder="例如：0912345678")

# 完全移除管理者欄位與按鈕，讓介面乾淨無暇

st.title("🔮 數位易經能量鑑定所")

if raw_input:
    engine = DigitalIChingPro()
    clean_nums = engine.convert_to_nums(raw_input)
    details, score = engine.analyze(clean_nums)
    
    # 支付檢查
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
        # 修正變數接收，避免報錯
        r_code, r_score, r_details, r_expl = engine.generate_dynamic_remedy(clean_nums)
        
        st.markdown("### **【大師親批：為何需要此化解？】**")
        st.write(r_expl)
        
        st.info(f"✨ 建議開運化解碼：**{r_code}** (預期能級：{r_score}分)")
        st.table(pd.DataFrame(r_details))
        
        if st.sidebar.button("🔄 刷新當下能量感應"):
            st.rerun()
    else:
        st.warning("🔒 鑑定報告已被封印")
        st.info(f"📍 **{selected_type}：{raw_input}** 的數據已演算完畢，請解鎖查閱詳細大師報告。")
        st.link_button("💳 支付 1 USD 解鎖鑑定與化解方案", "https://paypal.me/yourlink")
else:
    st.info("👈 請於左側選單輸入您的號碼，開啟命運之門。")