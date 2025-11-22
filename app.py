import gradio as gr
from PIL import Image
import tempfile
import socket
import requests

from captioning import generate_caption
from pose_clothing import analyze_pose_clothing
from prompt_builder import build_prompt
from sd_api import send_to_sd_txt2img
from utils import translate_ru_to_en

# импортируем функции истории
from history import save_prompt_to_history, read_history_table, find_by_id, clear_history


def make_tmp_txt(text: str) -> str:
    """Создать временный .txt и вернуть путь к файлу."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
    tmp.write(text or "")
    tmp.close()
    return tmp.name


# ====== Генерация ======
def on_process(image: Image.Image, style_extra, w_char, w_pose, w_bg, w_cloth, translate_ru):
    if image is None:
        empty_file = make_tmp_txt("Upload an image first.")
        return "Upload an image first.", "", "", "", "", "", "", empty_file

    base = generate_caption(image)

    if translate_ru:
        style_extra = translate_ru_to_en(style_extra)

    attrs = analyze_pose_clothing(base)

    prompt, neg = build_prompt(
        base_caption=base,
        character=attrs["character"],
        pose=attrs["pose"],
        background=attrs["background"],
        clothing=attrs["clothing"],
        w_char=w_char, w_pose=w_pose, w_bg=w_bg, w_cloth=w_cloth,
        extra_styles=[style_extra.strip()] if style_extra and style_extra.strip() else []
    )

    # автосохранение в историю
    save_prompt_to_history(prompt, neg)

    prompt_file_path = make_tmp_txt(prompt)

    return base, attrs["character"], attrs["pose"], attrs["background"], attrs["clothing"], prompt, neg, prompt_file_path


# ====== Отправка в SD WebUI ======

# ====== Отправка в SD WebUI + сохранение ======


#def send_to_sd(sd_url, prompt, neg):
    if not prompt:
        return "Prompt is empty"
    try:
        # Сохраняем в историю
        save_prompt_to_history(prompt, neg)

        # Отправляем только в поля WebUI (без генерации)
        payload = {
            "prompt": prompt,
            "negative_prompt": neg
        }
        r = requests.post(f"{sd_url}/sdapi/v1/options", json=payload)
        if r.status_code == 200:
            return "✅ Prompt and negative prompt saved to history and sent to SD UI fields."
        else:
            return f"❌ Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"❌ Error: {e}"


# ====== Интерфейс ======
with gr.Blocks(title="Photo → Prompt (EN)") as demo:
    gr.Markdown("# Photo → Prompt for Stable Diffusion (EN)")

    with gr.Row():
        with gr.Column():
            img = gr.Image(type="pil", image_mode="RGB", label="Upload photo")
            style_extra = gr.Textbox(label="Extra style (optional)")
            w_char = gr.Slider(0.5, 2.0, 1.2, step=0.05, label="Character weight")
            w_pose = gr.Slider(0.5, 2.0, 1.1, step=0.05, label="Pose weight")
            w_bg = gr.Slider(0.5, 2.0, 1.0, step=0.05, label="Background weight")
            w_cloth = gr.Slider(0.5, 2.0, 1.2, step=0.05, label="Clothing weight")
            translate_ru = gr.Checkbox(value=True, label="Translate Russian styles to English")
            btn = gr.Button("Generate")

        with gr.Column():
            base_out = gr.Textbox(label="Auto caption (EN)")
            char_out = gr.Textbox(label="Character")
            pose_out = gr.Textbox(label="Pose")
            bg_out = gr.Textbox(label="Background")
            cloth_out = gr.Textbox(label="Clothing")
            prompt_out = gr.Textbox(label="Final prompt")
            neg_out = gr.Textbox(label="Negative prompt")
            download = gr.DownloadButton(label="Download prompt.txt")

            copy_btn = gr.Button("Copy prompt")

    #gr.Markdown("### SD WebUI settings")
    #sd_url = gr.Textbox(value="http://127.0.0.1:7860", label="SD WebUI URL")
    #send_btn = gr.Button("Send to SD WebUI")
    #sd_status = gr.Textbox(label="SD status")

    # ====== Блок истории ======
    gr.Markdown("### Prompt history")
    with gr.Row():
        history_view = gr.Dataframe(
            headers=["ID", "Date", "Prompt", "Negative"],
            label="Prompt history",
            wrap=True
        )

    with gr.Row():
        clear_btn = gr.Button("Clear history")

    with gr.Row():
        search_id = gr.Textbox(label="Search by ID (e.g., 01)")
        search_btn = gr.Button("Find")
        search_result = gr.Textbox(label="Found Prompt", lines=10, max_lines=20)
        search_negative = gr.Textbox(label="Found Negative Prompt", lines=10, max_lines=20)

    # ====== Привязки ======
    btn.click(
        fn=on_process,
        inputs=[img, style_extra, w_char, w_pose, w_bg, w_cloth, translate_ru],
        outputs=[base_out, char_out, pose_out, bg_out, cloth_out, prompt_out, neg_out, download]
    )

    # обновление истории после генерации
    btn.click(fn=lambda *args: read_history_table(), inputs=[], outputs=[history_view])

    #send_btn.click(
        #fn=send_to_sd,
        #inputs=[sd_url, prompt_out, neg_out],
        #outputs=[sd_status]
    #)

    def copy_prompt(p):
        return p
    copy_btn.click(fn=copy_prompt, inputs=[prompt_out], outputs=[prompt_out])

    clear_btn.click(fn=clear_history, inputs=[], outputs=[history_view])

    search_btn.click(fn=find_by_id, inputs=[search_id], outputs=[search_result, search_negative])

    # загрузка истории при старте
    demo.load(fn=lambda: read_history_table(), inputs=None, outputs=history_view)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 7862

    # Получаем локальный IP
    local_ip = socket.gethostbyname(socket.gethostname())

    print("======================================")
    print(" Photo → Prompt server starting...")
    print(f" Local URL:   http://{host}:{port}")
    print("======================================")

    demo.launch(server_name=host, server_port=port)