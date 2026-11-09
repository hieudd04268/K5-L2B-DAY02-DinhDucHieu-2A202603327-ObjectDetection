# Mini guideline — bài làm cá nhân

> Điền nội dung này trước khi bắt đầu gán nhãn. Giữ lại các quyết định sau khi self-QC.

## Định nghĩa lớp

> Định nghĩa vận hành để gán nhãn, bám theo cách phân loại xe thông dụng của Luật Giao thông đường bộ Việt Nam và QCVN 41. Khi cách gọi dân gian khác schema thì ưu tiên schema 4 lớp. Thứ tự phân biệt: **kiểu thân xe → số chỗ → kích thước**, không phân loại theo màu, hãng hay độ sang.

| Lớp | Định nghĩa của bạn | Ví dụ/điểm phân biệt |
| --- | --- | --- |
| `car` | Xe ô tô con chở người đến 9 chỗ (kể cả tài xế), dựng trên khung gầm xe con, có ca-pô/đuôi hoặc hatchback liền khối, cửa bên mở bằng bản lề. Gồm sedan, hatchback, coupe, convertible, SUV/CUV và MPV/SUV 7–9 chỗ dùng cửa bản lề. Không có thùng chở hàng hở, không phải thân xe khách chuyên dụng. | Vios, City, Accent, Mazda 3, Civic; CR-V, Fortuner, Everest, Santa Fe, Sorento; Innova, Xpander, Veloz, Avanza. **Điểm phân biệt:** 7–9 chỗ/SUV/MPV cửa bản lề vẫn là `car`; không xếp vào `van` chỉ vì có 7–9 chỗ. |
| `truck` | Xe ô tô tải chở hàng: ca-bin tài xế tách khỏi khoang chở hàng (thùng hở, thùng kín, thùng ben, container), thường có từ 2 trục. Gồm xe tải nhẹ, tải thùng, xe ben, đầu kéo + rơ-moóc/sơ-mi và xe bán tải (pickup) có thùng hàng hở phía sau. | Hino/Isuzu/Howo thùng kín, xe ben, xe container, Ford Ranger, Toyota Hilux, Mitsubishi Triton. **Điểm phân biệt:** có ca-bin riêng + thùng/khoang hàng = `truck`; xe one-box bịt kín kiểu Transit chở hàng vẫn là `van`, không phải `truck`. |
| `bus` | Xe ô tô chở khách chuyên dụng: thân dài, nhiều hàng ghế, cửa lên xuống bên hông, dãy cửa sổ hành khách chạy dọc thân; thường từ 10 chỗ trở lên (không kể tài xế). Gồm xe buýt nội thành, xe khách liên tỉnh/giường nằm, limousine cỡ lớn, school bus và minibus 16–29 chỗ. | Bus Thaco/VinBus, Hyundai County, Samco, Universe, xe khách giường nằm. **Điểm phân biệt:** thân xe được thiết kế chuyên để chở khách, cửa lên xuống lớn; khác `van` ở kiểu thân chuyên dụng (không phải thân van cải tạo) và kích thước. |
| `van` | Xe van/minivan thương mại thùng kín liền khối (one-box), gầm thấp, thường có cửa trượt bên hông; dùng chở người hoặc chở hàng. Khoang khách/hàng liền với ca-bin, không có ca-pô/đuôi tách rời kiểu sedan và không có thùng hàng hở. | Ford Transit, Mercedes Sprinter, Hyundai Solati, Toyota Hiace, Gazelle; van chở hàng bịt kín. **Điểm phân biệt:** một khối liền + cửa trượt = `van`; nếu có ca-bin riêng và thùng hàng = `truck`; nếu là SUV/MPV cửa bản lề = `car`. Hiace/Transit bản 10–16 chỗ giữ nguyên thân van xếp `van`; bản cải tạo thành xe khách chuyên dụng xếp `bus`. |

## Quy tắc chung

- Box bám sát vật thể nghĩa là: hình chữ nhật nhỏ nhất bao trọn **phần thân xe nhìn thấy** (vỏ, kính, bánh, cản, gương, giá nóc/hành lý gắn liền); không lấy bóng đổ, mặt đường, trời, cột điện, biển báo hay xe bên cạnh. Sai số mỗi cạnh chỉ khoảng 2–3% kích thước vật thể.
- Vật thể bị che khuất: vẫn gán nếu nhìn đủ đặc trưng để xác định chắc lớp; box chỉ ôm phần nhìn thấy, **không nội suy/đoán phần bị che**. Nếu bị che quá nhiều (chỉ còn mảnh nhỏ, không chắc là xe hay loại xe) thì bỏ qua và ghi vào mục ca mơ hồ.
- Vật thể bị cắt bởi rìa ảnh: box dừng đúng rìa ảnh, không kéo dài ra ngoài; vẫn gán nếu phần nhìn thấy đủ nhận diện lớp. Nếu chỉ còn một mảnh sát rìa, áp dụng quy tắc vật thể rất nhỏ.
- Vật thể rất nhỏ/mơ hồ: chỉ gán khi phân biệt được lớp và thấy rõ đường bao; ngưỡng tham khảo cạnh ngắn ≥ ~12 px hoặc diện tích ≥ ~0,15% ảnh. Dưới ngưỡng này mà không chắc lớp thì **không đoán**, bỏ qua và ghi case.
- Không gán người, xe đạp, mô tô/xe máy, biển báo, đèn giao thông, phản chiếu trong kính/gương, hình xe trên biển quảng cáo; xe đang đỗ vẫn gán theo đúng loại xe.

## Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_058` | Cảnh có 1 xe buýt và 6 xe van/minivan cỡ lớn (kiểu Transit/Hiace/Solati) đứng gần nhau, dễ nhầm xe van 16 chỗ với bus. | Xe thân bus dài, nhiều cửa sổ hành khách và cửa lên xuống lớn → `bus`; các xe one-box, cửa trượt → `van`. | Ưu tiên kiểu thân xe và số chỗ: bus là thân chuyên dụng ≥ 10 chỗ; van là one-box liền khối. Không đổi lớp theo kích thước hiển thị trong ảnh. |
| `drive_053` | Có 1 xe tải và 2 van; xe thùng kín cỡ nhỏ (hoặc bán tải có nắp thùng) dễ bị nhầm giữa `truck` và `van`. | Xe có ca-bin tách khỏi khoang hàng, kể cả thùng kín/bán tải → `truck`; xe one-box liền khối → `van`. | Theo cấu trúc thân: ca-bin riêng + thùng hàng = truck; khoang hàng liền ca-bin, không thùng hở = van. |
| `drive_052` | Có 1 xe tải, 1 van và nhiều car; xe 7 chỗ/MPV và minivan cỡ lớn cùng xuất hiện. | SUV/MPV 7 chỗ cửa bản lề, có ca-pô → `car`; minivan cửa trượt, thân one-box → `van`. | Theo kiểu thân và cửa: xe con có ca-pô/đuôi, cửa bản lề là car; one-box cửa trượt là van. Số chỗ chỉ dùng để phân biệt bus với van, không dùng để đẩy car sang van. |
