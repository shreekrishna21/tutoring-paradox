"""
Shared train/test split for M2 (Tutoring Paradox).

Everyone imports from this file, so every experiment and model uses the
same students for training, validation and testing.

- One row = one student in one subject.
- Test set: 20% of students, held out and used ONCE at the end.
- Training set: the other 80% of students, used with 5-fold cross-validation.
- Splits are by student, so the same student is never in two sets.
- Splits keep about the same share of term-3 failures in every set.
"""

import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

# Fixed settings, so the split is the same every time
RANDOM_STATE = 42
N_FOLDS = 5
TARGET = "failed_t3"
GROUP = "student_id"
FEATURES_PATH = "../data/features.csv"


def load_features(path=FEATURES_PATH):
    """Load the feature table, keeping student_id as text."""
    return pd.read_csv(path, dtype={"student_id": str})


def get_train_test(df):
    """Split rows into train (80% of students) and test (20% of students)."""
    splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    train_idx, test_idx = next(splitter.split(df, df[TARGET], groups=df[GROUP]))
    train = df.iloc[train_idx].reset_index(drop=True)
    test = df.iloc[test_idx].reset_index(drop=True)
    return train, test


def get_cv_folds(train):
    """Return the 5 cross-validation folds on the training set as (train_idx, val_idx) pairs."""
    splitter = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    return list(splitter.split(train, train[TARGET], groups=train[GROUP]))