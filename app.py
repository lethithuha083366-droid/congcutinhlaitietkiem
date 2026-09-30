import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(amount):
    return f"{amount:,.0f} VNĐ"


# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 APP TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.markdown(
    "Tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép** "
    "với nhiều hình thức nhận lãi."
)

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================
col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=10000000.0,
        step=1000000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

with col2:
    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1
    )

    loai_lai = st.selectbox(
        "🧮 Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

# =========================
# HÌNH THỨC NHẬN LÃI
# =========================
hinh_thuc_nhan_lai = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# =========================
# NÚT TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH TIỀN LÃI", type="primary", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất theo tháng
    lai_suat_thang = lai_suat / 100 / 12

    # Tổng số tháng
    tong_thang = int(ky_han)

    # =========================
    # XÁC ĐỊNH CHU KỲ NHẬN LÃI
    # =========================
    if hinh_thuc_nhan_lai == "Lãnh lãi hàng tháng":
        so_thang_moi_ky = 1

    elif hinh_thuc_nhan_lai == "Lãnh lãi hàng quý":
        so_thang_moi_ky = 3

    else:
        so_thang_moi_ky = tong_thang

    # Số kỳ
    so_ky = (tong_thang + so_thang_moi_ky - 1) // so_thang_moi_ky

    # =========================
    # TÍNH LÃI
    # =========================
    bang_du_lieu = []

    von_ban_dau = so_tien_gui
    so_du = so_tien_gui
    tong_lai = 0

    # -------------------------------------------------
    # LÃI ĐƠN
    # -------------------------------------------------
    if loai_lai == "Lãi đơn":

        for ky in range(1, so_ky + 1):

            thang_bat_dau = (ky - 1) * so_thang_moi_ky + 1
            thang_ket_thuc = min(
                ky * so_thang_moi_ky,
                tong_thang
            )

            so_thang_thuc_te = thang_ket_thuc - thang_bat_dau + 1

            # Tiền lãi của kỳ
            tien_lai_ky = (
                von_ban_dau
                * lai_suat / 100
                * so_thang_thuc_te / 12
            )

            tong_lai += tien_lai_ky

            # Với lãi đơn:
            # tiền lãi được trả ra ngoài,
            # không cộng vào vốn.
            so_du_hien_tai = von_ban_dau

            bang_du_lieu.append({
                "Kỳ": ky,
                "Thời gian": f"Tháng {thang_bat_dau} - {thang_ket_thuc}",
                "Tiền gốc": format_money(so_du_hien_tai),
                "Tiền lãi kỳ này": format_money(tien_lai_ky),
                "Tổng lãi": format_money(tong_lai)
            })

        tong_goc_lai = von_ban_dau + tong_lai

    # -------------------------------------------------
    # LÃI KÉP
    # -------------------------------------------------
    else:

        # Nếu nhận lãi cuối kỳ:
        # lãi được nhập vào vốn sau toàn bộ kỳ hạn.
        if hinh_thuc_nhan_lai == "Lãnh lãi cuối kỳ":

            so_du = von_ban_dau

            for thang in range(1, tong_thang + 1):

                lai_thang = so_du * lai_suat_thang
                so_du += lai_thang
                tong_lai += lai_thang

                # Chỉ lưu dữ liệu từng tháng
                bang_du_lieu.append({
                    "Kỳ": thang,
                    "Thời gian": f"Tháng {thang}",
                    "Tiền gốc": format_money(
                        so_du - lai_thang
                    ),
                    "Tiền lãi kỳ này": format_money(
                        lai_thang
                    ),
                    "Tổng lãi": format_money(
                        tong_lai
                    )
                })

            tong_goc_lai = so_du

        # ---------------------------------------------
        # LÃI KÉP + NHẬN LÃI THÁNG / QUÝ
        # ---------------------------------------------
        else:

            # Lưu số dư đầu kỳ
            so_du = von_ban_dau

            for ky in range(1, so_ky + 1):

                thang_bat_dau = (ky - 1) * so_thang_moi_ky + 1
                thang_ket_thuc = min(
                    ky * so_thang_moi_ky,
                    tong_thang
                )

                so_thang_thuc_te = (
                    thang_ket_thuc - thang_bat_dau + 1
                )

                so_du_dau_ky = so_du

                # Tính lãi kép trong kỳ
                so_du_cuoi_ky = (
                    so_du
                    * (1 + lai_suat_thang) ** so_thang_thuc_te
                )

                tien_lai_ky = so_du_cuoi_ky - so_du

                tong_lai += tien_lai_ky

                # Lãi được nhập vào vốn
                so_du = so_du_cuoi_ky

                bang_du_lieu.append({
                    "Kỳ": ky,
                    "Thời gian": f"Tháng {thang_bat_dau} - {thang_ket_thuc}",
                    "Tiền gốc đầu kỳ": format_money(so_du_dau_ky),
                    "Tiền lãi kỳ này": format_money(tien_lai_ky),
                    "Số dư cuối kỳ": format_money(so_du),
                    "Tổng lãi": format_money(tong_lai)
                })

            tong_goc_lai = so_du

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Tính toán thành công!")

    st.subheader("📊 KẾT QUẢ")

    col1, col2, col3 = st.columns(3)

    # Tiền lãi định kỳ
    if hinh_thuc_nhan_lai == "Lãnh lãi cuối kỳ":
        tien_lai_dinh_ky = tong_lai
        ten_lai = "💰 Tổng tiền lãi"
    else:
        if len(bang_du_lieu) > 0:
            # Lấy kỳ cuối cùng
            tien_lai_dinh_ky = (
                float(
                    bang_du_lieu[-1]["Tiền lãi kỳ này"]
                    .replace(" VNĐ", "")
                    .replace(",", "")
                )
            )
        else:
            tien_lai_dinh_ky = 0

        ten_lai = "💵 Tiền lãi kỳ gần nhất"

    with col1:
        st.metric(
            "💵 Tiền gốc",
            format_money(von_ban_dau)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_lai)
        )

    with col3:
        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_goc_lai)
        )

    st.divider()

    # =========================
    # LÃI ĐỊNH KỲ
    # =========================
    st.subheader("💳 Tiền lãi định kỳ")

    if hinh_thuc_nhan_lai == "Lãnh lãi hàng tháng":

        lai_dinh_ky = (
            von_ban_dau * lai_suat / 100 / 12
        )

        st.info(
            f"Bạn nhận khoảng **{format_money(lai_dinh_ky)} / tháng**."
        )

    elif hinh_thuc_nhan_lai == "Lãnh lãi hàng quý":

        lai_dinh_ky = (
            von_ban_dau * lai_suat / 100 / 4
        )

        st.info(
            f"Bạn nhận khoảng **{format_money(lai_dinh_ky)} / quý**."
        )

    else:

        st.info(
            f"Bạn nhận **{format_money(tong_lai)}** "
            f"tiền lãi khi đến hạn."
        )

    # =========================
    # BẢNG CHI TIẾT
    # =========================
    st.subheader("📋 Chi tiết tiền lãi")

    df = pd.DataFrame(bang_du_lieu)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # THÔNG TIN TÓM TẮT
    # =========================
    st.divider()

    st.subheader("📝 Thông tin khoản tiền gửi")

    col1, col2 = st.columns(2)

    with col1:
        st.write(
            f"**Số tiền gửi:** {format_money(von_ban_dau)}"
        )

        st.write(
            f"**Kỳ hạn:** {tong_thang} tháng"
        )

        st.write(
            f"**Lãi suất:** {lai_suat:.2f}%/năm"
        )

    with col2:
        st.write(
            f"**Hình thức tính:** {loai_lai}"
        )

        st.write(
            f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}"
        )

        st.write(
            f"**Tổng nhận cuối kỳ:** "
            f"{format_money(tong_goc_lai)}"
        )


# =========================
# FOOTER
# =========================
st.divider()

st.caption(
    "💡 Công cụ mang tính chất tham khảo. "
    "Kết quả thực tế có thể khác tùy theo quy định của từng ngân hàng."
)
