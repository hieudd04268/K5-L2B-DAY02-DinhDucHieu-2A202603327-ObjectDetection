#!/usr/bin/env python3
"""Pre-label ảnh bằng YOLO và xuất file ZIP theo định dạng
"Ultralytics YOLO Detection 1.0" để import vào CVAT.

Cấu trúc ZIP sinh ra (đúng chuẩn CVAT - Tasks > Actions > Import dataset
hoặc Upload annotations với format "Ultralytics YOLO Detection 1.0"):

    archive.zip/
    ├── data.yaml            # path + train + names (đúng thứ tự class)
    ├── train.txt            # danh sách ảnh: images/<split>/<ten_anh>
    ├── images/<split>/...   # ảnh gốc (có thể bỏ bằng --no-images)
    └── labels/<split>/...   # mỗi ảnh một .txt: <id> <xc> <yc> <w> <h>

Ví dụ (chạy từ thư mục gốc repo):

    python tools/prelabel_yolo.py --weights yolo11n.pt
    python tools/prelabel_yolo.py --weights best.pt --conf 0.3
    python tools/prelabel_yolo.py --weights best.pt --images dataset/images/train \
        --output prelabel_output --split train

Lưu ý:
  - Tên class lấy từ data.yaml (car, truck, bus, van). Có thể ghi đè --names.
  - Dự đoán của model được map theo TÊN class; class không có trong schema bị bỏ.
  - Ảnh không có box vẫn được ghi file .txt rỗng (CVAT hiểu là ảnh nền).
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

APP_ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pre-label bằng YOLO, xuất ZIP chuẩn Ultralytics YOLO Detection 1.0 cho CVAT."
    )
    parser.add_argument("--weights", required=True, help="Đường dẫn model .pt (ví dụ yolo11n.pt / best.pt)")
    parser.add_argument("--images", default=str(APP_ROOT / "dataset" / "images" / "train"),
                        help="Thư mục ảnh đầu vào (mặc định dataset/images/train)")
    parser.add_argument("--output", default=str(APP_ROOT / "prelabel_output"),
                        help="Thư mục output riêng (mặc định prelabel_output/)")
    parser.add_argument("--data", default=str(APP_ROOT / "data.yaml"),
                        help="File data.yaml để lấy tên class (mặc định data.yaml)")
    parser.add_argument("--names", default=None,
                        help="Ghi đè tên class, cách nhau dấu phẩy (thứ tự = class id)")
    parser.add_argument("--split", default="train", help="Tên split trong ZIP (mặc định train)")
    parser.add_argument("--conf", type=float, default=0.25, help="Ngưỡng confidence (mặc định 0.25)")
    parser.add_argument("--iou", type=float, default=0.7, help="Ngưỡng IoU cho NMS (mặc định 0.7)")
    parser.add_argument("--imgsz", type=int, default=640, help="Kích thước ảnh khi infer (mặc định 640)")
    parser.add_argument("--device", default=None, help="Thiết bị: cpu, 0, ... (mặc định tự chọn)")
    parser.add_argument("--batch", type=int, default=16, help="Số ảnh mỗi lần infer (mặc định 16)")
    parser.add_argument("--no-images", action="store_true",
                        help="Không đóng gói ảnh vào ZIP (chỉ có data.yaml, train.txt, labels)")
    return parser.parse_args()


def load_names_from_data(data_file: Path) -> list[str] | None:
    if not data_file.is_file():
        return None
    try:
        import yaml
    except ImportError:
        return None
    try:
        data = yaml.safe_load(data_file.read_text(encoding="utf-8")) or {}
    except Exception:
        return None
    names = data.get("names")
    if isinstance(names, dict):
        return [str(names[k]) for k in sorted(names)]
    if isinstance(names, list):
        return [str(n) for n in names]
    return None


def model_class_names(model) -> dict[int, str]:
    names = getattr(model, "names", {}) or {}
    if isinstance(names, dict):
        return {int(k): str(v) for k, v in names.items()}
    return {i: str(v) for i, v in enumerate(names)}


def list_images(folder: Path) -> list[Path]:
    return sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS)


def write_data_yaml(names: list[str]) -> str:
    lines = ["path: .", "train: train.txt", "val: train.txt", "names:"]
    for idx, name in enumerate(names):
        lines.append(f"  {idx}: {name}")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()

    try:
        from ultralytics import YOLO
    except ImportError:
        print("Lỗi: chưa cài ultralytics. Chạy: pip install ultralytics")
        return 1

    images_dir = Path(args.images)
    if not images_dir.is_dir():
        print(f"Lỗi: không tìm thấy thư mục ảnh: {images_dir}")
        return 1

    images = list_images(images_dir)
    if not images:
        print(f"Lỗi: không có ảnh nào trong {images_dir}")
        return 1

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        model = YOLO(args.weights)
    except FileNotFoundError:
        print(f"Lỗi: không tìm thấy model: {args.weights}")
        print("Gợi ý: dùng model có sẵn hoặc tên model chính thức như 'yolo11n.pt' (tự tải).")
        return 1
    model_names = model_class_names(model)

    if args.names:
        target_names = [n.strip() for n in args.names.split(",") if n.strip()]
    else:
        target_names = load_names_from_data(Path(args.data))
        if not target_names:
            target_names = [model_names[k] for k in sorted(model_names)]

    name_to_id = {n: i for i, n in enumerate(target_names)}
    print(f"Classes ({len(target_names)}): {target_names}")
    print(f"Tìm thấy {len(images)} ảnh. Đang infer...")

    labels: dict[str, list[str]] = {}
    total_boxes = 0

    for start in range(0, len(images), args.batch):
        chunk = images[start:start + args.batch]
        results = model.predict(
            [str(p) for p in chunk],
            conf=args.conf,
            iou=args.iou,
            imgsz=args.imgsz,
            device=args.device,
            verbose=False,
        )
        for img_path, result in zip(chunk, results):
            h, w = result.orig_shape
            lines: list[str] = []
            if result.boxes is not None:
                for box in result.boxes:
                    model_cid = int(box.cls.item())
                    cls_name = model_names.get(model_cid, str(model_cid))
                    target_id = name_to_id.get(cls_name)
                    if target_id is None:
                        continue
                    x0, y0, x1, y1 = (float(v) for v in box.xyxy[0].tolist())
                    x0, x1 = max(0.0, min(w, x0)), max(0.0, min(w, x1))
                    y0, y1 = max(0.0, min(h, y0)), max(0.0, min(h, y1))
                    if x1 - x0 < 2 or y1 - y0 < 2:
                        continue
                    cx = (x0 + x1) / 2 / w
                    cy = (y0 + y1) / 2 / h
                    bw = (x1 - x0) / w
                    bh = (y1 - y0) / h
                    lines.append(f"{target_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")
            labels[img_path.name] = lines
            total_boxes += len(lines)
        print(f"  {min(start + args.batch, len(images))}/{len(images)}")

    split = args.split.strip("/\\") or "train"
    zip_path = out_dir / "prelabel_ultralytics_yolo.zip"
    train_lines = "\n".join(f"images/{split}/{name}" for name in labels) + "\n"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("data.yaml", write_data_yaml(target_names))
        zf.writestr("train.txt", train_lines)
        for name, lines in labels.items():
            label_name = f"{Path(name).stem}.txt"
            zf.writestr(f"labels/{split}/{label_name}", "\n".join(lines) + ("\n" if lines else ""))
        if not args.no_images:
            for src in images:
                zf.write(src, arcname=f"images/{split}/{src.name}")

    print("=" * 60)
    print(f"Xong: {len(labels)} ảnh, {total_boxes} box")
    print(f"ZIP: {zip_path}")
    print("Import vào CVAT: Tasks > Actions > Upload annotations (hoặc Import dataset)")
    print("Chọn format: 'Ultralytics YOLO Detection 1.0'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
