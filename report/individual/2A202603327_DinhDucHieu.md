# Báo cáo cá nhân — Ngày 2 Object Detection

## 1. Thông tin học viên

- Họ tên: Đinh Đức Hiếu
- MSSV: 2A202603327
- Email: 26ai.hieudd3@vinuni.edu.vn
- Lớp: L2B
- Link repo bài làm: https://github.com/hieudd04268/K5-L2B-DAY02-DinhDucHieu-2A202603327-ObjectDetection.git
- Link Colab đã chạy: https://colab.research.google.com/drive/1kfnoAxS_Dfl_4UnCO_n5d0zQYCltv_rZ?usp=sharing

## 2. Schema và mini guideline

Dẫn tới [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md). Schema 4 lớp trong `data.yaml`: `0 car`, `1 truck`, `2 bus`, `3 van`. Thứ tự phân biệt: kiểu thân xe → số chỗ → kích thước; không phân loại theo màu, hãng hay độ sang. `car` gồm sedan/hatchback/SUV/CUV/MPV 7–9 chỗ dùng cửa bản lề; `van` là one-box thùng kín liền khối, cửa trượt; `truck` có ca-bin tách khỏi khoang chở hàng; `bus` là thân chuyên dụng chở khách, nhiều cửa sổ hành khách và cửa lên xuống lớn, thường từ 10 chỗ.

Ba ca mơ hồ đã quyết định:

- `drive_058`: cảnh có 1 bus và 6 van/minivan cỡ lớn. Xe thân bus dài, nhiều cửa sổ hành khách, cửa lên xuống lớn → `bus`; các xe one-box, cửa trượt → `van`.
- `drive_053`: có 1 truck và 2 van; xe thùng kín cỡ nhỏ hoặc bán tải có nắp thùng dễ nhầm. Xe có ca-bin tách khỏi khoang hàng → `truck`; xe one-box liền khối → `van`.
- `drive_052`: có 1 truck, 1 van và nhiều car. SUV/MPV 7 chỗ cửa bản lề, có ca-pô → `car`; minivan cửa trượt, thân one-box → `van`.

Phần cần giảng viên làm rõ: (1) Transit/Hiace 16 chỗ cải tạo thành xe khách chuyên dụng xếp `van` hay `bus`; (2) pickup có nắp thùng kín xếp `truck` hay `van`; (3) ngưỡng vật thể rất nhỏ/bị che (cạnh ngắn khoảng 12 px hoặc diện tích khoảng 0,15% ảnh) khi chỉ còn một mảnh không đủ nhận diện lớp.

## 3. Annotation và self-QC

- Số file nhãn train: 50 file, 1.616 dòng; 876 box unique sau khi bỏ 740 dòng trùng text. Theo thứ tự lưu hiện tại: car 741, bus 23, van 78, truck 34; nếu remap sang schema: car 741, truck 34, bus 23, van 78.
- Kết quả checker và lỗi đã xử lý: `ĐẠT cấu trúc: 50/50 file nhãn hợp lệ. Chờ ground truth để chấm chất lượng.` Lỗi `UnicodeEncodeError: 'charmap' codec ...` trên Windows được xử lý bằng `$env:PYTHONIOENCODING="utf-8"`; không còn lỗi format.
- Danh sách ít nhất 10 ảnh đã rà bằng mắt: `drive_003`, `drive_006`, `drive_009`, `drive_012`, `drive_015`, `drive_024`, `drive_026`, `drive_027`, `drive_030`, `drive_050`.
- Lỗi bỏ sót/box/class phát hiện khi rà và cách sửa:

Số TP/FP/FN dưới đây lấy từ `outputs/annotation_evaluation.json` (trước sửa). Phần "lỗi chính" dùng đối chiếu class sau remap để đọc đúng tên lớp; không phải nhãn đã được sửa.

| Ảnh | Gold / Student | TP / FP / FN trước sửa | Lỗi chính và cách sửa |
|---|---:|---:|---|
| `drive_003` | 18 / 54 | 13 / 41 / 5 | 25 dòng trùng; 1 cặp van/truck trùng; car thừa; thiếu 1 bus. Bỏ duplicate, giữ box đúng, thêm bus nếu thấy. |
| `drive_006` | 21 / 56 | 19 / 37 / 2 | 28 dòng trùng; chỉ có car, thiếu 1 bus + 1 van; car thừa. Bỏ duplicate, thêm bus/van. |
| `drive_009` | 21 / 48 | 7 / 41 / 14 | 21 dòng trùng; 7 box van nhưng gold là truck; thiếu 1 bus; car thừa. Sửa truck → van theo ca-bin/thùng. |
| `drive_012` | 23 / 64 | 18 / 46 / 5 | 28 dòng trùng; car/van thừa; thiếu 3 bus; truck lệch 1. Bỏ box thừa, thêm bus/truck. |
| `drive_015` | 12 / 17 | 6 / 11 / 6 | 7 dòng trùng; 1 cặp bus/car trùng; thiếu 3 car + 1 truck. Bỏ duplicate, thêm car/truck. |
| `drive_024` | 30 / 50 | 14 / 36 / 16 | 23 dòng trùng; thiếu 2 car + 3 bus; 2 van thừa. Thêm box thiếu, bỏ van sai. |
| `drive_026` | 39 / 57 | 22 / 35 / 17 | 25 dòng trùng; 6 truck bị gọi van; thiếu car; 1 bus thừa. Sửa van → truck, thêm car. |
| `drive_027` | 31 / 56 | 19 / 37 / 12 | 25 dòng trùng; 1 cặp car/truck trùng; thiếu 3 bus; 2 van thừa. Bỏ duplicate, thêm bus, bỏ van sai. |
| `drive_030` | 20 / 69 | 14 / 55 / 6 | 32 dòng trùng; 32 car so với 16 gold; thiếu 3 bus; truck/van lệch. Bỏ box car thừa/trùng, thêm bus. |
| `drive_050` | 18 / 66 | 14 / 52 / 4 | 32 dòng trùng; 32 car so với 16 gold; thiếu 1 bus; 1 van thừa. Bỏ box car thừa/trùng, thêm bus. |

- Commit khóa nhãn ban đầu: `f5a17aa` (export annotation from CVAT); bản dùng cho lần chạy Colab là `1e225c7` (v2).

## 4. Gold QC và rework

| Chỉ số | Trước sửa | Sau sửa nếu có |
|---|---:|---:|
| TP | 441 | — |
| FP | 1175 | — |
| FN | 212 | — |
| Precision | 0.2729 | — |
| Recall | 0.6753 | — |
| F1 | 0.3887 | — |
| mean_iou_of_matches | 0.8452 | — |
| passed | false | — |

Dẫn tới [`outputs/annotation_evaluation.json`](../../outputs/annotation_evaluation.json) trong repo. Trong phạm vi bài nộp em **chưa rework** ghi đè nhãn và **chưa tạo** `outputs/annotation_evaluation_after_rework.json`, nên cột "Sau sửa" để trống. Không có kết quả rework chính thức để báo cáo.

Phân tích lỗi (không ghi đè nhãn): 740 dòng trùng text; 3 cặp box trùng khác class (`drive_003` van/truck, `drive_015` bus/car, `drive_027` car/truck) và 1 cặp cùng class (`drive_040`); thứ tự ID lưu là `car, bus, van, truck`. Nếu remap `{0:0, 1:2, 2:3, 3:1}` và bỏ 4 box trùng gần (IoU ≥ 0.95), còn 872 box; mô phỏng cho TP 533, FP 339, FN 120, P 0.6112, R 0.8162, F1 0.6990, mIoU 0.8495. Đây là ước tính, không phải kết quả chính thức; F1 vẫn dưới 0.80 nên nhãn cần sửa thêm. Hướng sửa đề xuất: remap + dedupe, rà các ảnh top FP/FN (`drive_026`, `drive_030`, `drive_027`, `drive_024`, `drive_012`, `drive_050`, `drive_003`, `drive_009`), sửa theo guideline; không dùng gold để sửa trực tiếp.

## 5. Kết quả YOLO

- Runtime, GPU/CPU, phiên bản Ultralytics và Torch: Tesla T4 16 GB (CUDA 0), 50 epoch trong 0.025 giờ (khoảng 88,6 giây theo `results.csv`); Ultralytics 8.4.208, Torch 2.14.1+cu130, Python 3.13.16.
- Các tham số thay đổi so với notebook nếu có và lý do: không đổi tham số. `batch=-1` được AutoBatch chọn 45; `optimizer=auto` chọn AdamW với lr0 = 0.00125, momentum = 0.9 (theo log); epochs 50, imgsz 640, seed 20260909, patience 100.
- Đường dẫn best checkpoint trong phiên chạy: `/content/Day2-Lab/outputs/yolo26_runs/vehicle_annotation/weights/best.pt`. Theo `results.csv`, mAP50–95 cao nhất ở epoch 2 (0.20077); các epoch sau không vượt lại, nên 50 epoch là dư so với 50 ảnh.

| Chỉ số trên 10 ảnh eval | Giá trị |
|---|---:|
| Precision | 0.3156 |
| Recall | 0.3066 |
| mAP50 | 0.2740 |
| mAP50–95 | 0.2006 |

Per-class (số trong ngoặc là số instance):

| Lớp | Precision | Recall | mAP50 | mAP50–95 | Instances |
|---|---:|---:|---:|---:|---:|
| `car` | 0.629 | 0.777 | 0.738 | 0.521 | 94 |
| `truck` | 0.391 | 0.200 | 0.235 | 0.203 | 5 |
| `bus` | 0.000 | 0.000 | 0.0079 | 0.0031 | 2 |
| `van` | 0.243 | 0.250 | 0.115 | 0.0754 | 12 |

Lưu ý: Precision/Recall/mAP trong bảng tổng của Ultralytics là trung bình macro theo lớp, không phải TP/tổng instance; vì vậy 0.3066 không suy ra trực tiếp từ 73 + 1 + 0 + 3. Cách tính macro này khiến các lớp hiếm (`bus`, `truck`, `van`) kéo điểm tổng xuống mạnh.

Assets: [`eval_predictions/`](assets/eval_predictions/), [`yolo26_runs/`](assets/yolo26_runs/), [`model_eval_metrics.json`](assets/model_eval_metrics.json). Ảnh và vật thể cụ thể: [`drive_051`](assets/eval_predictions/visuals/drive_051.jpg) có gold 8 car + 1 bus, dự đoán 8 car + 1 van và 0 bus → chiếc bus bị bỏ sót hoặc bị gọi thành van. [`drive_058`](assets/eval_predictions/visuals/drive_058.jpg) có gold 32 car + 1 bus + 6 van, dự đoán 20 car + 2 bus + 0 van → cụm van bị bỏ, bus bị dương tính giả. Các hình phân tích: [`results.png`](assets/yolo26_runs/vehicle_annotation/results.png), [`confusion_matrix.png`](assets/yolo26_runs/vehicle_annotation/confusion_matrix.png), [`labels.jpg`](assets/yolo26_runs/vehicle_annotation/labels.jpg).

Trả lời bốn câu hỏi cuối notebook:

1. **Lớp nào recall thấp nhất? Ảnh nào minh họa?**

   `bus` có recall thấp nhất: 0.000 (0/2); tiếp theo là `truck` 0.200 (1/5), `van` 0.250 (3/12), `car` 0.777 (73/94). Ảnh minh họa là `drive_051`: gold 8 car + 1 bus, dự đoán 8 car + 1 van, 0 bus; chiếc bus bị bỏ sót hoặc bị gọi thành van. Ảnh thứ hai là `drive_058`: gold 32 car + 1 bus + 6 van, dự đoán 20 car + 2 bus + 0 van. Lưu ý `bus` chỉ có 2 instance và nhãn train chưa remap class ID, nên per-class của run này bị nhiễu; không kết luận chỉ từ recall.

2. **Nếu mAP50 cao nhưng mAP50–95 thấp, cần kiểm điều gì trên box?**

   `mAP50` chỉ cần IoU ≥ 0.5, nên box đúng vật/đúng lớp nhưng hơi lỏng vẫn được điểm. `mAP50–95` lấy trung bình từ 0.50 đến 0.95, nên box lỏng/lệch cạnh tụt mạnh. Cần kiểm: cạnh box có bám sát phần thân xe nhìn thấy không (sai số khoảng 2–3% mỗi cạnh); box có lấy thêm bóng đổ/mặt đường/trời/cột điện không; xe nhỏ, xa, bị che hoặc bị cắt khung có box ổn định không; có gộp hai xe vào một box hoặc để nhiều box trùng/chồng lên cùng xe không. Trong run này `car` là ví dụ rõ: mAP50 0.738 nhưng mAP50–95 0.521. Với `truck`, `bus`, `van`, cả hai chỉ số đều thấp nên vấn đề chính là detection/classification, không chỉ độ sát box.

3. **Lỗi class nào có thể liên quan guideline? Dữ kiện nào hỗ trợ nhận xét?**

   Có, nhưng phải tách hai nhóm. Nhóm liên quan guideline là `van` vs `bus` và `truck` vs `van`. Dẫn chứng: `drive_058` có gold 1 bus + 6 van nhưng dự đoán 0 van + 2 bus; `drive_053` có gold 1 truck + 2 van nhưng dự đoán 3 bus + 1 van; `drive_056` có gold 1 truck + 1 van nhưng dự đoán 1 bus + 3 van. Đây đúng là các ca biên trong guideline: one-box cửa trượt là `van`; ca-bin tách + thùng là `truck`; thân dài nhiều cửa sổ/cửa lên xuống là `bus`.

   Nhóm lớn hơn đang chi phối run hiện tại là lỗi pipeline: nhãn train lưu ID theo thứ tự `car, bus, van, truck` nhưng `data.yaml` là `car, truck, bus, van`. Overlap với gold cho thấy ID 0 khớp car nhiều nhất (446 box), ID 1 khớp bus 18/20, ID 2 khớp van 54/54, ID 3 khớp truck 25/46; remap đúng là `{0:0, 1:2, 2:3, 3:1}`. Vì ID sai, model học bus thành truck, van thành bus, truck thành van; `car` không bị ảnh hưởng vì ID 0 trùng. `cls_remap=True` trong Ultralytics 8.4.208 chỉ remap head pretrained theo tên lớp, không sửa ID trong file nhãn, nên không cứu được lỗi này. Ngoài ra còn nhầm annotation: `drive_009` có 7 box van nhưng gold là truck; `drive_026` có 6 truck bị gọi van. Kết luận: không quy tất cả lỗi cho guideline; phải remap + rà box trước khi đánh giá guideline.

4. **Vì sao không dùng 10 ảnh eval để train? Vai trò validation của chúng trong notebook là gì?**

   Eval là tập held-out duy nhất. Dùng eval để train sẽ leak đánh giá, làm mAP đẹp giả tạo và vi phạm rubric (mất điểm phần pipeline). Trong notebook, eval là `val` để theo dõi từng epoch, chọn `best.pt` theo fitness và đo/visualize cuối; vì vậy nó là validation, không phải test set độc lập. Muốn test độc lập thật cần split thứ ba. Với 50 ảnh train, cách cải thiện đúng là rà/sửa nhãn train, thêm ảnh cùng phân bố hoặc augmentation — không lấy eval bù vào train. Gold eval chỉ dùng QC, không dùng để sửa nhãn train.

## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|
| Kiểm tra nhãn trên Windows | `UnicodeEncodeError: 'charmap' codec ...` khi chạy checker | Đặt `$env:PYTHONIOENCODING="utf-8"` | Checker chạy, 50/50 file hợp lệ. |
| Đối chiếu gold | Nhãn train lưu ID `car, bus, van, truck` nhưng `data.yaml` là `car, truck, bus, van` | So overlap với gold, thử 24 hoán vị; xác định remap `{0:0, 1:2, 2:3, 3:1}` | Phát hiện lỗi; chưa sửa nhãn/retrain trong phạm vi bài nộp. |
| Làm sạch nhãn | 1.616 dòng, 740 dòng trùng; 3 cặp box trùng khác class + 1 cặp cùng class | Ultralytics báo bỏ duplicate khi quét dataset; mô phỏng dedupe IoU ≥ 0.95 | Nhãn hiện tại vẫn còn duplicate; nếu rework còn 872 box. |
| Train Colab | `data.yaml` path tương đối bị Ultralytics resolve sai thư mục | Notebook rewrite `path` thành absolute `/content/Day2-Lab/dataset` | Train chạy được; 10 ảnh eval. |
| Tải output | `day2_colab_outputs.zip` không tự có trong repo; runtime có thể ngắt | Tải zip từ Colab, kiểm tra 46 entry, 10 ảnh 640×640, best.pt 5,45 MB | Zip hợp lệ; đã copy assets vào report. |
| Chọn checkpoint | 50 epoch nhưng best ở epoch 2; epoch 50 mAP50–95 còn 0.16309 | Đọc `results.csv`, so với `best.pt` | best.pt ở epoch 2; 48 epoch sau không cải thiện; nên giảm epoch/patience nếu chạy lại. |
| Đánh giá | Eval được dùng làm `val` và chọn `best.pt`, không phải test độc lập | Ghi rõ trong report; không train trên eval | Chưa có test set thứ ba. |
| Class ID | `cls_remap=True` chỉ remap head pretrained theo tên, không sửa ID nhãn | Kiểm tra source Ultralytics 8.4.208 | Lỗi hoán vị còn; cần remap + train lại nếu muốn metrics sạch. |

## 7. Tự đánh giá theo rubric

Đối chiếu [RUBRIC.md](../../RUBRIC.md):

| Tiêu chí | Trạng thái | Dẫn chứng |
|---|---|---|
| Hoàn thành và định dạng YOLO | Một phần | 50 file, 5 cột, normalized, checker pass; nhưng ID lưu sai thứ tự schema (`car, bus, van, truck` thay vì `car, truck, bus, van`). |
| Đầy đủ vật thể | Chưa đạt | F1 0.3887, FN 212; top FN ở `drive_026`, `drive_024`, `drive_027`. |
| Độ bám sát và hình học box | Một phần | mIoU 0.8452 ≥ 0.70 nhưng còn 1.175 FP/box lỏng; cần rà. |
| Phân lớp nhất quán | Chưa đạt | Sai thứ tự ID và nhầm truck/van/bus (`drive_009`, `drive_026`, `drive_058`, `drive_053`, `drive_056`). |
| Mini guideline và quyết định mơ hồ | Đạt | 3 ca `drive_058`, `drive_053`, `drive_052`; có quy tắc box và ngưỡng vật thể nhỏ. |
| Gold-set annotation QC | Chưa đạt | F1 0.3887 < 0.80; chưa rework; mô phỏng F1 0.6990 vẫn < 0.80. |
| Pipeline YOLO và phân tích | Đạt một phần | Colab T4 chạy, có metrics/ảnh eval/nhận xét; eval dùng làm val nên không phải test độc lập. |
| Điều kiện bắt buộc | Đạt | 50 file, checker pass, gold eval; không bị cap. |

Không tự nhận hoàn thành phần chưa chạy: chưa rework nhãn, chưa có test set thứ ba, chưa sửa class ID trong `dataset/labels/train`.

## 8. Công cụ AI và tài liệu tham khảo

- opencode (AI assistant): đọc report và các file `GUIDE.md`, `RUBRIC.md`, `CHECKPOINTS.md`, `SUBMISSION.md`; kiểm tra nhãn, tính metric, soạn bản thảo. Các số liệu đã đối chiếu với `tools/check_yolo_labels.py`, `tools/evaluate_annotations.py` và output Colab.
- Ultralytics 8.4.208 (source và tài liệu): kiểm tra `cls_remap`, YOLO format, `results.csv`.
- CVAT "Ultralytics YOLO Detection 1.0" format: từ `tools/prelabel_yolo.py` và tài liệu CVAT.
- Tài liệu trong repo: `GUIDE.md`, `RUBRIC.md`, `CHECKPOINTS.md`, `SUBMISSION.md`, `GUIDELINE_MINI.md`.

Không dùng gold để sửa nhãn train; không đưa token/mật khẩu; không tìm nhãn ngoài repo. Cần tự kiểm tra lại: số per-class từ notebook cell 7, assets, và 10 ảnh đã rà.
