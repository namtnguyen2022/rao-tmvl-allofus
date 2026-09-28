# Source provenance and distribution preparation

Prepared for repository distribution on 2026-09-28. This repository represents the v2.3 analysis source, not a new run of the All of Us analysis. No participant-level analysis was rerun during repository preparation.

## Sources inspected

The main Python and companion R notebooks were supplied as `.ipynb` files, with corresponding executed HTML exports. All 11 Python code-cell sources and all 4 R code-cell sources matched their respective HTML input cells after removing trailing whitespace from each cell. The original `.ipynb` files were already unexecuted.

Full source-file SHA-256 checksums before distribution edits:

| Source | SHA-256 |
| --- | --- |
| `rao_tmvl_testing_v2_3.ipynb` | `21542cb312213fe72edc5318f9ccb449d6ed28fae5bcae706966a14e3ccad50e` |
| `rao_tmvl_ph_check_v2_3.ipynb` | `555d8784cad4761ab67373f3a6f6fb0f912701aab187bfccbe0d20dc914ca293` |
| `rao_tmvl_testing_v2_3.html` | `9147cbd77fb1278378e44914aabcfbbbb77e9226c800d0bc8e9d25df5e01db56` |
| `rao_tmvl_ph_check_v2_3.html` | `e69ca184e7e1111fa7df4427327d7db8890399c2aa1610270a057fc4453e6049` |
| `procedure_concepts (3).csv` | `60fb9a3ede2dcb98ea9e4b3e48ecd7264e27a199cd1be2d7a3e884d058cb6592` |

The executed HTML exports are not distributed because they contain analysis outputs. These checksums identify the audited originals, not the sanitized files in this repository.

For a source-text-only comparison, concatenate code-cell source text in notebook order with two newline characters between cells and hash the UTF-8 bytes. Under that convention, the original main notebook hash is `f63af50603c4c9e5f0aaddb9781b71f20d940ec9e3477f5118773958039002b7`; the original R notebook hash is `6a4277aee5a5336b80994e820159d9339a97c8d299a0cf33e4ecd96d340598bb`.

## Procedure definition provenance

The reviewed source CSV has MD5 `87b0959cd9e9481774cb58be7349b656`, matching the checksum recorded in the executed main notebook. It contains 140 concept/test rows; this is a definition-row count, not a participant count. Both the supplied `(3).csv` and `(3) (1).csv` copies have that checksum. Earlier numbered files have different checksums and should not be substituted.

For public distribution, the `people` column was removed. The retained columns are concept identifier, concept name, vocabulary, concept code, test category, inclusion flag, and review note. The reviewed notes describe clinical code-selection decisions, not participant counts. Both CPT 93313 and 93316 are marked excluded. Removing the count column changes the file checksum without changing the concept inclusion decisions.

The CSV is the reviewed input definition. At runtime, the notebook additionally drops abnormal-finding concepts and can assign head-and-neck angiograms to the carotid category. The effective definition therefore consists of this CSV plus the procedure-handling code, not the CSV in isolation.

## Distribution changes

- Replace the source workspace's hardcoded BigQuery dataset identifier with an environment-configured `ALL_OF_US_CDR` value with format validation so each authorized user supplies their own accessible dataset resource.
- Keep notebooks unexecuted, with empty outputs and no execution counts or embedded result images.
- Remove participant counts from the distributed procedure definition file.
- Remove the R notebook’s exact model-row-count print to reduce cross-table disclosure risk. Model fitting is unchanged.
- Add an internal-only output notice and remove the blanket sharing claim from the R notebook’s introductory text. Strip notebook and cell metadata except the kernel/language specification.
- Add documentation, dependency guidance, and file-sharing safeguards. These do not constitute an independently reproduced study execution.

The intended statistical definitions and estimators are retained. No care-cascade analysis, coding comparison, or additional stroke sensitivity is represented as implemented. Original package versions were not recorded, so the repository does not claim bit-for-bit environment reproduction.

## Files kept outside version control

Participant-level data, internal audit outputs, executed notebooks/HTML, generated results, and the manuscript are excluded from this release. The internal Python-to-R file contains individual-level rows even though it omits participant identifiers. It must remain inside the authorized Workbench. This repository provides source code and static definitions only.


## Distributed definition checksum

The count-free `definitions/procedure_concepts.csv` has SHA-256 `d8b020cdf3ee83d89fa342d4dda39426f804de4469c674089031db41cbea2e3b`. Runtime MD5 values will differ from the original count-bearing file. The retained rows and inclusion decisions are unchanged.
