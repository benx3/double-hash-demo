"""
Streamlit Web Application for Double Hashing Product Management
Run with: streamlit run app.py
"""
import streamlit as st
import pandas as pd
from models import Product
from double_hashing import DoubleHashTable
from database import DatabaseManager


# Page configuration
st.set_page_config(
    page_title="Double Hashing - Quản lý Sản phẩm",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stAlert {
        margin-top: 1rem;
    }
    .hash-slot {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        text-align: center;
    }
    .slot-empty {
        background-color: #f0f0f0;
        color: #666;
    }
    .slot-occupied {
        background-color: #4CAF50;
        color: white;
    }
    .slot-deleted {
        background-color: #ff9800;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'hash_table' not in st.session_state:
        st.session_state.hash_table = None
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    if 'last_operation' not in st.session_state:
        st.session_state.last_operation = None


def create_new_table(size: int):
    """Create a new hash table"""
    st.session_state.hash_table = DoubleHashTable(size)
    st.session_state.db_manager.save(st.session_state.hash_table)
    st.success(f"✅ Đã tạo Hash Table mới với kích thước {size}")


def load_table():
    """Load hash table from database"""
    ht = st.session_state.db_manager.load()
    if ht:
        st.session_state.hash_table = ht
        st.success("✅ Đã load dữ liệu từ database")
        return True
    return False


def visualize_hash_table():
    """Visualize hash table with color coding"""
    if st.session_state.hash_table is None:
        return
    
    st.subheader("📊 Trực quan Hash Table")
    
    table_state = st.session_state.hash_table.get_table_state()
    
    # Create columns for grid layout
    cols_per_row = 5
    for i in range(0, len(table_state), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(table_state):
                slot = table_state[i + j]
                with col:
                    if slot["status"] == "empty":
                        st.markdown(
                            f"<div class='hash-slot slot-empty'><b>[{slot['index']}]</b><br>TRỐNG</div>",
                            unsafe_allow_html=True
                        )
                    elif slot["status"] == "deleted":
                        st.markdown(
                            f"<div class='hash-slot slot-deleted'><b>[{slot['index']}]</b><br>ĐÃ XÓA<br><small>{slot['product']}</small></div>",
                            unsafe_allow_html=True
                        )
                    else:
                        product = slot["product"]
                        st.markdown(
                            f"<div class='hash-slot slot-occupied'><b>[{slot['index']}]</b><br>{product.ma_san_pham}<br><small>{product.ten_san_pham}</small></div>",
                            unsafe_allow_html=True
                        )


def show_statistics():
    """Display hash table statistics"""
    if st.session_state.hash_table is None:
        return
    
    stats = st.session_state.hash_table.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Kích thước", stats["size"])
    with col2:
        st.metric("Đã sử dụng", stats["occupied"])
    with col3:
        st.metric("Load Factor", f"{stats['load_factor']:.2%}")
    with col4:
        st.metric("Số va chạm", stats["collisions"])


def show_probe_sequence(probe_seq: list, message: str):
    """Display probe sequence"""
    if probe_seq:
        st.info(f"🔍 {message}\n\nChuỗi thăm dò: {' → '.join(map(str, probe_seq))}")


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.title("📦 Hệ thống Quản lý Sản phẩm")
    st.markdown("### Sử dụng Double Hashing")
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Cấu hình")
        
        # Check if database exists
        if st.session_state.db_manager.exists() and st.session_state.hash_table is None:
            if st.button("📂 Load Database hiện có", use_container_width=True):
                load_table()
        
        # Create new table
        st.subheader("Tạo Hash Table mới")
        table_size = st.number_input(
            "Kích thước Hash Table",
            min_value=5,
            max_value=100,
            value=11,
            step=1,
            help="Nên chọn số nguyên tố để giảm va chạm"
        )
        
        if st.button("🆕 Tạo mới", use_container_width=True):
            create_new_table(table_size)
            st.rerun()
        
        # Prime number suggestions
        st.caption("💡 Các số nguyên tố gợi ý: 11, 13, 17, 19, 23, 29, 31, 37, 41, 47, 53")
        
        st.divider()
        
        # Reset database
        if st.button("🗑️ Xóa Database", use_container_width=True, type="secondary"):
            if st.session_state.db_manager.delete():
                st.session_state.hash_table = None
                st.success("✅ Đã xóa database")
                st.rerun()
    
    # Main content
    if st.session_state.hash_table is None:
        st.info("👈 Vui lòng tạo Hash Table mới hoặc load database từ sidebar")
        return
    
    # Statistics
    show_statistics()
    st.divider()
    
    # Tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Thêm sản phẩm", "🔍 Tìm kiếm", "🗑️ Xóa sản phẩm", "📋 Danh sách"])
    
    # Tab 1: Add Product
    with tab1:
        st.subheader("Thêm sản phẩm mới")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ma_sp = st.text_input("Mã sản phẩm *", key="add_ma")
            ten_sp = st.text_input("Tên sản phẩm *", key="add_ten")
            gia = st.number_input("Giá (VNĐ) *", min_value=0.0, step=1000.0, key="add_gia")
        
        with col2:
            so_luong = st.number_input("Số lượng *", min_value=0, step=1, key="add_sl")
            mo_ta = st.text_area("Mô tả", key="add_mota")
        
        if st.button("➕ Thêm sản phẩm", type="primary", use_container_width=True):
            if not ma_sp or not ten_sp:
                st.error("❌ Vui lòng nhập đầy đủ thông tin bắt buộc!")
            else:
                product = Product(
                    ma_san_pham=ma_sp,
                    ten_san_pham=ten_sp,
                    gia=gia,
                    so_luong=so_luong,
                    mo_ta=mo_ta
                )
                
                success, message, probe_seq = st.session_state.hash_table.insert(product)
                
                if success:
                    st.success(f"✅ {message}")
                    show_probe_sequence(probe_seq, "Quá trình tìm vị trí")
                    st.session_state.db_manager.save(st.session_state.hash_table)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
                    if probe_seq:
                        show_probe_sequence(probe_seq, "Quá trình thử tìm vị trí")
    
    # Tab 2: Search Product
    with tab2:
        st.subheader("Tìm kiếm sản phẩm")
        
        search_key = st.text_input("Nhập mã sản phẩm cần tìm:", key="search_key")
        
        if st.button("🔍 Tìm kiếm", type="primary", use_container_width=True):
            if not search_key:
                st.warning("⚠️ Vui lòng nhập mã sản phẩm")
            else:
                product, pos, probe_seq = st.session_state.hash_table.search(search_key)
                
                if product:
                    st.success(f"✅ Tìm thấy tại vị trí {pos}")
                    show_probe_sequence(probe_seq, "Quá trình tìm kiếm")
                    
                    # Display product details
                    st.subheader("Thông tin sản phẩm:")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Mã SP:** {product.ma_san_pham}")
                        st.write(f"**Tên:** {product.ten_san_pham}")
                        st.write(f"**Giá:** {product.gia:,.0f}đ")
                    with col2:
                        st.write(f"**Số lượng:** {product.so_luong}")
                        st.write(f"**Mô tả:** {product.mo_ta}")
                else:
                    st.error("❌ Không tìm thấy sản phẩm")
                    show_probe_sequence(probe_seq, "Quá trình tìm kiếm")
    
    # Tab 3: Delete Product
    with tab3:
        st.subheader("Xóa sản phẩm")
        
        delete_key = st.text_input("Nhập mã sản phẩm cần xóa:", key="delete_key")
        
        if st.button("🗑️ Xóa sản phẩm", type="primary", use_container_width=True):
            if not delete_key:
                st.warning("⚠️ Vui lòng nhập mã sản phẩm")
            else:
                success, message, probe_seq = st.session_state.hash_table.delete(delete_key)
                
                if success:
                    st.success(f"✅ {message}")
                    show_probe_sequence(probe_seq, "Quá trình tìm kiếm để xóa")
                    st.session_state.db_manager.save(st.session_state.hash_table)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
                    show_probe_sequence(probe_seq, "Quá trình tìm kiếm")
    
    # Tab 4: List All Products
    with tab4:
        st.subheader("Danh sách tất cả sản phẩm")
        
        products = st.session_state.hash_table.get_all_products()
        
        if products:
            # Create DataFrame for display
            data = []
            for pos, product in products:
                data.append({
                    "Vị trí": pos,
                    "Mã SP": product.ma_san_pham,
                    "Tên sản phẩm": product.ten_san_pham,
                    "Giá": f"{product.gia:,.0f}đ",
                    "Số lượng": product.so_luong,
                    "Mô tả": product.mo_ta
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.caption(f"📊 Tổng số: {len(products)} sản phẩm")
        else:
            st.info("📭 Chưa có sản phẩm nào trong hệ thống")
    
    # Visualization at bottom
    st.divider()
    visualize_hash_table()
    
    # Collision logs section
    st.divider()
    st.subheader("📋 Chi tiết Va chạm & Cách xử lý")
    
    collision_logs = st.session_state.hash_table.get_collision_logs()
    
    if collision_logs:
        st.markdown("""
        **Double Hashing** xử lý va chạm bằng cách:
        1. **Hash lần 1**: Tính vị trí ban đầu `h1(key)`
        2. **Nếu va chạm**: Sử dụng hash lần 2 `h2(key)` làm bước nhảy
        3. **Thăm dò**: `position = (h1 + i × h2) mod size` với i = 0, 1, 2, ...
        4. **Tiếp tục** cho đến khi tìm được vị trí trống hoặc tìm thấy key
        """)
        
        # Create expander for each collision event
        for i, log in enumerate(reversed(collision_logs[-10:])):  # Show last 10
            with st.expander(f"🔴 Event #{len(collision_logs) - i}: {log['operation']} - Key: {log['key']} ({log['collision_count']} va chạm)"):
                col1, col2 = st.columns([2, 3])
                
                with col1:
                    st.write("**Thông tin:**")
                    st.write(f"- Phép toán: `{log['operation']}`")
                    st.write(f"- Mã SP: `{log['key']}`")
                    st.write(f"- Số va chạm: `{log['collision_count']}`")
                
                with col2:
                    st.write("**Chuỗi thăm dò:**")
                    probe_str = " → ".join([f"**[{p}]**" if i == len(log['probe_sequence'])-1 else f"[{p}]" 
                                            for i, p in enumerate(log['probe_sequence'])])
                    st.markdown(probe_str)
                
                st.info(f"✅ **Kết quả**: {log['resolution']}")
        
        if len(collision_logs) > 10:
            st.caption(f"Hiển thị 10 sự kiện gần nhất. Tổng cộng: {len(collision_logs)} sự kiện va chạm")
    else:
        st.info("✨ Chưa có va chạm nào xảy ra. Thử thêm nhiều sản phẩm hơn!")


if __name__ == "__main__":
    main()
