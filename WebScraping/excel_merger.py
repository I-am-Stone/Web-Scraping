import pandas as pd
from pathlib import Path

class ExcelFileMerger:

    def __init__(self, old_file_path: str, new_file_path: str):

        """
        Initialize the merger with paths to old and new Excel files.
        
        Args:
            old_file_path (str): Path to the old Excel file
            new_file_path (str): Path to the new Excel file
        """


        self.old_file_path = Path(old_file_path)
        self.new_file_path = Path(new_file_path)
        
        if not self.old_file_path.exists():
            raise FileNotFoundError(f"Old file not found: {old_file_path}")
        if not self.new_file_path.exists():
            raise FileNotFoundError(f"New file not found: {new_file_path}")

    def clean_course_name(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'Course Name' in df.columns:
            df['Course Name'] = df['Course Name'].str.split("(").str[0].str.strip()
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
            df_old = pd.read_excel(self.old_file_path, engine='openpyxl')
            df_new = pd.read_excel(self.new_file_path, engine='openpyxl')
            
            df_new = self.clean_course_name(df_new)
            
            duplicates = df_old[df_old.index.duplicated()]
            if not duplicates.empty:
                print("Warning: Duplicates found in old file:")
                print(duplicates)
            
            df_new = df_new.set_index('Course Website')
            df_old = df_old.set_index('Course Website')
            df_new.dropna(how="all", inplace=True)
            df_old.update(df_new)
            final_df = df_old.reset_index()

            output_dir = Path('merger_file')
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / output_path
            
            final_df.to_excel('merger_file/'+ output_path, engine='openpyxl', index=False)
            print(f"Merged file saved successfully to: {output_path}")
            
            return final_df
            
        except Exception as e:
            raise Exception(f"Error during file merger: {str(e)}")

if __name__ == "__main__":
    merger = ExcelFileMerger(
        old_file_path="/home/stone/Downloads/Griffith University update23 AUS (2024).xlsx",
        new_file_path="WebScraping/excle_file/Griffith Univeristy 2025.xlsx"
    )
    merged_df = merger.merge_files("Griffith University 2025 merged.xlsx")