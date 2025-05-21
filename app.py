import streamlit as st
import pandas as pd
import random

# Her seferde sesli uyarı tetiklesin
def speak_text(text):
    unique = random.randint(0, 1000000)
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{text} {unique}");
        msg.text = "{text}";
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# Ayakkabı grubu - ModelTanim için eşleşme listesi
ayakkabi_modelleri = [
    "SANDALS", "Slippers", "Beach Slippers", "Shoes", "Beach Shoes", "Home Shoes", "Beach Sandals",
    "HOME SLIPPERS", "Boots", "Rain Boots", "ТУФЛИ", "ОБУВЬ ПЛЯЖНАЯ", "САНДАЛИИ", "ТАПОЧКИ",
    "КЕДЫ", "ДОМАШНЯЯ ОБУВЬ", "ЭСПАДРИЛЬИ", "Home Boots"
]

st.set_page_config(page_title="Komponent Kontrol", layout="wide")
st.title("🔍 Komponent Kontrol Uygulaması")

uploaded_file = st.file_uploader("Excel dosyanı yükle (.xlsx)", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    selected_df = None

    for sheet_name, df in all_sheets.items():
        if 'TemaTakipNo' in df.columns and 'KomponentId' in df.columns and 'ModelTanim' in df.columns:
            selected_df = df.copy()
            break

    if selected_df is not None:
        df = selected_df
        df['Renk'] = ''

        # KomponentId > 0 olanları sarıya boya
        df.loc[df['KomponentId'] > 0, 'Renk'] = 'Sarı'

        # Ayakkabı grubu modelleri varsa onları da sarıya boya
        df.loc[df['ModelTanim'].isin(ayakkabi_modelleri), 'Renk'] = 'Sarı'

        st.success(f"Sayfa bulundu ve yüklendi: {sheet_name}")
        st.dataframe(df)

        ttn_input = st.text_input("TemaTakipNo gir (sadece numara):")

        if ttn_input:
            ttn_input = str(ttn_input).strip()
            if (df['TemaTakipNo'].astype(str) == ttn_input).any():
                mask = (df['TemaTakipNo'].astype(str) == ttn_input)

                # Kontrol: KomponentId > 0 veya ModelTanim eşleşmesi varsa
                kontrol_var = (
                    (df.loc[mask, 'KomponentId'] > 0).any() or 
                    (df.loc[mask, 'ModelTanim'].isin(ayakkabi_modelleri)).any()
                )

                if kontrol_var:
                    speak_text("Komponent var")
                    if (df.loc[mask, 'Renk'] == 'Sarı').any():
                        df.loc[mask, 'Renk'] = 'Kırmızı'

                st.dataframe(df)
            else:
                st.error("Bu TemaTakipNo bulunamadı!")
    else:
        st.error("Gerekli sütunlar (TemaTakipNo, KomponentId, ModelTanim) bulunamadı.")
