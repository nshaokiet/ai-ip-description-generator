"""Reproduce AC-02 from hash-verified public scan pixels and PDF coordinates.

Usage: measure_p2_006_references.py SOURCE_DIR [--verify COMMITTED_JSON]
       [--compare SYNTHETIC_QA_DIR]
No network, renderer input, invention text extraction or source artwork ingestion.
Only geometry is serialized; public screenshots stay in the temporary QA directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from statistics import median
import subprocess

from PIL import Image, ImageDraw
from pypdf import PdfReader
from pypdf.generic import ContentStream

REFERENCES = {
    "US11367264": {
        "url": "https://patentimages.storage.googleapis.com/91/f6/9b/18dc2af29220c8/US11367264.pdf",
        "sha256": "6f30294a48e11e22f28e8fbfd5eb3c6f3dbe28c391bac54f1f763e565d0170bf",
        "pages": 33, "body_page": 20, "drawing_page": 2,
        "title_band": [95, 120, 295, 160],
        "heading_band": [95, 348, 285, 363],
        "prose_band": [75, 168, 295, 249],
        "abstract_band": [309, 318, 530, 468],
    },
    "US11044591": {
        "url": "https://patentimages.storage.googleapis.com/42/19/af/1c5089854ab9d4/US11044591.pdf",
        "sha256": "712a1eca1b98d49bd2ef7482412f496fc1e612044484b5c0b2f1a3e3bb7642c7",
        "pages": 19, "body_page": 10, "drawing_page": 3,
        "title_band": [95, 120, 295, 151],
        "heading_band": [145, 122, 225, 136],
        "prose_band": [75, 146, 295, 205],
        "abstract_band": [309, 358, 530, 496],
    },
}


def pixel_window(box, sx, sy, offset_x=0):
    return tuple(round(v) for v in ((box[0]-offset_x)/sx, box[1]/sy,
                                   (box[2]-offset_x)/sx, box[3]/sy))


def geometry(image, box, sx, sy, offset_x=0):
    """Threshold=128; axis-aligned visible ink box, not nominal font metrics."""
    window = pixel_window(box, sx, sy, offset_x)
    mask = image.convert("L").crop(window).point(lambda p: 255 if p < 128 else 0)
    bounds = mask.getbbox()
    if bounds is None:
        raise ValueError("Empty measurement window")
    bbox = [round((bounds[0]+window[0])*sx+offset_x, 2),
            round((bounds[1]+window[1])*sy, 2),
            round((bounds[2]+window[0])*sx+offset_x, 2),
            round((bounds[3]+window[1])*sy, 2)]
    projection = mask.getprojection()[1]
    runs, start = [], None
    for y, present in enumerate(projection + [0]):
        if present and start is None:
            start = y
        elif not present and start is not None:
            if y-start >= 3:
                runs.append((start, y))
            start = None
    centers = [(a+b)/2*sy for a,b in runs]
    return {"window_pt": box, "ink_bbox_pt": bbox,
            "width_pt": round(bbox[2]-bbox[0], 2),
            "height_pt": round(bbox[3]-bbox[1], 2),
            "ink_row_run_heights_pt": [round((b-a)*sy, 2) for a,b in runs],
            "row_center_steps_pt": [round(b-a, 2) for a,b in zip(centers, centers[1:])],
            "row_count": len(runs)}


def scan(reader, index):
    page = reader.pages[index]
    images = list(page.images)
    if len(images) != 1 or images[0].image.size != (2560, 3300):
        raise ValueError("Unexpected reference scan representation")
    operations = ContentStream(page.get_contents(), reader).operations
    # Verify actual visible image placement, rather than assuming MediaBox scaling.
    drawing = next(i for i, (_, op) in enumerate(operations) if op == b"Do")
    matrices = [list(map(float, values)) for values, op in operations[:drawing] if op == b"cm"]
    if matrices != [[614.4, 0.0, 0.0, 792.0, -1.2, 0.0]]:
        raise ValueError("Reference image transform changed")
    if list(map(float, page.mediabox)) != [0.0, 0.0, 612.0, 792.0] or page.rotation:
        raise ValueError("Reference page box/rotation changed")
    return images[0].image, {"pdf_page": index+1, "mediabox_pt": [0,0,612,792],
                              "scan_pixels": [2560,3300], "image_matrix": matrices[0]}


def measure(root):
    result = {"version": "1.0.0", "method": "visible-scan-ink-threshold-128",
              "coordinate_system": "points; top-left origin; x=0.24*pixel_x-1.2; y=0.24*pixel_y",
              "uncertainty_pt": 0.48, "references": {}}
    for name, config in REFERENCES.items():
        path = root / (name+".pdf")
        if hashlib.sha256(path.read_bytes()).hexdigest() != config["sha256"]:
            raise ValueError("Reference hash mismatch: "+name)
        reader = PdfReader(path)
        if len(reader.pages) != config["pages"]:
            raise ValueError("Reference page count mismatch")
        cover, cover_info = scan(reader, 0)
        body, body_info = scan(reader, config["body_page"]-1)
        drawing, drawing_info = scan(reader, config["drawing_page"]-1)
        def g(image, box):
            return geometry(image, box, .24, .24, -1.2)
        cover_bottom = 490 if name == "US11367264" else 517
        regions = {
            "cover_left_fields": g(cover, [70,115,295,cover_bottom]),
            "cover_right_fields": g(cover, [309,115,535,cover_bottom]),
            "cover_rule": g(cover, [70,103,535,107]),
            "cover_title": g(cover, config["title_band"]),
            "cover_abstract": g(cover, config["abstract_band"]),
            "body_left": g(body, [70,80,295,752]),
            "body_right": g(body, [309,80,535,752]),
            "body_title": g(body, [95,82,280,125] if name=="US11367264" else [105,82,275,113]),
            "body_heading": g(body, config["heading_band"]),
            "body_prose": g(body, config["prose_band"]),
            "body_line_numbers": g(body, [297,120,307,735]),
            "drawing_ink": g(drawing, [60,90,555,750]),
        }
        l, r = regions["body_left"]["ink_bbox_pt"], regions["body_right"]["ink_bbox_pt"]
        cl, cr = regions["cover_left_fields"]["ink_bbox_pt"], regions["cover_right_fields"]["ink_bbox_pt"]
        result["references"][name] = {
            "source_url": config["url"], "sha256": config["sha256"],
            "page_count": len(reader.pages), "cover": cover_info,
            "first_body": body_info, "drawing_observation_only": drawing_info,
            "regions": regions,
            "body_margins_pt": {"left": l[0], "right": round(612-r[2],2),
                                "top": min(l[1],r[1]), "bottom": round(792-max(l[3],r[3]),2)},
            "body_ink_gutter_pt": round(r[0]-l[2], 2),
            "cover_ink_gutter_pt": round(cr[0]-cl[2], 2),
            "prose_median_row_pitch_pt": round(median(regions["body_prose"]["row_center_steps_pt"]),2),
            "line_number_median_pitch_pt": round(median(regions["body_line_numbers"]["row_center_steps_pt"]),2),
            "font_family_and_nominal_point_size": "NOT MEASURABLE: visible raster scan; Courier is invisible OCR, not the visible serif font",
        }
    return result


def comparisons(root, qa):
    """Separate public-source QA montages; never become generated draft pages."""
    structures = {}
    for profile in ("B2_REFERENCE_PREVIEW", "USPTO_APPLICATION_DRAFT"):
        for engine in ("NATIVE", "LO"):
            suffix = "p02" if profile == "B2_REFERENCE_PREVIEW" else "cover"
            path = qa / f"{profile}-{engine}-{suffix}.png"
            image = Image.open(path)
            sx, sy = 612/image.width, 792/image.height
            boxes = ([[50,65,306,736], [325,65,565,736]] if profile == "B2_REFERENCE_PREVIEW"
                     else [[70,65,560,736]])
            regions = [geometry(image, box, sx, sy) for box in boxes]
            structures[profile+"-"+engine] = {
                "measured_screenshot": path.name, "pdf_page": 2 if suffix == "p02" else 1,
                "page_pt": [612,792], "regions": regions,
                "ink_gutter_pt": round(regions[1]["ink_bbox_pt"][0]-regions[0]["ink_bbox_pt"][2],2)
                if len(regions)==2 else None,
                "warning": "Ink extents are occupied sample bounds, not nominal frame/font metrics",
            }
    (root/"synthetic-structure.json").write_text(json.dumps(structures,indent=2)+"\n")
    for name, config in REFERENCES.items():
        for role, page_number, suffix in (("cover",1,"cover"),("body",config["body_page"],"p02")):
            source = root / f"{name}-{role}.png"
            subprocess.run(["pdftoppm", "-f", str(page_number), "-l", str(page_number),
                            "-r", "300", "-singlefile", "-png", str(root/(name+".pdf")),
                            str(source.with_suffix(""))], check=True, capture_output=True)
            for profile in ("B2_REFERENCE_PREVIEW", "USPTO_APPLICATION_DRAFT"):
                for engine in ("NATIVE", "LO"):
                    output = qa / f"{profile}-{engine}-{suffix}.png"
                    panels = [Image.open(source).convert("RGB"), Image.open(output).convert("RGB")]
                    canvas = Image.new("RGB", (1700,1150), "white")
                    draw = ImageDraw.Draw(canvas)
                    labels = [f"{name} PDF p.{page_number}: PUBLIC REFERENCE ONLY",
                              f"P2-006 {profile} - {engine} p.{1 if role=='cover' else 2}"]
                    for i, panel in enumerate(panels):
                        canvas.paste(panel.resize((850,1100)), (850*i,50))
                        draw.text((850*i+8,15), labels[i], fill="black")
                    canvas.save(root/f"{name}-{role}-vs-{profile}-{engine}.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args()
    data = measure(args.source_dir)
    if args.verify and json.loads(args.verify.read_text()) != data:
        raise ValueError("Committed measurement evidence differs from verified source geometry")
    target = args.source_dir/"reference-measurements.json"
    target.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    if args.compare:
        comparisons(args.source_dir,args.compare)
    print("AC-02: both hash-verified sources measured; geometry evidence:",target)


if __name__ == "__main__":
    main()
