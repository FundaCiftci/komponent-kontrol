import streamlit as st
import pandas as pd
import random

# SESLİ KOMUT - Her tetikleme için eşsizleştir
def speak_text(text):
    unique = random.randint(0, 1000000)
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{text} {unique}");
        msg.text = "{text}";
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# Ayakkabı grubu kontrol listesi (ModelTanim eşleşmesi)
ayakkabi_modelleri = [
    "SANDALS", "Slippers", "Beach Slippers", "Shoes", "Beach Shoes", "Home Shoes", "Beach Sandals",
    "HOME SLIPPERS", "Boots", "Rain Boots", "ТУФЛИ", "ОБУВЬ ПЛЯЖНАЯ", "САНДАЛИИ", "ТАПОЧКИ",
    "КЕДЫ", "ДОМАШНЯЯ ОБУВЬ", "ЭСПАДРИЛЬИ", "Home Boots"
]

# Hariç tutulacak modeller (KomponentId > 0 olsa bile sarı/kırmızı yapılmayacak)
istisna_model_listesi = [
    "Trainer Socks", "Crown Headband", "Socks", "Bath Mat", "Plate Charger", "Rollers", "Toy Set",
    "Invisible Socks", "Water Bottle", "Sunglasses", "Toy Car", "Plate", "Toy Figurin (Unfilled)",
    "Hair Clip", "Hair Elastic", "Below Knee Socks", "Suitcase", "Cake Stand", "Fun Toys", "Gift Bag",
    "Shopping Bag", "Backpack", "Hair Brush", "Fan/Ventilator", "Toy Figurin Filled", "Frame", "Necklace",
    "Beach Bag", "Waist Bag", "Jug", "Ring", "Hair Conb", "TOY DOLL", "Rug", "Salad Bowl", "Pen",
    "Snorkel Set", "GLASS", "Toy Vehicles", "Mug", "Swimming Goggle", "Soap Dispenser",
    "Stationery Equipment", "Bowl", "Coffee cup and saucer", "Handbag", "Wallet", "Make Up Brush",
    "Basket", "Baker", "Vase", "Notebook", "Eye Lash Curler", "Make Up Sponge", "COLORING BOOK",
    "Laptop Bag", "TOY", "Dish Drying Pad", "Sticker", "Felt-tip pen", "Salt/Pepper Shaker", "Watch",
    "Card Holder", "Watercolor", "Painting Stencil", "Eraser", "Adhesive Silicone Bra", "Bracelet",
    "Sleeping Eye Mask", "Key Chain", "Pencil Case", "Candle Holder", "Pencil", "Colour Pencil", "Earrings",
    "DIGITAL WRITING BOARD", "Bracelet - Accessory", "Kitchen Utensils", "Coaster", "Tweezers",
    "Eyebrow Correction Apparatus", "Travel Size Toiletry Bottle", "Nut Bowl", "Play Dough",
    "Serving Board", "Stamp", "Decoration Accessory", "Lunch Box Bag", "Pencil Sharpener", "Tray",
    "Brush", "Earmuffs", "Napkin Holder", "Artificial Flower", "Tie Bow Tie", "Box", "UMBRELLA",
    "Plush Backpack", "Chopping Board", "Nail File", "Nail Trimmer", "НОСКИ", "ПОДСЛЕДНИКИ",
    "ТРЕНИРОВОЧНЫЕ НОСКИ", "Drinking Straw", "КОЛЬЦО", "ГОЛЬФЫ", "РЮКЗАК", "СУМКА", "СУМОЧКА",
    "СУМКА ДЛЯ КОМПЬЮТЕРА", "Diffuser", "ЗАКОЛКА", "БЛЕЙЗЕР", "ЛЕГИНСЫ", "Storage Bag", "ЧЕМОДАН",
    "КОШЕЛЕК", "ПАРФЮМЕРНАЯ ВОДА", "Organizer", "ОЧКИ ДЛЯ МОРЯ", "КУХОННАЯ УТВАРЬ", "School bag",
    "Cologne", "ГРАФИН", "ПОЯСНАЯ СУМКА", "КОВРИК ДЛЯ ВАННЫ", "EDT- Eau De Toilette", "КОРЗИНА",
    "ОБОДОК", "МИСКА", "ТАРЕЛКА", "КАРДХОЛДЕР", "Room Spray", "ВАЗА", "EDP- Eau De Parfum",
    "ПОДСТАКАННИК", "СТАКАН", "Car Freshner", "ОЖЕРЕЛЬЕ", "Tea Pot", "Lint Roller", "Swim Ring",
    "Candle", "ПОДСТАВКА ДЛЯ ТОРТА", "СПОРТИВНАЯ СУМКА", "Nail Nipper", "СОЛОНКА/ПЕРЕЧНИЦА",
    "Saucer", "БРАСЛЕТ", "ДИСПЕНСЕР ДЛЯ ЖИДКОГО МЫЛА", "Makeup Brush Cleaner", "Ruler",
    "Soap Tray", "Toothbrush Holder", "Food Container", "Shoe Cleaning Sponge", "Candlestick",
    "Bag", "Suspenders"
]

st.set_page_config(page_title="Komponent Kontrol", layout="wide")
st.title("🔍 Komponent Kontrol Uygulaması")

uploaded_file = st.file_uploader("Excel dosyanı yükle (.xlsx)", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    selected_df = None

    for sheet_name, df in all_sheets.items():
        if all(col in df.columns for col in ['TemaTakipNo', 'KomponentId', 'ModelTanim']):
            selected_df = df.copy()
            break

    if selected_df is not None:
        df = selected_df
        df['Renk'] = ''

        # 1. KomponentId > 0 ama istisna modellerde değilse sarı
        df.loc[(df['KomponentId'] > 0) & (~df['ModelTanim'].isin(istisna_model_listesi)), 'Renk'] = 'Sarı'

        # 2. Ayakkabı grubu modelleri varsa sarı
        df.loc[df['ModelTanim'].isin(ayakkabi_modelleri), 'Renk'] = 'Sarı'

        st.success(f"Sayfa bulundu ve yüklendi: {sheet_name}")
        st.dataframe(df)

        ttn_input = st.text_input("TemaTakipNo gir (sadece numara):")

        if ttn_input:
            ttn_input = str(ttn_input).strip()
            if (df['TemaTakipNo'].astype(str) == ttn_input).any():
                mask = (df['TemaTakipNo'].astype(str) == ttn_input)

                kontrol_var = (
                    ((df.loc[mask, 'KomponentId'] > 0) & (~df.loc[mask, 'ModelTanim'].isin(istisna_model_listesi))).any()
                    or (df.loc[mask, 'ModelTanim'].isin(ayakkabi_modelleri)).any()
                )

                if kontrol_var:
                    speak_text("Kontrol et")
                    if (df.loc[mask, 'Renk'] == 'Sarı').any():
                        df.loc[mask, 'Renk'] = 'Kırmızı'

                st.dataframe(df)
            else:
                st.error("Bu TemaTakipNo bulunamadı!")
    else:
        st.error("TemaTakipNo, KomponentId ve ModelTanim sütunları bulunamadı.")
