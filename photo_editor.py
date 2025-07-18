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

def edit_image(image, brightness, watermark_text, watermark_color, selected_filters):
    edit = image.convert('RGB')
    # Applying selected filters
    if "Sharpen" in selected_filters:
        edit = edit.filter(ImageFilter.SHARPEN)
    if "Blur" in selected_filters: 
        edit = edit.filter(ImageFilter.BLUR)
    if "Grayscale" in selected_filters:
        edit = edit.convert('L').convert


    # drawing the watermark 
    font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 70)
    draw = ImageDraw.Draw(edit)
    draw.text((10, 10), watermark_text, font=font, fill= rgba_to_rgb_tuple(watermark_color))

    return edit


# Gradio UI
iface = gr.Interface (
    fn=edit_image,
    inputs=[
        gr.Image(type="pil", label="Upload your Image"),
        gr.Slider(0.5, 2.0, value=1.2, label="Brightness"),
        gr.Textbox("Isha", label="Watermark Text"),
        gr.ColorPicker(value="red", label="Watermark Color")
    ],
    outputs=gr.Image(type="pil", label="Edited Image"),
    title="Isha's Stylish Photo Editor",
    description="Enhance your photos and brand them with style!"
)

iface.launch() 

