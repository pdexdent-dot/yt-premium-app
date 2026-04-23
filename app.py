import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="YT Premium Manager", layout="wide")

# เชื่อมต่อกับ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# ฟังก์ชันดึงข้อมูลแบบบังคับให้เป็นข้อความเพื่อป้องกัน Error
def get_data():
    # ดึงข้อมูลและบังคับให้ทุกคอลัมน์เป็น String (ข้อความ) เพื่อลดปัญหา TypeError
    data = conn.read(spreadsheet=st.secrets["public_gsheets_url"], ttl=0)
    return data.astype(str)

df = get_data()

# ล้างค่า 'nan' หรือ 'None' ให้เป็นช่องว่างเพื่อให้ดูสวยงาม
df = df.replace(['nan', 'None', '<NA>'], '')

st.sidebar.title("เมนูการใช้งาน")
app_mode = st.sidebar.selectbox("เลือกหน้าจอ", ["หน้าส่งสลิป (Member)", "Dashboard (Admin)"])

if app_mode == "หน้าส่งสลิป (Member)":
    st.title("📺 ส่งสลิป YouTube Premium")
    
    with st.form("upload_form", clear_on_submit=True):
        # ป้องกันกรณีดึงชื่อมาไม่ได้
        names_list = df['Name'].tolist() if 'Name' in df.columns else []
        name = st.selectbox("เลือกชื่อของคุณ", names_list)
        
        uploaded_file = st.file_uploader("แนบรูปสลิปการโอนเงิน", type=['png', 'jpg', 'jpeg'])
        submit = st.form_submit_button("ส่งหลักฐาน")
        
        if submit:
            if uploaded_file is not None:
                # อัปเดตข้อมูลแบบปลอดภัย
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                # ค้นหาแถวที่ชื่อตรงกันและอัปเดต
                df.loc[df['Name'] == name, 'Status'] = 'รอตรวจสอบ'
                df.loc[df['Name'] == name, 'Last_Paid'] = now_str
                
                # ส่งข้อมูลกลับไปที่ Google Sheets
                try:
                    conn.update(spreadsheet=st.secrets["public_gsheets_url"], data=df)
                    st.success(f"บันทึกข้อมูลเรียบร้อย! ขอบคุณครับคุณ {name}")
                    st.balloons() # เพิ่มความสวยงามเวลาส่งสำเร็จ
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ Sheets: {e}")
            else:
                st.error("กรุณาแนบรูปสลิปก่อนครับ")

else:
    st.title("📊 Dashboard สำหรับ Admin")
    
    # คำนวณสถิติแบบง่าย
    c1, c2 = st.columns(2)
    with c1:
        st.metric("จำนวนสมาชิกทั้งหมด", len(df))
    with c2:
        pending = len(df[df['Status'] == 'รอตรวจสอบ'])
        st.metric("รอตรวจสอบ", pending)

    st.divider()
    st.subheader("ตารางสถานะปัจจุบัน")
    
    # ตกแต่งตารางให้ดูง่ายขึ้น
    st.dataframe(
        df, 
        use_container_width=True,
        column_config={
            "Status": st.column_config.TextColumn("สถานะ"),
            "Last_Paid": st.column_config.TextColumn("จ่ายล่าสุดเมื่อ")
        }
    )
    
    if st.button("🔄 รีเฟรชข้อมูล"):
        st.rerun()
