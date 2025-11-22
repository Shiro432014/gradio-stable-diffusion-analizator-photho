def segment(text, weight):
    if not text: return ""
    return f"({text}:{weight})"

def build_prompt(base_caption, character, pose, background, clothing,
                 w_char, w_pose, w_bg, w_cloth, extra_styles):
    parts = [base_caption,
             segment(character, w_char),
             segment(pose, w_pose),
             segment(f"{background} background", w_bg),
             segment(clothing, w_cloth)]
    if extra_styles:
        parts.extend(extra_styles)
    prompt = ", ".join([p for p in parts if p])
    neg = "low quality, blurry, bad anatomy, extra fingers, deformed, watermark, text"
    return prompt, neg
