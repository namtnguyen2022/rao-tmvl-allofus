# Implemented analysis plan: version 2.3

This document describes the supplied code. It is not a claim of prospective registration and does not substitute for a complete study protocol.

## Questions and data source

The primary question is whether documented cardiovascular testing differs after a first recorded qualifying RAO versus TMVL diagnosis, accounting for measured demographic characteristics, clinical history, healthcare use, and the care setting at diagnosis. Secondary analyses compare subsequent recorded stroke incidence and hazards. The source analysis uses All of Us Registered Tier CDR v9, R2025Q4R6.

The code queries OMOP `person`, `condition_occurrence`, `visit_occurrence`, `procedure_occurrence`, `drug_exposure`, `death`, `concept`, and `concept_ancestor` tables. Registered Tier date shifting limits interpretation of calendar periods; periods are approximate.

## Exposure definitions and eligibility

The primary RAO definition uses exact standard concept identifiers for central and branch retinal artery occlusion. Exposure definitions do not automatically expand through descendant concepts.

| Set | Concept identifiers |
| --- | --- |
| Central RAO | 437540, 37207895, 37207955, 37310623 |
| Branch RAO | 36713329, 36713330, 3657106 |
| Additional RAO concepts for broad sensitivity only | 437847, 3656884, 3656968, 4334245, 4096157, 3657144 |
| TMVL | 4338523, 36712812, 36712813, 3656941, 3656857 |

TMVL includes amaurosis fugax and transient retinal artery occlusion. The broad RAO sensitivity additionally includes partial/unspecified occlusion, thrombosis, and cholesterol embolus concepts. Labels are queried from the selected CDR vocabulary during execution.

The index date is the earliest qualifying RAO or TMVL record. RAO wins same-day ties. Participants initially assigned TMVL remain in that group if RAO is later recorded. Eligibility requires age at least 18 years and a visit start at least 365 days before index. Age is index calendar year minus birth year. This prior-record requirement does not establish continuous observation or a disease-free washout period.

## Testing and medication outcomes

Procedures are identified using the reviewed definition file, matching standard or source concept identifiers. An explicitly excluded source or standard concept cannot re-enter through the other field. Abnormal findings alone do not count as performed tests. Head-and-neck angiograms can contribute to both brain and carotid/neck vessel imaging. Probe-placement-only CPT codes 93313 and 93316 are excluded.

| Outcome | Window and exclusions |
| --- | --- |
| Echocardiography excluding stress studies | Days 0–30 and 0–90; exclude the same test in days −180 through −1 |
| Ambulatory rhythm monitoring | Same windows and prior-test exclusion; additionally exclude previously recorded AF |
| Carotid/neck vessel imaging | Days 0–30 and 0–90; exclude the same test in days −180 through −1 |
| Brain imaging | Days 0–30 and 0–90; exclude the same test in days −180 through −1 |
| Any core testing | Any echocardiography, rhythm monitoring, or carotid/neck imaging in days 0–90; no blanket exclusion of prior tests or AF |
| Any core testing without recent core tests | Same composite restricted to no core test in days −180 through −1 |
| Newly recorded statin exposure | Drug exposure start in days 0–90, with no statin exposure start in days −365 through −1 |

The statin definition covers atorvastatin, rosuvastatin, simvastatin, pravastatin, lovastatin, fluvastatin, and pitavastatin using RxNorm ingredient descendants. This represents newly recorded exposure under the specified lookback, not confirmed medication initiation or lifelong statin-naive status.

Testing analyses require a latest visit end at or beyond the applicable 30- or 90-day window, or recorded death during the window. A sensitivity analysis removes that requirement. Neither rule establishes complete capture of all care.

## Baseline variables and testing models

Clinical histories use available records before index for hypertension, diabetes, hyperlipidemia, coronary artery disease, heart failure, chronic kidney disease, AF, stroke, and myocardial infarction. They are not limited to the one-year utilization window. Outcome/covariate definitions use specified ancestor concepts and their descendants. Post-index records whose labels indicate history, sequelae, or related excluded terms do not count as new stroke.

Healthcare use is the number of distinct prior-year visit start dates, modeled as `log(1 + visits)`. Care setting uses the encounter linked to the index diagnosis and relevant encounter dates. It distinguishes ED/inpatient, positively identified outpatient, and unknown. Unrecognized encounter types are not assumed to be outpatient.

Race/ethnicity is categorized as non-Hispanic White, non-Hispanic Black, Hispanic, or Other/Unknown. Non-Hispanic assignment requires explicitly recorded non-Hispanic ethnicity. Female/male sex-at-birth categories are used for the regression analyses; other/unknown records are not included in those models.

Sequential logistic models estimate RAO-versus-TMVL odds ratios:

1. M1: age, sex, race/ethnicity, and approximate diagnosis period.
2. M2: M1 plus the nine clinical histories.
3. M3: M2 plus prior-year healthcare use.
4. M4: M3 plus the care setting of the index diagnosis.

Diagnosis periods are 2016 or earlier, 2017–2020, and 2021 onward using shifted dates. All analyses are observational; no multiple-comparison adjustment is implemented.

## Stroke analyses

Participants with prior recorded stroke are excluded from the stroke risk population. Stroke identification uses cerebral infarction and cerebrovascular accident concept families. It is not an adjudicated ischemic-stroke-only endpoint.

Follow-up ends at the earliest recorded stroke, death, latest available visit end, or 1,095 days. The code adds half a day to event/censoring times to retain day-zero events. Stroke takes priority when stroke and death share a date. Cumulative incidence uses an Aalen–Johansen calculation with death as a competing event. Cox models estimate cause-specific stroke hazards, treating death as censoring.

The adjusted stroke model includes age, sex, race/ethnicity, and clinical histories. It does not include diagnosis period, prior-year visit frequency, or index care setting. Constant covariates are removed; prior stroke is absent by eligibility. Cox model ties use the Breslow method.

The companion R notebook reconstructs the model from the internal analysis matrix. It runs `cox.zph` with Kaplan–Meier and log time transforms at one- and three-year horizons, generates RAO coefficient plots, and fits one joint piecewise model for days 0–30 versus 31–1,095 with an interaction test. The separate Python period estimates and joint R estimates come from different specifications and must not be presented as interchangeable.

## Implemented sensitivity analyses

- Broader RAO exposure definition.
- Any core testing among participants without core testing in the preceding 180 days.
- Removal of the post-index observation requirement for testing.
- Extension of the testing window to include days −14 through 90.
- Exclusion of shifted calendar years immediately before the period boundaries.
- A selected subgroup requiring RAO records on at least two dates. This uses later records and has no equivalent repeat-confirmation requirement for TMVL; it is not phenotype validation.
- Stroke analyses excluding same-day recorded strokes and a day-30 landmark analysis.
- Period-specific stroke estimates and formal proportional-hazards diagnostics.

## Outstanding work and proposed extensions

A focused stroke-model sensitivity allowing nonproportional effects or suitable stratification for chronic kidney disease and the combined Other/Unknown race/ethnicity category remains pending. The current proportional-hazards diagnostics must be interpreted before treating an overall hazard ratio as a constant effect over time.

The carotid imaging → recorded stenosis → revascularization pathway, AF → oral anticoagulation pathway, and G45.3-versus-H34.0 coding comparison have not been implemented. These require feasibility checks, explicit timing and eligibility rules, and definition review. They should not be described as completed analyses.

## Interpretation and disclosure limits

The study measures records of evaluation and outcomes. It cannot determine whether absent documentation represents absent care, whether testing was clinically indicated, or whether a particular patient's care was inappropriate. It does not estimate a causal effect of testing on stroke. Residual confounding, diagnosis timing, care setting, missing records, selection, and phenotype misclassification remain relevant.

The notebooks include small-cell and selected complementary/cross-table suppression. Some internal outputs intentionally retain restricted detail for analysis. All generated outputs need review under the program's current requirements before export; code-based suppression alone does not establish permission to publish them.
