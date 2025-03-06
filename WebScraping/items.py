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
    
class StudyLoadProcessor:
    study_laod_mapping = {
        'Part-time': 'Part Time',
        'part-time': 'Part Time',
        'Full-Time': 'Full Time',
        'full-time': 'Full Time',
    }

    @staticmethod
    def process_study_load(value: Optional[str]) -> str:
        study_load=[]
        """
        Process the study load value and map it to a corresponding formatted value.

        Args:
            value (Optional[str]): The study load value to process.

        Returns:
            str: The formatted study load value, or an empty string if no mapping is found.
        """

        if not value:
            return ""
        value = TextCleaner.clean_base(value[0])
        for key, mapped_value in StudyLoadProcessor.study_laod_mapping.items():
            if key in value:
                return study_load.append(mapped_value)
            if study_load:
                return ", ".join(study_load)

        return ""



class IntakeProcessor:
    
    Intake_Mapping = {
    'Feb': 'February',
    'February': 'February',
    'Jul': 'July',
    'July': 'July',
    'Jan': 'January',
    'January': 'January',
    'Mar': 'March',
    'March': 'March',
    'Apr': 'April',
    'April': 'April',
    'May': 'May',
    'Jun': 'June',
    'June': 'June',
    'Jul': 'July',
    'July': 'July',
    'Aug': 'August',
    'August': 'August',
    'Sep': 'September',
    'Sept': 'September',
    'September': 'September',
    'Oct': 'October',
    'October': 'October',
    'Nov': 'November',
    'November': 'November',
    'Dec': 'December',
    'December': 'December'
}
    @staticmethod
    def process_intake(value:Optional[str]) -> str:

        intakes = []
        """
        Process intake value and map it to a corresponding value from the Intake_Mapping dictionary.
        
        Args:
            value (Optional[str]): The intake value to process.
            
        Returns:
            str: The mapped value corresponding to the intake value.
        """
        if not value:
            return ""
        value = TextCleaner.clean_base(value[0])
        value = TextCleaner.remove_numbers(value[0])
        for key, mapped_value in IntakeProcessor.Intake_Mapping.items():
            if key in value:
                intakes.append(mapped_value)
        if intakes:
            return ", ".join(intakes)
        return ""

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
    def process_term(value: Optional[str]TypeError: to_unicode must receive bytes or str, got Selector
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

        # if len(numbers) > 1:
        #     total = int(numbers[0]) * int(numbers[1])
       
        # duration_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:year|yr)', value, re.IGNORECASE)

        # if duration_match:
        #     duration = float(duration_match.group(1))
        #     total = total/duration
            
        # print(total)
        return numbers[0] if numbers else None

class DegreeLevelProcessor:
    DEGREE_LEVEL_MAPPING = {
        'certificate': 'Certificate & Diploma',
        'Certificate': 'Certificate & Diploma',
        'diploma': 'Certificate & Diploma',
        'Diploma': 'Certificate & Diploma',
        'Bachelor': 'Bachelor',
        'BA': 'Bachelor',
        'BSc': 'Bachelor',
        'Undergraduate': 'Bachelor',
        'bachelor degree': 'Bachelor',
        'bachelor degree': 'Bachelor',
        'Master': 'Master',
        'master': 'Master',
        'master degree': 'Master', 
        'master degree': 'Master',    
        'MSc': 'Master',    
        'MA': 'Master',    
        'LLM': 'Master',    
        'Post Graduate': 'Master', 
        'graduate degree': 'Graduate Certificate & Diploma', 
        'graduate degree': 'Graduate Certificate & Diploma',    
        'graduate certificate': 'Graduate Certificate & Diploma',     
        'graduate certificate': 'Graduate Certificate & Diploma',
    }    
    @staticmethod
    def process_degree_level(value: Optional[str]) -> str:
        if not value:
            return ""
        value = TextCleaner.clean_base(value[0])
        for key, mapped_value in DegreeLevelProcessor.DEGREE_LEVEL_MAPPING.items():
            if key in value:
                return mapped_value
        return ""

class WebscrapingItem(scrapy.Item):
    # Basic course information
    Course_Website = scrapy.Field()
    Course_Name = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html),
        output_processor=TakeFirst()
    )
    Course_Description = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html),
        output_processor=TakeFirst()
    )
            item.add_value('Course_Description', course_description)
        item.add_value('Duration_Term', duration)
        item.add_value('Study_Load', duration)
        item.add_value('Career', carrer)
        item.add_value('International_Fee', inter_fee)
        item.add_value('Fee_Year', year)
        item.add_value('Fee_Term', term)
        item.add_value('Currency', currency)
        
    # Location and career info
    Career = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_base),
        output_processor=TakeFirst()
    )
    City = scrapy.Field(
        input_processor=MapCompose(TextCleaner.clean_html),
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
        input_processor=MapCompose(TextCleaner.clean_html),
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
    Degree_level = scrapy.Field(IntakeProcessor=MapCompose(TextCleaner.clean_base, DegreeLevelProcessor.process_degree_level))
    Domestic_only = scrapy.Field()
    Other_Test = scrapy.Field()
    Academic_Score = scrapy.Field()
    Score_Type = scrapy.Field()
    Academic_Country = scrapy.Field()
    Score = scrapy.Field()
    Scholarship = scrapy.Field()