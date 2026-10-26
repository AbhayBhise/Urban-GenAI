import os
import shutil

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def move_if_exists(src, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    if os.path.exists(src):
        dest = os.path.join(dest_dir, os.path.basename(src))
        shutil.move(src, dest)
        print(f"Moved: {os.path.relpath(src, REPO_ROOT)} -> {os.path.relpath(dest, REPO_ROOT)}")

def organize():
    archive_dir = os.path.join(REPO_ROOT, "archive")
    pres_dir = os.path.join(archive_dir, "presentations")
    logs_dir = os.path.join(archive_dir, "runtime_logs")
    notebooks_dir = os.path.join(archive_dir, "notebooks")
    scratch_dir = os.path.join(archive_dir, "scratch_debug_assets")

    # 1. Presentations & Deliverables
    presentations = [
        "UrbanGenAI_Presentation.pptx",
        "UrbanGenAI_Professor_Presentation.pptx",
        "UrbanGenAI_Professor_Presentation_Updated.pptx",
        "UrbanGenAI_ppt.pptx",
        "UrbanGenAI_Demo_Script.docx",
        "UrbanGenAI_Presenter_Script.md",
        "2022_REVISION _(2.0)_COMP_SYLLABUS.pdf"
    ]
    for p in presentations:
        move_if_exists(os.path.join(REPO_ROOT, p), pres_dir)

    # 2. Notebooks
    notebooks = [
        "Untitled0.ipynb"
    ]
    for nb in notebooks:
        move_if_exists(os.path.join(REPO_ROOT, nb), notebooks_dir)

    # 3. Root Runtime Logs
    logs = [
        "api.log",
        "frontend.log",
        "train_ae_unet.log",
        "train_gan.log",
        "train_vae_perceptual.log"
    ]
    for lg in logs:
        move_if_exists(os.path.join(REPO_ROOT, lg), logs_dir)

    # 4. Backend temporary debug images & test scripts
    backend_dir = os.path.join(REPO_ROOT, "backend")
    if os.path.exists(backend_dir):
        for item in os.listdir(backend_dir):
            if item.startswith("scratch_") or item.startswith("test_") or item.startswith("live_api_") or item == "gputest_inbackend.py":
                full_p = os.path.join(backend_dir, item)
                if os.path.isfile(full_p):
                    move_if_exists(full_p, scratch_dir)

    # 5. Create archive README
    readme_path = os.path.join(archive_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("""# UrbanGen AI — Archived Deliverables & Artifacts

This directory stores non-core, historical, and presentation deliverables to maintain a clean and professional repository root.

## 📁 Directory Structure

- **`presentations/`**: Contains academic evaluation presentations, slide decks, speech scripts, and syllabus reference documents:
  - `UrbanGenAI_Professor_Presentation_Updated.pptx`: Comprehensive 18-slide deck for academic defense.
  - `UrbanGenAI_Professor_Presentation.pptx`, `UrbanGenAI_Presentation.pptx`, `UrbanGenAI_ppt.pptx`: Previous versions of presentation slide decks.
  - `UrbanGenAI_Demo_Script.docx`, `UrbanGenAI_Presenter_Script.md`: Demonstration presenter scripts.
  - `2022_REVISION _(2.0)_COMP_SYLLABUS.pdf`: Academic reference curriculum.
- **`notebooks/`**: Exploratory data ingestion and STAC/Planetary Computer experimental notebooks (`Untitled0.ipynb`).
- **`runtime_logs/`**: Raw training and development execution logs (`api.log`, `frontend.log`, `train_*.log`).
- **`scratch_debug_assets/`**: Intermediate visual verification images and quick test routines generated during model validation.

All active research code, benchmark figures, trained model checkpoints, and publication assets remain in their primary directories (`backend/`, `frontend/`, `docs/`, `outputs/`, `paper_package/`).
""")
    print("Created archive/README.md")

if __name__ == "__main__":
    organize()
