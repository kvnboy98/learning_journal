import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
from scipy import stats

def app():

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

    st.markdown("<h1 style='text-align: center; color: black;'> ➡️HYPOTHESIS SECTION⬅️ </h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>Hypothesis Crosscheck Regarding Costumer Rating</h1>", unsafe_allow_html=True)

    st.subheader('Why We Care So Much About Rating?')
    st.write('''Rating is the main indicator that show us a customer satisfication level, its extremely important for someone
    who want to run a business. Hence a good rating business means how reliable the business is, its affect many thing from gaining trust
    to cause reccuring transaction or deal. ''')

    st.write('''so our problems here we need to find out whether the mean of customer rating on mandalay, naypitaw, and yangon is different or not.
    before we jump into the final conclusion, lets check the distibution of dataset for each city''')
    mandalay_rating = df[df['branch_city']=='Mandalay/B']['rating'].reset_index().drop(columns='index')
    naypitaw_rating = df[df['branch_city']=='Naypyitaw/C']['rating'].reset_index().drop(columns='index')
    yangon_rating = df[df['branch_city']=='Yangon/A']['rating'].reset_index().drop(columns='index')
    
    col11, col12, col13 = st.columns([1,1,1])
    fig = px.histogram(mandalay_rating)
    fig.update_layout(showlegend=False,
        autosize=False,
        width=400,
        height=300,
        title_text='Histogram Rating For Mandalay City', xaxis_title='Rating (0-10)') 
    col11.plotly_chart(fig)

    fig = px.histogram(naypitaw_rating)
    fig.update_layout(showlegend=False,
        autosize=False,
        width=400,
        height=300,
        title_text='Histogram Rating For Naypitaw City', xaxis_title='Rating (0-10)') 
    col12.plotly_chart(fig)

    fig = px.histogram(yangon_rating)
    fig.update_layout(showlegend=False,
        autosize=False,
        width=400,
        height=300,
        title_text='Histogram Rating For Yangon City', xaxis_title='Rating (0-10)') 
    col13.plotly_chart(fig)

    col21, col22, col23 = st.columns([1,1,1])
    with col21.expander("Read Central Tendendy"):
         st.write('Mean : ', mandalay_rating.mean()[0].round(2))
         st.write('Median : ', mandalay_rating.median()[0].round(2))
    
    with col22.expander("Read Central Tendendy"):
         st.write('Mean : ', naypitaw_rating.mean()[0].round(2))
         st.write('Median : ', naypitaw_rating.median()[0].round(2))
         
    with col23.expander("Read Central Tendendy"):
         st.write('Mean : ', yangon_rating.mean()[0].round(2))
         st.write('Median : ', yangon_rating.median()[0].round(2))
    
    st.subheader('Are They Share The Same Rating Average?')
    st.write('''As analyst, we can't blatantly saying that average of dataset is same or not, hence we need to perform statisticly 
    procedure to check them up. so for this case we consider to use ANOVA hypothesis testing. why ANOVA? its simply because our case
    involving more that two variables. ANOVA is similar to the t-test. It used for testing whether more than two variables are significantly 
    different or not. So, we will test whether the mean Customer rating on Mandalay, Naypitaw, and Yangon are significantly different or not.''')

    st.subheader('H0 : Mean CR on Mandalay = Mean CR on Naypitaw = Mean CR on Yangon')
    st.subheader('H1 : All the mean are not equal')
    st.write("Note")
    st.write("CR = Customer Rating")

    f_stat,p_value = stats.f_oneway(mandalay_rating, naypitaw_rating, yangon_rating)

    st.write("After some calculation, we have p_value = ", str(p_value))
    st.write('''Since p_value > 0.05, then its strong evidence that we should reject H1 and accept H0. so our final 
            conclusion is the difference of them is statistically insignificant or we can just simply say that 
            they share the same average.''')

