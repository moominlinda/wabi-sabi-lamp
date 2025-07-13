
import gradio as gr
import numpy as np
import cv2
from PIL import Image
import pandas as pd
import os
import shutil
from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")

light_rgb = np.array([248, 232, 168])
dark_rgb = np.array([12, 12, 10])

def center_weight_mask(h, w):
    y, x = np.mgrid[0:h, 0:w]
    cx, cy = w / 2, h / 2
    sigma = 0.4 * min(h, w)
    gaussian = np.exp(-((x - cx)**2 + (y - cy)**2) / (2.0 * sigma**2))
    return gaussian / gaussian.max()

def generate_csv(image):
    image_np = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape
    mask = center_weight_mask(h, w)
    level = (gray / 255.0 * 9).astype(int)
    proportions = mask / mask.sum()
    data = []

    for y in range(h):
        for x in range(w):
            data.append({
                "X": x,
                "Y": y,
                "Level": level[y, x],
                "Proportion": round(float(proportions[y, x]), 6)
            })

    df = pd.DataFrame(data)
    output_csv = "output.csv"
    df.to_csv(output_csv, index=False)
    return output_csv

def generate_animation_site(csv_file):
    output_folder = "lamp_site_output"
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    shutil.copytree("lamp_template", output_folder)
    shutil.copy(csv_file, os.path.join(output_folder, "data.csv"))

    with open(os.path.join(output_folder, "index.html")) as f:
        html = f.read()
    return html

def process(image):
    csv_path = generate_csv(image)
    html_content = generate_animation_site(csv_path)
    return csv_path, html_content

# 初始預覽動畫（尚未上傳圖片時的預設動畫畫面）
with open("lamp_template/index.html", "r") as f:
    default_html = f.read()

with gr.Blocks() as demo:
    gr.Markdown("# 🪔 Wabi-Sabi Mosaic → Lamp Animation")

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="上傳圖片")
            btn = gr.Button("產生動畫")

        with gr.Column():
            csv_output = gr.File(label="CSV 檔案")
            html_output = gr.HTML(default_html, label="動畫預覽")

    btn.click(fn=process, inputs=[image_input], outputs=[csv_output, html_output])

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port, share=True, show_error=True)
