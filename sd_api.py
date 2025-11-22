import requests

def send_to_sd_txt2img(base_url, prompt, negative_prompt, steps=20, cfg_scale=7.0,
                       width=512, height=512, sampler_name="Euler", seed=-1):
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "width": width,
        "height": height,
        "sampler_name": sampler_name,
        "seed": seed
    }
    r = requests.post(f"{base_url}/sdapi/v1/txt2img", json=payload, timeout=60)
    r.raise_for_status()
    return r.json()
