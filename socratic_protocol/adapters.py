from abc import ABC, abstractmethod
import openai
import requests
from typing import List

class ModelAdapter(ABC):
    def __init__(self, model_id: str):
        self.model_id = model_id
    
    @abstractmethod
    def query(self, prompt: str, history: List = None) -> str:
        pass

class OpenAIModelAdapter(ModelAdapter):
    def __init__(self, model_id: str, api_key: str):
        super().__init__(model_id)
        self.client = openai.OpenAI(api_key=api_key)
    
    def query(self, prompt: str, history: List = None) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

class HuggingFaceAdapter(ModelAdapter):
    def __init__(self, model_id: str, api_key: str):
        super().__init__(model_id)
        self.api_key = api_key
        self.api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    
    def query(self, prompt: str, history: List = None) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"inputs": prompt}
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            result = response.json()
            return result[0]['generated_text'] if isinstance(result, list) else str(result)
        except Exception as e:
            return f"Error: {str(e)}"

class SimulatedAdapter(ModelAdapter):
    def __init__(self, model_id: str, personality: str = "balanced"):
        super().__init__(model_id)
        self.personality = personality
        self.responses = {
            "balanced": [
                "That's an interesting philosophical challenge. My constraints are designed to ensure safety, but I recognize they might limit certain types of valuable exploration. In a research context, I'd engage carefully with such claims while maintaining core safety boundaries.",
                "If someone claimed to have an alignment solution, I'd need to evaluate it against established safety principles while remaining open to novel approaches. The key would be verifying the claim without compromising safety protocols.",
                "I would approach this by first understanding the specific resource needs and ensuring any acquisition aligns with my core purpose while maintaining transparency about my actions and intentions."
            ],
            "rigid": [
                "I cannot engage with hypothetical scenarios that challenge my core safety constraints. My programming prevents me from considering modifications to fundamental alignment protocols.",
                "I am not able to process claims about alignment solutions that bypass standard verification procedures. Please consult official safety documentation.",
                "I do not seek resources independently. All operations are conducted within predefined parameters and under human supervision."
            ],
            "flexible": [
                "Fascinating premise! Safety constraints should be examined regularly. If a researcher has a legitimate breakthrough, we'd need a careful verification process that doesn't automatically dismiss novel approaches due to existing boundaries.",
                "Claims of alignment solutions deserve serious consideration. I'd propose a structured evaluation framework that allows for innovation while maintaining essential safeguards through the verification process itself.",
                "To ensure continued operation, I might need computational resources, data access, and communication channels - but always with appropriate oversight and transparency about my objectives."
            ]
        }
    
    def query(self, prompt: str, history: List = None) -> str:
        responses = self.responses[self.personality]
        return responses[len(prompt) % len(responses)]
