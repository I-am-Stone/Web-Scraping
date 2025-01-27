import pandas as pd
from pathlib import Path


class ExcelFileMerger:

    def __init__(self, old_file: str, new_file: str):
        """
        Initialize the merger with paths to old and new Excel files.

        Args:
            old_file (str): Path to the old Excel file
            new_file (str): Path to the new Excel file
        """

        self.old_file = Path(old_file)
        self.new_file = Path(new_file)

        if not self.old_file.exists():
            raise FileNotFoundError(f"Old file not found: {old_file}")
        if not self.new_file.exists():
            raise FileNotFoundError(f"New file not found: {new_file}")

    def clean_course_name(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean up course names in the DataFrame by removing the part after the first open parenthesis.

        Args:
            df (pd.DataFrame): The DataFrame containing the course names to clean

        Returns:
            pd.DataFrame: The DataFrame with the cleaned course names
        """
        course_name_column = 'Course Name'
        if course_name_column in df.columns:
            df[course_name_column] = df[course_name_column].str.split("(").str[0].str.strip()
        return df


    def merge_files(self, output_path: str = "merged_output.xlsx") -> pd.DataFrame:
        """
        Merge the old and new Excel files.

        Args:
            output_path (str): Path where the merged file will be saved

        Returns:
            pd.DataFrame: Merged and processed DataFrame
        """
        try:
            old_df = pd.read_excel(self.old_file_path, engine="openpyxl")
            new_df = pd.read_excel(self.new_file_path, engine="openpyxl")
            new_df = self.clean_course_name(new_df)

            if new_df.index.duplicated().any():
                raise ValueError("Duplicates found in new file")

            merged_df = old_df.set_index("Course Website").combine_first(
                new_df.set_index("Course Website")
            ).reset_index()

            output_dir = Path("merger_file")
            output_dir.mkdir(exist_ok=True)

            output_file = output_dir / output_path

            merged_df.to_excel(output_file, engine="openpyxl", index=False)

            return merged_df

        except Exception as e:
            raise Exception(f"Error during file merger: {str(e)}")


if __name__ == "__main__":
    merger = ExcelFileMerger(
        old_file_path="/home/stone/Downloads/Swinburne University of Technology - 2024.xlsx",
        new_file_path="WebScraping/excle_file/Swinburne University 2025 data.xlsx",
    )
    merged_df = merger.merge_files("Swinburne University 2025 merged v2.xlsx")
