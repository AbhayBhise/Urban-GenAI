import urllib.request
import zlib
from PIL import Image

def encode_plantuml(text: str) -> str:
    mapping = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    compressed = zlib.compress(text.encode("utf-8"))[2:-4]
    res = []
    for i in range(0, len(compressed), 3):
        b1 = compressed[i]
        b2 = compressed[i+1] if i+1 < len(compressed) else 0
        b3 = compressed[i+2] if i+2 < len(compressed) else 0
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        res.append(mapping[c1]); res.append(mapping[c2])
        res.append(mapping[c3] if i+1 < len(compressed) else "0")
        res.append(mapping[c4] if i+2 < len(compressed) else "0")
    return "".join(res)

with open("C:/Users/HP/.gemini/antigravity/brain/7a2c521c-9251-41f2-b44d-f0b19d5fe7c6/scratch/generate_all_plantuml.py", "r", encoding="utf-8") as f:
    code = f.read()

start = code.find('PIPELINE_PLANTUML = """') + len('PIPELINE_PLANTUML = """')
end = code.find('"""', start)
puml = code[start:end].strip()

enc = encode_plantuml(puml)
url = f"https://www.plantuml.com/plantuml/png/{enc}"
req = urllib.request.Request(url, headers={"User-Agent": "UrbanGenAI/1.0"})
with urllib.request.urlopen(req, timeout=30) as r:
    data = r.read()

with open("scratch_orig_puml.png", "wb") as f:
    f.write(data)

im = Image.open("scratch_orig_puml.png")
print("Original PIPELINE_PLANTUML size:", im.size)

