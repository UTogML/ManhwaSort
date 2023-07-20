import pandas as pd
import streamlit as st
st.set_page_config(
        page_title="ManhwaSort",
        layout="wide"
)
st.title("Manhwa Sort")

df = pd.read_csv("./ManhwaList.csv")
df.drop('Legend:', axis=1, inplace=True)
df.drop([1,0], axis=0, inplace=True)
# st.dataframe(df)


def extract_name(cell):
    parts = cell.split('(')
    name = parts[0].strip()
    return name
def extract_rating(cell):
    if "(HR)" in cell:
        return "Highly Recommended"
    elif "(R)" in cell:
        return "Recommended"
    elif "(G)" in cell:
        return "Good"
    elif "(D)" in cell:
        return "Decent"
    elif "(M)" in cell:
        return "Meh"
    else:
        return None
def extract_length(cell):
    if "(+100)" in cell:
        return "Over a Hundred Chapters"
    elif "(-100)" in cell:
        return "Less than a Hundred Chapters"
    else:
        return None
name_genre_dict = {}
for index, row in df.iterrows():
    for column in df.columns:
        cell_value = row[column]
        if pd.notna(cell_value):
            name = extract_name(cell_value)
            rating = extract_rating(cell_value)
            length = extract_length(cell_value)
            genre = column

            if name in name_genre_dict:
                name_genre_dict[name]['Genre'].append(genre)
            else:
                name_genre_dict[name] = {'Name': name, 'Rating': rating, 'Genre': [genre], 'Length': length}

new_df = pd.DataFrame(list(name_genre_dict.values()))



st.sidebar.header("Filters")

rating = st.sidebar.multiselect(
    "Select Rating:", 
    options=new_df['Rating'].unique(),
    default=new_df['Rating'].unique()
)
length = st.sidebar.multiselect(
    "Select Length:", 
    options=new_df['Length'].unique(),
    default=new_df['Length'].unique()
)
genre = st.sidebar.multiselect(
    "Select Genre:", 
    options=new_df['Genre'].explode().unique(),
    default=new_df['Genre'].explode().unique()
)

def has_selected_genre(selected_genres, all_genres):
    return any(genre in all_genres for genre in selected_genres)

mask = (
    new_df["Rating"].isin(rating) &
    new_df["Length"].isin(length) &
    new_df["Genre"].apply(lambda g : has_selected_genre(genre, g))
)

df_selection = new_df[mask].reset_index(drop=True)

st.dataframe(df_selection)