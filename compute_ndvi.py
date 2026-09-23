"""
NDVI Calculator from Sentinel-2 Satellite Bands
-------------------------------------------------
Computes the Normalized Difference Vegetation Index (NDVI) from
raw Sentinel-2 Red (B04) and Near-Infrared (B08) band data.

NDVI = (NIR - Red) / (NIR + Red)

Output:
  - output/ndvi_output.tif   -> NDVI as a GeoTIFF (for GIS tools / further processing)
  - output/ndvi_map.png      -> Visual NDVI map (green = healthy vegetation)

Requirements:
  pip install rasterio numpy matplotlib
"""

import rasterio
import numpy as np
import matplotlib.pyplot as plt

# ---- File paths ----
RED_FILE = "data/B04_Red.tiff"   # Red band
NIR_FILE = "data/B08_NIR.tiff"   # Near-Infrared band

OUTPUT_TIF = "output/ndvi_output.tif"
OUTPUT_PNG = "output/ndvi_map.png"


def load_band(path):
    with rasterio.open(path) as src:
        data = src.read(1).astype("float32")
        profile = src.profile
    return data, profile


def compute_ndvi(red, nir):
    epsilon = 1e-6  # avoid division by zero
    ndvi = (nir - red) / (nir + red + epsilon)
    return ndvi


def classify_ndvi(ndvi):
    total = ndvi.size
    healthy = (ndvi > 0.5).sum()
    moderate = ((ndvi > 0.2) & (ndvi <= 0.5)).sum()
    stressed = ((ndvi > 0) & (ndvi <= 0.2)).sum()
    non_veg = (ndvi <= 0).sum()

    print("\nClassification breakdown:")
    print(f"  Healthy vegetation (NDVI > 0.5):   {healthy:>7} px  ({100*healthy/total:.1f}%)")
    print(f"  Moderate vegetation (0.2-0.5):     {moderate:>7} px  ({100*moderate/total:.1f}%)")
    print(f"  Stressed/sparse (0-0.2):           {stressed:>7} px  ({100*stressed/total:.1f}%)")
    print(f"  Non-vegetation/water/bare (<=0):   {non_veg:>7} px  ({100*non_veg/total:.1f}%)")


def main():
    print("Loading Red (B04) and NIR (B08) bands...")
    red, profile = load_band(RED_FILE)
    nir, _ = load_band(NIR_FILE)

    print("Computing NDVI...")
    ndvi = compute_ndvi(red, nir)

    print("\nNDVI stats:")
    print("  min :", ndvi.min())
    print("  max :", ndvi.max())
    print("  mean:", ndvi.mean())

    # Save as GeoTIFF (preserves geo-referencing for GIS tools)
    profile.update(dtype="float32", count=1)
    with rasterio.open(OUTPUT_TIF, "w", **profile) as dst:
        dst.write(ndvi, 1)

    # Save visual map
    plt.figure(figsize=(10, 7))
    plt.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
    plt.colorbar(label="NDVI")
    plt.title("NDVI Map (Sentinel-2: B08 NIR & B04 Red)")
    plt.axis("off")
    plt.savefig(OUTPUT_PNG, dpi=150, bbox_inches="tight")

    print(f"\nSaved: {OUTPUT_TIF}")
    print(f"Saved: {OUTPUT_PNG}")

    classify_ndvi(ndvi)


if __name__ == "__main__":
    main()
