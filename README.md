# agronomy-thesis-data-analysis
Automated Statistical Analysis for Soil Science Thesis
This repository contains the Python scripts and results for an automated data analysis pipeline created for an undergraduate thesis in Agronomy. The project focuses on performing statistical analysis on soil sample data and automatically generating a comprehensive report with visualizations and test results.

1. Project Objective
The main goal was to automate the entire statistical workflow for a scientific research project. This includes data cleaning, performing descriptive and inferential statistical tests (ANOVA and Tukey's HSD), generating relevant visualizations, and compiling all results into a final, multi-page PDF report. This pipeline saves significant time and ensures the reproducibility and accuracy of the analysis.

2. Data & Methodology
The analysis was performed on a dataset containing measurements from soil samples (dados_tcc_organizados.csv). The methodology, executed via Python scripts in the /scripts folder, involved:

Data Cleaning: Loading the raw data, handling missing values, and structuring it for analysis.

Descriptive Statistics: Calculating key metrics like mean, standard deviation, and counts for each variable.

Inferential Statistics: Applying Analysis of Variance (ANOVA) to determine if there were statistically significant differences between sample groups. A Tukey's HSD post-hoc test was used to identify which specific groups were different from each other.

Automated Report Generation: All statistical tables and visualizations were programmatically compiled into a final PDF report, tcc_relatorio_completo.pdf, located in the /report folder.

3. Key Findings & Visualizations
The analysis successfully identified significant differences in key soil metrics across different collection points. The boxplots below visually represent the data distribution that was formally tested with ANOVA.

(Action: Take a screenshot of one of your best boxplots, save it as boxplot_example.png in the visualizations folder, and the line below will display it.)

!(visualizations/boxplot_example.png)

A full breakdown of all statistical results and graphs is available in the complete report in the /report folder.

4. Tech Stack
Language: Python

Libraries:

Pandas (for data manipulation)

Matplotlib / Seaborn (for visualizations)

SciPy / Statsmodels (for ANOVA and Tukey's HSD tests)

FPDF / ReportLab (for PDF report generation - adjust as needed)

How to Run
Clone this repository.

Install the required libraries: pip install -r requirements.txt

Run the main script from the /scripts folder to process the data in /data and generate the final report.
