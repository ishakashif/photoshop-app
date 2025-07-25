import gradio as gr
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont


# Convert a color string from Gradio into a format compatible with Pillow.
# If the color is in "rgba(r, g, b, a)" format, convert it to an (R, G, B) tuple.
# If it's a named color like "red" or a hex code like "#ff0000", return it as-is.
def rgba_to_rgb_tuple(color_string):
    if color_string.startswith("rgba"):
        color_string = color_string.replace("rgba(", "").replace(")", "")
        r, g, b, a = map(float, color_string.split(","))
        return (int(r), int(g), int(b))
    else:
        return color_string  

# Finding the position of the Watermark to allow users to be able to move it where
# they would like!
def get_position(image_size, text_size, position):
    W, H = image_size
    w, h = text_size

    if position == "Top-Left":
        return (10, 10)
    elif position == "Top-Right":
        return (W - w - 10, 10)
    elif position == "Top-Center":
        return ((W - w) // 2, 10)
    elif position == "Bottom-Left":
        return (10, H - h - 10)
    elif position == "Bottom-Right":
        return (W - w - 10, H - h - 20)
    elif position == "Bottom-Center":
        return ((W - w) // 2, H - h - 20)
    elif position == "Center":
        return ((W - w) // 2, (H - h) // 2)

# Fonts to select from for users' Watermark option!
font_paths = {
    "Arial": "/Library/Fonts/Arial.ttf",
    "Times New Roman": "/Library/Fonts/Times New Roman.ttf",
    "Courier New": "/Library/Fonts/Courier New.ttf",
    "Georgia": "/Library/Fonts/Georgia.ttf",
    "Verdana": "/Library/Fonts/Verdana.ttf"
}

def edit_image(image, brightness, watermark_text, watermark_color, watermark_position, selected_filters, preset, font_size, font_style, custom_font_file, crop_enabled, crop_left, crop_top, crop_right, crop_bottom):
    # Convert to RGB
    edit = image.convert('RGB')

    # Handle Cropping 
    if crop_enabled:
        width, height = edit.size  

    # Use full width/height if right/bottom not set
        if crop_right == 0:
            crop_right = width
        if crop_bottom == 0:
            crop_bottom = height

        left = max(0, min(crop_left, width - 1))
        top = max(0, min(crop_top, height - 1))
        right = max(left + 1, min(crop_right, width))
        bottom = max(top + 1, min(crop_bottom, height))

        if (left != 0 or top != 0 or right != width or bottom != height):
            edit = edit.crop((left, top, right, bottom))
    

    # Applying selected filters
    if "Sharpen" in selected_filters:
        edit = edit.filter(ImageFilter.SHARPEN)
    if "Blur" in selected_filters: 
        edit = edit.filter(ImageFilter.BLUR)
    if "Grayscale" in selected_filters:
        edit = edit.convert('L').convert("RGB") # RGB maintainence for watermarking (it won't change color otherwise!)
    if "Contour" in selected_filters:
        edit = edit.filter(ImageFilter.CONTOUR)
    if "Emboss" in selected_filters:
        edit = edit.filter(ImageFilter.EMBOSS)
    if "Edge Enhance" in selected_filters:
        edit = edit.filter(ImageFilter.EDGE_ENHANCE)

    #applying brightness

    enhancer = ImageEnhance.Brightness(edit)
    edit = enhancer.enhance(brightness)

    # defining presets
    if preset == "Vintage":
        edit = ImageEnhance.Color(edit).enhance(0.7)
        edit = ImageEnhance.Contrast(edit).enhance(1.2)
        edit = edit.filter(ImageFilter.GaussianBlur(1))
    elif preset == "Dreamy":
        edit = ImageEnhance.Brightness(edit).enhance(1.3)
        edit = ImageEnhance.Sharpness(edit).enhance(0.7)
        edit = edit.filter(ImageFilter.BLUR)
    elif preset == "Drama":
        edit = ImageEnhance.Contrast(edit).enhance(1.5)
        edit = ImageEnhance.Sharpness(edit).enhance(2.0)
        edit = edit.filter(ImageFilter.EDGE_ENHANCE)
    elif preset == "Cool Tones":
        r, g, b = edit.split()
        b = ImageEnhance.Brightness(b).enhance(1.3)
        edit = Image.merge("RGB", (r, g, b))

    #draw watermark
    try:
        if custom_font_file is not None:
            font_path = custom_font_file.name 
        else:
            font_path = font_paths.get(font_style, "/Library/Fonts/Arial.ttf")
        font = ImageFont.truetype(font_path, int(font_size))
    except Exception as e:
        print(f"⚠️ Error loading font: {e}. Falling back to Arial.")
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", int(font_size))


    # end of font handling
    draw = ImageDraw.Draw(edit)
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_size = (text_width, text_height)
    pos = get_position(edit.size, text_size, watermark_position)
    draw.text(pos, watermark_text, font=font, fill=rgba_to_rgb_tuple(watermark_color))

    return edit


# Gradio UI
iface = gr.Interface(
    fn=edit_image,
    inputs=[
        gr.Image(type="pil", label="Upload your Image"),
        gr.Slider(0.5, 2.0, value=1.2, label="Brightness"),
        gr.Textbox("Isha", label="Watermark Text"),
        gr.ColorPicker(value="red", label="Watermark Color"),
        gr.Dropdown(
            choices=["Top-Left", "Top-Right", "Top-Center", "Bottom-Left", "Bottom-Right", "Bottom-Center", "Center"],
            value="Top-Left",
            label="Watermark Position"
        ),

        gr.CheckboxGroup(
            choices=["Sharpen", "Blur", "Grayscale", "Contour", "Emboss", "Edge Enhance"],
            label="Choose Filters to Apply",
            value=["Sharpen"]
        ),

        gr.Dropdown(
            choices=["None", "Vintage", "Dreamy", "Drama", "Cool Tones"],
            label="Filter Preset (Pre-Styled)"
        ),

        gr.Slider(10, 150, value=70, step=1, label="Watermark Font Size"),

        gr.Dropdown(
            choices=["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"],
            value="Arial",
            label="Watermark Font Style"
        ),

        gr.File(label="Upload Your Own .ttf Font (Optional)", type ="filepath"),

        gr.Checkbox(label="Enable Cropping", value=False),
        gr.Slider(0, 100, value=0, step=1, label="Crop Left"),
        gr.Slider(0, 100, value=0, step=1, label="Crop Top"),
        gr.Slider(0, 100, value=0, step=1, label="Crop Right"),
        gr.Slider(0, 100, value=0, step=1, label="Crop Bottom")
    ],
    outputs=gr.Image(type="pil", label="Edited Image"),
    title="📸 Isha's Stylish Photo Editor",
    description="Upload your image, customize filters and watermark, and watch your photo transform!"
)


iface.launch()


# adding basic comments! 