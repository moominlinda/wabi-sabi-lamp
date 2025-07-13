
import gradio as gr
import os

# 載入預設動畫頁面
with open("lamp_template/index.html", "r") as f:
    default_html = f.read()

def fake_process(image):
    # 這是簡化版，只回傳預設動畫
    return "data.csv（模擬）", default_html

with gr.Blocks() as demo:
    gr.Markdown("# 🪔 Wabi-Sabi Mosaic → Lamp Animation (精簡版)")

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="上傳圖片")
            btn = gr.Button("產生動畫")
        with gr.Column():
            csv_output = gr.File(label="CSV（模擬）")
            html_output = gr.HTML(default_html, label="動畫預覽")

    btn.click(fn=fake_process, inputs=[image_input], outputs=[csv_output, html_output])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port, show_error=True, share=True)
