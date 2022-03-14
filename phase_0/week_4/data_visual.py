from calendar import week
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

def app():
    #st.cache

    st.set_option('deprecation.showPyplotGlobalUse', False)

    df = pd.read_csv('supermarket_sales.csv')
    df_ori = df
    #renaming columns
    df = df.rename(columns={
        'Invoice ID': 'invoice_id', 'Branch': 'branch', 'City': 'city', 'Customer type': 'cust_type',
        'Gender': 'gender', 'Product line': 'products', 'Unit price': 'unit_price', 'Quantity': 'qty', 
        'Tax 5%': 'tax5%', 'Total': 'total', 'Payment': 'payment', 'gross margin percentage': 'gross_margin',
        'gross income': 'gross_income', 'Rating': 'rating'}
        )
    #adding rating description columns
    df['rating3'] = 'empty'
    df['rating2'] = 'empty'
    for i in range(df.shape[0]):
        df.iloc[i,-2] = df.iloc[i,16]/10*5
        if 5 >= df.iloc[i,-2] >4:
            df.iloc[i,-1] = 'Very Good'
        elif 4 >= df.iloc[i,-2] >3:
            df.iloc[i,-1] = 'Good'
        elif 3 >= df.iloc[i,-2] >2:
            df.iloc[i,-1] = 'Not Good'
        elif 2 >= df.iloc[i,-2] >1:
            df.iloc[i,-1] = 'Bad'
        else:
            df.iloc[i,-1] = 'Very Bad'
    df = df.drop(columns='rating3')

    #merging city and branch
    df['branch_city'] = 'empty'
    for i in range(df.shape[0]):
        df.iloc[i,-1] = df.iloc[i,2]+'/'+df.iloc[i,1]
    df = df.drop(columns=['branch', 'city'])

    #adding hour and minute column
    df['hour'] = 0.0
    df['minute'] = 0.0
    for i in range(df.shape[0]):
        df.iloc[i,-2] = float(df.iloc[i,9][0:2])
        df.iloc[i,-1] = float(df.iloc[i,9][3:5])

    #separating day and month as a columns
    df.Date = pd.to_datetime(df.Date)
    df['day'] = 0
    df['month'] = 0
    for i in range(df.shape[0]):
        df.iloc[i,-2] = str(df.iloc[i,8].day)
        df.iloc[i,-1] = str(df.iloc[i,8].month)

    ########################## Page Border #############################
    st.markdown("<h1 style='text-align: center; color: black;'> ➡️INFOGRAPHIC SECTION⬅️ </h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>Finance Growth & Customer Satisfication</h1>", unsafe_allow_html=True)

    with st.expander("Dataset Info"):
        show_df= st.checkbox('show dataframe')
        #st.write(show_df) #true atau false
        if show_df:
            st.write(df_ori)
        st.write("""
            The dataset was downloaded on kaggle.com. it was uploaded by Aung Pyae and updated 3 years ago. 
        """)
        st.write('Context')
        st.write('''The growth of supermarkets in most populated cities are increasing and market competitions are also high. The dataset is one of the historical sales of 
                supermarket company which has recorded in 3 different branches for 3 months data.''')
        
        ket = pd.DataFrame({'Invoice id': ['Computer generated sales slip invoice identification number'],
        'Branch': ['Branch of supercenter (3 branches are available identified by A, B and C).'],
        'city': ['Location of supercenters'], 
        'Customer Type': ['Type of customers, recorded by Members for customers using member card and Normal for without member card.'],
        'Gender': ['Gender type of customer'],
        'Product Line': ['General item categorization groups - Electronic accessories, Fashion accessories, Food and beverages, Health and beauty, Home and lifestyle, Sports and travel'],
        'Unit price': ['Price of each product in $'],
        'Quantity': ['Number of products purchased by customer'],
        'Tax': ['5% tax fee for customer buyingr'],
        'Total': ['Total price including tax'],
        'Date': ['Date of purchase (Record available from January 2019 to March 2019)'],
        'Total': ['Total price including tax'],
        'Time': ['Purchase time (10am to 9pm)'],
        'Payment': ['Payment used by customer for purchase (3 methods are available – Cash, Credit card and Ewallet)'],
        'COGS': ['Cost of goods sold'],
        'Gross income': ['Gross income'],
        'Gross margin percentage': ['Gross margin percentage'],
        'Rating': ['Customer stratification rating on their overall shopping experience (On a scale of 1 to 10) Acknowledgements']
        })
        st.table(ket.T)

    st.header('Get To Know Our Customer')

    col1, col2, col3 = st.columns([1, 0.2, 1])
    prod = df.products.value_counts().to_frame().reset_index().rename(columns={'products': 'Quantity', 'index': 'Products'})
    fig = px.pie(prod, values='Quantity', names='Products', title='Product Unit Sold Within 3 Months')
    col1.plotly_chart(fig)

    product_by_gender = df.groupby(['products', 'gender']).size().unstack()
    product_by_gender = pd.DataFrame(product_by_gender).reset_index()
    with plt.style.context('ggplot'):
        plt.figure(figsize=(13,8))
        ind = np.arange(6)
        w = 0.3
        plt.bar(ind, product_by_gender.Male, w, label='Male', color='#6495ED')
        plt.bar(ind+w, product_by_gender.Female, w, label='Female', color='#EEA2AD')
        plt.xlabel('Products')
        plt.ylabel('Customer Counts')
        plt.title('Male Vs Female Product Line')
        plt.xticks(ind + w / 2, product_by_gender.products)
        plt.ylim(0, 110)
        plt.legend(loc='best')
        plt.show()
        col3.pyplot()

    col21, col22, col23 = st.columns([1, 0.2, 1])
    with col21.expander("Enlighten me 🔎"):
        st.write("""
            Its seems like the pie is equally sliced into the same pieces, 
            but if we look closer there is some product that leads in term of sold unit. In top place, 
            Fashion products took 17.8 % of unit sold while the other product such as health and beauty stated in the lowest precentage.
        """)

    with col23.expander("Enlighten me 🔎"):
        st.write("""
            The bar chart above simply tell us about what women/men likes to buy. lets evaluate the extreme case! in the Fashion accesoris section, 
            there is a pretty huge gaps between the number of man and woman that buy those products. its indicating, that female love to buy
            fashion accesoris product more than men do. now lets move to health and beauty product, the gaps between them is quite big right. this can
            be indication too that men love health and beauty product more dan women do.
        """)

    col31, col32, col33, col34 = st.columns([1, 0.2, 1, 0.25])
    pay = df.payment.value_counts().to_frame().reset_index().rename(columns={'index': 'Payment', 'payment': 'Counts'})
    fig = px.pie(pay, values='Counts', names='Payment', title='Customer Counts Based on Payment Method')
    col31.plotly_chart(fig)

    cities =col34.selectbox(
        "Choose City",
        ('All Cities', 'Yangon', 'Mandalay', 'Naypyitaw'))

    if cities == 'Yangon':
        sale_by_hour = df[df['branch_city']=='Yangon/A'].groupby(['hour']).size().reset_index(name='counts')
    elif cities == 'Mandalay':
        sale_by_hour = df[df['branch_city']=='Mandalay/B'].groupby(['hour']).size().reset_index(name='counts')
    elif cities == 'Naypyitaw':
        sale_by_hour = df[df['branch_city']=='Naypyitaw/C'].groupby(['hour']).size().reset_index(name='counts')
    else:
        sale_by_hour = df.groupby(['hour']).size().reset_index(name='counts')

    with plt.style.context('ggplot'):
        fig=px.bar(sale_by_hour, x='hour', y='counts', title='Customer Total Volume for Every Specific Hours in {}'.format(cities))
        plt.show()
        col33.plotly_chart(fig)

    col41, col42, col43 = st.columns([1, 0.2, 1])
    with col41.expander("Enlighten me 🔎"):
        st.write("""
            for once again at the first glance the pie chart seems like being sliced equally. but if we look closer, we can conclude that
            credit card method is less common payment method than the other two method. 
        """)

    with col43.expander("Enlighten me 🔎"):
        st.write("""
            The bar chart above show us a total purchase that occuring in specific hours for last 3 months. there is a pattern we can see here.
            by observing the peak bar, we can assuming that there are some busy hours. for example, on 10 AM, 1 PM, and 7 PM the amount of
            transaction goes highest than the other hours. its a good sign so we can maximize our sale in this crucial hours.
        """)


    st.subheader("What's their thoughts about ours")

    days = st.slider('What DAY you want to inspect?', 1, 89, 89)

    rating_day = df.groupby(['Date','rating2'])['rating2'].count().unstack().reset_index().set_index('Date')
    rating_day.insert(0, 'Very Bad', 0)
    rating_day = rating_day.replace(np.nan, 0)
    rating_day['mean'] = df.groupby(['Date'])['rating'].mean()
    rating_day['sum'] = rating_day.T.iloc[0:5].sum()

    st.write('Date : ', str(rating_day.index[days-1])[0:10])

    col51, col52, col53, col54 = st.columns([0.8,1,1,0.1])
    col52.metric("Rating by Average", rating_day['mean'][days-1].round(2), 
                (rating_day['mean'][days-1]-rating_day['mean'][days-2]).round(2)
                )
    col53.metric("Customer Total Count", rating_day['sum'][days-1], rating_day['sum'][days-1]-rating_day['sum'][days-2])

    fig = go.Figure(go.Bar(
                x=rating_day.iloc[days-1][0:5].values,
                y=['Very Bad (R <= 20)', 'Bad (20 < R <= 40)', 'Not Good (40 < R <= 60)', 'Good (60 < R <= 80)', 'Very Good (R > 80)'],
                orientation='h'))
    fig.update_layout(autosize=False,
        width=1400,
        height=400,
        title_text='Rating For Specific Days', xaxis_title='Customer Count')
    st.plotly_chart(fig)

    #############
    rat= df.groupby(['branch_city', 'rating2']).size().unstack()
    rat = pd.DataFrame(rat).reset_index()
    cit = ['Mandalay/B', 'Naypyitaw/C', 'Yangon/A']

    fig = go.Figure(data=[
        go.Bar(name='Very Good', x=cit, y=rat['Very Good']),
        go.Bar(name='Good', x=cit, y=rat['Good']),
        go.Bar(name='Not Good', x=cit, y=rat['Not Good']),
        go.Bar(name='Bad', x=cit, y=rat['Bad']),
        go.Bar(name='Very Bad', x=cit, y=[0,0,0]),
    ])
    fig.update_layout(autosize=False,
        width=1400,
        height=400,
        title_text='Rating Summary by City/Branch'
        )
    st.plotly_chart(fig)
    with st.expander("Enlighten me 🔎"):
        st.write("""
            The bar chart above is a summerize rating for each branch/city for last 3 motnths. visually, Naypitaw/C has really good rating
            summary. the blue bar of Naypitaw/C which refer to 'Very Good' rating is the highest than the rest of branch/city. but overall, there is no
            'very bad' rating in all branch, which mean we have to keep this up and increaring the 'very good' rating significanly.
        """)

    #####################
    st.header('Business Growth Overview')
    month_3 = ['January', 'February', 'March']
    fig = go.Figure(go.Bar(
                x=df.groupby('month')['total'].sum(),
                y=month_3,
                orientation='h'))
    fig.update_layout(autosize=False,
        width=1400,
        height=400,
        title_text='Monthly Revenue', xaxis_title='Revenue')
    st.plotly_chart(fig)

    col51, col52 = st.columns(2)
    branch_products_count = df.groupby(['branch_city','products'])['qty'].sum()
    branch_products_count = pd.DataFrame(branch_products_count).reset_index()

    fig = go.Figure(data=[
        go.Bar(name=branch_products_count['products'][0:18:6].loc[0], x=cit, y=branch_products_count['qty'][0:18:6]),
        go.Bar(name=branch_products_count['products'][1:18:6].loc[1], x=cit, y=branch_products_count['qty'][1:18:6]),
        go.Bar(name=branch_products_count['products'][2:18:6].loc[2], x=cit, y=branch_products_count['qty'][2:18:6]),
        go.Bar(name=branch_products_count['products'][3:18:6].loc[3], x=cit, y=branch_products_count['qty'][3:18:6]),
        go.Bar(name=branch_products_count['products'][4:18:6].loc[4], x=cit, y=branch_products_count['qty'][4:18:6])
    ])
    fig.update_layout(
        title_text='Most Purchased Product on Each City/Branch',
        xaxis_title='City/Branch',
        yaxis_title='Total Units Sold'
        )
    col51.plotly_chart(fig)

    branch_products_revenue = df.groupby(['branch_city','products'])['total'].sum()
    branch_products_revenue = pd.DataFrame(branch_products_revenue).reset_index()

    fig = go.Figure(data=[
        go.Bar(name=branch_products_revenue['products'][0:18:6].loc[0], x=cit, y=branch_products_revenue['total'][0:18:6]),
        go.Bar(name=branch_products_revenue['products'][1:18:6].loc[1], x=cit, y=branch_products_revenue['total'][1:18:6]),
        go.Bar(name=branch_products_revenue['products'][2:18:6].loc[2], x=cit, y=branch_products_revenue['total'][2:18:6]),
        go.Bar(name=branch_products_revenue['products'][3:18:6].loc[3], x=cit, y=branch_products_revenue['total'][3:18:6]),
        go.Bar(name=branch_products_revenue['products'][4:18:6].loc[4], x=cit, y=branch_products_revenue['total'][4:18:6])
    ])
    fig.update_layout(
        title_text='Best Sales Product on Each City/Branch',
        xaxis_title='City/Branch',
        yaxis_title='Total Revenue Earned'
        )
    col52.plotly_chart(fig)

    # col61, col62 = st.columns(2)
    # with col61.expander("Enlighten me 🔎"):
    #      st.write("""
    #          Under modified
    #      """)
    # with col62.expander("Enlighten me 🔎"):
    #      st.write("""
    #          Under modified
    #      """)

    total_by_day = df.groupby(['month', 'day'])['total'].sum().unstack()
    total_by_day = pd.DataFrame(total_by_day)
    list_total_day = list(total_by_day.iloc[0]) + list(total_by_day.iloc[1]) + list(total_by_day.iloc[2])
    list_total_day = [x for x in list_total_day if str(x) != 'nan']
    list_total_week = []
    for i in range(12):
        list_total_week.append(sum(list_total_day[i*7:(i+1)*7])/7)
    list_total_week.append(sum(list_total_day[84:90])/5)
    df2 =pd.DataFrame({'week': list(np.linspace(1,13, 13)), 'val': list_total_week})

    fig = px.line(df2, x='week', y='val')
    fig.update_layout(autosize=False,
        width=1450,
        height=400,
        title_text='Weekly Total Sales Mean',
        xaxis_title='Week',
        yaxis_title='Total Sales Mean'
        )
    st.plotly_chart(fig)