# tutoring-paradox

## Team Members
- Derrilon Young
- Shree Krishna Shrestha
- Emilio El-Zahr

## Topic
The Tutoring Paradox in Education: students who get tutoring seem to fail more
often, and the district is considering cutting the program. We test whether this is
because struggling students are the ones being referred (Simpson's paradox), and
whether attending more sessions helps.

## Conclusion (M3)

**Decision (R1):** should the district keep, change, or cut funding for the tutoring program?

| Hypothesis | Evidence | Verdict |
|---|---|---|
| **H1** Referred students fail more because they were already struggling | Overall, referred students failed more (19.6% vs. 8.9%), but inside all 7 groups with the same prior GPA and term 1 result, they failed **less**. Referral adds nothing to prediction once prior GPA is known (CV AUC 0.874 → 0.865). | **Supported** |
| **H2** Referred students who attend more fail less | The planned rule (failure drops at every attendance step) held in only 2 of 5 GPA groups. Among lower-GPA students, the highest attendance group failed much less than the lowest (Q1: 44.3% → 18.7%). | **Revised** |

**Limits of the evidence**
- This is past data, not an experiment, so we cannot prove that tutoring *causes* lower failure.
- Motivation and family support are not in the data and could affect both attendance and passing.
- One school year only. The reason for each referral is not recorded.
- The chosen model's probabilities are overconfident (Brier 0.109 vs. 0.088 for a constant guess), so we use its ranking, not its numbers.

**Recommendation:** keep funding the tutoring program, and at the start of each term use
model M2 to refer the 20% of students with the highest predicted risk (on the test set,
that 20% included 68% of all term 3 failures).

**Monitoring:** each term, check what share of that term's failures were in M2's top 20%.
On our test set it was 68%. **If it falls below 60%, review the model.**

## The chosen model in MLflow
- Model: M2 (GaussianNB pipeline with median fill for missing prior GPA), saved by `notebooks/07_save_model.ipynb`
- MLflow server: http://10.0.100.20:5000 (lab network), experiment `tutoring-paradox-r7`, run `M2_final_model`
- **Run id: `6f90acd9ca49441aab6266696cdd3a19`** (also in `results/model_run_id.txt`)
- Load it with:
  ```python
  import mlflow.sklearn
  model = mlflow.sklearn.load_model("runs:/6f90acd9ca49441aab6266696cdd3a19/model")
  model.predict_proba(X)   # X = the 10 feature columns, prepared as in 07_save_model
  ```

## How to Reproduce

### Environment
- Python 3.11
- `pip install -r requirements.txt`
- **scikit-learn must be 1.3.0.** The shared split in `src/split.py` uses
  `StratifiedGroupKFold(shuffle=True)`, and a newer scikit-learn puts different students
  in the test set, which changes the R8 numbers.
- `mlflow` is only needed for `04_models` and `07_save_model`, which run on the lab
  machine (the course MLflow server is only reachable from the lab network).

### Data
Download the raw CSV files from the course repository
(`final-project/Topic5_Education_The_Tutoring_Paradox/data`) and put them in `data/raw/`.

### Run order
Open the notebooks from the `notebooks/` folder (they use paths like `../data/raw/`) and
run each with **Restart → Run All**:
1. `01_cleaning.ipynb` → saves the cleaned files to `data/clean/`
2. `Exploration.ipynb` (R4)
3. `02_features.ipynb` → saves `data/features.csv`
4. `03_experiments.ipynb` (R6: H1, H2, bus riders)
5. `04_models.ipynb` (R7, lab machine) → logs runs to MLflow, saves `results/mlflow_runs.csv`
6. `05_validation.ipynb` (R8) → scores the test set once, saves `results/test_result.csv`
7. `06_figures.ipynb` → makes every chart in the presentation, saved in `figures/`
8. `07_save_model.ipynb` (lab machine) → saves M2 in MLflow, saves `results/model_run_id.txt`

### Where each number in the presentation comes from
| Slide | Number | Source |
|---|---|---|
| The problem | 19.6% vs. 8.9% failed | `03_experiments`, Step 3 (overall rates) |
| Our data | 120,000 rows, 10.2% failed, 95,991 / 24,009 split | `02_features`, Steps 7–8 |
| H1 | 7 groups, referred fail less in all 7 | `03_experiments`, Step 3; chart `06_figures`, Step 2 |
| H2 | 2 of 5 groups; Q1 44.3% → 18.7% | `03_experiments`, Step 4 and extra check; chart `06_figures`, Step 3 |
| Bus riders | 53% vs. 62% attendance; 6–9 points per GPA group | `03_experiments`, Step 5; chart `06_figures`, Step 4 |
| Models | CV AUC 0.785 – 0.874, ± SD | `04_models` → `results/mlflow_runs.csv`; chart `06_figures`, Step 5 |
| Validation | Test AUC 0.871, Brier 0.109, baseline 0.088, top 20% = 68% | `05_validation`, Steps 4–5 → `results/test_result.csv` |
| Probability check | "98%" predicted → 46% failed | `05_validation`, Step 5; chart `06_figures`, Step 6 |
| Recommendation | 68% → review below 60% | `05_validation`, Step 5 |

## File Guide

### Milestone 1
| File | What it is |
|---|---|
| `R1_problem.md` | Problem statement, the decision, and four questions with goals |
| `R2_inputs_graph.png` | Graph of all meaningful inputs, with arrows |
| `notebooks/01_cleaning.ipynb` | Loads every raw file, applies each cleaning step in order, prints rows before/after each step with the reason |
| `notebooks/Exploration.ipynb`, `docs/r4_notes.md` | R4: visualisations, summary statistics and comparisons between variables |
| `docs/R5_hypotheses.md`, `figures/R5_hypotheses_graph.png` | R5: two if-then hypotheses (H1, H2) with predictions and planned tests |
| `DATA_DICTIONARY.md` | Description of every column in each raw CSV file |
| `notebooks/first_look.py`, `notebooks/attendance.py` | Helper scripts used while exploring the data for R4 |
| `notebooks/r5_graph.py` | Draws the R5 hypotheses graph (`figures/R5_hypotheses_graph.png`) |

### Milestone 2
| File | What it is |
|---|---|
| `notebooks/02_features.ipynb` | Builds the feature table: one row per student × subject (120,000 rows), only information from before term 3. Includes a feature guide and the split check |
| `data/features.csv` | The feature table used by all M2 notebooks |
| `src/split.py` | Shared split: 20% of students held out as the test set; 5-fold cross-validation grouped by student on the rest (seed 42) |
| `notebooks/03_experiments.ipynb` | R6: tests H1 and H2 with group comparisons and 95% Wilson confidence intervals |
| `notebooks/04_models.ipynb` | R7: naive Bayes models M0–M5, every run logged in MLflow (course server) |
| `results/mlflow_runs.csv` | R7: exported MLflow run table (6 runs: features, reason, CV AUC ± SD, Brier, train/CV gap) |
| `notebooks/05_validation.ipynb` | R8: model choice, test set scored once, probability check, final verdicts |
| `results/test_result.csv` | R8: test set result for the chosen model (M2) |

### Milestone 3
| File | What it is |
|---|---|
| `presentation/Tutoring_Paradox.pdf` | The presentation deck (12 minutes) |
| `notebooks/06_figures.ipynb`, `figures/m3_*.png` | Every chart in the presentation, recomputed from the data and results files |
| `notebooks/07_save_model.ipynb` | Saves the chosen model (M2) in MLflow and checks it loads |
| `results/model_run_id.txt` | MLflow run id of the saved model |
| `requirements.txt` | Package versions used |

## AI Use

### Milestone 1
- **R1 (Problem):** The team chose the problem and questions. Claude helped simplify the wording.
- **R2 (Inputs Graph):** The team built the graph. AI helped us understand the expert inputs.
- **R3 (01_cleaning.ipynb):** The team decided the cleaning steps and checked every
  result. Claude helped structure the notebook and write and explain the code.
- **R4 (Exploration.ipynb):** The team chose what to explore. AI helped explain the
  analysis and write code.


### Milestone 2
- **Features and split:** We decided which features to use and checked that no term 3
  information was included. Claude helped write the code.
- **R6 (Experiments):** We followed the tests planned in R5 and decided on the verdicts
  (H1 supported, H2 revised). Claude helped write the code.
- **R7 (Models):** Derrilon designed and ran the five planned naive Bayes models
  (M0–M4) plus an extra model (M5) to test why attendance lowered the score, logged
  every run to the course MLflow server and wrote the results.
  AI helped write and explain parts of the code.
- **R8 (Validation):** We set the rule for choosing the model, chose M2, and checked the
  test result. Claude helped write the code.

### Milestone 3
- **Conclusion and recommendation:** The team chose the recommendation and the
  monitoring threshold. 
- **Figures and model saving (`06_figures`, `07_save_model`):** Claude helped write the
  code; we ran it and checked that the numbers match our notebooks.
- **README:** Claude helped organize the reproduction steps and the number-to-source table.

All content was reviewed by the team and can be explained and reproduced by us.

**Version note (found during M3):** `04_models` and `07_save_model` ran on the lab machine
with scikit-learn **1.9.1**, while `02_features`, `05_validation` and `06_figures` ran on a
laptop with scikit-learn **1.3.0**. The two versions put different students in the test set,
so the R8 test set is not exactly the set held out during R7. We checked this by repeating
R8 with scikit-learn 1.9.1: test AUC 0.871 (same), Brier 0.113 (vs. 0.109), and the top 20%
of predicted risk still holds 67% of failures (vs. 68%). The model choice and all conclusions
are unchanged. Future work: one scikit-learn version for every machine.