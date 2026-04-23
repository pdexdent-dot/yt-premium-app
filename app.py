import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="YouTube Premium Dashboard", layout="wide")

# เชื่อมต่อกับ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    # เปลี่ยนลิงก์ใน Secrets ให้เป็นลิงก์ของ Sheet ที่เก็บคำตอบจาก Form
    data = conn.read(spreadsheet=st.secrets["public_gsheets_url"], ttl=0)
    return data.astype(str)

try:
    df = get_data()
    df = df.replace(['nan', 'None', '<NA>'], '')

    st.title("📊 YouTube Premium Dashboard")
    st.info("💡 สมาชิกกรุณาส่งสลิปผ่าน Google Form ที่ Admin แจ้งในกลุ่มนะครับ")

    # ส่วนสรุปจำนวน
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("สมาชิกทั้งหมด", len(df))
    with c2:
        # สมมติว่ามีคอลัมน์ชื่อ 'สถานะ' ใน Sheet
        if 'สถานะ' in df.columns:
            paid = len(df[df['สถานะ'] == 'จ่ายแล้ว'])
            st.metric("จ่ายแล้ว", paid)
    
    st.divider()
    
    # แสดงตารางรายชื่อ
    st.subheader("📋 ตรวจสอบสถานะการชำระเงิน")
    st.dataframe(df, use_container_width=True)

    if st.button("🔄 อัปเดตข้อมูลล่าสุด"):
        st.rerun()

except Exception as e:
    st.error(f"ไม่สามารถดึงข้อมูลได้: {e}")
    st.info("กรุณาตรวจสอบว่าได้ตั้งค่าลิงก์ใน Secrets ถูกต้องและเปิดแชร์เป็น Anyone with the link หรือยัง")
