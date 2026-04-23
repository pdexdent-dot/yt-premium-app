import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="YT Premium Manager", layout="wide")

# เชื่อมต่อกับ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# ฟังก์ชันดึงข้อมูลใหม่ล่าสุด
def get_data():
    return conn.read(spreadsheet=st.secrets["public_gsheets_url"], ttl=0)

df = get_data()

st.sidebar.title("เมนูการใช้งาน")
app_mode = st.sidebar.selectbox("เลือกหน้าจอ", ["หน้าส่งสลิป (Member)", "Dashboard (Admin)"])

if app_mode == "หน้าส่งสลิป (Member)":
    st.title("📺 ส่งสลิป YouTube Premium")
    
    with st.form("upload_form", clear_on_submit=True):
        name = st.selectbox("เลือกชื่อของคุณ", df['Name'].tolist())
        uploaded_file = st.file_uploader("แนบรูปสลิปการโอนเงิน", type=['png', 'jpg', 'jpeg'])
        submit = st.form_submit_button("ส่งหลักฐาน")
        
        if submit:
            if uploaded_file is not None:
                # อัปเดตสถานะใน DataFrame
                df.loc[df['Name'] == name, 'Status'] = 'รอตรวจสอบ'
                df.loc[df['Name'] == name, 'Last_Paid'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                # บันทึกกลับไปที่ Google Sheets
                conn.update(spreadsheet=st.secrets["public_gsheets_url"], data=df)
                st.success(f"ส่งหลักฐานเรียบร้อยแล้วครับคุณ {name}! Admin กำลังตรวจสอบนะ")
            else:
                st.error("กรุณาแนบรูปสลิปก่อนกดส่งนะครับ")

else:
    st.title("📊 Dashboard สำหรับ Admin")
    
    # ส่วนแสดงตารางข้อมูล
    st.subheader("สถานะการจ่ายเงินปัจจุบัน")
    st.dataframe(df, use_container_width=True)
    
    if st.button("รีเฟรชข้อมูล"):
        st.rerun()
