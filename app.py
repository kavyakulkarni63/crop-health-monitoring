import streamlit as st
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Crop Health Monitoring",
    page_icon="🌱",
    layout="wide"
)

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"

# --------------------------------------------------
# NDVI MAPS
# --------------------------------------------------
ndvi_maps = {
    "29 March 2026": OUTPUT_DIR / "ndvi_2026-03-29.png",
    "28 April 2026": OUTPUT_DIR / "ndvi_2026-04-28.png",
    "02 June 2026": OUTPUT_DIR / "ndvi_2026-06-02.png",
}

difference_map = OUTPUT_DIR / "ndvi_difference.png"

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("🌱 Crop Health Monitoring System")

st.subheader(
    "Sentinel-2 Satellite Imagery Based NDVI Analysis"
)

st.write(
    "This application analyzes vegetation using NDVI "
    "(Normalized Difference Vegetation Index) and provides "
    "a simple crop-health interpretation."
)

st.divider()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("🛰️ Satellite Data")

selected_date = st.sidebar.selectbox(
    "Select Satellite Image Date",
    list(ndvi_maps.keys())
)

st.sidebar.write("**Satellite:** Sentinel-2")
st.sidebar.write("**Data:** Level-2A")
st.sidebar.write("**Bands:** B04 Red + B08 NIR")
st.sidebar.write("**Index:** NDVI")

# --------------------------------------------------
# SELECTED IMAGE
# --------------------------------------------------
selected_image = ndvi_maps[selected_date]

st.header("📍 NDVI Analysis")

st.write(f"**Selected Date:** {selected_date}")

if selected_image.exists():

    st.image(
        str(selected_image),
        caption=f"NDVI Map — {selected_date}",
        use_container_width=True
    )

else:
    st.error(f"Image not found: {selected_image}")

# --------------------------------------------------
# HEALTH INTERPRETATION
# --------------------------------------------------
st.header("🌿 Crop Health Interpretation")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success("🟢 Healthy")
    st.write("NDVI > 0.5")
    st.write("Dense and healthy vegetation")

with col2:
    st.warning("🟡 Moderate")
    st.write("NDVI 0.2 – 0.5")
    st.write("Moderate or sparse vegetation")

with col3:
    st.info("🟠 Low")
    st.write("NDVI 0 – 0.2")
    st.write("Sparse vegetation or bare soil")

with col4:
    st.error("🔴 Non-Vegetation")
    st.write("NDVI ≤ 0")
    st.write("Water, buildings or other non-vegetated areas")

# --------------------------------------------------
# TEMPORAL ANALYSIS
# --------------------------------------------------
st.divider()

st.header("📊 Temporal Analysis")

st.write(
    "The system contains NDVI maps from three different dates. "
    "These maps can be compared to observe changes in vegetation."
)

date1, date2, date3 = st.columns(3)

with date1:
    st.write("**29 March 2026**")
    if ndvi_maps["29 March 2026"].exists():
        st.image(
            str(ndvi_maps["29 March 2026"]),
            use_container_width=True
        )

with date2:
    st.write("**28 April 2026**")
    if ndvi_maps["28 April 2026"].exists():
        st.image(
            str(ndvi_maps["28 April 2026"]),
            use_container_width=True
        )

with date3:
    st.write("**02 June 2026**")
    if ndvi_maps["02 June 2026"].exists():
        st.image(
            str(ndvi_maps["02 June 2026"]),
            use_container_width=True
        )

# --------------------------------------------------
# DIFFERENCE MAP
# --------------------------------------------------
st.divider()

st.header("🔍 NDVI Difference Map")

if difference_map.exists():

    st.image(
        str(difference_map),
        caption="NDVI Difference Map",
        use_container_width=True
    )

    st.write(
        "The difference map helps visualize changes in vegetation "
        "between the available observation dates."
    )

else:
    st.warning("NDVI difference map was not found.")

# --------------------------------------------------
# METHODOLOGY
# --------------------------------------------------
st.divider()

st.header("⚙️ Methodology")

st.write("The system follows these steps:")

st.markdown("""
1. **Satellite Data Collection** – Sentinel-2 Level-2A imagery
2. **Band Selection** – Red band (B04) and Near Infrared band (B08)
3. **NDVI Calculation** – Calculate vegetation index
4. **NDVI Visualization** – Generate spatial NDVI maps
5. **Temporal Comparison** – Compare NDVI across different dates
6. **Crop Health Interpretation** – Classify vegetation condition using NDVI ranges
""")

# --------------------------------------------------
# FORMULA
# --------------------------------------------------
st.header("🧮 NDVI Formula")

st.latex(
    r"NDVI = \frac{B08 - B04}{B08 + B04}"
)

st.write(
    "Higher NDVI values generally indicate stronger vegetation "
    "presence, while lower values indicate sparse vegetation or "
    "non-vegetated areas."
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.caption(
    "Crop Health Detection Using Sentinel-2 Satellite Imagery and NDVI"
)