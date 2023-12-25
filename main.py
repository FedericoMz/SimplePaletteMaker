import streamlit as st
from io import BytesIO

def save_palette(colors, name, LCD):

    # Create a BytesIO object to store the binary data
    file_buffer = BytesIO()

    # Iterate through the RGB colors and convert them to bytes
    for color in colors:
        # Convert hexadecimal to bytes (3 bytes for RGB)
        rgb_bytes = bytes.fromhex(color)
        # Write the RGB bytes to the BytesIO object
        file_buffer.write(rgb_bytes)

    # Write the LCDoff and footer using the first color from BG (see Analogue documentation)
    lcd_off_footer = bytes.fromhex(LCD[1:]) + b'\x81\x41\x50\x47\x42'
    file_buffer.write(lcd_off_footer)

    st.download_button(
        label="Download Palette",
        data=file_buffer.getvalue(),
        file_name=name+".pal",
        key="download_button"
    )

st.set_page_config(page_title="Simple Palette Maker", page_icon=":art:")

logo_image = st.image("logo.png", use_column_width=True)



col_dummy, col_dummy0, col_dummy1, col_dummy2, col_dummy3 = st.columns(5)
with col_dummy:
    st.header("")

with col_dummy0:
    st.header("C0")

with col_dummy1:
    st.header("C1")

with col_dummy2:
    st.header("C2")

with col_dummy3:
    st.header("C3")


col0, col1, col2, col3, col4 = st.columns(5)

with col0:
    st.header("BG")
bg0 = col1.color_picker('', '#ffffff', key=0)
bg1 = col2.color_picker('', '#ffffff', key=1)
bg2 = col3.color_picker('', '#ffffff', key=2)
bg3 = col4.color_picker('', '#ffffff', key=3)

LCD = col_dummy.color_picker('LCD', bg3, key=12)

col5, col6, col7, col8, col9 = st.columns(5)

with col5:
    st.header("OB0")
obA0 = col6.color_picker('', bg0, key=4)
obA1 = col7.color_picker('', bg1, key=5)
obA2 = col8.color_picker('', bg2, key=6)
obA3 = col9.color_picker('', bg3, key=7)

colA, colB, colC, colD, colE = st.columns(5)

with colA:
    st.header("OB1")
obB0 = colB.color_picker('', obA0, key=8)
obB1 = colC.color_picker('', obA1, key=9)
obB2 = colD.color_picker('', obA2, key=10)
obB3 = colE.color_picker('', obA3, key=11)

colors_to_save = [
bg3[1:], bg2[1:], bg1[1:], bg0[1:],  # BG
obA3[1:], obA2[1:], obA1[1:], obA0[1:],  # OBJ1
obB3[1:], obB2[1:], obB1[1:], obB0[1:],  # OBJ2
bg3[1:], bg2[1:], bg1[1:], bg0[1:],  # Window [same as BG]
]

file_name = st.text_input("File Name:")

if file_name:
    palette_data = save_palette(colors_to_save, file_name, LCD)

st.subheader("How to use")
st.markdown("""
This app lets you create .pal files for the Analogue Pocket.

Game Boy games have three layers:

- a background layer;
- a "main" object layer (e.g., for characters and enemies);
- a secondary object layer (for small effects or objects, e.g., the whip in _Castlevania_).

The black & white Game Boy uses the same 4-shader palette for all of them. The Analogue Pocket (and the Game Boy Color) allows you to assign a 4-color palette to _each_ layer. Moreover, you can also decide the color of the LCD turned off.

The app uses the BG3 color for LCD by default, following the community-made GBC and SGB palettes. By default, the app also assigns the BG palette to OB1, and the OB1 palette to OB2. This is to make it easy to create a simple GB 4-shader palette without fancy colors for characters or enemies.

""")



