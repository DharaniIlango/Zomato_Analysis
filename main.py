import streamlit as st
from streamlit_option_menu import option_menu
import webbrowser
import yfinance as yf
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Zomato Sales Analysis",
    page_icon=":ramen:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🥐:red[ Dig - In !!]")

with st.sidebar:
    selected = option_menu("Zomato Dashboard", ["Overview", "Food", "Food Menu", "Orders", "Restaurant", "User"],
                           icons=["globe-central-south-asia","repeat","journal-richtext","receipt","shop","people"],
                           menu_icon="option",
                           default_index=0,
                           styles={'nav-link':{'font-size':'15px', 'text-align':'left', 'margin':'-2px', '--hover-color':'rgb(203, 32, 45)'}, 'nav-link-selected':{'background-color': "rgb(203, 32, 45)"}})
    
#Loading the data files into the pandas df
df_food = pd.read_excel(io="zomato_data.xlsx",
                        engine='openpyxl',
                        sheet_name='food',
                        usecols='A:C',
                        nrows=371561)

#Menu1 - Overview Section
if selected=='Overview':
    st.markdown("## :red[Zomato] : Better Food for More People")
    col1, col2, col3 = st.columns([2, 0.5, 2])
    with col1:
        st.header("About")
        text = """
        <div style="text-align: justify;">
        Launched in 2010, the technology platform connects customers, restaurant partners, and delivery partners, serving their multiple needs. The platform is used by customers to search and discover restaurants, read and write customer-generated reviews, view and upload photos, order food delivery, book tables, and make payments while dining out at restaurants. On the other hand, restaurant partners are provided with industry-specific marketing tools, which enable engagement and acquisition of customers to grow their businesses, while a reliable and efficient last-mile delivery service is also provided. Additionally, a one-stop procurement solution, Hyperpure, is operated to supply high-quality ingredients and kitchen products to restaurant partners. Delivery partners are provided with transparent and flexible earning opportunities.
        </div>
        """
        st.write(text, unsafe_allow_html=True)
        
    with col3:
        st.header("Stock Value")
        ticker_symbol = "ZOMATO.NS"
        ticker_data = yf.Ticker(ticker_symbol)
        ticker_df = ticker_data.history(period='1y', interval='1h')
        chart = alt.Chart(ticker_df.reset_index()).mark_line(color='rgb(203, 32, 45)').encode(
                    x='Datetime:T',
                    y='Close:Q'
                ).properties(
                    width=800,
                    height=400
                )
        st.altair_chart(chart, use_container_width=True)
        
    column1, column2, column3 = st.columns([3,0.5,3])

    with column1:
        st.header("Goals")
        st.write("""
                    - Driving the force of :red[Assortment]
                    - Focussing on :red[Affordability]
                    - Boosting :red[Accessibility] for customers
                    - Improving :red[Quality] of Food
                    """)
        st.write("")
        url = "https://zomato.onelink.me/xqzv/CTA"
        if st.button("Get Your App Now"):
            webbrowser.open_new_tab(url)

    with column3:
        st.image("./Assets/zomato_icon.jpg")
        
#Menu2 - Food Section
if selected=='Food':
    st.markdown("## Food 🍽️")
    # Basic statistics
    st.write("### Basic Statistics")
    st.write(df_food.describe())

    # Count of Veg vs Non-Veg items
    st.write("### Count of Veg vs Non-Veg Items")
    veg_count = df_food['veg_or_non_veg'].value_counts().reset_index()
    veg_count.columns = ['Type', 'Count']
    veg_chart = alt.Chart(veg_count).mark_bar().encode(
        x='Type',
        y='Count',
        color='Type'
    ).properties(
        title='Count of Veg vs Non-Veg Items'
    )
    st.altair_chart(veg_chart, use_container_width=True)

    # Unique items by type
    st.write("### Unique Items by Type")
    unique_items = df_food.groupby('veg_or_non_veg')['item'].nunique().reset_index()
    unique_items.columns = ['Type', 'Unique Items']
    unique_items_chart = alt.Chart(unique_items).mark_bar().encode(
        x='Type',
        y='Unique Items',
        color='Type'
    ).properties(
        title='Unique Items by Type'
    )
    st.altair_chart(unique_items_chart, use_container_width=True)

    # Pie chart of Veg vs Non-Veg items
    st.write("### Pie Chart of Veg vs Non-Veg Items")
    veg_pie_chart = alt.Chart(veg_count).mark_arc().encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Type", type="nominal")
    ).properties(
        title='Veg vs Non-Veg Items'
    )
    st.altair_chart(veg_pie_chart, use_container_width=True)