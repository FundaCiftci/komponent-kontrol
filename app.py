
import streamlit as st
import pandas as pd
import random
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

def speak_text(text):
    unique = random.randint(0, 1000000)
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{text} {unique}");
        msg.text = "{text}";
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# Ayakkabı ve istisna listeleri (önceki kodundaki gibi olacak, burada kısaltıldı)
ayakkabi_modelleri = [...]  # LİSTEYİ YUKARIDAN KOPYALAYABİLİRSİN
istisnalar = [...]          # LİSTEYİ YUKARIDAN KOPYALAYABİLİRSİN

st.set_page_config(page_title="Komponent Kontrol", layout="wide")
st.title("👟 Komponent Kontrol Uygulaması")

uploaded_file = st.file_uploader("📁 Excel dosyanı yükle (.xlsx)", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None, dtype=str)
    selected_df = None

    for sheet_name, df in all_sheets.items():
        if all(col in df.columns for col in ['TemaTakipNo', 'KomponentId', 'ModelTanim']):
            selected_df = df.copy()
            break

    if selected_df is not None:
        df = selected_df
        df['Renk'] = ''
        df.loc[(df['KomponentId'].astype(float) > 0) & (~df['ModelTanim'].isin(istisnalar)), 'Renk'] = 'Sarı'
        df.loc[df['ModelTanim'].isin(ayakkabi_modelleri), 'Renk'] = 'Sarı'

        ttn_input = st.text_input("🎯 TemaTakipNo gir (sadece numara):", key="inputbox")

        if ttn_input:
            ttn_input = ttn_input.strip()
            mask = df['TemaTakipNo'] == ttn_input

            if mask.any():
                kontrol_var = (
                    ((df.loc[mask, 'KomponentId'].astype(float) > 0) & (~df.loc[mask, 'ModelTanim'].isin(istisnalar))).any()
                    or (df.loc[mask, 'ModelTanim'].isin(ayakkabi_modelleri)).any()
                )
                if kontrol_var:
                    speak_text("Kontrol et")
                    df.loc[mask & (df['Renk'] == 'Sarı'), 'Renk'] = 'Kırmızı'
            else:
                st.error("Bu TemaTakipNo bulunamadı!")

        # Arka plan rengi ayarlamak için JS kodu
        renk_kodlari = JsCode("""
        function(params) {
            if (params.data.Renk == 'Sarı') {
                return { 'backgroundColor': 'yellow' }
            } else if (params.data.Renk == 'Kırmızı') {
                return { 'backgroundColor': 'red', 'color': 'white' }
            }
        }
        """)

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(resizable=True, filterable=True, sortable=True)
        gb.configure_column("Renk", cellStyle=renk_kodlari)
        gb.configure_pagination()
        gridOptions = gb.build()

        st.markdown("### 📋 Tüm Liste (Renkli)")
        AgGrid(df, gridOptions=gridOptions, height=600, theme="material")
    else:
        st.error("TemaTakipNo, KomponentId ve ModelTanim sütunları eksik.")
