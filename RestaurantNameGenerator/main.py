import streamlit as st
import streamlit.components.v1 as components
import langchain_helper
import random

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Culinary Compass | Restaurant Generator",
    page_icon="🍽️",
    layout="wide",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
  html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d0d !important;
    color: #f0ece4;
    font-family: 'Lato', sans-serif;
  }
  #MainMenu, footer, header { visibility: hidden; }
  [data-testid="stSidebar"] > div:first-child {
    background: #111111 !important;
    border-right: 1px solid #2a2a2a;
  }
  [data-testid="stSelectbox"] label { color: #aaa !important; font-size:.85rem !important; }
  div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #c9a84c, #a07830) !important;
    color: #0d0d0d !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    font-size: .75rem !important;
    border: none !important;
    border-radius: 6px !important;
    width: 100% !important;
    margin-top: .8rem !important;
  }
  div[data-testid="stButton"] > button:hover { opacity:.85 !important; }
</style>
""", unsafe_allow_html=True)

# ── Full Indian menu ──────────────────────────────────────────────────────────
INDIAN_MENU = {
    "🥗 Starters & Appetizers": [
        ("Samosa (2 pcs)",       "🥟", "Crispy pastry filled with spiced potato & peas, served with mint chutney",          "$8"),
        ("Paneer Tikka",         "🧀", "Cottage cheese cubes marinated in tandoori spices, grilled in clay oven",            "$13"),
        ("Chicken Seekh Kebab",  "🍢", "Minced chicken with ginger, chilli & coriander, skewered & chargrilled",             "$14"),
        ("Aloo Tikki Chaat",     "🥔", "Potato patties topped with yoghurt, tamarind chutney & pomegranate seeds",           "$10"),
        ("Onion Bhaji",          "🧅", "Golden fried onion fritters with cumin & green chilli, served with raita",           "$9"),
        ("Hara Bhara Kebab",     "🌿", "Spinach & pea patties with a paneer centre, pan-seared to perfection",              "$11"),
    ],
    "🍛 Curries & Mains": [
        ("Butter Chicken",       "🍗", "Tender tandoor-roasted chicken in a rich tomato-butter-cream sauce",                 "$18"),
        ("Chicken Tikka Masala", "🫕", "Chargrilled chicken in a smoky, spiced tomato & cashew gravy",                      "$18"),
        ("Palak Paneer",         "🥬", "Fresh cottage cheese cubes simmered in a velvety spinach & fenugreek sauce",         "$16"),
        ("Lamb Rogan Josh",      "🥩", "Slow-braised Kashmiri lamb with aromatic whole spices & Kashmiri chilli",            "$22"),
        ("Dal Makhani",          "🫘", "Black lentils slow-cooked overnight with butter, cream & tomato",                   "$14"),
        ("Prawn Masala",         "🦐", "Tiger prawns in a coastal spiced onion-tomato gravy",                               "$24"),
        ("Chana Masala",         "🌶️","Chickpeas in a boldly spiced tamarind & tomato sauce — vegan & hearty",             "$13"),
        ("Chicken Korma",        "🍲", "Mild, fragrant chicken in a creamy almond & cardamom sauce",                        "$17"),
        ("Fish Curry (Goan)",    "🐟", "Fresh fish in a tangy coconut milk & raw mango gravy",                              "$20"),
        ("Egg Curry",            "🥚", "Hard-boiled eggs in a spiced onion-tomato masala, South Indian style",              "$13"),
    ],
    "🍚 Rice & Biryani": [
        ("Mutton Biryani",       "🍖", "Dum-cooked basmati rice layered with spiced mutton, rose water & saffron",          "$26"),
        ("Chicken Biryani",      "🍗", "Long-grain basmati with spiced chicken, saffron & caramelised onion",               "$20"),
        ("Vegetable Biryani",    "🥦", "Fragrant basmati dum-cooked with seasonal vegetables & whole spices",               "$15"),
        ("Jeera Rice",           "🍚", "Steamed basmati tossed with cumin seeds & ghee",                                    "$6"),
    ],
    "🫓 Breads": [
        ("Butter Naan",          "🫓", "Leavened bread baked in tandoor, finished with salted butter",                      "$4"),
        ("Garlic Naan",          "🧄", "Tandoor naan topped with roasted garlic & fresh coriander",                         "$5"),
        ("Laccha Paratha",       "🌀", "Multi-layered flaky whole-wheat bread with a crisp exterior",                       "$5"),
        ("Puri",                 "🫓", "Deep-fried puffed bread, light & airy — served with curry",                        "$4"),
    ],
    "🍮 Desserts": [
        ("Gulab Jamun",          "🟤", "Soft milk-solid dumplings soaked in rose & cardamom syrup — served warm",           "$7"),
        ("Mango Kulfi",          "🥭", "Dense Indian ice cream with real Alphonso mango, pistachios & saffron",             "$8"),
        ("Gajar Halwa",          "🥕", "Slow-cooked carrot pudding with khoya, almonds & cardamom",                        "$8"),
        ("Rasmalai",             "⚪", "Soft cottage cheese discs soaked in chilled saffron-cardamom milk",                 "$7"),
    ],
    "🥤 Drinks": [
        ("Mango Lassi",          "🥭", "Chilled yoghurt blended with Alphonso mango pulp & a hint of cardamom",            "$6"),
        ("Sweet Lassi",          "🥛", "Whipped yoghurt with sugar, rose water & crushed ice",                             "$5"),
        ("Masala Chai",          "☕", "Spiced black tea brewed with ginger, cardamom, clove & cinnamon",                  "$4"),
        ("Shikanji",             "🍋", "Fresh lemon cooler with black salt, cumin & mint — Indian lemonade",               "$5"),
    ],
}

CUISINE_META = {
    "Indian":   {"emoji":"🪔","flag":"🇮🇳","tagline":"Bold spices. Ancient recipes. Unforgettable warmth."},
    "Italian":  {"emoji":"🫙","flag":"🇮🇹","tagline":"La cucina vera. Simple ingredients, extraordinary soul."},
    "Mexican":  {"emoji":"🌶️","flag":"🇲🇽","tagline":"Fire & fiesta. Authentic flavours from the heart of Mexico."},
    "Arabic":   {"emoji":"🌙","flag":"🌍","tagline":"Marhaba. Lavish hospitality. Timeless Levantine tradition."},
    "American": {"emoji":"🦅","flag":"🇺🇸","tagline":"Classic comfort. Big flavours. No apologies."},
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<p style='font-family:serif;font-size:1.1rem;color:#c9a84c;margin:0;'>🍽️ Culinary Compass</p>", unsafe_allow_html=True)
    st.markdown("---")
    cuisine = st.selectbox("Select a cuisine", list(CUISINE_META.keys()), index=0)
    generate = st.button("✦ Generate Restaurant")
    st.markdown("---")
    st.markdown("<small style='color:#444;'>Powered by LangChain + Claude</small>", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
components.html("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
<div style="text-align:center;padding:3rem 1rem 2rem;border-bottom:1px solid #2a2a2a;
     background:radial-gradient(ellipse at 50% 0%,#1e1209,#0d0d0d 70%);box-sizing:border-box;">
  <p style="font-family:Lato,sans-serif;letter-spacing:.35em;font-size:.67rem;text-transform:uppercase;color:#c9a84c;margin:0 0 .5rem;">✦ AI Culinary Studio ✦</p>
  <h1 style="font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:700;color:#f0ece4;margin:0;line-height:1.15;">Restaurant Name Generator</h1>
  <p style="font-size:.88rem;color:#555;margin:.7rem 0 0;">Craft a unique restaurant identity in seconds</p>
  <div style="width:60px;height:2px;background:linear-gradient(90deg,transparent,#c9a84c,transparent);margin:1rem auto 0;"></div>
</div>
""", height=190)

# ── Main ──────────────────────────────────────────────────────────────────────
if generate or cuisine:
    meta = CUISINE_META[cuisine]

    with st.spinner("Crafting your restaurant concept..."):
        response = langchain_helper.generate_restaurant_name_and_items(cuisine)

    restaurant_name = response['restaurant_name'].strip()
    raw_items = response['menu_items'].strip().split(",")
    ai_items = [x.strip() for x in raw_items if x.strip()]
    random.seed(restaurant_name)

    # ── Identity card ─────────────────────────────────────────────────────────
    components.html(f"""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
<div style="background:linear-gradient(135deg,#181510,#1c1710);border:1px solid #2e2620;border-radius:12px;
     padding:2rem 2.4rem;margin:1rem 0;position:relative;overflow:hidden;box-sizing:border-box;">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at top left,rgba(201,168,76,.07),transparent 60%);pointer-events:none;"></div>
  <span style="position:absolute;top:1rem;right:1.4rem;font-size:2rem;opacity:.18;">{meta['emoji']}</span>
  <div style="display:inline-block;font-family:Lato,sans-serif;font-size:.6rem;letter-spacing:.3em;text-transform:uppercase;
       color:#c9a84c;border:1px solid #c9a84c44;border-radius:999px;padding:.2rem .8rem;margin-bottom:.8rem;">
    {meta['flag']}  {cuisine} Cuisine
  </div>
  <h2 style="font-family:'Playfair Display',serif;font-size:2.3rem;font-weight:700;color:#f5f0e8;margin:0 0 .3rem;line-height:1.2;">{restaurant_name}</h2>
  <p style="font-style:italic;color:#6b6355;font-size:.86rem;margin:0;">{meta['tagline']}</p>
</div>
""", height=185)

    # ── Chef's specials pills ─────────────────────────────────────────────────
    pills = "".join([
        f'<span style="background:#1e1a12;border:1px solid #2e2620;border-radius:999px;padding:.18rem .7rem;font-size:.72rem;color:#c9a84c;margin:.18rem .18rem 0 0;display:inline-block;">{item}</span>'
        for item in ai_items
    ])
    components.html(f"""
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">
<div style="background:#100e0a;border:1px solid #1e1a12;border-radius:10px;padding:1rem 1.3rem;margin-bottom:.5rem;box-sizing:border-box;">
  <p style="font-family:Lato,sans-serif;font-size:.58rem;letter-spacing:.25em;text-transform:uppercase;color:#c9a84c;margin:0 0 .55rem;">✦ Chef's Specials Tonight</p>
  <div style="display:flex;flex-wrap:wrap;">{pills}</div>
</div>
""", height=100)

    # ── Full menu ─────────────────────────────────────────────────────────────
    if cuisine == "Indian":
        menu_data = INDIAN_MENU
    else:
        other_icons = {"Italian":"🍝","Mexican":"🌮","Arabic":"🧆","American":"🍔"}
        ic = other_icons.get(cuisine,"🍽️")
        menu_data = {
            f"{ic} Signature Dishes": [
                (item, ic, "Chef's signature preparation, made fresh daily", f"${random.randint(12,38)}.00")
                for item in ai_items
            ]
        }

    # Build sections
    sections_html = ""
    for sec, dishes in menu_data.items():
        rows_html = ""
        for name, icon, desc, price in dishes:
            rows_html += f"""
            <div style="background:#141414;border:1px solid #252525;border-radius:10px;
                 padding:.9rem 1.1rem;display:flex;align-items:flex-start;gap:.75rem;">
              <div style="font-size:1.4rem;flex-shrink:0;margin-top:.05rem;">{icon}</div>
              <div>
                <div style="font-family:'Playfair Display',serif;font-size:.95rem;color:#f0ece4;font-weight:600;">{name}</div>
                <div style="font-size:.73rem;color:#454035;margin-top:.15rem;line-height:1.4;">{desc}</div>
                <div style="font-size:.78rem;color:#c9a84c;margin-top:.28rem;font-weight:700;">{price}</div>
              </div>
            </div>"""

        sections_html += f"""
        <div style="margin-bottom:1.8rem;">
          <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.6rem;">
            <h3 style="font-family:'Playfair Display',serif;font-size:1.2rem;color:#f0ece4;margin:0;white-space:nowrap;">{sec}</h3>
            <div style="flex:1;height:1px;background:linear-gradient(90deg,#2a2a2a,transparent);"></div>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:.7rem;">
            {rows_html}
          </div>
        </div>"""

    total = sum(len(v) for v in menu_data.values())
    frame_h = max(600, total * 90)

    components.html(f"""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
<div style="background:#0d0d0d;padding:.8rem 0 2rem;font-family:Lato,sans-serif;box-sizing:border-box;">
  <div style="margin-bottom:1.2rem;">
    <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.15rem;">
      <h2 style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#f0ece4;margin:0;">Our Menu</h2>
      <div style="flex:1;height:1px;background:linear-gradient(90deg,#2a2a2a,transparent);"></div>
    </div>
    <p style="font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;color:#c9a84c;margin:0;">Full Menu · {total} Dishes</p>
  </div>
  {sections_html}
  <div style="border-top:1px solid #1a1a1a;padding-top:.8rem;text-align:center;font-size:.68rem;color:#282828;letter-spacing:.08em;margin-top:.5rem;">
    {restaurant_name} · {cuisine} Kitchen · Est. 2024
  </div>
</div>
""", height=frame_h, scrolling=True)

else:
    components.html("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,400&display=swap" rel="stylesheet">
<div style="text-align:center;padding:4rem 1rem;color:#2e2e2e;">
  <div style="font-size:3rem;">🍽️</div>
  <p style="font-family:'Playfair Display',serif;font-size:1.15rem;color:#333;margin-top:1rem;">
    Select a cuisine and click Generate
  </p>
</div>
""", height=200)