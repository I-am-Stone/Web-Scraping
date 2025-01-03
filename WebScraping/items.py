# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re
from typing import Optional, Union

class TextCleaner:
    @staticmethod
    def clean_base(value: Optional[str]) -> Optional[str]:
        """Base cleaning function for text values."""
        if value is None:
            return None
        return re.sub(r'^\s+|\s+$', '', value.replace('\xa0', ' '))
    
    @staticmethod
    def clean_html(value: Optional[str]) -> Optional[str]:
        """Remove HTML tags and clean whitespace."""
        if value is None:
            return None
        return TextCleaner.clean_base(remove_tags(value))
    
    @staticmethod
    def remove_numbers(value: Optional[str]) -> Optional[str]:
        """Remove numeric characters from text."""
        if value is None:
            return None
        return re.sub(r'\d+', '', value)

class DurationProcessor:
    DURATION_MAPPING = {
        'years': 'Year',
        'year': 'Year',
        'Year': 'Year',
        'months': 'Month',
        'Weeks': 'Week',
        'day': 'Day',
        'hours': 'Hour',
        'semester': 'Semester'
    }
    
    @staticmethod
    def process_term(value: Optional[str]) -> str:
        """Process duration term with simplified logic."""
        if not value:
            return ""
        value = TextCleaner.clean_base(value)
        for key, mapped_value in DurationProcessor.DURATION_MAPPING.items():
            if key in value:
                return mapped_value
        return ""
    
    @staticmethod
    def clean_duration(value: Optional[str]) -> Optional[str]:
        """Clean and format duration values."""
        if not value:
            return None
            
        value = value.replace('2025 tuition fee', '').replace('120 points', '').replace('180 points', '').replace('140 points', '')
        
        numbers = re.findall(r'\d+\.*\d*', value)
        if not numbers:
            return None
            
        if ' - ' in value or 'to' in value:
            return f"{numbers[0]} to {numbers[1]}" if len(numbers) >= 2 else numbers[0]
            
        return numbers[0]

class FeeProcessor:
    @staticmethod
    def clean_fee(value: Optional[str]) -> Optional[str]:
        """Extract and clean fee values."""
        if not value:
            return None
        total = None
        value = value.replace('2025', '')
        numbers = re.findall(r'\d+,*\d*', value)

        if len(numbers) > 1:
            total = int(numbers[0]) * int(numbers[1])
       
        duration_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:year|yr)', value, re.IGNORECASE)

        if duration_match:
            duration = float(duration_match.group(1))
            total = total/duration
            
        print(total)
        return total if total else None

class WebscrapingItem(scrapy.Item):
    # Basic course information
    Course_Website = scrapy.Field()
    Course_Name = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html, str.title),
        output_processor=TakeFirst()
    )
    Course_Description = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html),
        output_processor=TakeFirst()
    )
    
    # Location and career info
    Career = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_base),
        output_processor=TakeFirst()
    )
    City = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html, lambda x: x.replace('Distance Learning', '')),
        output_processor=TakeFirst()
    )
    
    # Fee information
    International_Fee = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html, FeeProcessor.clean_fee),
        output_processor=TakeFirst()
    )
    Domestic_fee = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html, FeeProcessor.clean_fee),
        output_processor=TakeFirst()
    )
    Currency = scrapy.Field()
    Fee_Term = scrapy.Field()
    Fee_Year = scrapy.Field()
    
    # Duration and schedule
    Duration = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html, DurationProcessor.clean_duration),
        output_processor=TakeFirst()
    )
    Duration_Term = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html, TextCleaner.remove_numbers, DurationProcessor.process_term),
        output_processor=TakeFirst()
    )
    Study_Load = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html, TextCleaner.remove_numbers),
        output_processor=TakeFirst()
    )
    Study_mode = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html),
        output_processor=TakeFirst()
    )
    
    # Intake information
    Intake_Month = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html, TextCleaner.remove_numbers),
        output_processor=TakeFirst()
    )
    Intake_Day = scrapy.Field()
    Apply_Month = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html, TextCleaner.remove_numbers),
        output_processor=TakeFirst()
    )
    Apply_Day = scrapy.Field()
    
    # Language test scores
    for test in ['IELTS', 'TOEFL', 'PTE']:
        for component in ['Overall', 'Reading', 'Writing', 'Speaking', 'Listening']:
            locals()[f"{test}_{component}"] = scrapy.Field(
                input_processor=MapCompose(TextCleaner.clean_html),
                output_processor=TakeFirst()
            )
    
    # Additional fields
    Course_Structure = scrapy.Field(input_processor=MapCompose(TextCleaner.clean_base))
    Other_Requriment = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_base),
        output_processor=TakeFirst()
    )
    Category = scrapy.Field()
    Sub_Category = scrapy.Field()
    Language = scrapy.Field()
    Degree_level = scrapy.Field()
    Domestic_only = scrapy.Field()
    Other_Test = scrapy.Field()
    Academic_Score = scrapy.Field()
    Score_Type = scrapy.Field()
    Academic_Country = scrapy.Field()
    Score = scrapy.Field()
    Scholarship = scrapy.Field()