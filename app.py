import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="100K Films Explorer",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 100K Films Explorer")
st.write("Movie ratings analysis dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("films_analysis.csv")

df = load_data()

st.sidebar.header("Filters")

search = st.sidebar.text_input("Search movie title")

min_rating = st.sidebar.slider(
    "Minimum rating",
    1, 5, 1
)

filtered = df[
    (df["rating"] >= min_rating)
]

if search:
    filtered = filtered[
        filtered["title"].str.contains(
            search, case=False, na=False
        )
    ]

c1, c2, c3 = st.columns(3)

c1.metric("Ratings displayed", f"{len(filtered):,}")
c2.metric("Movies displayed", f"{filtered['movie_id'].nunique():,}")
c3.metric(
    "Average rating",
    f"{filtered['rating'].mean():.2f}"
    if len(filtered) else "N/A"
)

st.subheader("Rating Distribution")

if len(filtered):
    fig, ax = plt.subplots()
    filtered["rating"].value_counts().sort_index().plot(
        kind="bar", ax=ax
    )
    ax.set_xlabel("Rating")
    ax.set_ylabel("Number of ratings")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Top Movies")

    stats = filtered.groupby("title").agg(
        average_rating=("rating", "mean"),
        number_of_ratings=("rating", "count")
    )

    stats = stats[stats["number_of_ratings"] >= 20]
    stats = stats.sort_values(
        "average_rating", ascending=False
    ).head(10)

    st.dataframe(stats)

    st.subheader("Most Rated Movies")

    popular = filtered.groupby("title").agg(
        number_of_ratings=("rating", "count"),
        average_rating=("rating", "mean")
    ).sort_values(
        "number_of_ratings", ascending=False
    ).head(10)

    st.dataframe(popular)

    st.subheader("Explore Ratings")
    st.dataframe(filtered.head(100))

else:
    st.warning("No movies match your filters.")
