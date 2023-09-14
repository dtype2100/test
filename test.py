import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# select_target_label
# drop_columns
# drop_labels
# label_encoder
# prepro_datetime

def run():
    uploaded_file = st.sidebar.file_uploader('csv 파일 업로드', type='csv')
    updated_df = None
    le = LabelEncoder()
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df)

        col_list = df.columns.tolist()

    # if uploaded_file is None:
        
    #     df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], 'C': [7, 8, 9], 'target': ['one', 'two', 'three']})
    #     col_list = df.columns.tolist()

        target_feture = st.sidebar.multiselect('Select Target Column', options=col_list)
        drop_columns = st.sidebar.multiselect("Select drop columns", options=col_list)
        drop_labels = st.sidebar.multiselect("Select drop labels", options=col_list)
        label_encoder = st.sidebar.multiselect("label encoder", options=col_list)
        prepro_datetime = st.sidebar.multiselect("Select prepro_datetime", options=col_list)
    
        if st.sidebar.button('start preprocessing'):
            # updated_df = df
            if drop_columns:
                updated_df = df.drop(drop_columns, axis=1)
            if drop_labels:
                updated_df = df[df[drop_labels] != drop_labels]
            if label_encoder:
                st.write(label_encoder)
                if updated_df is None:
                    updated_df[label_encoder] = le.fit_transform(df[label_encoder[0]])
                if updated_df is not None:
                    updated_df[label_encoder] = le.fit_transform(updated_df[label_encoder[0]])
            st.write(updated_df)


if __name__ == "__main__":
    run()