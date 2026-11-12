# Hashtag Pulse — Twitter Hashtag Frequency Analysis

An aesthetic, interactive Big Data Analytics mini-project that extracts hashtags from tweet text, counts their frequency, ranks popular hashtags, and displays interactive charts.

## Features
- Upload your own CSV dataset
- Detect hashtags from tweet text (for example, `#AI`, `#BigData`)
- Calculate total posts, hashtag mentions, unique hashtags, and the most-used hashtag
- Interactive bar chart and donut chart
- Searchable frequency table
- Download the hashtag frequency report as CSV
- Included sample dataset for instant testing

## Run locally
1. Install Python 3.9 or newer.
2. Open a terminal in this project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the dashboard:
   ```bash
   streamlit run app.py
   ```

## CSV format
The easiest format is a CSV with a column named `text`, `tweet`, `content`, `post`, or `message`.

Example:

| text |
|---|
| Learning #Python and #DataScience today |
| Exploring #BigData analytics |
| #AI is changing technology |

A CSV with a `hashtag` or `hashtags` column is also supported.

## Project workflow
1. Load tweet records from the sample file or uploaded CSV.
2. Identify hashtag strings using a regular expression.
3. Normalize hashtags to lowercase.
4. Count each hashtag using Python's `Counter`.
5. Display ranked results and visualizations.
6. Export the frequency report.

## Technologies
Python · Pandas · Regular Expressions · Streamlit · Plotly

## Note
The included CSV is a small illustrative sample, not a live Twitter/X feed. Use a dataset you are permitted to access and analyze.
