\# Product-Pulse-AI

\### An End-to-End E-Commerce Analytics, Data Quality \& AI-Assisted Decision Intelligence Platform



Product-Pulse-AI is an analytics engineering and decision-support project built on the \*\*Olist Brazilian E-Commerce Public Dataset\*\*. It transforms raw e-commerce data into validated analytical models, reusable business marts, revenue decomposition, customer voice insights, and AI-assisted decision reasoning.



The project demonstrates how raw transactional data can be transformed into governed, testable, and decision-ready information for product, business, and analytics teams.



\## Project Objectives



\- Build a reproducible data pipeline from raw datasets to analytical outputs.

\- Implement dimensional modeling and a warehouse-style architecture.

\- Establish explicit data quality rules and validation checks.

\- Create customer, market, and product performance marts.

\- Decompose revenue movements into interpretable components.

\- Generate AI-assisted decision reasoning with evidence grounding and human review.

\- Deliver business-facing dashboards through Power BI.



\## Key Capabilities



\### 1. Data Engineering \& Analytics Architecture



\- Raw data ingestion and staging across nine source CSV files.

\- Warehouse-style fact and dimension tables.

\- Reusable analytical marts at defined grains.

\- Parquet-based analytical outputs.

\- Data validation, grain checks, and persistence safeguards.

\- Version-controlled source code, configurations, and tests.



\### 2. Dimensional Modeling



The warehouse pipeline persists ten tables.



| Table | Rows |

|---|---:|

| `fact\_order` | 99,441 |

| `fact\_order\_item` | 112,650 |

| `fact\_payment` | 103,886 |

| `fact\_review` | 99,224 |

| `dim\_date` | 1,561 |

| `dim\_customer` | 99,441 |

| `dim\_product` | 32,951 |

| `dim\_seller` | 3,095 |

| `dim\_category` | 71 |

| `dim\_geography` | 1,000,163 |



These counts describe persisted table sizes, not necessarily distinct business entities in every table.



\### 3. Data Quality \& Governance



The project implements a configurable data quality framework with \*\*44 rules\*\*.



It produces machine-readable results and summary artifacts for tracking rule outcomes, severity, and affected records.



Latest verified execution:



\- Rules evaluated: 44

\- Passing rules: 38

\- Failing rules: 6

\- Critical failures: 0

\- Warning-level failures: 6

\- Affected records summed across rules: 2,058



The six warning-level failures are retained and reported rather than hidden by weakening the checks or altering source data.



Generated artifacts:



\- `data/processed/quality/dq\_results.csv`

\- `data/processed/quality/dq\_summary.json`



\### 4. Analytical Data Marts



The project builds reusable outputs for different business questions.



| Analytical output | Latest verified size |

|---|---:|

| Customer performance mart | 97,319 rows |

| Market performance mart | 69,722 rows |

| Product performance mart | 94,591 rows |

| Product-market monthly mart | 102,171 rows |



The marts include grain validation and persisted analytical outputs. Their row counts should be interpreted in the context of each mart's defined grain.



\### 5. Revenue Decomposition



The revenue decomposition module produces a monthly analytical bridge for understanding revenue changes.



Verified validation results:



\- 24 monthly records.

\- No duplicate monthly grain.

\- Maximum reconciliation difference of approximately \\(9.79 \\times 10^{-11}\\).

\- September 2018 identified as a partial month.



The reconciliation check verifies the arithmetic consistency of the decomposition; it does not independently establish the business cause of every movement.



\### 6. Customer Voice Analytics



The Customer Voice workflow processes review text and produces sentiment-oriented analytical outputs.



A verified in-memory build processed 99,224 review records:



\- Text-bearing reviews: 42,687

\- Textless reviews: 56,537

\- Sentiment predictions generated for text-bearing reviews: 42,687



The latest rebuild was stopped by an existing-output overwrite safeguard. These figures describe the validated in-memory build and should not be interpreted as confirmation that the protected output file was regenerated.



\### 7. AI-Assisted Decision Intelligence



The project includes an AI-assisted decision-reasoning workflow using a live language-model API.



A verified reasoning batch produced six records, persisted in:



`data/processed/marts/mart\_llm\_decision\_reasoning.parquet`



The batch passed checks for unique, non-null identifiers, evidence grounding, and human-review requirements.



AI-generated reasoning is decision support, not an automatically approved business decision. Review and validation remain important.



\### 8. Power BI Dashboards



The Power BI report is located at:



`powerbi/Product\_Pulse\_AI.pbix`



\*\*Verified:\*\* The report opened in Power BI Desktop, its dashboards were visible, and a manual refresh completed successfully.



The report is maintained separately from the two Git commits documented below.



\## Architecture



```text

Olist Raw CSV Dataset

&#x20;       |

&#x20;       v

Staging \& Source Validation

&#x20;       |

&#x20;       v

Warehouse Fact and Dimension Tables

&#x20;       |

&#x20;       v

Analytical Data Marts

&#x20;       |

&#x20;       +----------------------+

&#x20;       |                      |

&#x20;       v                      v

Revenue Decomposition    Customer Voice

&#x20;       |                      |

&#x20;       +-----------+----------+

&#x20;                   |

&#x20;                   v

&#x20;      AI-Assisted Decision Reasoning

&#x20;                   |

&#x20;                   v

&#x20;         Power BI Dashboards

```



Cross-cutting capabilities include automated testing, configurable data quality rules, validation checks, and version control.



This diagram represents the project's major processing stages rather than every runtime dependency.



\## Technology Stack



\- \*\*Language:\*\* Python 3.11

\- \*\*Data processing:\*\* Pandas, NumPy, PyArrow

\- \*\*Storage:\*\* Parquet and CSV analytical artifacts

\- \*\*Data architecture:\*\* Staging, fact and dimension tables, analytical marts

\- \*\*AI:\*\* Language-model API integration and evidence-grounded reasoning

\- \*\*Business intelligence:\*\* Microsoft Power BI

\- \*\*Testing:\*\* pytest

\- \*\*Configuration:\*\* YAML

\- \*\*Version control:\*\* Git



\## Repository Structure



```text

PRODUCT-PULSE-AI/

├── configs/          # Project and data quality configuration

├── data/

│   ├── raw/          # Source CSV files

│   └── processed/    # Quality, warehouse and analytical outputs

├── docs/             # Project documentation and runbook

├── logs/             # Execution logs

├── notebooks/        # Exploration and experimentation

├── outputs/          # Validation and reporting artifacts

├── powerbi/          # Power BI report

├── scripts/          # Pipeline entry points and validation scripts

├── sql/              # SQL assets

├── src/              # Reusable project modules

├── tests/            # Automated tests

├── .gitignore

└── README.md

```



\## Setup



Prerequisites:



\- Python 3.11

\- Git

\- Power BI Desktop for the report



Clone the repository and enter the project directory:



```powershell

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd PRODUCT-PULSE-AI

```



Create and activate an environment:



```powershell

conda create -n product\_pulse python=3.11 -y

conda activate product\_pulse

```



Install the project's dependencies using the repository's dependency manifest, if provided. Verify the required packages and external API configuration before running the pipeline.



\*\*Note:\*\* This repository's current setup should be checked for a complete dependency manifest and documented API requirements before claiming a clean-machine, one-command installation.



\## Running the Pipeline



The following commands were executed successfully in the development environment:



```powershell

python scripts/run\_current\_data\_quality.py

python scripts/run\_staging.py

python scripts/run\_warehouse.py

python scripts/run\_customer\_performance\_mart.py

python scripts/run\_market\_performance\_mart.py

python scripts/run\_product\_performance\_mart.py

python scripts/run\_product\_market\_performance\_monthly.py

python scripts/run\_revenue\_decomposition.py

python scripts/validate\_revenue\_decomposition.py

```



Run the automated tests:



```powershell

python -m pytest -q

```



\*\*Latest verified full-suite result:\*\* 539 tests passed.



Check `docs/RUNBOOK.md` for the execution sequence and important safeguards.



Some workflows depend on existing outputs or external API access. Review their configuration before rerunning them. In particular, the AI reasoning workflow can make live API calls, and the Customer Voice build has an overwrite safeguard.



\## Dataset



\*\*Source:\*\* Olist Brazilian E-Commerce Public Dataset.



The dataset contains Brazilian e-commerce transaction, customer, product, seller, payment, review, and geographic information.



The project uses nine source CSV files. Follow the original dataset provider's terms and attribution requirements when redistributing data.



The dataset covers a historical period, with the analytical outputs spanning approximately September 2016 to September 2018. September 2018 is a partial month in the revenue decomposition output.



\## Git \& Reproducibility



The current development repository includes these commits:



\- `6dc5772` — Build Product Pulse AI analytics and decision pipeline

\- `8dc14c5` — Document project execution and validation runbook



The project has passed its latest full automated test run and the documented revenue decomposition checks.



The Power BI report exists locally in `powerbi/` and is currently untracked by Git. If you publish this project, decide deliberately whether to keep the report outside Git, publish it separately, or use an appropriate large-file hosting approach.



\## Business Value



The platform is designed to support questions such as:



\- How are customer and product performance changing over time?

\- Which market segments contribute to revenue movements?

\- Are analytical outputs trustworthy enough for decision-making?

\- What themes and sentiment appear in customer reviews?

\- What evidence supports an AI-generated recommendation?

\- Which data quality failures require investigation before business use?



These are intended decision-support use cases. Quantified business impact has not been independently measured in this project.



\## Current Limitations



\- Six warning-level data quality rules fail and require investigation.

\- The Customer Voice rebuild did not overwrite the existing persisted output.

\- AI-generated reasoning requires human review.

\- The dataset is historical rather than live operational data.

\- Power BI opening and manual refresh were verified, but deployment, scheduled refresh, and service-level access controls have not been established by these checks.



\## Future Enhancements



\- Add a clean-environment installation and reproducible end-to-end setup.

\- Investigate and document the six warning-level data quality failures.

\- Add automated data freshness and pipeline observability.

\- Formalize metric definitions and semantic-model documentation.

\- Improve the traceability of AI reasoning from source evidence to reviewed decisions.

\- Document Power BI measures, report pages, and refresh dependencies.

\- Add business-facing case studies that connect analytical findings to proposed actions and measurable outcomes.



\## Author's Note



Product-Pulse-AI is an end-to-end portfolio project focused on analytics engineering, data quality, business intelligence, and AI-assisted decision support. It emphasizes validated outputs, explicit limitations, and reproducible engineering practices over unsupported performance claims.
