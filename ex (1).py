from textblob import TextBlob
import pandas as pd 
import streamlit as st
import cleantext

st.header('Sentiment Analysis')
st.write('The keyword input is given by running csvcreate.py')
st.write()
st.write('Provide the file- Analyse.csv from working directory')

with st.expander('Analyzed CSV'):
        
       # print('The URL link: ',df1[0][0])
        upl = st.file_uploader('Upload file: ')

        def score(x):
            blob1 = TextBlob(x)
            return blob1.sentiment.polarity
        
        def analyze(x):
            if x >= 0.5:
                return 'Positive'
            elif x<= -0.5:
                return 'Negative'
            else:
                return 'Neutral'
    
        if upl:
            df = pd.read_csv(upl)
                #del df['Unnamed:0']
            df['score'] = df['tweets'].apply(score)
            df['analysis'] = df['score'].apply(analyze)
            st.write(df.head())
            @st.cache_data
            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8')

            csv = convert_df(df)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='sentiment.csv',
                mime='text/csv', 
            )
            st.write('By downloading a sentiment.csv file is obtained')