"""Age distribution visualization script for various tech communities."""

import matplotlib.pyplot as plt
import numpy as np

# Sources:
#
# openSUSE Maintainers Survey (2021)
# 182 respondents
# https://en.opensuse.org/Maintainers-surveys_2021
#
# Stackoverflow Developer Survey 2023
# https://survey.stackoverflow.co/2023/#developer-profile-demographics
#
# Linux Foundation Diversity, Equity, and Inclusion in Open Source (2021)
# https://8112310.fs1.hubspotusercontent-na1.net/hubfs/8112310/LF%20Research/2021%20DEI%20Survey%20-%20Report.pdf
#
# Debian Project Survey 2016
# https://dcpc.info/wp-content/uploads/2021/12/DCPC_2016_debian_survey.pdf
#
# CNCF: DeveloperNation report — State of Cloud Native Development, Q1 2025
# 10500 respondents
# https://www.cncf.io/wp-content/uploads/2025/04/Blue-DN29-State-of-Cloud-Native-Development.pdf

# GLOBAL DIMENSION SETTINGS - Adjust these to customize output sizes
INDIVIDUAL_GRAPH_WIDTH = 8  # Width in inches
INDIVIDUAL_GRAPH_HEIGHT = 6  # Height in inches
COMBINED_GRAPH_WIDTH = 14  # Width in inches
COMBINED_GRAPH_HEIGHT = 8  # Height in inches
DPI = 300  # Resolution for rasterized elements in SVG


# Data extraction and conversion to percentages

# 1. openSUSE
opensuse_bins = ["≤25", "25-34", "35-49", "50+"]
opensuse_values = [19, 26, 42, 12.5]

# 2. Stackoverflow - convert counts to percentages
stackoverflow_bins = [
    "<18",
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-64",
    "≥65",
    "No answer",
]
# 89184 responses
stackoverflow_2023_counts = [4128, 17931, 33247, 20532, 8334, 3392, 1171, 449]
stackoverflow_2023_total = sum(stackoverflow_2023_counts)
stackoverflow_2023_values = [
    count / stackoverflow_2023_total * 100 for count in stackoverflow_2023_counts
]

# https://survey.stackoverflow.co/2025/developers/#1-age
# 49019 responses
stackoverflow_2025_values = [0, 18.7, 33.6, 26.9, 12.8, 5.3, 1.9, 0.8]
# https://survey.stackoverflow.co/2021#age
# 82407 responses
stackoverflow_2021_values = [6.52, 25.47, 39.52, 18.42, 6.64, 2.21, 0.51, 0.7]

# https://survey.stackoverflow.co/2016#developer-profile-age
# sadly, different binning…
# < 20: 7.1%
# 20-24: 23.6%
# 25-29: 28.4%
# 30-34: 18.1%
# 35-39: 10.2%
# 40-49: 8.9%
# 50-59: 3.0%
# > 60: 0.8%
#
# 55338 responses

stackoverflow_2016_values = [
    4.3,  # Approx. 60% of the original "< 20" bin
    26.4,  # the "20-24" bin (23.6%) + approx. 40% of the "< 20" bin
    28.4 + 18.1,  # sum of "25-29" and "30-34"
    14.7,  # "35-39" (10.2%) + half of "40-49" (4.45%)
    6.0,  # half of "40-49" (4.45%) + half of "50-59" (1.5%)
    2.0,  # half of "50-59" (1.5%) + est. share of ">60" (0.5%)
    0.3,  # remaining estimated share from the ">60" bin
]

# 3. LinuxFoundation
linux_foundation_bins = [
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-64",
    "65-74",
    "≥75",
    "No answer",
]
linux_foundation_values = [8, 22, 29, 21, 13, 4, 2, 1]

# 4. Debian - convert counts to percentages
debian_bins = ["<20", "20-29", "30-39", "40-49", "50-59", ">60"]
debian_counts = [15, 132, 378, 225, 57, 15]
debian_total = sum(debian_counts)
debian_values = [count / debian_total * 100 for count in debian_counts]

# 5. CNCF
cncf_bins = ["<18", "18-24", "25-34", "35-44", "45-54", "≥55"]
cncf_values = [1, 22, 32, 25, 12, 7]


# Define consistent Stack Overflow reference using normalized positions
# We'll plot Stack Overflow at consistent "age positions" across all graphs
so_bins_for_reference = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
so_values_for_reference = stackoverflow_2023_values[:-1]

# Age midpoints for Stack Overflow bins (will be used for consistent positioning)
so_age_positions = [16, 21, 29.5, 39.5, 49.5, 59.5, 70]


# Create individual graphs for each source with Stack Overflow reference line
# Each graph is saved as a separate SVG file

# openSUSE
fig1, ax1 = plt.subplots(figsize=(INDIVIDUAL_GRAPH_WIDTH, INDIVIDUAL_GRAPH_HEIGHT))
opensuse_age_positions = [20, 29.5, 42, 60]  # Midpoints of ≤25, 25-34, 35-49, 50+
bars1 = ax1.bar(
    opensuse_age_positions,
    opensuse_values,
    width=8,
    color="#73ba25",
    alpha=0.8,
    edgecolor="black",
    label="openSUSE",
)
line1 = ax1.plot(
    so_age_positions,
    stackoverflow_2021_values[:-1],
    color="black",
    marker=".",
    linestyle="-.",
    linewidth=2.5,
    markersize=8,
    label="Stack Overflow (2021)",
    zorder=5,
)
ax1.set_title("openSUSE Maintainers Survey (2021)", fontweight="bold", fontsize=14)
ax1.set_ylabel("Percentage (%)", fontsize=12)
ax1.set_xlabel("Age Range", fontsize=12)
ax1.set_xlim(10, 75)
ax1.set_xticks(opensuse_age_positions)
ax1.set_xticklabels(opensuse_bins)
ax1.legend(loc="upper right", fontsize=10)
ax1.grid(axis="y", alpha=0.3)
for i, (bar, value) in enumerate(zip(bars1, opensuse_values)):
    ax1.text(
        opensuse_age_positions[i],
        value,
        f"{value:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10,
    )
plt.tight_layout()
plt.savefig(
    "media/opensuse_distribution.svg",
    format="svg",
    dpi=DPI,
    bbox_inches="tight",
)
plt.close()


# Stack Overflow
fig2, ax2 = plt.subplots(figsize=(INDIVIDUAL_GRAPH_WIDTH, INDIVIDUAL_GRAPH_HEIGHT))
stackoverflow_age_positions_plot = [
    14,
    21,
    29.5,
    39.5,
    49.5,
    59.5,
    70,
]
ax2.plot(
    stackoverflow_age_positions_plot,
    stackoverflow_2016_values,
    color="#6A4C93",
    marker="x",
    linestyle=":",
    linewidth=2.5,
    markersize=8,
    label="2016",
)
ax2.plot(
    stackoverflow_age_positions_plot,
    stackoverflow_2021_values[:-1],
    color="#8AC926",
    marker=".",
    linestyle="-.",
    linewidth=2.5,
    markersize=8,
    label="2021",
)
ax2.plot(
    stackoverflow_age_positions_plot,
    so_values_for_reference,
    color="#f48024",
    marker="s",
    linewidth=2.5,
    markersize=8,
    label="2023",
)
ax2.plot(
    stackoverflow_age_positions_plot,
    stackoverflow_2025_values[:-1],
    color="#5BC0EB",
    marker="o",
    linestyle="--",
    linewidth=2.5,
    markersize=8,
    label="2025",
)

ax2.set_title("Stack Overflow Developer Survey", fontweight="bold", fontsize=14)
ax2.set_ylabel("Percentage (%)", fontsize=12)
ax2.set_xlabel("Age Range", fontsize=12)
ax2.set_xlim(10, 75)
ax2.set_xticks(stackoverflow_age_positions_plot)
ax2.set_xticklabels(so_bins_for_reference, rotation=45, ha="right")
ax2.grid(axis="y", alpha=0.3)
ax2.legend(loc="upper right", fontsize=10)

# for i, value in enumerate(so_values_for_reference):
#     ax2.text(
#         stackoverflow_age_positions_plot[i],
#         value,
#         f"{value:.1f}%",
#         ha="center",
#         va="bottom",
#         fontsize=10,
#     )
plt.tight_layout()
plt.savefig(
    "media/stackoverflow_distribution.svg",
    format="svg",
    dpi=DPI,
    bbox_inches="tight",
)
plt.close()

# Linux Foundation
fig3, ax3 = plt.subplots(figsize=(INDIVIDUAL_GRAPH_WIDTH, INDIVIDUAL_GRAPH_HEIGHT))
linux_foundation_age_positions = [21, 29.5, 39.5, 49.5, 59.5, 69.5, 77.5]
lf_values = linux_foundation_values[:7]
bars3 = ax3.bar(
    linux_foundation_age_positions,
    lf_values,
    width=6,
    color="#003764",
    alpha=0.8,
    edgecolor="black",
    label="Linux Foundation",
)
line3 = ax3.plot(
    so_age_positions,
    stackoverflow_2021_values[:-1],
    color="black",
    marker=".",
    linestyle="-.",
    linewidth=2.5,
    markersize=8,
    label="Stack Overflow (2021)",
    zorder=5,
)
ax3.set_title("Linux Foundation Survey 2021", fontweight="bold", fontsize=14)
ax3.set_ylabel("Percentage (%)", fontsize=12)
ax3.set_xlabel("Age Range", fontsize=12)
ax3.set_xlim(10, 80)
ax3.set_xticks(linux_foundation_age_positions)
ax3.set_xticklabels(linux_foundation_bins[:7], rotation=45, ha="right")
ax3.legend(loc="upper right", fontsize=10)
ax3.grid(axis="y", alpha=0.3)
for i, value in enumerate(lf_values):
    ax3.text(
        linux_foundation_age_positions[i],
        value,
        f"{value:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10,
    )
plt.tight_layout()
plt.savefig(
    "media/linux_foundation_distribution.svg",
    format="svg",
    dpi=DPI,
    bbox_inches="tight",
)
plt.close()

# Debian
fig4, ax4 = plt.subplots(figsize=(INDIVIDUAL_GRAPH_WIDTH, INDIVIDUAL_GRAPH_HEIGHT))
debian_age_positions = [16, 24.5, 34.5, 44.5, 54.5, 65]
bars4 = ax4.bar(
    debian_age_positions,
    debian_values,
    width=7,
    color="#d70751",
    alpha=0.8,
    edgecolor="black",
    label="Debian",
)
line4 = ax4.plot(
    so_age_positions,
    stackoverflow_2016_values,
    color="black",
    marker="x",
    linestyle=":",
    linewidth=2.5,
    markersize=8,
    label="Stack Overflow (2016)",
    zorder=5,
)
ax4.set_title("Debian Contributor Survey 2016", fontweight="bold", fontsize=14)
ax4.set_ylabel("Percentage (%)", fontsize=12)
ax4.set_xlabel("Age Range", fontsize=12)
ax4.set_xlim(10, 75)
ax4.set_xticks(debian_age_positions)
ax4.set_xticklabels(debian_bins)
ax4.legend(loc="upper right", fontsize=10)
ax4.grid(axis="y", alpha=0.3)
for i, value in enumerate(debian_values):
    ax4.text(
        debian_age_positions[i],
        value,
        f"{value:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10,
    )
plt.tight_layout()
plt.savefig(
    "media/debian_distribution.svg",
    format="svg",
    dpi=DPI,
    bbox_inches="tight",
)
plt.close()

# CNCF
fig5, ax5 = plt.subplots(figsize=(INDIVIDUAL_GRAPH_WIDTH, INDIVIDUAL_GRAPH_HEIGHT))
cncf_age_positions = [13, 21, 29.5, 39.5, 49.5, 60]
bars5 = ax5.bar(
    cncf_age_positions,
    cncf_values,
    width=7,
    color="#326ce5",
    alpha=0.8,
    edgecolor="black",
    label="CNCF",
)
line5 = ax5.plot(
    so_age_positions,
    stackoverflow_2025_values[:-1],
    color="black",
    marker="o",
    linestyle="--",
    linewidth=2.5,
    markersize=8,
    label="Stack Overflow (2025)",
    zorder=5,
)
ax5.set_title("CNCF Age Distribution", fontweight="bold", fontsize=14)
ax5.set_ylabel("Percentage (%)", fontsize=12)
ax5.set_xlabel("Age Range", fontsize=12)
ax5.set_xlim(10, 75)
ax5.set_xticks(cncf_age_positions)
ax5.set_xticklabels(cncf_bins)
ax5.legend(loc="upper right", fontsize=10)
ax5.grid(axis="y", alpha=0.3)
for i, value in enumerate(cncf_values):
    ax5.text(
        cncf_age_positions[i],
        value,
        f"{value:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10,
    )
plt.tight_layout()
plt.savefig(
    "media/cncf_distribution.svg",
    format="svg",
    dpi=DPI,
    bbox_inches="tight",
)
plt.close()


fig2, ax = plt.subplots(figsize=(COMBINED_GRAPH_WIDTH, COMBINED_GRAPH_HEIGHT))

# Define COARSE standardized bins (5 bins for better slide readability)
coarse_bins = ["<25", "25-34", "35-44", "45-54", "55+"]

# Map each source to coarse bins
# openSUSE mapping
opensuse_coarse = [
    opensuse_values[0],  # <25
    opensuse_values[1],  # 25-34
    opensuse_values[2] * 0.67,  # 35-44 (2/3 of 35-49)
    opensuse_values[2] * 0.33,  # 45-54 (1/3 of 35-49)
    opensuse_values[3],  # 55+ (all of 50+)
]

# Stack Overflow mapping
stackoverflow_coarse = [
    stackoverflow_2023_values[0] + stackoverflow_2023_values[1],  # <25
    stackoverflow_2023_values[2],  # 25-34
    stackoverflow_2023_values[3],  # 35-44
    stackoverflow_2023_values[4],  # 45-54
    stackoverflow_2023_values[5] + stackoverflow_2023_values[6],  # 55+
]

# Linux Foundation mapping
linux_foundation_coarse = [
    linux_foundation_values[0],  # <25 (only 18-24, no <18 data)
    linux_foundation_values[1],  # 25-34
    linux_foundation_values[2],  # 35-44
    linux_foundation_values[3],  # 45-54
    (
        linux_foundation_values[4]
        + linux_foundation_values[5]
        + linux_foundation_values[6]
    ),  # 55+
]

# Debian mapping
debian_coarse = [
    debian_values[0] + debian_values[1] * 0.4,  # <25
    debian_values[1] * 0.6 + debian_values[2] * 0.4,  # 25-34
    debian_values[2] * 0.6 + debian_values[3] * 0.4,  # 35-44
    debian_values[3] * 0.6 + debian_values[4] * 0.4,  # 45-54
    debian_values[4] * 0.6 + debian_values[5],  # 55+
]

# CNCF mapping
cncf_coarse = [
    cncf_values[0] + cncf_values[1],  # <25 (<18 + 18-24)
    cncf_values[2],  # 25-34
    cncf_values[3],  # 35-44
    cncf_values[4],  # 45-54
    cncf_values[5],  # 55+
]

# Prepare data for grouped bar chart
x = np.arange(len(coarse_bins))
width = 0.20

# Plot grouped bars (without Stack Overflow)
bars1 = ax.bar(
    x - 1.5 * width,
    opensuse_coarse,
    width,
    label="openSUSE (2021)",
    color="#73ba25",
    alpha=0.85,
    edgecolor="black",
    linewidth=1.2,
)
bars2 = ax.bar(
    x - 0.5 * width,
    linux_foundation_coarse,
    width,
    label="Linux Foundation (2021)",
    color="#003764",
    alpha=0.85,
    edgecolor="black",
    linewidth=1.2,
)
bars3 = ax.bar(
    x + 0.5 * width,
    debian_coarse,
    width,
    label="Debian (2016)",
    color="#d70751",
    alpha=0.85,
    edgecolor="black",
    linewidth=1.2,
)
bars4 = ax.bar(
    x + 1.5 * width,
    cncf_coarse,
    width,
    label="CNCF (2025)",
    color="#326ce5",
    alpha=0.85,
    edgecolor="black",
    linewidth=1.2,
)

# Add Stack Overflow as a reference line using the SAME data as individual distributions
# Map Stack Overflow age positions to the x-axis scale
# Age range: roughly 15-70, X range: roughly -0.5 to 4.5
# Linear mapping: x = (age - 15) / (70 - 15) * 5 - 0.5
so_x_positions = [(age - 15) / (70 - 15) * 5 - 0.5 for age in so_age_positions]

line_so = ax.plot(
    so_x_positions,
    so_values_for_reference,
    color="#f48024",
    marker="o",
    linewidth=3,
    markersize=10,
    label="Stack Overflow (2023)",
    zorder=10,
    markeredgecolor="black",
    markeredgewidth=1.5,
)

# Add value labels for Stack Overflow line (only for key points)
for i, (xi, yi) in enumerate(zip(so_x_positions, so_values_for_reference)):
    if yi > 5:  # Only label significant values
        ax.text(
            xi,
            yi + 1.5,
            f"{yi:.0f}%",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#f48024",
        )

# Add value labels on bars for better readability
for bars in [bars1, bars2, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.0f}%",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
            )

ax.set_xlabel("Age Range", fontweight="bold", fontsize=14)
ax.set_ylabel("Percentage (%)", fontweight="bold", fontsize=14)
ax.set_title(
    "Age Distribution Comparison Across Sources", fontweight="bold", fontsize=16
)
ax.set_xticks(x)
ax.set_xticklabels(coarse_bins, fontsize=13)
ax.set_ylim(
    0,
    max(
        [
            max(opensuse_coarse),
            max(stackoverflow_coarse),
            max(linux_foundation_coarse),
            max(debian_coarse),
            max(cncf_coarse),
        ]
    )
    * 1.15,
)
ax.legend(loc="upper right", fontsize=11, framealpha=0.9)
ax.grid(axis="y", alpha=0.3, linewidth=0.8)
ax.tick_params(axis="both", which="major", labelsize=11)

plt.tight_layout()
plt.savefig(
    "media/combined_comparison.svg",
    format="svg",
    dpi=DPI,
    bbox_inches="tight",
)
plt.close()
