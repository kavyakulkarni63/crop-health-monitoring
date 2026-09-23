# NDVI Calculator & Time-Series Analysis — Sentinel-2 Satellite Data

This is a small starter project: it takes raw Sentinel-2 satellite band data
(Red and Near-Infrared) and computes **NDVI (Normalized Difference Vegetation
Index)** — a measure of vegetation health used widely in agriculture, crop
monitoring, and environmental analysis.

It now also includes a **time-series analysis** across 3 dates, showing how
vegetation health changes over time — including a trend chart and a
"change map" highlighting where vegetation increased or decreased.

This was built as a first step toward exploring satellite-data + AI projects
(e.g. crop health / irrigation advisory systems).

---

## What is NDVI?

NDVI = (NIR − Red) / (NIR + Red)

- Healthy plants reflect a lot of near-infrared (NIR) light and absorb red light.
- The result ranges from -1 to +1:
  - **> 0.5** → healthy, dense vegetation
  - **0.2 – 0.5** → moderate/sparse vegetation, possibly stressed crops
  - **0 – 0.2** → very sparse vegetation or bare soil
  - **<= 0** → water, rock, urban areas, no vegetation

---

## Project Structure

```
ndvi_project/
├── compute_ndvi.py          # single-date NDVI script
├── timeseries_ndvi.py        # multi-date NDVI + trend + change map
├── data/
│   ├── 2026-03-29/
│   │   ├── B04_Red.tiff
│   │   └── B08_NIR.tiff
│   ├── 2026-04-28/
│   │   ├── B04_Red.tiff
│   │   └── B08_NIR.tiff
│   └── 2026-06-02/
│       ├── B04_Red.tiff
│       └── B08_NIR.tiff
├── output/
│   ├── ndvi_<date>.tif       # NDVI GeoTIFF per date
│   ├── ndvi_<date>.png       # NDVI visual map per date
│   ├── ndvi_trend.png        # Average NDVI over time (line chart)
│   └── ndvi_difference.png   # Change map (last date - first date)
└── README.md
```

---

## How to Run

1. Install dependencies:
   ```
   pip install rasterio numpy matplotlib
   ```

2. Run the single-date script (computes NDVI for one date):
   ```
   python compute_ndvi.py
   ```

3. Run the time-series script (computes NDVI for all 3 dates, trend chart, change map):
   ```
   python timeseries_ndvi.py
   ```

Output will be generated in the `output/` folder.

---

## Where the Data Came From

Data downloaded from **Copernicus Browser**
(https://browser.dataspace.copernicus.eu) — free, no special access required.

Settings used:
- Satellite: Sentinel-2 L2A
- Bands: B04 (Red), B08 (Near-Infrared) — Raw, 16-bit
- Coordinate System: WGS 84 (EPSG:4326)
- Dates: 29 March 2026, 28 April 2026, 02 June 2026 (same area, for time-series comparison)

---

## Findings So Far

- **Average NDVI trend:** 0.345 (Mar 29) -> 0.287 (Apr 28) -> 0.304 (Jun 2)
  — a dip after late March likely reflects rabi (winter crop) harvest,
  with partial green-up by early June (pre-monsoon sowing).
- **Change map (Mar 29 -> Jun 2):** ~46% of the area shows a notable NDVI
  decrease (harvested fields), ~20% shows an increase (newly sown/growing
  fields), and the rest is roughly stable.
- This kind of before/after comparison is the basic signal an irrigation or
  crop-stage advisory system would use to flag fields that may need attention.

---

## Next Steps / Ideas

- **Time-series analysis**: download the same area across multiple dates to
  track how vegetation health changes over a crop's growth cycle.
- **Combine with soil moisture data** (e.g. Sentinel-1 radar/SAR) for a more
  complete crop-stress picture.
- **Build a dashboard**: visualize NDVI zones on an interactive map (e.g. with
  a PWA + Firebase backend) — color-code areas by health status.
- **Add irrigation advisory logic**: based on NDVI + moisture thresholds,
  generate simple recommendations (e.g. "Zone 3: low NDVI + low moisture →
  irrigation recommended").

---

## Concepts Covered

- Reading raw satellite imagery (GeoTIFF) with `rasterio`
- Understanding multispectral bands (Red, NIR)
- Computing a remote-sensing vegetation index (NDVI)
- Classifying pixel values into meaningful categories
- Visualizing geospatial raster data with `matplotlib`
