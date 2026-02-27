#!/usr/bin/env python3
"""Make the dark square background transparent; keep the circular logo."""
from PIL import Image
import sys

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "assets/logo.png"
    out = sys.argv[2] if len(sys.argv) > 2 else "assets/logo-nobg.png"
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    data = img.getdata()

    # Sample background from corners (the dark grey square)
    corners = [data[0], data[w - 1], data[(h - 1) * w], data[(h - 1) * w + w - 1]]
    def rgb(c):
        return (c[0], c[1], c[2])
    # Use top-left as reference; allow some tolerance
    r0, g0, b0 = rgb(corners[0])
    tol = 25  # color tolerance

    new_data = []
    for i, px in enumerate(data):
        r, g, b, a = px
        if abs(r - r0) <= tol and abs(g - g0) <= tol and abs(b - b0) <= tol:
            new_data.append((r, g, b, 0))
        else:
            new_data.append(px)

    img.putdata(new_data)
    img.save(out, "PNG")
    print("Saved:", out)

if __name__ == "__main__":
    main()
