import streamlit as st
import pandas as pd
import warnings
import plotly.express as px
warnings.filterwarnings('ignore')

df = pd.read_csv('main_data.csv')
df['order_approved_at'] = pd.to_datetime(df['order_approved_at'], errors='coerce')

#Sidebar berisi Filter, Titles dan Description
with st.sidebar:
    #Titles dan Description
    st.title("Dicoding E-Commerce Dataset Analysis")
    st.write("By Muhammad Nur Irfan   itzirfanmt@gmail.com")
    st.caption('Menyelesaikan pertanyaan bisnis E-Commerce')

    #Filters Tahun!
    df['year'] = df['order_approved_at'].dt.year
    years = ["All Year"] + sorted(df['year'].dropna().unique().tolist())
    selected_year = st.selectbox("Select Year:", years)

if selected_year == "All Year":
    filtered_df = df 
else:
    filtered_df = df[df['year'] == selected_year]

#Responsive Titles dengan selected year
if selected_year == "All Year":
    st.header('Analisis Transaksi pada tahun 2016-2018')
else:
    st.header(f'Analisis Transaksi pada tahun {selected_year}')

#Jumlah User dan Jumlah Transaksi 
col1, col2 = st.columns(2)
#Jumlah User
with col1:
    total_users = filtered_df['customer_unique_id'].nunique()
    st.metric("Jumlah User: ", value=total_users)

#Jumlah Transaksi
with col2:
    total_orders = filtered_df['order_id'].nunique()
    st.metric("Jumlah Transaksi: ", value=total_orders)


#Grafik perkembangan order ditambah filter selected year
if selected_year == "All Year":
    st.subheader('Grafik transaksi per Hari dari 2016-2028')
else:
    st.subheader(f'Grafik transaksi per Hari pada tahun {selected_year}')
fig_transaction = px.area(
    filtered_df.groupby(['order_approved_at']).count(),
    labels = {
        'order_approved_at': 'Tanggal Pesanan',
        'order_id': 'Jumlah Transaksi'
    },
    y='order_id'
    )
fig_transaction.update_traces(line_color='#19A7CE')
st.plotly_chart(fig_transaction, use_container_width=True)


#Status Order & Rating Orders
st.subheader("Status Orders & Rating Orders")
col1, col2 = st.columns(2)
with col1:
    #Status Order Pie Chart
    st.write('Status Order berdasarkan banyak Order: ')

    # Memetakan status
    status_mapping = {
        'delivered': 'Finished',
        'shipped': 'Unfinished',
        'invoiced': 'Unfinished',
        'processing': 'Unfinished',
        'approved': 'Unfinished',
        'canceled': 'Finished',
        'unavailable': 'Unfinished'
    }
    df['order_status'] = df['order_status'].replace(status_mapping)

    # Menghitung kategori
    category_counts = filtered_df['order_status'].value_counts()

    # Membuat pie chart menggunakan Plotly Express
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        color_discrete_sequence=['#244993', '#AF3123']
    )
    fig.update_traces(textinfo='percent+label', textfont_size=18, marker=dict(line=dict(color='#000000',width=1)))
    # Menampilkan pie chart di Streamlit
    st.plotly_chart(fig)

with col2:

    st.write('Persebaran Rating pada Orders: ')

    review_orders = filtered_df.groupby(by="review_score").order_id.nunique()
    nozero_review_orders = review_orders[review_orders.index != 0]
    filtered_df['review_category'] = filtered_df['review_score'].apply(lambda x: 'Puas' if x > 3 else 'Tidak Puas')
    review_category_counts = filtered_df['review_category'].value_counts()

    # Membuat pie chart menggunakan Plotly
    fig = px.pie(
        values=review_category_counts.values,
        names=review_category_counts.index,
        color_discrete_sequence=['#FFC000', '#F3EFF5']
    )
    fig.update_traces(textinfo='percent+label', textfont_size=18, marker=dict(line=dict(color='#000000',width=1)))
    st.plotly_chart(fig)

st.subheader("Product's Best Category vs Worst Category ")
col1, col2 = st.columns(2)

category_order_counts = filtered_df.groupby('product_category_name_english')['order_id'].count().sort_values(ascending=False)

 #Menentukan best category & worst category
best_category = category_order_counts.head(5)
worst_category = category_order_counts.tail(5)

    # Plot Top 5 Category dengan Plotly
fig_best_category = px.bar(
    best_category,
    x=best_category.values,
    y=best_category.index,
    orientation='h',
    color_discrete_sequence=['#50C878'],
    text_auto='.2s'
)
fig_best_category.update_layout(xaxis_title="Jumlah Pelanggan Unik", yaxis_title="Category", yaxis=dict(autorange="reversed"))


# Plot Bottom 5 Category dengan Plotly
fig_worst_category = px.bar(
     worst_category,
     x=worst_category.values,
     y=worst_category.index,
     orientation='h',
     color_discrete_sequence=['red'],
     text_auto='.2s'
)
fig_worst_category.update_layout(xaxis_title="Jumlah Pelanggan Unik", yaxis_title="Category")
fig_worst_category.update_xaxes(range=[0,100])

col1.write('Top 5 Best Category: ')
col1.plotly_chart(fig_best_category, use_container_width=True)

col2.write('Bottom 5 Worst Category: ')
col2.plotly_chart(fig_worst_category, use_container_width=True)


st.subheader("Order's best State vs Order's Worst State")
col1, col2 = st.columns(2)

cus_state_perform = filtered_df.groupby(by="customer_state").customer_id.nunique().sort_values(ascending=False)
filtered_customers_state = cus_state_perform[cus_state_perform.index != 'Unknown']

# Mendapatkan top 5 dan bottom 5 negara bagian
best_state = filtered_customers_state.head(5)
worst_state = filtered_customers_state.tail(5)

# Plot untuk Top 5 Negara Bagian
fig_best_state = px.bar(
    best_state,
    x=best_state.index,
    y=best_state.values,
    color_discrete_sequence=['green'],
    text_auto='.2s'
)
fig_best_state.update_layout(xaxis_title="Negara Bagian", yaxis_title="Jumlah Pelanggan Unik")


# Plot untuk Bottom 5 Negara Bagian
fig_worst_state = px.bar(
    worst_state,
    x=worst_state.index,
    y=worst_state.values,
    color_discrete_sequence=['red'],
    text_auto='.2s'
)
fig_worst_state.update_layout(xaxis_title="Negara Bagian", yaxis_title="Jumlah Pelanggan Unik")
fig_worst_state.update_yaxes(range=[0,1000])
# Menampilkan Grafik
col1.write("Top 5 Order's Best State: ")
col1.plotly_chart(fig_best_state, use_container_width=True)

col2.write("Bottom 5 Order's Worst State: ")
col2.plotly_chart(fig_worst_state, use_container_width=True)

# Filter untuk mengkalkulasi hanya jika order_status adalah Finished
completed_orders = filtered_df[filtered_df['order_status'] == 'Finished']
reference_date = completed_orders['order_approved_at'].max()

# Menghitung metrik RFM
rfm_data = completed_orders.groupby('customer_id').agg({
    'order_approved_at': lambda x: (reference_date - x.max()).days,  # Recency
    'order_id': 'nunique',                                           # Frequency
    'price': 'sum'                                                   # Monetary
}).reset_index()

rfm_data.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']

# Plot Recency
fig_recency = px.histogram(rfm_data, x='Recency', nbins=20, title="Distribusi Recency")
fig_recency.update_layout(xaxis_title="Recency (days)", yaxis_title="Number of Customers")

# Plot Frequency
fig_frequency = px.histogram(rfm_data, x='Frequency', title="Distribusi Frequency")
fig_frequency.update_layout(xaxis_title="Frequency (orders)", yaxis_title="Number of Customers", bargap=0.8)

# Plot Monetary
fig_monetary = px.histogram(rfm_data, x='Monetary', nbins=10, title="Distribusi Monetary")
fig_monetary.update_layout(xaxis_title="Monetary (spending)", yaxis_title="Number of Customers")

st.subheader('RFM Analysis')
col1, col2, col3 = st.columns(3)
# Menampilkan Grafik
col1.plotly_chart(fig_recency, use_container_width=True)
col2.plotly_chart(fig_frequency, use_container_width=True)
col3.plotly_chart(fig_monetary, use_container_width=True)

# Penjelasan RFM
with st.expander("Lihat Penjelasan RFM"):
        st.subheader("Recency: ")
        st.write("Recency digunakan untuk mengetahui jumlah hari transaksi yang pelanggan lakukan terakhir kali. Jika grafik menunjukkan Skewed menuju low value, berarti terdapat beberapa pelanggan yang baru saja malekukan pemesanan ")
        st.subheader("Frequency: ")
        st.write("Frequency digunakan untuk mengetahui jumlah transaksi yang biasanya pelanggan gunakan. Dalam grafik dapat disimpulkan bahwa pelanggan hanyak melakukan 1 kali transaksi")
        st.subheader("Monetary: ")
        st.write("Monetary digunakan untuk mengetahui jumlah pengeluaran yang dilakukan pelanggan. Kelompok pelanggan yang melakukan monetary sedikit sebaiknya diberikan promo bundling, sementara kelompok pelanggan yang melakukan monetary besar sebaiknya diberikan diskon ")

