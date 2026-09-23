"""
NDVI Time-Series Analysis from Sentinel-2 Satellite Data
----------------------------------------------------------
Computes NDVI for multiple dates over the same area, then:
  - Plots how average NDVI changes over time
  - Generates a "difference map" showing where vegetation
    increased or decreased between the first and last date

Folder structure expected:
  data/
    2026-03-29/B04_Red.tiff, B08_NIR.tiff
    2026-04-28/B04_Red.tiff, B08_NIR.tiff
    2026-06-02/B04_Red.tiff, B08_NIR.tiff

Output:
  output/ndvi_<date>.tif        -> NDVI GeoTIFF for each date
  output/ndvi_<date>.png        -> NDVI visual map for each date
  output/ndvi_trend.png          -> Average NDVI over time (line chart)
  output/ndvi_difference.png     -> Change map (last date - first date)

Requirements:
  pip install rasterio numpy matplotlib
"""

import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

DATA_DIR = "data"
OUTPUT_DIR = "output"

# Dates in chronological order (folder names)
DATES = ["2026-03-29", "2026-04-28", "2026-06-02"]


def load_band(path):
    with rasterio.open(path) as src:
        data = src.read(1).astype("float32")
        profile = src.profile
    return data, profile


def compute_ndvi(red, nir):
    epsilon = 1e-6
    return (nir - red) / (nir + red + epsilon)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ndvi_maps = {}
    mean_ndvi = []

    # Step 1: Compute NDVI for each date
    for date in DATES:
        red_path = os.path.join(DATA_DIR, date, "B04_Red.tiff")
        nir_path = os.path.join(DATA_DIR, date, "B08_NIR.tiff")

        red, profile = load_band(red_path)
        nir, _ = load_band(nir_path)

        ndvi = compute_ndvi(red, nir)
        ndvi_maps[date] = ndvi
        mean_ndvi.append(ndvi.mean())

        print(f"{date}: mean NDVI = {ndvi.mean():.4f}")

        # Save individual NDVI GeoTIFF
        profile.update(dtype="float32", count=1)
        with rasterio.open(os.path.join(OUTPUT_DIR, f"ndvi_{date}.tif"), "w", **profile) as dst:
            dst.write(ndvi, 1)

        # Save individual NDVI visual
        plt.figure(figsize=(10, 7))
        plt.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
        plt.colorbar(label="NDVI")
        plt.title(f"NDVI Map - {date}")
        plt.axis("off")
        plt.savefig(os.path.join(OUTPUT_DIR, f"ndvi_{date}.png"), dpi=150, bbox_inches="tight")
        plt.close()

    # Step 2: Trend line - average NDVI over time
    plt.figure(figsize=(8, 5))
    plt.plot(DATES, mean_ndvi, marker="o", linewidth=2, color="green")
    plt.title("Average NDVI Over Time")
    plt.xlabel("Date")
    plt.ylabel("Mean NDVI")
    plt.grid(True, alpha=0.3)
    for i, val in enumerate(mean_ndvi):
        plt.annotate(f"{val:.3f}", (DATES[i], mean_ndvi[i]),
                      textcoords="offset points", xytext=(0, 8), ha="center")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "ndvi_trend.png"), dpi=150)
    plt.close()
    print(f"\nSaved trend chart: {OUTPUT_DIR}/ndvi_trend.png")

    # Step 3: Difference map - last date minus first date
    first_date, last_date = DATES[0], DATES[-1]
    diff = ndvi_maps[last_date] - ndvi_maps[first_date]

    plt.figure(figsize=(10, 7))
    plt.imshow(diff, cmap="RdYlGn", vmin=-0.5, vmax=0.5)
    plt.colorbar(label=f"NDVI change ({last_date} minus {first_date})")
    plt.title(f"Vegetation Change: {first_date} -> {last_date}\n(Green = increase, Red = decrease)")
    plt.axis("off")
    plt.savefig(os.path.join(OUTPUT_DIR, "ndvi_difference.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved difference map: {OUTPUT_DIR}/ndvi_difference.png")

    # Step 4: Simple summary stats for the difference map
    increased = (diff > 0.05).sum()
    decreased = (diff < -0.05).sum()
    stable = diff.size - increased - decreased
    total = diff.size

    print("\nChange summary (between first and last date):")
    print(f"  Increased vegetation (NDVI up > 0.05):   {increased:>7} px ({100*increased/total:.1f}%)")
    print(f"  Decreased vegetation (NDVI down > 0.05): {decreased:>7} px ({100*decreased/total:.1f}%)")
    print(f"  Roughly stable:                          {stable:>7} px ({100*stable/total:.1f}%)")


if __name__ == "__main__":
    main()
