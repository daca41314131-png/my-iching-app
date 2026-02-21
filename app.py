import streamlit as st
import re

class DigitalIChingPro:
    def __init__(self):
        # 八星對應表與基礎分數 (吉星正分, 凶星負分)
        # 能量等級：13(1級), 68(2級), 49(3級), 27(4級)
        self.star_config = {
            "天醫(吉)": {"pairs": ["13", "31", "68", "86", "49", "94", "27", "72"], "score": 20},
            "生氣(吉)": {"pairs": ["14", "41", "67", "76", "39", "93", "28", "82"], "score": 15},
            "延年(吉)": {"pairs": ["19", "91", "78", "87", "34", "43", "26", "62"], "score": 15},
            "伏位(吉)": {"pairs": ["11", "22", "33", "44", "66", "77", "88", "99"], "score": 10},
            "絕命(凶)": {"pairs": ["12", "21", "69", "96", "48", "84", "37", "73"], "score": -20},
            "五鬼(凶)": {"pairs": ["18", "81", "79", "97", "36", "63", "24", "42"], "score": -20},
            "六煞(凶)": {"pairs": ["16", "61", "47", "74", "38", "83", "29", "92"], "score": -15},
            "禍害(凶)": {"pairs": ["17", "71", "89", "98", "46", "64", "23", "32"], "score": -15}
        }

    def analyze(self, nums):
        results = []
        total_score = 60  # 基礎分
        i = 0
        while i < len(nums) - 1:
            current = nums[i]
            if current in '05':
                i += 1
                continue

            next_idx = i + 1
            has_zero, has_five = False, False
            while next_idx < len(nums) and nums[next_idx] in '05':
                if nums[next_idx] == '0': has_zero = True
                if nums[next_idx] == '5': has_five = True
                next_idx += 1
            
            if next_idx < len(nums):
                pair = current + nums[next_idx]
                star_name, base_score = self.get_star_info(pair)
                
                # 權重修正邏輯
                final_pair_score = base_score
                note = "正常"
                
                if has_five: # 5 強化能量
                    final_pair_score *= 1.2
                    note = "🔥 能量凸顯強化"
                if has_zero: # 0 隱藏/削弱能量
                    final_pair_score *= 0.5
                    note = "☁️ 能量隱藏削弱"
                
                total_score += final_pair_score
                results.append({
                    "區段": nums[i:next_idx+1],
                    "星號": star_name,
                    "調整分": round(final_pair_score, 1),
                    "備註": note
                })
            i += 1
        
        # 分數限制作業
        total_score = max(0, min(100, total_score))
        return results, round(total_score, 1)

    def get_star_info(self, pair):
        for name, info in self.star_config.items():
            if pair in info["pairs"]:
                return name, info["score"]
        return "未知", 0

# --- Streamlit 網頁介面 ---
st.set_page_config(page_title="數字易經能量分析", page_icon="🔮")

st.title("🔮 數字易經能量分析系統")
st.markdown("輸入你的手機號碼或身分證字號，分析數位磁場吉凶。")

with st.sidebar:
    st.header("系統說明")
    st.info("本系統根據數字易經八星邏輯開發，並針對數字 0 與 5 進行了能量權重修正。")
    st.write("🟢 吉星：天醫、生氣、延年、伏位")
    st.write("🔴 凶星：絕命、五鬼、六煞、禍害")

input_number = st.text_input("請輸入號碼：", placeholder="例如：0912345678")

if input_number:
    clean_nums = re.sub(r'\D', '', input_number)
    if len(clean_nums) < 3:
        st.warning("請輸入較長的數字以利分析。")
    else:
        engine = DigitalIChingPro()
        details, score = engine.analyze(clean_nums)
        
        # 顯示總分
        col1, col2 = st.columns(2)
        with col1:
            st.metric("能量總評分", f"{score} 分")
        with col2:
            if score >= 80: st.success("磁場極佳：大吉")
            elif score >= 60: st.info("磁場平穩：中吉")
            else: st.error("磁場混亂：建議調整")

        # 顯示分析表格
        st.subheader("📊 詳細磁場分析")
        st.table(details)

        # 結論建議
        st.subheader("💡 命理建議")
        if "五鬼(凶)" in str(details):
            st.write("- 號碼中帶有 **五鬼**，需注意情緒起伏與夜間睡眠，雖然才華橫溢但較不安定。")
        if "天醫(吉)" in str(details):
            st.write("- 號碼中帶有 **天醫**，有利財運與正緣，請好好把握賺錢機會。")
        if score < 50:
            st.write("- 整體分數較低，代表號碼磁場內耗較大，容易勞而獲少。")

st.caption("免責聲明：本分析僅供娛樂參考，生活幸福仍需靠自身努力。")
