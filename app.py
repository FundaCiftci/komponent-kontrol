import streamlit as st
import pandas as pd
import random
from st_aggrid import AgGrid, GridOptionsBuilder

def speak_text(text):
    unique = random.randint(0, 1000000)
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{text} {unique}");
        msg.text = "{text}";
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# Ayakkabı ve istisna listeleri (senin önceki kodundakiyle aynı, buraya tekrar yazabilirim istersen)
ayakkabi_modelleri = [...]  # Kısaltıldı
istisnalar = [...]          # Kısaltıldı

st.set_page_config(page_title="Komponent Kontrol", layout="wide")
st.title("👟 Komponent Kontrol Uygulaması")

uploaded_file = st.file_uploader("📁 Excel dosyanı yükle (.xlsx)", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    selected_df = None

    for sheet_name, df in all_sheets.items():
        if all(k in df.columns for k in ['TemaTakipNo', 'KomponentId', 'ModelTanim']):
            selected_df = df.copy()
            break

    if selected_df is not None:
        df = selected_df
        df['Renk'] = ''

        df.loc[(df['KomponentId'] > 0) & (~df['ModelTanim'].isin(istisnalar)), 'Renk'] = 'Sarı'
        df.loc[df['ModelTanim'].isin(ayakkabi_modelleri), 'Renk'] = 'Sarı'

        kontrol_edilecek = df[df['Renk'] == 'Sarı'].copy()
        kontrol_edilenler = pd.DataFrame(columns=df.columns)

        st.success(f"Sayfa bulundu: {sheet_name}")
        ttn_input = st.text_input("🎯 TemaTakipNo gir (sadece numara):")

        if ttn_input:
            ttn_input = str(ttn_input).strip()
            mask = (df['TemaTakipNo'].astype(str) == ttn_input)

            if mask.any():
                kontrol_var = (
                    ((df.loc[mask, 'KomponentId'] > 0) & (~df.loc[mask, 'ModelTanim'].isin(istisnalar))).any()
                    or (df.loc[mask, 'ModelTanim'].isin(ayakkabi_modelleri)).any()
                )

                if kontrol_var:
                    speak_text("Kontrol et")
                    df.loc[mask & (df['Renk'] == 'Sarı'), 'Renk'] = 'Kırmızı'

                kontrol_edilenler = df[df['Renk'] == 'Kırmızı']
            else:
                st.error("Bu TemaTakipNo bulunamadı!")

        # 🎨 Görseller
        st.subheader("🟡 Kontrol Edilecek Satırlar")
        AgGrid(kontrol_edilecek, height=300, theme="balham")

        st.subheader("🔴 Kontrol Edilen (Kırmızıya Dönüşenler)")
        AgGrid(df[df['Renk'] == 'Kırmızı'], height=300, theme="balham")

    else:
        st.error("TemaTakipNo, KomponentId ve ModelTanim sütunları eksik.")
