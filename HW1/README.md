# Homework 1 — Bass Diffusion Model

## Predicting the Diffusion of Oura Ring 4 Using Historical Fitbit Data

### Project Overview

This project analyzes the potential worldwide adoption of **Oura Ring 4**, one of TIME magazine's Best Inventions of 2025, using the **Bass Diffusion Model**.

Historical Fitbit device sales data from 2014 to 2025 are used to estimate the model's parameters. These parameters are then applied to predict a hypothetical diffusion scenario for Oura Ring 4 from 2025 to 2034.

The analysis was performed using Python and Jupyter Notebook.

### Project Structure

```text
HW1/
├── bass_model.ipynb
├── README.md
├── data/
│   ├── fitbit_sales_businessofapps_2014_2025.csv
│   ├── fitbit_bass_fit_results.csv
│   └── oura_ring_4_forecast.csv
├── img/
│   ├── fitbit_annual_sales.png
│   ├── fitbit_bass_model_comparison.png
│   ├── oura_annual_adopters.png
│   └── oura_cumulative_adopters.png
└── report/
    ├── report.pdf
    ├── report_source.md
    └── references.md
```

### Methodology

The project uses the Bass Diffusion Model to estimate innovation adoption over time.

1. Collect historical Fitbit annual device sales data.
2. Visualize the historical sales pattern.
3. Estimate the Bass Model parameters using nonlinear least squares.
4. Evaluate model performance using RMSE and R².
5. Estimate Oura Ring 4's global market potential using a Fermi-style approximation.
6. Predict annual and cumulative adopters from 2025 to 2034.
7. Visualize the adoption forecasts.

### Key Results

**Estimated Fitbit Bass Model Parameters**

| Parameter | Value |
|---|---:|
| Innovation coefficient (p) | 0.1047 |
| Imitation coefficient (q) | 0.2534 |
| Market potential (M) | 160.19 million |

**Model Performance**

| Metric | Value |
|---|---:|
| RMSE | 3.1897 million |
| R² | 0.7740 |

**Oura Ring 4 Forecast**

| Metric | Estimated Value |
|---|---:|
| Global market potential | 18.67 million |
| Peak adoption year | 2028 |
| Peak annual adopters | 2.348 million |
| Cumulative adopters by 2034 | 17.371 million |

These results represent a hypothetical forecast based on the model assumptions, not verified future adoption figures.

### Technologies Used

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- SciPy

### How to Run the Project

1. Download or clone the repository.
2. Open a terminal in the `HW1` directory.
3. Install the required Python packages if necessary:

```bash
python3 -m pip install notebook pandas numpy matplotlib scipy
```

4. Launch Jupyter Notebook:

```bash
jupyter notebook
```

5. Open `bass_model.ipynb`.
6. Select **Kernel → Restart Kernel and Run All Cells**.

The notebook will load the historical Fitbit dataset, estimate the Bass Model parameters, generate the forecasts, and save the resulting tables and graphs.

### Final Report

The complete academic report is available in report/report.pdf.

