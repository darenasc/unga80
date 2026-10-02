import sqlite3
from pathlib import Path
from random import randrange

import geopandas as gpd
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="#UNGA80",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def get_data(db: Path) -> pd.DataFrame:
    """Returns a pd.DataFrame with the following columns:
    - country
    - url
    - full_speech
    - summary
    - countries_mentioned
    - risks
    - haiku
    - word
    """
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        rows = cursor.execute("""SELECT * FROM countries;""").fetchall()
        column_names = [x[0] for x in cursor.description]
        cursor.close()

    df = pd.DataFrame(rows, columns=column_names)
    return df


df = get_data(Path(__file__).absolute().parent / "countries.db")
geo_data = gpd.read_file(
    Path(__file__).absolute().parent / "ne_110m_admin_0_countries.zip"
)

if "random_initial_country" not in st.session_state:
    st.session_state.random_initial_country = randrange(len(df))
    st.session_state.disabled = False

with st.sidebar:
    country_selection = st.selectbox(
        "Country",
        df["country"].sort_values().to_list(),
        index=st.session_state.random_initial_country,
    )  # type: ignore
    ISO_3 = df[df["country"] == country_selection].iso_3.values[0]

title = f"UNGA80 {country_selection}"

st.title(title)

with st.sidebar:
    st.divider()
    if ISO_3 in geo_data["ADM0_A3"].unique():
        st.caption(f'{geo_data[geo_data["ADM0_A3"]==ISO_3]["CONTINENT"].values[0]}')
        st.caption(
            f'(Economy) {str(geo_data[geo_data["ADM0_A3"]==ISO_3]["ECONOMY"].values[0]).split(". ")[-1]}'
        )
        st.caption(
            f'(Income group) {str(geo_data[geo_data["ADM0_A3"]==ISO_3]["INCOME_GRP"].values[0]).split(". ")[-1]}'
        )
        st.caption(
            f'Population: {geo_data[geo_data["ADM0_A3"]==ISO_3]["POP_EST"].apply(int).values[0]:,} (Est. {geo_data[geo_data["ADM0_A3"]==ISO_3]["POP_YEAR"].values[0]})'
        )
        st.caption(
            f'GDP: USD${geo_data[geo_data["ADM0_A3"]==ISO_3]["GDP_MD"].apply(int).values[0]:,}M ({geo_data[geo_data["ADM0_A3"]==ISO_3]["GDP_YEAR"].apply(int).values[0]})'
        )
    st.divider()

    # TBA:
    # Capital
    # Area
    # Timezones
    # Currency
    # Languages
    # Gini
    # Borders
    # Flag
    # Coat of arms

    st.divider()

    st.markdown(
        "[Feedback and comments are welcomed](https://github.com/darenasc/unga80/issues)"
    )


col1, col2 = st.columns(2)

with col1:
    fig = px.choropleth(
        locations=[ISO_3],
        locationmode="ISO-3",
    )
    st.plotly_chart(fig)

    if df[df["country"] == country_selection]["summary"].values[0]:
        st.header("Summary")
        st.markdown(df[df["country"] == country_selection]["summary"].values[0])

with col2:
    st.video(str(df[df["country"] == country_selection]["url"].values[0]))

    col3, col4 = st.columns(2)

    with col3:
        if df[df["country"] == country_selection]["haiku"].values[0]:
            st.header("Haiku")
            st.text(df[df["country"] == country_selection]["haiku"].values[0])

    with col4:
        if df[df["country"] == country_selection]["word"].values[0]:
            st.header("In One Word")
            st.title(f'{df[df["country"] == country_selection]["word"].values[0]}')
        if (
            Path(__file__).absolute().parent / "audio" / f"{country_selection}_yoda.wav"
        ).exists():
            st.header("Yoda & Sagan")
            st.audio(
                Path(__file__).absolute().parent
                / "audio"
                / f"{country_selection}_yoda.wav",
                format="audio/wav",
            )


if df[df["country"] == country_selection]["risks"].values[0]:
    st.header("Risks")
    st.markdown(df[df["country"] == country_selection]["risks"].values[0])

if df[df["country"] == country_selection]["countries_mentioned"].values[0]:
    st.header("Countries mentioned")
    st.markdown(df[df["country"] == country_selection]["countries_mentioned"].values[0])
