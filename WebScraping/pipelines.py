# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
from pathlib import Path
from datetime import datetime
import os
from typing import List, Dict, Any
import logging


class MergercrapingPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
       
        output_dir = Path('WebScraping/excle_file')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{spider.file_name}.xlsx"
        
        try:
            # Save to Excel
            df.to_excel(output_file, index=False)
            print("----------------------------------------")
            print("Item exported successfully to:", output_file)
            print("----------------------------------------")
        except Exception as e:
            print(f"Failed to save Excel file: {e}")


class WebscrapingPipeline:
    """
    Pipeline for processing the siper items and exporting data in excel
    """
    def __init__(self):
        self.items:list[Dict[Any,Any]] = []
        self.logger = logging.getLogger(__name__)

        self.all_columns = [
            'Course_Website', 'Course_Name', 'Course_Description', 'Career',
            'City', 'International_Fee', 'Domestic_fee', 'Currency',
            'Intake_Month', 'Apply_Month', 'Study_Load', 'Duration_Term',
            'Fee_Term', 'Duration', 'Study_mode', 'Course_Structure',
            'Other_Requriment', 'Category', 'Sub_Category', 'Apply_Day',
            'Fee_Year', 'Intake_Day', 'Language', 'Degree_level',
            'Domestic_only', 'Other_Test', 'Academic_Score', 'Score_Type',
            'Academic_Country', 'Score', 'Scholarship',
            'IELTS_Overall', 'IELTS_Reading', 'IELTS_Writing', 'IELTS_Speaking', 'IELTS_Listening',
            'TOEFL_Overall', 'TOEFL_Reading', 'TOEFL_Writing', 'TOEFL_Speaking', 'TOEFL_Listening',
            'PTE_Overall', 'PTE_Reading', 'PTE_Writing', 'PTE_Speaking', 'PTE_Listening'
        ]
        self.exporting_file =Path("WebScraping/excle_file")
        self.exporting_file.mkdir(parents=True, exist_ok=True)

    def process_item(self, item:Dict[str,Any], spider) -> Dict[str,Any]:
        """
        Here we process each item and add to columans
        """
        try:
            item_dict = dict(ItemAdapter(item))
            for columan in self.all_columns:
                if columan not in item_dict:
                    item_dict[columan] = None
            self.items.append(item_dict)
            self.logger.debug(f"Successfully processed item: {item_dict.get('Course_Name', 'Unknown Course')}")

        except Exception as e:
            self.logger.error(f"Error processing item: {str(e)}")
        
        return item


    def close_spider(self, spider):
        """
        This exports data to excel
        """
        try:
            df = pd.DataFrame(self.items, columns=self.all_columns)

            if 'Course_Name' in df.columns:
                df.sort_values(by="Course_Name", axis=0, inplace=True, ascending=True)
            
            filename = f"{spider.file_name}.xlsx"
            filepath = os.path.join(self.exporting_file, filename)

            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(
                    writer,
                    index=False,
                    sheet_name='course',
                )
            self.logger.info(f"""
            ----------------------------------------
            Export Successful:
            - Total items: {len(df)}
            - Columns: {len(df.columns)}
            - File: {filename}
            ----------------------------------------
            """)

        except Exception as e:
            self.logger.error(f"""
            ----------------------------------------
            return statistics about the exported data.""")
        return {
            'total_items': len(self.items),
            'total_columns': len(self.all_columns),
            'non_null_values': sum(1 for item in self.items if any(item.values()))
        }
    def get_export_stats(self) -> Dict[str, int]:
        """Return statistics about the exported data."""
        return {
            'total_items': len(self.items),
            'total_columns': len(self.all_columns),
            'non_null_values': sum(1 for item in self.items if any(item.values()))
        }

    
