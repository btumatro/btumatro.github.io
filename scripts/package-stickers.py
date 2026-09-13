"""Sticker görsellerini, istemleri ve kaynakları tekrar paketler."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
docs = root / "docs/sticker-paketi"
with ZipFile(docs / "matro-sticker-paketi.zip", "w", ZIP_DEFLATED) as archive:
    for path in sorted((root / "public/media/stickers").rglob("*")):
        if path.is_file():
            archive.write(path, "assets/" + str(path.relative_to(root / "public/media/stickers")))
    for path in sorted(docs.rglob("*")):
        if path.is_file() and path.suffix in {".md", ".txt", ".json", ".ai", ".pdf"}:
            archive.write(path, "kaynaklar/" + str(path.relative_to(docs)))
    for name in ["logo-btu.png", "logo-matro-siyah.png", "matro-logo-siyah.svg"]:
        archive.write(root / "public" / name, "kaynaklar/logolar/" + name)
    archive.write(__file__, "scripts/package-stickers.py")
    archive.write(root / "scripts/build-brand-stickers.mjs", "scripts/build-brand-stickers.mjs")
    for name in ["logo-matro-mavi.png", "logo-matro-beyaz.png"]:
        archive.write(root / "public" / name, "kaynaklar/logolar/" + name)
print(docs / "matro-sticker-paketi.zip")
