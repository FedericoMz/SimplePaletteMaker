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

    # Write the LCD off and the footer (see Analogue documentation)
    lcd_off_footer = bytes.fromhex(LCD[1:]) + b'\x81\x41\x50\x47\x42'
    file_buffer.write(lcd_off_footer)

    st.download_button(
        label="Download Palette",
        data=file_buffer.getvalue(),
        file_name=name+".pal",
        key="download_button"
    )

def read_pal_file(uploaded_file):
    colors = []

    # Read the file content
    file_content = uploaded_file.read()

    # Iterate over the content, assuming each color is represented by 3 bytes
    for i in range(0, len(file_content), 3):
        # Convert the bytes to hex and append to the colors list
        color_hex = file_content[i:i + 3].hex().upper()
        colors.append(color_hex)

    return colors

st.set_page_config(page_title="Simple Palette Maker", page_icon=":art:")
logo_image = st.sidebar.image("logo.png", use_container_width=True)

uploaded_file = st.sidebar.file_uploader("Upload an existing .pal file (optional)", type="pal")
st.sidebar.subheader("Options")
GB_mode = st.sidebar.checkbox('Super Game Boy Mode')
invert = st.sidebar.checkbox('Inverted Palette')

if uploaded_file is not None:
    # Read colors from the uploaded file
    r_color = read_pal_file(uploaded_file)

    r_bg0 = '#' + r_color[3]
    r_bg1 = '#' + r_color[2]
    r_bg2 = '#' + r_color[1]
    r_bg3 = '#' + r_color[0]

    r_obA0 = '#' + r_color[7]
    r_obA1 = '#' + r_color[6]
    r_obA2 = '#' + r_color[5]
    r_obA3 = '#' + r_color[4]

    r_obB0 = '#' + r_color[11]
    r_obB1 = '#' + r_color[10]
    r_obB2 = '#' + r_color[9]
    r_obB3 = '#' + r_color[8]

    r_LCD = '#' + r_color[12]
else:
    r_bg0 = '#ffffff'
    r_bg1 = '#ffffff'
    r_bg2 = '#ffffff'
    r_bg3 = '#000000'

    r_obA0 = '#ffffff'
    r_obA1 = '#ffffff'
    r_obA2 = '#ffffff'
    r_obA3 = '#000000'

    r_obB0 = '#ffffff'
    r_obB1 = '#ffffff'
    r_obB2 = '#ffffff'
    r_obB3 = '#000000'

    r_LCD = '#000000'

LCD_check = st.sidebar.checkbox('Use BG for LCD', True)

if LCD_check and not invert:
    LCD = r_bg3
elif LCD_check and invert:
    LCD = r_bg0
else:
    LCD = st.sidebar.color_picker('LCD Color', '#000000', key=12)

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
bg0 = col1.color_picker('', r_bg0, key=0)
bg1 = col2.color_picker('', r_bg1, key=1)
bg2 = col3.color_picker('', r_bg2, key=2)
bg3 = col4.color_picker('', r_bg3, key=3)

if GB_mode is not True:

    col5, col6, col7, col8, col9 = st.columns(5)

    with col5:
        st.header("OB0")
    obA0 = col6.color_picker('', r_obA0, key=4)
    obA1 = col7.color_picker('', r_obA1, key=5)
    obA2 = col8.color_picker('', r_obA2, key=6)
    obA3 = col9.color_picker('', r_obA3, key=7)

    colA, colB, colC, colD, colE = st.columns(5)

    with colA:
        st.header("OB1")
    obB0 = colB.color_picker('', r_obB0, key=8)
    obB1 = colC.color_picker('', r_obB1, key=9)
    obB2 = colD.color_picker('', r_obB2, key=10)
    obB3 = colE.color_picker('', r_obB3, key=11)

else:
    obA0, obB0 = bg0, bg0
    obA1, obB1 = bg1, bg1
    obA2, obB2 = bg2, bg2
    obA3, obB3 = bg3, bg3


if invert is not True:
    colors_to_save = [
    bg3[1:], bg2[1:], bg1[1:], bg0[1:],  # BG
    obA3[1:], obA2[1:], obA1[1:], obA0[1:],  # OBJ1
    obB3[1:], obB2[1:], obB1[1:], obB0[1:],  # OBJ2
    bg3[1:], bg2[1:], bg1[1:], bg0[1:],  # Window [same as BG]
    ]
else:
    colors_to_save = [
    bg0[1:], bg1[1:], bg2[1:], bg3[1:],  # BG
    obA0[1:], obA1[1:], obA2[1:], obA3[1:],  # OBJ1
    obB0[1:], obB1[1:], obB2[1:], obB3[1:],  # OBJ2
    bg0[1:], bg1[1:], bg2[1:], bg3[1:],  # Window
    ]  

file_name = st.text_input("", placeholder="Write the palette name here and press enter to download")

if file_name:
    palette_data = save_palette(colors_to_save, file_name, LCD)


st.subheader("How to use")
st.markdown("""
This app lets you create .pal files for the Analogue Pocket.

Game Boy games have three layers:

- background (BG);
- main objects such as characters and enemies (OB0);
- minor objects, like effects or weapons (OB1).

The Super Game Boy colorized Game Boy games by [assigning the same 4-color palette to BG, OB0, and OB1](https://wildleoknight.itch.io/super-game-boy-palettes). If you want to use this "simple" colorization, enable _Super Game Boy Mode_.

On the other hand, the Game Boy Color colorized Game Boy games by assigning different palettes to BG, OB0, and OB1 (e.g., in [_Metroid II_](https://d2rd7etdn93tqb.cloudfront.net/wp-content/uploads/2023/02/metroid-2-game-boy-fighting-omega-metroid-022223.jpg) the BG is blue, and everything else red-ish).

You can also choose the color of the LCD screen while off. By default, the app uses the BG3 color, following the community-made GBC and SGB palettes. 
            
The _Inverted Palette_ option inverts the order of colors (e.g, the downloaded palette will have Color 0 assigned to Color 3).

Most official palettes have Color 0 set to white and Color 3 set to black for all the layers.

""")



