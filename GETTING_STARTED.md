# Getting started

[← Portfolio home](README.md)

## Explore the projects

Each folder in `projects` contains a short project description and a Power BI report (`.pbix`). Download the report and open it in Power BI Desktop to view the interactive visuals. If you refresh a report and Power BI cannot find its original source, update its data-source location. The CSVs included alongside three reports are available for analysis; the stock project's separate source file was not supplied.

The retail folder also contains the SQL script, Python notebook, and sales CSV. The SQL is read-only and expects the CSV to be imported into a MySQL table named `retail_sales`. See the [retail project page](projects/retail-sales/README.md) for setup.

## Publish this portfolio on GitHub

1. Extract the downloaded ZIP on your computer.
2. Sign in to GitHub, create a new repository, and name it `data-analytics-portfolio` (or choose your own name).
3. In that repository, choose **Add file → Upload files**, then upload the **contents** of the extracted folder, including `README.md`, `projects`, `scripts`, and `requirements.txt`. Keep the project folders together so links and images work. Commit the files.
4. Open the repository's main page and check that the README, project links, and images display. You can add your LinkedIn or contact information later if you wish.

The project is packaged for GitHub, but it has not been published to an account. Choosing a public repository makes its files, data, and reports available to anyone. Before sharing publicly, confirm you have permission to share the retail data and review the PBIX files for any source paths or information you do not want to publish.

## Check the numbers and regenerate previews

From the repository folder, install the Python packages listed in `requirements.txt`. Then run:

```bash
python scripts/validate_data.py
python scripts/create_previews.py
```

The first command checks the cited figures against the three included CSV snapshots. The second recreates the three static charts shown on the project pages. They are generated data previews, not screenshots of the Power BI dashboards. Neither command tests the Power BI reports, their DAX measures, or the stock project.
