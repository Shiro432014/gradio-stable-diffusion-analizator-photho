CLOTHING = ["dress","shirt","t-shirt","jacket","coat","hoodie","sweater","skirt","pants","jeans","shorts","suit","armor","kimono"]
POSE = ["standing","sitting","walking","running","jumping","kneeling","lying","portrait","close-up","profile","looking at camera","hands on hips","arms crossed"]
BACKGROUND = ["forest","street","city","room","studio","beach","mountain","night","sunset","indoor","outdoor","snow","rain","sky"]
CHARACTER_HINTS = ["woman","man","girl","boy","person","character","warrior","mage","cyborg","elf","soldier","model"]

def extract_attributes(caption: str):
    low = caption.lower()
    def find_any(words): return ", ".join(sorted(set([w for w in words if w in low])))
    clothing = find_any(CLOTHING)
    pose = find_any(POSE)
    background = find_any(BACKGROUND)
    char = find_any(CHARACTER_HINTS)
    if not char:
        if "portrait" in low or "close-up" in low:
            char = "character"
        elif "woman" in low or "girl" in low:
            char = "woman"
        elif "man" in low or "boy" in low:
            char = "man"
        else:
            char = "person"
    return {
        "character": char,
        "pose": pose or "standing",
        "background": background or "studio",
        "clothing": clothing or "casual outfit"
    }
