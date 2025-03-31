import pandas as pd
from sklearn.model_selection import train_test_split

# Function to load and split ECG data
def load_and_split_ecg_data(file_path):
    try:
        # Load the CSV file
        data = pd.read_csv(file_path)
        print(f"Initial number of rows (ECG): {len(data)}")

        # Optional: Basic cleaning (remove rows with missing values)
        data = data.dropna()
        print(f"Rows after removing missing values (ECG): {len(data)}")

        # Features (ECG signals) and labels
        X = data.iloc[:, :-1]  # Columns 0-186 (signals)
        y = data.iloc[:, -1]   # Column 187 (labels)

        # First split: 70% train, 30% temp (validation + test)
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.3, stratify=y, random_state=42
        )

        # Second split: 50% of temp for validation, 50% for test (15% each of original)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
        )

        # Combine features and labels back into DataFrames
        train_data = pd.concat([X_train, y_train], axis=1)
        val_data = pd.concat([X_val, y_val], axis=1)
        test_data = pd.concat([X_test, y_test], axis=1)

        print(f"Training set (ECG): {len(train_data)} rows")
        print(f"Validation set (ECG): {len(val_data)} rows")
        print(f"Test set (ECG): {len(test_data)} rows")

        return train_data, val_data, test_data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None, None, None
    except Exception as e:
        print(f"Error processing ECG data: {e}")
        return None, None, None

# Function to load and split Diabetes data
def load_and_split_diabetes_data(file_path):
    try:
        # Load the CSV file
        data = pd.read_csv(file_path)
        print(f"Initial number of rows (Diabetes): {len(data)}")

        # Optional: Basic cleaning (remove rows with missing values)
        data = data.dropna()
        print(f"Rows after removing missing values (Diabetes): {len(data)}")

        # Features and target
        X = data.drop(columns=['diabetes'])  # All columns except target
        y = data['diabetes']                 # Target column

        # First split: 70% train, 30% temp (validation + test)
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.3, stratify=y, random_state=42
        )

        # Second split: 50% of temp for validation, 50% for test (15% each of original)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
        )

        # Combine features and target back into DataFrames
        train_data = pd.concat([X_train, y_train], axis=1)
        val_data = pd.concat([X_val, y_val], axis=1)
        test_data = pd.concat([X_test, y_test], axis=1)

        print(f"Training set (Diabetes): {len(train_data)} rows")
        print(f"Validation set (Diabetes): {len(val_data)} rows")
        print(f"Test set (Diabetes): {len(test_data)} rows")

        return train_data, val_data, test_data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None, None, None
    except Exception as e:
        print(f"Error processing Diabetes data: {e}")
        return None, None, None

# File paths
ecg_path = r"D:\سارا\ترم 3 دانشگاه قم\mitbih_test.csv"
diabetes_path = r"D:\سارا\ترم 3 دانشگاه قم\diabetes_prediction_dataset.csv"

# Load and split ECG data
ecg_train, ecg_val, ecg_test = load_and_split_ecg_data(ecg_path)

# Load and split Diabetes data
diabetes_train, diabetes_val, diabetes_test = load_and_split_diabetes_data(diabetes_path)

# Optional: Display first few rows of each set
if ecg_train is not None:
    print("\nECG Training Set (First 5 Rows):")
    print(ecg_train.head(5).to_string(index=False))
if diabetes_train is not None:
    print("\nDiabetes Training Set (First 5 Rows):")
    print(diabetes_train.head(5).to_string(index=False))