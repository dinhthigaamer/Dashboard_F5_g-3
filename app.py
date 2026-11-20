import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="F5 – Sức khỏe điểm đo AADT",
    page_icon="🚦",
    layout="wide",
)

# ----------------------------- Dữ liệu ---------------------------------
YEARS = list(range(2015, 2026))
N = None

HEAT = [
    ("London", 69038, [
     1, 1, .939, .934, .94, .922, .934, .932, .923, .919, .913]),
    ("Madrid", 35284, [N, N, N, N, N, N, N, .111, .034, .034, .083]),
    ("Stockholm", 14810,
     [.199, .227, .225, .21, .203, .203, .201, .193, .194, .198, .198]),
    ("Birmingham", 7609, [1, 1, .996, .989, .993, .991, .991, 1, 1, .995, 1]),
    ("Hamburg", 6858, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("Glasgow", 6589,
     [.802, .833, .829, .848, .854, .883, .884, .924, .884, .854, .829]),
    ("Manchester", 5894, [
     1, 1, .983, .978, .995, .994, .994, .989, .994, .989, .983]),
    ("Brno", 5296, [0, 0, 0, 0, 0, 0, 0, 0, 0, N, N]),
    ("Luxembourg", 5230, [
     N, .23, .226, .223, .212, .193, .139, .138, .139, .139, 1]),
    ("Zurich", 3878,
     [.018, .018, .018, .017, .016, .016, .016, .017, .017, .017, .017]),
    ("Oslo", 3690, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("Montpellier", 3524,
     [.569, .589, .626, .72, .711, .733, .7, .739, .735, .732, .709]),
    ("Edinburgh", 3321,
     [.961, .97, .931, .947, .914, .968, .958, .886, .898, .896, .893]),
    ("Barcelona", 3092, [
     N, N, .019, .019, .031, .029, .066, .059, .061, .061, .03]),
    ("Cardiff", 2789, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
    ("Vienna", 2736, [N, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("Bordeaux", 2681, [N, N, N, N, 0, 0, 0, 0, 0, 0, 0]),
    ("Lille", 2014, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("Rennes", 1848, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("Malmo", 1315, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("Rouen", 1238, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("Helsinki", 1120,
     [.018, .018, .018, .018, .018, .018, .018, .018, .018, .018, N]),
    ("Valencia", 222, [N, 0, 0, 0, 0, 0, 0, 0, N, N, N]),
    ("Lisbon", 96, [N, N, N, N, N, N, 0, 0, 0, 0, N]),
    ("Toulouse", 24, [N, N, N, .5, 0, 1, .333, .667, 0, N, N]),
]

FLAGS = [
    ("(không có cờ)", .5566, "191.563"),
    ("carried_forward", .162, "55.755"),
    ("multi_geometry_id;duplicate_key;same_value_copies", .1171, "40.294"),
    ("single_day_count_expanded", .0755, "25.971"),
    ("source_total_of_directions", .0244, "8.402"),
    ("derived_from_neighbour", .0164, "5.640"),
    ("carried_forward;station_moved", .011, "3.792"),
    ("duplicate_key;same_value_copies", .0102, "3.501"),
]

DIAGNOSTICS = {
    "Metric": [
        ("2W_AADT", .368, "28.110"), ("TR_AADT", .2963, "30.489"),
        ("AADT", .2234, "54.586"), ("TR_AADT_weekday_proxy", .1349, "504"),
        ("AAWT_as_AADT", .1001, "6.764"), ("AAWT", .0884, "24.630"),
        ("TR_AAWT_as_AADT", .0666, "5.432"), ("AADT_weekday_proxy", .0599, "1.418"),
        ("TR_AAWT", .0577, "2.409"),
    ],
    "Cấp đường": [
        ("residential", .3707, "17.238"), ("unclassified", .3374, "2.543"),
        ("trunk", .3326, "23.446"), ("motorway", .2943, "5.828"),
        ("trunk_link", .2699, "1.408"), ("motorway_link", .2668, "3.205"),
        ("living_street", .2542, "59"), ("(không có)", .2484, "2.355"),
        ("service", .2431, "2.809"), ("tertiary", .231, "19.347"),
        ("primary", .1524, "55.154"), ("secondary", .1405, "19.974"),
        ("primary_link", .1339, "747"), ("busway", .1194, "67"),
        ("secondary_link", .1194, "134"),
    ],
    "Thành phố": [
        ("London", .3527, "61.818"), ("Manchester", .3425, "5.256"),
        ("Birmingham", .3424, "6.654"), ("Cardiff", .3184, "2.406"),
        ("Edinburgh", .2826, "2.930"), ("Glasgow", .256, "5.863"),
        ("Montpellier", .1169, "2.661"), ("Valencia", .1158, "190"),
        ("Rennes", .1067, "1.097"), ("Rouen", .1065, "310"),
        ("Madrid", .1051, "26.463"), ("Helsinki", .1032, "1.008"),
        ("Oslo", .0926, "3.217"), ("Barcelona", .0871, "2.056"),
        ("Stockholm", .0852, "12.196"),
    ],
    "Độ phủ ngày đo": [
        ("≤ 0,5", .2957, "531"), ("0,5 – 0,8", .1714, "1.814"),
        ("0,8 – 0,95", .1394, "4.145"), ("> 0,95", .0838, "27.911"),
    ],
    "Cờ / ml_label_ok": [
        ("Có cờ chất lượng", .3005, "86.926"), ("Không có cờ", .133, "67.416"),
        ("ml_label_ok = True", .3114,
         "92.405"), ("ml_label_ok = False", .1018, "61.937"),
    ],
}

DIAGNOSTIC_NOTES = {
    "Metric": "Chênh lệch gấp 4–6 lần giữa nhóm 2W/TR_AADT và nhóm AAWT. Ba metric *_modelled không còn trong dữ liệu sau khi lọc.",
    "Cấp đường": "Chỉ hiển thị cấp đường có ít nhất 50 dòng, 15 cấp cao nhất. Chưa kiểm soát theo thành phố nên đừng đọc thành quan hệ riêng của cấp đường.",
    "Thành phố": "15 thành phố có tỷ lệ cao nhất (số bên phải là số dòng được chấm điểm). Sáu thành phố Anh đứng đầu.",
    "Độ phủ ngày đo": "Chỉ có ở Lisbon, Luxembourg, Madrid, Zurich; nhóm thấp nhất chỉ có 531 dòng.",
    "Cờ / ml_label_ok": "Hai cặp so sánh độc lập. ml_label_ok = True bất thường nhiều hơn nên chưa thể diễn giải; xem lưu ý ở trên.",
}

CITY_MODEL = [
    ("London", 2154, .736, .693), ("Madrid", 1081, .329, .104),
    ("Birmingham", 244, .64, .496), ("Manchester", 187, .657, .615),
    ("Glasgow", 169, .75, .87), ("Stockholm", 121, .522, .198),
    ("Edinburgh", 91, .674, .681), ("Cardiff", 59, .661, .695),
    ("Oslo", 38, .412, .184), ("Montpellier", 30, .111, .067),
    ("Luxembourg", 27, 0, 0), ("Hamburg", 20, 1, .05),
    ("Bordeaux", 19, 0, 0), ("Zurich", 18, 0, 0), ("Vienna", 14, 0, 0),
]

WATCHLIST = [
    ("14-SMD-2", "AADT", "trunk", .662, .6149),
    ("39-SMD-1", "AADT", "trunk", .5525, .478),
    ("36-SMD-2", "AADT", "trunk", .5309, .4554),
    ("36-SMD-1", "AADT", "trunk", .4934, .4186),
    ("39-SMD-1", "AAWT", "trunk", .4719, .4118),
    ("14-SMD-2", "AAWT", "trunk", .4082, .3852),
    ("8033", "AADT", "tertiary", .5521, .3546),
    ("36-SMD-2", "AAWT", "trunk", .3988, .351),
    ("10-SMD-2", "AADT", "trunk", .3717, .339),
    ("8033", "AAWT", "tertiary", .488, .329),
    ("1003", "AADT", "primary_link", .3983, .2409),
    ("6-SMD-1", "AADT", "trunk", .2475, .2368),
    ("4102", "AADT", "residential", .6019, .2243),
    ("36-SMD-1", "AAWT", "trunk", .2567, .2197),
    ("62-SMD-2", "AADT", "trunk", .2415, .2166),
]

# ----------------------------- Giao diện --------------------------------
st.title("🚦 F5 – Sức khỏe điểm đo AADT")
st.caption(
    "Kết quả 4 mức phân tích, lấy từ output của `eda.ipynb` "
    "(chưa tính lại từ dữ liệu gốc). "
    "🟢 **Chắc** = có số liệu trực tiếp · 🟠 **Có thể** = suy luận cần kiểm tra · "
    "⚪ **Chưa kết luận** = chưa đủ căn cứ."
)


def finding(level: str, text: str):
    styles = {
        "Chắc": ("🟢", "success"),
        "Có thể": ("🟠", "warning"),
        "Chưa kết luận": ("⚪", "info"),
        "Cần nhớ": ("🔎", "info"),
        "Lưu ý": ("⚠️", "warning"),
    }
    icon, kind = styles[level]
    getattr(st, kind)(f"**{icon} {level}:** {text}")


def percent(v, digits=1):
    return f"{v*100:.{digits}f}%".replace(".", ",")


def rows_df(rows, columns=("Nhóm", "Tỷ lệ bất thường", "Số dòng")):
    return pd.DataFrame([
        {columns[0]: r[0], columns[1]: percent(r[1]), columns[2]: r[2]}
        for r in rows
    ])


tabs = st.tabs([
    "Tổng quan", "1 · Descriptive", "2 · Diagnostic",
    "3 · Predictive", "4 · Prescriptive", "Lưu ý",
])

# Tổng quan
with tabs[0]:
    metrics = [
        ("25", "thành phố sau lọc"), ("26.585", "chuỗi điểm đo"),
        ("190.196", "dòng dữ liệu"), ("22,7%", "dòng “bất thường” (|z| > 3)"),
        ("0,614", "PR-AUC mô hình (baseline 0,368; ngẫu nhiên ≈ 0,20)"),
        ("×2,3", "precision@10 so với ngẫu nhiên"),
    ]
    cols = st.columns(3)
    for i, (value, label) in enumerate(metrics):
        cols[i % 3].metric(label, value)

    st.subheader("Ba điều quan trọng nhất")
    finding("Chắc", "Bất thường tập trung ở sáu thành phố Anh: chiếm 55% số dòng được chấm điểm nhưng 82,6% số dòng bị gắn nhãn bất thường. Con số 22,7% toàn bộ chủ yếu phản ánh nhóm này.")
    finding("Chắc", "Mô hình dự đoán tốt hơn baseline (PR-AUC 0,614 so với 0,368), nhưng 67% nhãn dương ở tập kiểm tra nằm ở sáu thành phố Anh. Ở Madrid (25% nhãn dương) recall chỉ 10%, và ở Zurich, Vienna, Bordeaux, Luxembourg mô hình không bắt được trường hợp nào.")
    finding("Có thể", "Tỷ lệ bất thường giảm sau 2022 (từ 23,3% xuống 18,3%) chủ yếu là hiệu ứng thành phần dữ liệu, không phải chất lượng tốt lên: số dòng được chấm điểm tăng gần gấp đôi cùng lúc Madrid (tỷ lệ ~10%) bắt đầu có dữ liệu.")

# Descriptive
with tabs[1]:
    st.header("Mức 1 – Descriptive: dữ liệu hiện ra sao?")
    finding("Chắc", "Dữ liệu tập trung: London 36,3%, Madrid 18,6%, Stockholm 7,8% (tổng 62,6% số dòng). Các số liệu gộp vì thế chủ yếu nói về ba thành phố này.")
    finding("Chắc", "Cờ chất lượng gần như là thuộc tính của thành phố, không phải của từng điểm đo: 11 thành phố có 0% cờ, sáu thành phố Anh có 86–100%, Montpellier 70%. Tỷ lệ này ổn định qua các năm trong mỗi thành phố.")
    finding("Chắc", "Độ dài chuỗi: 37,6% chuỗi chỉ có đúng 4 năm, 30,5% đủ 11 năm; 10,7% chuỗi bị đứt quãng.")
    finding("Có thể", "Cờ phổ biến nhất là `carried_forward` (16,2% toàn bộ dòng). Tên cờ gợi ý giá trị được chép từ kỳ trước, nhưng chưa đối chiếu với DATA_DICTIONARY nên chưa nên coi đó là “lỗi”.")
    finding("Chưa kết luận", "Độ phủ ngày đo chỉ có ở 4 thành phố (Lisbon, Luxembourg, Madrid, Zurich), ~23% số dòng, trung vị 0,989. Không suy rộng ra các thành phố khác.")

    st.subheader("Tỷ lệ dòng có cờ chất lượng (thành phố × năm)")
    st.caption("Cột “dòng” là số dòng sau lọc; ô trống = không có dữ liệu năm đó.")
    heat_rows = []
    for city, count, values in HEAT:
        row = {"Thành phố": city, "Dòng": count}
        row.update({str(y): v for y, v in zip(YEARS, values)})
        heat_rows.append(row)
    heat_df = pd.DataFrame(heat_rows).set_index("Thành phố")
    st.dataframe(
        heat_df.style.format(
            {str(y): (lambda x: "" if pd.isna(x) else f"{x:.1%}") for y in YEARS})
        .background_gradient(subset=[str(y) for y in YEARS], cmap="Reds", vmin=0, vmax=1)
        .format({"Dòng": "{:,.0f}"}),
        use_container_width=True,
    )

    st.subheader("Giá trị `quality_flags` phổ biến (toàn bộ 344.193 dòng)")
    flag_df = pd.DataFrame(FLAGS, columns=["Quality flag", "Tỷ lệ", "Số dòng"])
    flag_df["Tỷ lệ"] = flag_df["Tỷ lệ"].map(percent)
    st.dataframe(flag_df, hide_index=True, use_container_width=True)

# Diagnostic
with tabs[2]:
    st.header("Mức 2 – Diagnostic: vì sao bất thường?")
    st.caption("Bất thường = |Δlog| so với trung vị cùng thành phố, metric, năm có |z| > 3. Đây là bất thường thống kê, chưa phải lỗi thiết bị đã xác nhận, và các liên hệ dưới đây là tương quan.")
    finding("Chắc", "Tập trung ở Anh: London 35,3%, Manchester 34,3%, Birmingham 34,2%, Cardiff 31,8% so với 9–12% ở hầu hết thành phố còn lại.")
    finding("Có thể", "Luật bất thường có thể đang bị thổi phồng: nâng ngưỡng z từ 2,5 lên 4,0 chỉ giảm tỷ lệ từ 24,7% xuống 20,2%. Nếu là đuôi hiếm thật thì phải giảm mạnh hơn. Nghi ngờ MAD quá nhỏ ở các nhóm có nhiều giá trị chép lại (Δlog = 0); cần xem khối chẩn đoán MAD trong bản notebook mới.")
    finding("Có thể", "Độ phủ ngày đo thấp đi cùng nhiều bất thường hơn, giảm đều từ 29,6% xuống 8,4%. Nhưng chỉ có ở 4 thành phố (chủ yếu Madrid) và nhóm thấp nhất có 531 dòng.")
    finding("Có thể", "Metric: TR_AADT (lưu lượng xe tải/xe nặng trung bình ngày trong năm) có tỷ lệ bất thường 29,6%, cao hơn AADT tổng thể (22,3%). TR_AAWT (lưu lượng xe tải/xe nặng trung bình ngày từ thứ Hai đến thứ Sáu) là 5,8%, thấp hơn TR_AADT. Hai metric này gợi ý tỷ lệ bất thường khác nhau theo nhóm phương tiện và kỳ tính, nhưng chưa đủ để kết luận xe tải biến động mạnh hơn: cần kiểm tra phân bố theo thành phố, điểm đo và mức độ phủ dữ liệu. 2W_AADT (lưu lượng xe hai bánh trung bình ngày trong năm) có tỷ lệ 36,8%, nhưng hiện chỉ có ở Marseille nên không thể khái quát cho nhóm xe hai bánh nói chung.")
    finding("Chưa kết luận", "Cờ chất lượng đi cùng bất thường gấp 2,3 lần (30,0% so với 13,3%), nhưng cờ phụ thuộc thành phố nên chưa tách được. `ml_label_ok` cho kết quả ngược trực giác (True: 31,1%, False: 10,2%); cần tách theo metric và thành phố. Cấp đường (residential 37,1% so với primary 15,2%) cũng chưa kiểm soát theo thành phố.")

    st.subheader("Tỷ lệ bất thường theo từng yếu tố")
    selected = st.selectbox("Chọn yếu tố", list(DIAGNOSTICS.keys()))
    diag_rows = DIAGNOSTICS[selected]
    chart_df = pd.DataFrame({"Nhóm": [r[0] for r in diag_rows], "Tỷ lệ": [
                            r[1] for r in diag_rows]}).set_index("Nhóm")
    st.bar_chart(chart_df, y="Tỷ lệ", horizontal=True)
    st.dataframe(rows_df(diag_rows), hide_index=True, use_container_width=True)
    st.info(DIAGNOSTIC_NOTES[selected])

    st.subheader("Tỷ lệ bất thường theo năm")
    year_values = [.2259, .2701, .2632, .2716, .2398, .2732, .2335, .1833, .185, .2012]
    year_df = pd.DataFrame({"Năm": list(range(2016, 2026)),
                           "Tỷ lệ bất thường": year_values}).set_index("Năm")
    st.line_chart(year_df)
    st.caption("Loại bất thường: 59,5% là “kéo dài” (nhiều năm liền), 40,5% là “nhảy đột ngột”. Không thấy đỉnh COVID, hợp lý vì z-score so với trung vị cùng thành phố đã loại cú sốc chung.")


# Predictive
with tabs[3]:
    st.header("Mức 3 – Predictive: dự đoán bất thường năm kế tiếp")
    finding("Chắc", "Mô hình chọn theo tập kiểm định (HistGradientBoosting) đạt PR-AUC 0,614 trên tập kiểm tra, ≈ 3,1 lần mức ngẫu nhiên (0,20) và 1,7 lần baseline “năm trước bất thường thì năm sau cũng vậy”. PR-AUC kiểm định 0,624 gần với kiểm tra nên kết quả ổn định giữa các năm.")
    finding("Chắc", "Hiệu năng phụ thuộc thành phố: tốt ở nhóm Anh (precision 0,64–0,75), kém ở Madrid (recall 0,10), Stockholm (0,20), Oslo (0,18), và bằng 0 ở Zurich, Vienna, Bordeaux, Luxembourg. Con số gộp 0,614 vì vậy cao hơn khả năng tổng quát hóa thực tế.")
    finding("Có thể", "Mô hình nhiều khả năng học “lịch sử bất thường và cờ” là chính, vốn là đặc trưng của các thành phố Anh. Chưa kiểm tra bằng độ quan trọng đặc trưng hoặc bằng huấn luyện theo từng thành phố.")
    finding("Cần nhớ", "Nhãn do chính luật z-score tạo ra, nên mô hình dự đoán “luật sẽ báo bất thường”, chưa phải “thiết bị sẽ hỏng”.")

    st.subheader("Kết quả trên tập kiểm tra (nhãn năm 2025)")
    model_df = pd.DataFrame({
        "Mô hình": ["Baseline", "Logistic", "HistGradientBoosting"],
        "PR-AUC": [.3676, .5932, .6141],
        "Precision": [.542, .610, .669],
        "Recall": [.488, .512, .494],
    }).set_index("Mô hình")
    st.bar_chart(model_df[["PR-AUC"]])
    st.dataframe(model_df, use_container_width=True)
    st.caption("Tập: huấn luyện 111.366 dòng (24,1% dương), kiểm định 21.571 (18,5%), kiểm tra 21.405 (20,1%). Thanh = PR-AUC.")

    st.subheader("Theo thành phố (15 thành phố nhiều nhãn dương nhất)")
    city_df = pd.DataFrame(CITY_MODEL, columns=[
                           "Thành phố", "Nhãn dương", "Precision", "Recall"])
    st.dataframe(city_df, hide_index=True, use_container_width=True)

# Prescriptive
with tabs[4]:
    st.header("Mức 4 – Prescriptive: nên kiểm tra điểm đo nào trước?")
    finding("Chắc", "Xếp hạng bằng mô hình hơn hẳn ngẫu nhiên: precision@10 là 0,379 so với 0,162 (×2,3), @20 là ×2,2, @50 là ×2,0. Càng tăng k thì lợi thế càng giảm.")
    finding("Chắc", "Cờ chất lượng sẵn có gần như vô dụng khi dùng để xếp hạng trong thành phố (0,16–0,18, bằng ngẫu nhiên), vì ở các thành phố Anh gần như mọi dòng đều có cờ nên không phân biệt được.")
    finding("Có thể", "Nhân thêm “tầm quan trọng” (hạng AADT trong thành phố) làm precision@10 giảm từ 0,484 xuống 0,379. Đây là đánh đổi giữa độ chính xác và ưu tiên đường lớn; số liệu hiện có chưa chứng minh sự đánh đổi đó đáng giá.")
    finding("Lưu ý", "Một điểm đo xuất hiện nhiều lần (AADT và AAWT). Trong 15 dòng đầu của Barcelona chỉ có 10 điểm đo khác nhau; nên gộp theo điểm đo vật lý trước khi chọn top-k.")

    st.subheader("Precision@k (top-k mỗi thành phố, năm kiểm tra)")
    precision_df = pd.DataFrame({
        "k": ["10", "20", "50"],
        "Mô hình × tầm quan trọng": [.379, .350, .321],
        "Chỉ xác suất": [.484, .437, .391],
        "Cờ sẵn có": [.174, .179, .164],
        "Ngẫu nhiên": [.162, .162, .162],
    }).set_index("k")
    st.line_chart(precision_df)
    st.dataframe(precision_df, use_container_width=True)

st.subheader(
    "Ví dụ danh sách cần kiểm tra: Barcelona, dự báo năm 2026 (15 dòng đầu)"
)

watch_df = pd.DataFrame(
    WATCHLIST,
    columns=["Điểm đo", "Metric", "Cấp đường", "Xác suất", "Điểm ưu tiên"]
)

duplicate_ids = watch_df["Điểm đo"].duplicated(keep=False)

st.dataframe(
    watch_df.style.apply(
        lambda row: [
            "background-color: #263445; color: #F1F5F9; font-weight: 600;"
            if duplicate_ids.loc[row.name] else ""
            for _ in row
        ],
        axis=1,
    ).format({
        "Xác suất": "{:.4f}",
        "Điểm ưu tiên": "{:.4f}"
    }),
    hide_index=True,
    use_container_width=True,
)

st.caption("Dòng có nền xám xanh đậm là điểm đo xuất hiện nhiều lần.")

# Notes
with tabs[5]:
    st.header("Lưu ý khi dùng kết quả")
    notes = [
        "Số liệu lấy từ bản notebook chạy trước khi thêm điều kiện MIN_ABS_DLOG và sửa importance theo metric. Chạy lại bản mới có thể thay đổi các con số.",
        "File audit không có cột loại trừ (cột thật: city, tier, reason, covid_19_22_full…). Hai tên not_for_trend và id_not_stable_across_years thực ra là giá trị trong quality_flags (482 và 1.050 dòng); hiện chưa dùng để lọc.",
        "35.470 dòng trùng khóa đang được gộp bằng trung bình. Nhiều dòng trong số này mang cờ same_value_copies nên ít gây hại, nhưng chưa kiểm tra riêng.",
        "Bảng “bước lọc” ghi 0 chuỗi bị loại, nhiều khả năng do cell Bước 2 chạy hai lần. Không nên dùng con số đó.",
        "Ba metric *_modelled không còn trong dữ liệu phân tích sau khi lọc chuỗi; chưa rõ lý do.",
        "Hai cell bạn thêm chưa có kết quả: cell 13 báo lỗi d chưa định nghĩa, cell 20 chưa chạy và sẽ lỗi vì test không có cột severity.",
    ]
    for item in notes:
        st.warning(item)

st.divider()
st.caption("Dashboard chuyển từ HTML/JavaScript sang Streamlit. Các số liệu đang được nhúng tĩnh theo output notebook được cung cấp; cần thay bằng dữ liệu đọc trực tiếp nếu muốn tự động cập nhật.")
