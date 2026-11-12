# tutoring-paradox

## Team Members
- Derrilon Young
- Shree Krishna Shrestha
- Emilio El-Zahr

## Topic
The Tutoring Paradox in Education: students who get tutoring seem to fail more
often. We test whether this is because struggling students are the ones being
referred (Simpson's paradox), and whether attending more sessions helps.

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

## How to Run
1. Download the raw CSV files from the course repository
   (`final-project/Topic5_Education_The_Tutoring_Paradox/data`) and put them in `data/raw/`.
2. Open the notebooks from the `notebooks/` folder (they use paths like `../data/raw/`).
3. Run the notebooks in this order, using **Restart → Run All** for each:
   1. `01_cleaning.ipynb` (saves the cleaned files to `data/clean/`)
   2. `Exploration.ipynb`
   3. `02_features.ipynb` (saves `data/features.csv`)
   4. `03_experiments.ipynb`
      5. `04_models.ipynb` (needs `mlflow`; logs to the course server at http://10.0.100.20:5000, reachable from the lab network)
   6. `05_validation.ipynb`

## M2 Results
- **H1: Supported.** Overall, referred students failed more in term 3 (19.6% vs. 8.9%).
  But inside every group of students with the same prior GPA and term 1 result
  (7 groups), referred students failed **less**. This is Simpson's paradox: students
  are referred because they were already struggling.
- **H2: Revised.** Our planned rule (failure goes down at every attendance step) held
  in only 2 of 5 GPA groups. But among lower-GPA referred students, the highest
  attendance group failed much less than the lowest (Q1: 44.3% → 18.7%). Strong
  students almost never failed, so attendance could not make a measurable difference.
- **Extra:** bus riders attended about 6–9 points fewer sessions in every GPA group.
- **Models (R7):** prior GPA is what predicts failure (CV AUC 0.785 → 0.874). Adding
  referral or attendance after GPA makes naive Bayes slightly worse, because they mostly
  repeat what GPA already says.
- **Validation (R8):** we chose M2 (best CV AUC, lead 6× the SD). On the test set it
  scored AUC 0.871 (CV 0.874), so CV was trustworthy. Its probabilities are too extreme
  (Brier 0.109 vs. baseline 0.088), but the top 20% highest-risk rows catch 68% of failures.
- **Final verdicts:** H1 **supported**, H2 **revised**.

## AI Use
### Milestone 1
- **R2 (Inputs Graph):** The team built the graph. AI helped us understand the expert
  inputs.
- **R3 (01_cleaning.ipynb):** The team decided the cleaning steps and checked every
  result. Claude helped structure the notebook and write and explain the code.
- **R4 (Exploration.ipynb):** The team chose what to explore. AI helped explain the
  analysis and write code.

### Milestone 2
- **Features and split:** We decided which features to use and checked that no term 3
  information was included. Claude helped write the code and notebook text.
- **R6 (Experiments):** We followed the tests planned in R5 and decided on the verdicts
  (H1 supported, H2 revised). Claude helped write the code.
- **R7 (Models):** We designed and ran the five planned naive Bayes models
  (M0–M4) plus an extra model (M5) to test why attendance lowered the score. We logged
  every run to the course MLflow server and wrote the results.
  AI helped write and explain parts of the code.
- **R8 (Validation):** We set the rule for choosing the model, chose M2, and checked the
  test result. Claude helped write the code.



All content was reviewed by the team and can be explained and reproduced by us.