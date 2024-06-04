import pandas as pd

# Load the CSV file
folder_path = 'AI Piping\'
file_path = folder_path +'field_of_study_exercise.csv'

class CSVHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv(self):
        return pd.read_csv(self.file_path)

    def write_csv(self, df):
        df.to_csv(self.file_path, index=False)

    def clean_data(self, df):
        initial_missing_values = df.isnull().sum().sum()

        # Drop rows where 'field_of_study' is missing
        df_cleaned = df.dropna(subset=['field_of_study'])

        # Fill missing values in 'academic_field' with 'Unknown'
        df_cleaned['academic_field'].fillna('Unknown', inplace=True)

        final_missing_values = df_cleaned.isnull().sum().sum()
        removed_missing_values = initial_missing_values - final_missing_values

        return df_cleaned, initial_missing_values, removed_missing_values

    def summarize_cleaning(self, initial_missing, removed_missing):
        return {
            'initial_missing_values': initial_missing,
            'removed_missing_values': removed_missing,
            'remaining_missing_values': initial_missing - removed_missing
        }


if __name__ == "__main__":
    csv_handler = CSVHandler(file_path)
    data = csv_handler.read_csv()
    cleaned_data, initial_missing, removed_missing = csv_handler.clean_data(data)
    summary = csv_handler.summarize_cleaning(initial_missing, removed_missing)

# Print the summary
    print(summary)
    print(cleaned_data)

