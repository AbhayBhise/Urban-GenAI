import re

tex_path = "docs/IEEE_Conference_Paper.tex"

with open(tex_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract bibitems in order
bibitem_pattern = re.compile(r"\\bibitem\{([^}]+)\}")
bibitems = bibitem_pattern.findall(content)

print(f"Total bibitems in thebibliography: {len(bibitems)}")

# Find all citations in body text before thebibliography
body_text = content.split(r"\begin{thebibliography}")[0]
cite_pattern = re.compile(r"\\cite\{([^}]+)\}")
raw_cites = cite_pattern.findall(body_text)

# Flatten and preserve first occurrence
seen = []
for cite_group in raw_cites:
    keys = [k.strip() for k in cite_group.split(",")]
    for k in keys:
        if k not in seen:
            seen.append(k)

print(f"Total unique citations in text: {len(seen)}")

# Compare order
mismatch = False
for idx, (text_key, bib_key) in enumerate(zip(seen, bibitems), 1):
    status = "OK" if text_key == bib_key else "MISMATCH"
    if status == "MISMATCH":
        mismatch = True
    print(f"[{idx:02d}] Text: {text_key:<28} | Bib: {bib_key:<28} -> {status}")

if not mismatch and len(seen) == len(bibitems) == 40:
    print("\nPERFECT: All 40 citations are strictly serial and match 1-to-1!")
else:
    print("\nCHECK NEEDED!")
