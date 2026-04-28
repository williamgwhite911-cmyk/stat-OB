#!/usr/bin/env python3
"""
StatFlight protocol merger — self-service.

What it does
------------
Looks at every subfolder inside the same directory as this script
(e.g. protocols/cardiac/, protocols/trauma/, protocols/medical/...)
and merges all the PDFs / JPEGs / PNGs in each subfolder into a
single chapter PDF named PHI_<FolderName>.pdf in the protocols/ root.

How to use
----------
1. Drop your per-page files (PDF or image) into a subfolder named
   after the chapter:
       protocols/cardiac/    (any PDFs/JPEGs in here, names ending in a number)
       protocols/trauma/
       protocols/medical/

2. From a terminal:
       cd path/to/statflight/protocols
       python3 merge.py

3. The script writes:
       PHI_Cardiac.pdf
       PHI_Trauma.pdf
       PHI_Medical.pdf
       ...

4. Commit and push:
       git add PHI_*.pdf
       git commit -m "Refresh merged protocol chapters"
       git push

Requires pypdf and Pillow (auto-installs on first run if missing).
"""
import os
import re
import sys
import subprocess

SUPPORTED_EXT = (".pdf", ".jpg", ".jpeg", ".png")


def ensure_deps():
    needed = []
    try:
        import pypdf  # noqa
    except ImportError:
        needed.append("pypdf")
    try:
        from PIL import Image  # noqa
    except ImportError:
        needed.append("Pillow")
    if not needed:
        return
    print(f"Installing missing dependencies: {', '.join(needed)} ...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet"] + needed)
    except Exception:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "--user"] + needed)


def trailing_num(name: str) -> int:
    base = os.path.splitext(name)[0]
    m = re.search(r"(\d+)$", base)
    return int(m.group(1)) if m else 10**9


def chapter_label(folder: str) -> str:
    parts = re.split(r"[-_\s]+", folder.strip())
    return "".join(p.capitalize() for p in parts if p)


def image_to_pdf_bytes(img_path: str) -> bytes:
    from PIL import Image
    import io
    im = Image.open(img_path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGB")
    buf = io.BytesIO()
    im.save(buf, format="PDF", resolution=150.0)
    return buf.getvalue()


def merge_chapter(src_dir: str, out_path: str) -> dict:
    from pypdf import PdfReader, PdfWriter
    import io

    files = [
        f for f in os.listdir(src_dir)
        if f.lower().endswith(SUPPORTED_EXT) and not f.startswith(".")
    ]
    files.sort(key=trailing_num)
    if not files:
        return {"pages": 0, "files": []}

    writer = PdfWriter()
    toc = []
    page_count = 0

    for fname in files:
        full = os.path.join(src_dir, fname)
        ext = os.path.splitext(fname)[1].lower()
        try:
            if ext == ".pdf":
                reader = PdfReader(full)
            else:
                pdf_bytes = image_to_pdf_bytes(full)
                reader = PdfReader(io.BytesIO(pdf_bytes))
        except Exception as e:
            print(f"  ! skipping unreadable file {fname}: {e}")
            continue

        for p in reader.pages:
            writer.add_page(p)
            page_count += 1
            try:
                text = (p.extract_text() or "").strip() if ext == ".pdf" else ""
                snip = " ".join(text.split())[:120] if text else f"[image page from {fname}]"
            except Exception:
                snip = f"[page from {fname}]"
            toc.append((page_count, fname, snip))

    if page_count == 0:
        return {"pages": 0, "files": []}

    with open(out_path, "wb") as fh:
        writer.write(fh)

    return {"pages": page_count, "files": files, "toc": toc}


def main():
    ensure_deps()
    here = os.path.dirname(os.path.abspath(__file__))
    print(f"Scanning {here} for chapter folders...\n")

    subfolders = sorted([
        d for d in os.listdir(here)
        if os.path.isdir(os.path.join(here, d)) and not d.startswith(".")
    ])

    if not subfolders:
        print("No subfolders found. Drop chapter folders here and run again.")
        return

    merged_count = 0
    for folder in subfolders:
        src = os.path.join(here, folder)
        label = chapter_label(folder)
        out_path = os.path.join(here, f"PHI_{label}.pdf")
        print(f"Merging {folder}/ -> PHI_{label}.pdf")
        stats = merge_chapter(src, out_path)
        if stats["pages"] == 0:
            print(f"  (no PDFs/images found in {folder}/, skipped)\n")
            continue
        size_kb = os.path.getsize(out_path) / 1024
        print(f"  {stats['pages']} pages, {size_kb:.0f} KB")
        starts = [t for t in stats["toc"]
                  if re.search(r"\b\d+\.\d+\b\s", t[2]) and t[0] <= stats["pages"]]
        if starts:
            print("  Section starts detected:")
            for new_pg, fname, snip in starts[:30]:
                print(f"    p.{new_pg:3d}  {snip[:90]}")
        print()
        merged_count += 1

    if merged_count:
        print(f"Done. Wrote {merged_count} chapter PDF(s).")
        print("Next step:")
        print("  git add PHI_*.pdf")
        print("  git commit -m 'Refresh merged protocol chapters'")
        print("  git push")
    else:
        print("No PDFs were merged. Make sure each chapter folder has files inside.")


if __name__ == "__main__":
    main()
