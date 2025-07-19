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
    elif position == "Bottom-Left":
        return (10, H - h - 10)
    elif position == "Bottom-Right":
        return (W - w - 10, H - h - 10)
    elif position == "Center":
        return ((W - w) // 2, (H - h) // 2)



def edit_image(image, brightness, watermark_text, watermark_color, watermark_position, selected_filters):
    edit = image.convert('RGB')
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

    #draw watermark
    font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 70)
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
            choices=["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right", "Center"],
            value="Top-Left",
            label="Watermark Position"
        ),

        gr.CheckboxGroup(
            choices=["Sharpen", "Blur", "Grayscale", "Contour", "Emboss", "Edge Enhance"],
            label="Choose Filters to Apply",
            value=["Sharpen"]
        )

    ],
    outputs=gr.Image(type="pil", label="Edited Image"),
    title="📸 Isha's Stylish Photo Editor",
    description="Upload your image, customize filters and watermark, and watch your photo transform!"
)


iface.launch()