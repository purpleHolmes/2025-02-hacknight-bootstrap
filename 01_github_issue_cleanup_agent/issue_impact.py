from openai import OpenAI
import os
from typing import Optional

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_infra_impact(issue_title: str) -> Optional[str]:
    """Analyze the infrastructure impact of an issue based on its title.
    
    Args:
        issue_title (str): The title of the issue to analyze
        
    Returns:
        Optional[str]: Analysis of infrastructure impact, or None if unable to analyze
    """
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert at analyzing infrastructure impact from GitHub issues. 
                              Analyze the issue title 3 things
                                1. Is this issue critical, with reason ?
                                2. Is this issue a feature request or a bug report?
                                3. What is the impact of this issue on the infrastructure ?
                                4. What could be the cause of this issue ?    
                        """
                },
                {
                    "role": "user",
                    "content": f"Please analyze the issue title: {issue_title}"
                }
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error analyzing infrastructure impact: {str(e)}")
        return None
