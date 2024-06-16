from openai import AzureOpenAI
from typing import List


class LLM:
    def __init__(self, api_key: str, endpoint: str, api_version: str, model: str):
        self.client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=endpoint)
        self.model = model

    def invoke(self, system_content: str, user_content: str, temperature: float, num_samples: int) -> List[str]:
        """ Returns <num_samples> text responses"""
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
        response = self.client.chat.completions.create(model=self.model, messages=messages, temperature=temperature,
                                                       max_tokens=2048, n=num_samples)

        assert len(response.choices) == num_samples, 'Different number of samples generated'
        outputs = [choices.message.content for choices in response.choices]
        return outputs
