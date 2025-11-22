import re

POSE_PATTERNS = {
    "standing": r"\bstand(ing)?\b",
    "sitting": r"\bsit(ting)?\b",
    "walking": r"\bwalk(ing)?\b",
    "running": r"\brun(ning)?\b",
    "kneeling": r"\bkneel(ing)?\b",
    "lying": r"\blying\b|\blie\b",
    "portrait": r"\bportrait\b",
    "close-up": r"\bclose[- ]?up\b",
    "profile": r"\bprofile\b",
    "looking at camera": r"looking at camera",
    "arms crossed": r"arms crossed",
    "hands on hips": r"hands on hips"
}

CLOTHING_PATTERNS = {
    "dress": r"\bdress\b",
    "shirt": r"\bshirt\b",
    "jacket": r"\bjacket\b",
    "jeans": r"\bjeans\b",
    "suit": r"\bsuit\b",
    "hoodie": r"\bhoodie\b",
    "armor": r"\barmor\b",
    "kimono": r"\bkimono\b"
}

BACKGROUND_PATTERNS = {
    "forest": r"\bforest\b",
    "street": r"\bstreet\b",
    "city": r"\bcity\b",
    "room": r"\broom\b",
    "studio": r"\bstudio\b",
    "beach": r"\bbeach\b",
    "mountain": r"\bmountain\b",
    "night": r"\bnight\b",
    "sunset": r"\bsunset\b",
    "indoor": r"\bindoor\b",
    "outdoor": r"\boutdoor\b",
    "snow": r"\bsnow\b",
    "rain": r"\brain\b",
    "sky": r"\bsky\b"
}

def analyze_pose_clothing(caption: str):
    low = caption.lower()
    def match_any(patterns):
        return [k for k,v in patterns.items() if re.search(v, low)]
    return {
        "character": "person",
        "pose": ", ".join(match_any(POSE_PATTERNS)) or "standing",
        "background": ", ".join(match_any(BACKGROUND_PATTERNS)) or "studio",
        "clothing": ", ".join(match_any(CLOTHING_PATTERNS)) or "casual outfit"
    }
