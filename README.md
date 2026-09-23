# 🌱 Crop Health Monitoring Using Sentinel-2 Satellite Imagery

### NDVI-Based Crop Health Assessment and Temporal Vegetation Analysis

A remote-sensing based crop health monitoring system developed using
**Sentinel-2 satellite imagery**, **NDVI (Normalized Difference Vegetation Index)**,
Python, and Streamlit.

The project analyzes vegetation conditions using the Red and
Near-Infrared spectral bands of Sentinel-2 imagery. It generates
NDVI maps for different observation dates, performs temporal
vegetation analysis, and provides an interactive dashboard for
visualizing the results.

---

## 📌 Project Overview

Crop health monitoring using conventional field surveys can require
significant time and resources. Satellite imagery provides a
practical way to observe vegetation conditions over larger areas.

This project demonstrates a satellite-based approach for vegetation
and crop-health assessment using the **Normalized Difference
Vegetation Index (NDVI)**.

The workflow uses Sentinel-2 spectral information to calculate NDVI
and visualize spatial vegetation conditions across multiple
observation dates.

The generated results are presented through an interactive
**Streamlit dashboard**.

---

## 🎯 Objectives

The main objectives of this project are:

- To explore Sentinel-2 multispectral satellite imagery for
  vegetation monitoring.
- To use the Red (B04) and Near-Infrared (B08) bands for NDVI
  calculation.
- To generate spatial NDVI maps.
- To interpret vegetation conditions using NDVI ranges.
- To compare vegetation conditions across different observation
  dates.
- To generate an NDVI difference map for temporal comparison.
- To develop an interactive Streamlit-based visualization interface.

---

## 🛰️ Satellite Imagery

The project is based on **Sentinel-2 Level-2A multispectral
imagery**.

### Spectral Bands Used

| Band | Description | Role |
|------|-------------|------|
| B04 | Red | Red reflectance |
| B08 | Near-Infrared (NIR) | Vegetation response |

The Red and Near-Infrared bands are used to calculate the
Normalized Difference Vegetation Index.

---

## 🧮 NDVI Calculation

NDVI is calculated using the following equation:

```text
              B08 - B04
NDVI = -------------------------
              B08 + B04
