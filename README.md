# Cardiovascular testing and stroke after retinal ischemia in All of Us

Analysis code for an observational comparison of documented cardiovascular testing and subsequent recorded stroke after retinal artery occlusion (RAO) versus transient monocular vision loss (TMVL), using All of Us Registered Tier electronic health record data.

This repository contains unexecuted analysis notebooks, reviewed concept definitions, and documentation. It does not contain participant data, executed notebook outputs, result tables, or the manuscript. Access to this repository does not provide access to All of Us data.

## Status

The code reflects analysis version **2.3**, developed for Registered Tier **CDR v9, R2025Q4R6**. The notebook source was checked against the corresponding executed HTML exports before preparing this repository. Environment configuration and sharing safeguards were added for distribution; see [provenance](docs/provenance.md).

The analysis is a working research project. A focused stroke-model sensitivity analysis addressing potential nonproportional hazards for chronic kidney disease and the combined Other/Unknown race/ethnicity category remains pending. Carotid imaging-to-treatment, AF-to-anticoagulation, and G45.3-versus-H34.0 coding analyses are proposed extensions and are **not implemented** here.

## Repository contents

| File | Purpose |
| --- | --- |
| `rao_tmvl_testing_v2_3.ipynb` | Python cohort construction, testing models, stroke analyses, and sensitivity analyses |
| `rao_tmvl_ph_check_v2_3.ipynb` | R proportional-hazards diagnostics and a joint piecewise stroke model |
| `definitions/procedure_concepts.csv` | Reviewed procedure concept identifiers, labels, inclusion decisions, and review notes; participant counts removed |
| `docs/analysis-plan.md` | Implemented definitions, model specifications, and interpretation limits |
| `docs/provenance.md` | Source checksums, source verification, and distribution changes |

## Requirements

Run the analysis inside an authorized All of Us Researcher Workbench workspace with access to the specified Registered Tier release and a configured billing project. BigQuery queries can incur charges. Participant-level records and the internal Python-to-R transfer file must remain in the authorized environment.

The Python notebook uses NumPy, pandas, statsmodels, and the Google Cloud BigQuery client. BigQuery-to-pandas conversion also requires its supported dataframe dependencies, including `db-dtypes` and PyArrow. Jupyter/IPython provides notebook execution and display. The R notebook uses an R kernel and the `survival` package. Exact package versions from the original executed environment were not captured; a dependency list is not a verified environment lockfile.

## Run the analysis

1. Place this repository in the authorized Workbench environment. Keep both notebooks at the repository root so their relative paths resolve consistently.
2. Configure `ALL_OF_US_CDR` with the dataset resource accessible in your workspace, in `project.dataset` form. This value is a configuration setting, not a credential. The notebooks use the Workbench's existing Google authentication; do not add credential files to the repository.
3. Open `rao_tmvl_testing_v2_3.ipynb` with the Python kernel. Confirm the dataset release and review `definitions/procedure_concepts.csv`. The supplied list is already reviewed for the source analysis. Restart the kernel and run all cells in order.
4. The main notebook creates `results/`, internal audit files, and `internal/stroke_ph_data_INTERNAL.csv`. The latter contains individual-level analysis rows and is used only inside the Workbench.
5. Open `rao_tmvl_ph_check_v2_3.ipynb` with the R kernel in the same working directory. Restart and run all cells after the Python notebook has completed. This fits formal `survival::cox.zph` diagnostics and the joint early/late stroke model.
6. Review model-fit diagnostics, definitions, and disclosure controls before interpreting or exporting any outputs. The repository's automated suppression rules are not a substitute for the program's current disclosure review requirements.

If the procedure definition file is absent, the main notebook generates a candidate list and intentionally stops. Review candidates before setting `DEFINITIONS_FROZEN = True` and rerunning. A newly generated list can differ from the reviewed list used for this version.

## Interpretation

The primary outcome is **documented testing**, not a direct measure of care quality, clinical indication, or guideline adherence. Diagnoses identify first recorded qualifying events, not adjudicated incident events. Analyses compare RAO with TMVL; they do not estimate the effect of receiving testing on stroke. Missing records do not establish that care was not delivered. See the [analysis plan](docs/analysis-plan.md) for the implemented eligibility rules and limitations.

## Data and sharing

All of Us data must be accessed through the program's authorized process. See the [Researcher Workbench](https://www.researchallofus.org/data-tools/workbench/) and [Data Access Framework](https://support.researchallofus.org/hc/en-us/articles/22346942074132-Data-Access-Framework).

Do not commit `internal/`, `results/`, executed HTML exports, notebook outputs, credentials, participant identifiers, dates, or participant-level records. Internal audit tables may contain small cells even when they do not contain direct participant identifiers. Review the actual files being committed; an ignore rule alone does not make a file safe to share.


## Repository checks

See [CONTRIBUTING.md](CONTRIBUTING.md) for the pre-commit hook and publication
checks. GitHub Actions checks notebook cleanliness and Python syntax without
accessing All of Us or running the study. The R source is syntax-checked during
initial repository preparation. These checks do not reproduce the study results.

`requirements.txt` lists Python dependencies. Use the authorized Workbench's R
kernel with `survival` installed. Set `ALL_OF_US_CDR` in the kernel environment
before running. If the environment does not expose it, add the following line
after the imports in the main notebook's setup cell, replacing the placeholder
with your authorized dataset resource:

```python
os.environ["ALL_OF_US_CDR"] = "YOUR_AUTHORIZED_PROJECT.R2025Q4R6"
```

The supplied `.env.example` is documentation only; the notebooks do not load it
automatically. Retain the reviewed procedure CSV when moving the notebooks into
your workspace.

## License

No software license has been selected for this initial repository. Public
visibility does not grant access to restricted data or override applicable data
and terminology-use terms.
