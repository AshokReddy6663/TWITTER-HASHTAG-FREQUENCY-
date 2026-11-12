import re
from collections import Counter
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Hashtag Pulse | BDA", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(135deg,#080d1b 0%,#101a32 55%,#111827 100%);color:#f8fafc;}
h1,h2,h3 {font-family:'Space Grotesk',sans-serif;color:#f8fafc;}
[data-testid="stMetric"] {background:linear-gradient(145deg,#17243e,#111a2d);padding:18px;border:1px solid #263958;border-radius:18px;}
[data-testid="stFileUploader"] {background:#111c31;border:1px dashed #4b6b9b;border-radius:16px;padding:12px;}
div[data-testid="stDataFrame"] {border:1px solid #263958;border-radius:14px;overflow:hidden;}
.stTabs [data-baseweb="tab"] {color:#cbd5e1;}
.stButton>button {background:#5eead4;color:#082f49;border:0;border-radius:10px;font-weight:700;}
.small-muted {color:#94a3b8;font-size:0.92rem;}
.hero {padding:28px 30px;border:1px solid #263958;border-radius:22px;background:linear-gradient(110deg,rgba(45,212,191,.13),rgba(96,165,250,.10));margin-bottom:22px;}
.pill {display:inline-block;padding:5px 11px;border-radius:30px;background:#123b47;color:#99f6e4;font-size:12px;font-weight:700;letter-spacing:1px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<span class="pill">BIG DATA ANALYTICS • MINI PROJECT</span>
<h1 style="font-size:2.6rem;margin:12px 0 4px;"># Hashtag Pulse</h1>
<p class="small-muted">Twitter Hashtag Frequency Analysis · Discover trending topics through data.</p>
</div>
""", unsafe_allow_html=True)

def extract_hashtags(value):
    if pd.isna(value):
        return []
    return [tag.lower() for tag in re.findall(r"#([A-Za-z0-9_]+)", str(value))]

def load_data(uploaded):
    if uploaded is not None:
        try:
            return pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Could not read CSV: {e}")
            return None
    return pd.read_csv("data/sample_tweets.csv")

with st.sidebar:
    st.markdown("## ⚙️ Analysis settings")
    st.caption("Upload your own Twitter/X dataset or explore the included sample.")
    uploaded = st.file_uploader("Upload CSV file", type=["csv"])
    st.markdown("---")
    st.markdown("### Expected data")
    st.write("A CSV containing a text column such as `text`, `tweet`, `content`, or `post`.")
    st.caption("You can also upload a file with a column named `hashtag`.")

df = load_data(uploaded)
if df is None:
    st.stop()

text_candidates = ["text", "tweet", "content", "post", "tweets", "message"]
text_col = next((c for c in df.columns if c.lower() in text_candidates), None)
hashtag_col = next((c for c in df.columns if c.lower() in ["hashtag", "hashtags"]), None)

if text_col:
    df["__hashtags"] = df[text_col].apply(extract_hashtags)
elif hashtag_col:
    df["__hashtags"] = df[hashtag_col].fillna("").astype(str).apply(
        lambda x: [t.lower().lstrip("#").strip() for t in re.split(r"[,; ]+", x) if t.strip()]
    )
else:
    st.error("No suitable column found. Include a text/tweet/content column or a hashtag column.")
    st.info(f"Available columns: {', '.join(map(str, df.columns))}")
    st.stop()

all_tags = [tag for tags in df["__hashtags"] for tag in tags if tag]
counts = Counter(all_tags)
freq = pd.DataFrame(counts.most_common(), columns=["Hashtag", "Frequency"])
total_tweets = len(df)
unique_tags = len(counts)
total_mentions = sum(counts.values())
top_tag = freq.iloc[0]["Hashtag"] if not freq.empty else "—"

m1,m2,m3,m4 = st.columns(4)
m1.metric("Total posts", f"{total_tweets:,}")
m2.metric("Hashtag mentions", f"{total_mentions:,}")
m3.metric("Unique hashtags", f"{unique_tags:,}")
m4.metric("Top hashtag", f"#{top_tag}" if top_tag != "—" else "—")

st.markdown("## 📈 Explore the conversation")
if freq.empty:
    st.warning("No hashtags were found. Try a dataset containing hashtags such as #AI or #BigData.")
    st.stop()

left, right = st.columns([1.5,1])
with left:
    st.markdown("### Most-used hashtags")
    top_n = st.slider("Number of hashtags to display", 5, min(30, max(5, len(freq))), min(10, len(freq)))
    chart = px.bar(freq.head(top_n).sort_values("Frequency"), x="Frequency", y="Hashtag",
                   orientation="h", text="Frequency", color="Frequency",
                   color_continuous_scale=["#164e63","#2dd4bf","#93c5fd"])
    chart.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False,
                        margin=dict(l=10,r=10,t=15,b=10), height=440)
    st.plotly_chart(chart, use_container_width=True)
with right:
    st.markdown("### Hashtag share")
    pie = px.pie(freq.head(7), names="Hashtag", values="Frequency", hole=.62,
                 color_discrete_sequence=["#2dd4bf","#60a5fa","#a78bfa","#f472b6","#fbbf24","#34d399","#fb7185"])
    pie.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=5,r=5,t=15,b=5), height=440,
                      legend_title_text="")
    st.plotly_chart(pie, use_container_width=True)

st.markdown("## 🧾 Frequency table")
search = st.text_input("Search hashtag", placeholder="Type a hashtag...")
view = freq.copy()
if search:
    view = view[view["Hashtag"].str.contains(search.replace("#","").lower(), na=False)]
view.insert(0, "Rank", range(1, len(view)+1))
st.dataframe(view, use_container_width=True, hide_index=True)

csv = freq.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download hashtag report", csv, "hashtag_frequency_report.csv", "text/csv")

with st.expander("ℹ️ About this project"):
    st.write("This project identifies hashtags in tweet text, counts their frequency, ranks popular topics, and presents interactive visualizations. It can analyze the included sample data or a CSV uploaded by the user.")
    st.write("**Method:** hashtag extraction using regular expressions, frequency counting with Python Counter, and visualization with Plotly.")
st.caption("Hashtag Pulse · Big Data Analytics Project")
