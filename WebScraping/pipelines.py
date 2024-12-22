# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd

class WebscrapingPipeline:
    def __init__(self):
        self.items= []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        try:
            df.sort_values(by="Course_Name", axis=0,
                           inplace=True, ascending=True)
        except:
            print("error")      
        df.to_excel("excle_file/" + spider.file_name +  # "v1" +
                        ".xlsx", index=False)
        print("----------------------------------------")
        print("Item exported sucessfully")
        print("----------------------------------------")



# from itemadapter import ItemAdapter
# import pandas as pd
# from datetime import datetime
# import os
# from typing import List, Dict, Any
# import logging

# class SpiderPipeline:
#     """Pipeline for processing spider items and exporting to Excel."""
    
#     def __init__(self):
#         """Initialize the pipeline with required attributes."""
#         self.items: List[Dict[Any, Any]] = []
#         self.logger = logging.getLogger(__name__)
        
#         # Define all possible columns to ensure they're included even if empty
#         self.all_columns = [
#             'Course_Website', 'Course_Name', 'Course_Description', 'Career',
#             'City', 'International_Fee', 'Domestic_fee', 'Currency',
#             'Intake_Month', 'Apply_Month', 'Study_Load', 'Duration_Term',
#             'Fee_Term', 'Duration', 'Study_mode', 'Course_Structure',
#             'Other_Requriment', 'Category', 'Sub_Category', 'Apply_Day',
#             'Fee_Year', 'Intake_Day', 'Language', 'Degree_level',
#             'Domestic_only', 'Other_Test', 'Academic_Score', 'Score_Type',
#             'Academic_Country', 'Score', 'Scholarship',
#             # Language test scores
#             'IELTS_Overall', 'IELTS_Reading', 'IELTS_Writing', 'IELTS_Speaking', 'IELTS_Listening',
#             'TOEFL_Overall', 'TOEFL_Reading', 'TOEFL_Writing', 'TOEFL_Speaking', 'TOEFL_Listening',
#             'PTE_Overall', 'PTE_Reading', 'PTE_Writing', 'PTE_Speaking', 'PTE_Listening'
#         ]
        
#         # Ensure export directory exists
#         self.export_dir = "excel_file"
#         os.makedirs(self.export_dir, exist_ok=True)

#     def process_item(self, item: Dict[str, Any], spider) -> Dict[str, Any]:
#         """Process each item and add it to the items list."""
#         try:
#             # Convert item to dict if it's not already
#             item_dict = dict(ItemAdapter(item))
            
#             # Ensure all columns exist in the item
#             for column in self.all_columns:
#                 if column not in item_dict:
#                     item_dict[column] = None
                    
#             self.items.append(item_dict)
#             self.logger.debug(f"Successfully processed item: {item_dict.get('Course_Name', 'Unknown Course')}")
            
#         except Exception as e:
#             self.logger.error(f"Error processing item: {str(e)}")
            
#         return item

#     def close_spider(self, spider) -> None:
#         """
#         Handle spider closure by creating and exporting DataFrame to Excel.
#         Includes error handling and data validation.
#         """
#         try:
#             # Create DataFrame with all columns initialized
#             df = pd.DataFrame(self.items, columns=self.all_columns)
            
#             # Sort by Course_Name if it exists
#             if 'Course_Name' in df.columns:
#                 df.sort_values(by="Course_Name", axis=0, inplace=True, ascending=True)
            
#             # Generate filename with timestamp
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"{spider.file_name}_{timestamp}.xlsx"
#             filepath = os.path.join(self.export_dir, filename)
            
#             # Export to Excel with optimized settings
#             with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
#                 df.to_excel(
#                     writer,
#                     index=False,
#                     sheet_name='Course Data',
#                     float_format="%.2f"  # Format floating-point numbers
#                 )
                
#                 # Auto-adjust column widths
#                 worksheet = writer.sheets['Course Data']
#                 for idx, col in enumerate(df.columns):
#                     max_length = max(
#                         df[col].astype(str).apply(len).max(),
#                         len(str(col))
#                     ) + 2
#                     worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
            
#             # Log success
#             self.logger.info(f"""
#             ----------------------------------------
#             Export Successful:
#             - Total items: {len(df)}
#             - Columns: {len(df.columns)}
#             - File: {filename}
#             ----------------------------------------
#             """)
            
#         except Exception as e:
#             self.logger.error(f"""
#             ----------------------------------------
#             Export Failed:
#             - Error: {str(e)}
#             - Items: {len(self.items)}
#             ----------------------------------------
#             """)
#             raise

#     def get_export_stats(self) -> Dict[str, int]:
#         """Return statistics about the exported data."""
#         return {
#             'total_items': len(self.items),
#             'total_columns': len(self.all_columns),
#             'non_null_values': sum(1 for item in self.items if any(item.values()))
#         }