import os
import xml.etree.ElementTree as ET

def clean_svg_string(svg_text):
    # Replace undeclared HTML entities with valid XML entities / UTF-8 chars
    replacements = [
        ("&bull;", "&#8226;"),
        ("&times;", "&#215;"),
        ("&sigma;", "&#963;"),
        ("&rarr;", "&#8594;"),
        ("&in;", "&#8712;"),
        ("&Ropf;", "&#8477;"),
        ("&beta;", "&#946;"),
        ("&mu;", "&#956;"),
        ("&sup2;", "&#178;"),
        ("&sum;", "&#8721;"),
        ("&emsp;", "&#8195;"),
        ("<div style=\"display:flex;\">", ""),
        ("<div style='display:flex;'>", ""),
        ("</div>", ""),
        ("<b>", "<tspan font-weight=\"bold\">"),
        ("</b>", "</tspan>"),
    ]
    for old, new in replacements:
        svg_text = svg_text.replace(old, new)
    return svg_text

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    targets = [
        os.path.join(root, "docs", "poster", "figures", "clean_project_architecture.svg"),
        os.path.join(root, "docs", "poster", "figures", "pipeline_architecture_plantuml.svg"),
        os.path.join(root, "frontend", "public", "poster", "figures", "clean_project_architecture.svg"),
        os.path.join(root, "frontend", "public", "poster", "figures", "pipeline_architecture_plantuml.svg"),
    ]

    for p in targets:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            cleaned = clean_svg_string(content)
            # Verify with XML parser
            try:
                ET.fromstring(cleaned)
                print(f"[SUCCESS] Valid XML verified for: {p}")
                with open(p, "w", encoding="utf-8") as f:
                    f.write(cleaned)
            except Exception as e:
                print(f"[ERROR] Failed XML parsing for {p}: {e}")

if __name__ == "__main__":
    main()
