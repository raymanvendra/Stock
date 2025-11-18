import streamlit as st

# Page config 
st.set_page_config(
    page_title="Trading Guide App",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)
# Main content
st.markdown('<div class="overlay">', unsafe_allow_html=True)

# Social badges
st.markdown(
    """
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@manvendraroy22)
[![Follow](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/manvendraray)
""",
    unsafe_allow_html=True,
)

# Title
st.markdown("# Trading Guide App")
st.markdown("---")

# Banner image
st.image("Banner.jpg", use_container_width=True)

# Intro
st.markdown(
    """
Welcome to the **Trading Guide App** — a lightweight workspace for exploring trading ideas
with clear visuals and data-driven tools. Whether you're just getting started or already
active in the markets, the goal here is to keep things simple, readable, and grounded in
actual numbers.
"""
)

# Features
st.markdown("### Key Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-box">
          <h3> Stock Forecasting</h3>
          <p>Experiment with time-series models to explore potential future price paths.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-box">
          <h3> Technical Analysis</h3>
          <p>Plot moving averages, RSI, MACD, and other indicators to support your entries and exits.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-box">
          <h3> Smart Insights</h3>
          <p>Use clear, interpretable metrics instead of opaque black-box signals.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(" Use the sidebar to explore **Stock Analysis** and **Forecasting Tools**.")

# Footer
st.markdown(
    """
---
© 2025 Trading Guide App · Built with Streamlit
"""
)

st.markdown("</div>", unsafe_allow_html=True)
