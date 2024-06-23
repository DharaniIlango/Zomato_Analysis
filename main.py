import streamlit as st
from streamlit_option_menu import option_menu
import webbrowser
import yfinance as yf
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

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

df_user = pd.read_excel(io="zomato_data.xlsx",
                        engine='openpyxl',
                        sheet_name='users',
                        usecols='A:F',
                        nrows=100001)

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
        
# #Menu4 - User Section
if selected =='User':
    st.title("User 👤")
    st.write(df_user)
    user_select = st.selectbox("Choose the Field to be Analysed...",
                               ("Age", "Gender", "Marital Status", "Occupational Status"))
    if user_select == 'Age':
        st.header("Age")
        col1, col2, col3 = st.columns([2, 0.5, 2])
        with col1:
            age_distribution = df_user["Age"].value_counts().sort_index()
            st.subheader("Age Distribution")
        #barchart for age distribution
            fig_age_bar = px.bar(
                df_user,
                x = age_distribution.index,
                y = age_distribution.values,
                labels = {'x': "Age", 'y': "No. of Users"},
                hover_data = {'x': True, 'y': True},
                width = 800,
                height = 500,
                color='rgb(203, 32, 45)'
            )
            fig_age_bar.update_layout(
                xaxis_title = "Age",
                yaxis_title = "No. of Users",
                xaxis = dict(tickmode = 'linear')
            )
            st.plotly_chart(fig_age_bar)
            
        with col3:
            st.subheader("Trend of Age across Users")
            age_distribution.columns = ["Age", "Count"]
            chart = alt.Chart(age_distribution.mark_line(color='rgb(203, 32, 45)').encode(
                    x='Age',
                    y='Count',
                    tooltip = ["Age", "Count"]
                ).properties(
                    width=800,
                    height=500
                ).configure_title(
                    fontSize = 16,
                    anchor = 'middle'
                ).interactive())
            st.altair_chart(chart, use_container_width=True)
        
        fig = px.bar(
            x = age_distribution.index,
            y = age_distribution.values,
            color = df_user['Gender'],
            barmode = 'group',
            labels = {'Age': 'Age Group', 'Count': 'Count of Users', 'Gender': 'Gender'},
            title ='Age Distribution by Gender')
        
        fig.update_layout(
        xaxis_title='Age Group',
        yaxis_title='Count of Users',
        legend_title='Gender',
        width=800,
        height=500
        )
        st.subheader("Age Distribution by Gender")
        st.plotly_chart(fig)