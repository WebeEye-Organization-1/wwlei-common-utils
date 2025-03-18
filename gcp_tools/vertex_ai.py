import json
from typing import List

import vertexai
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig

from credentials import get_credentials
from https_tools.media_tools import get_mime_type


class VertexAIGemini:

    def __init__(self,
                 project: str,
                 location: str,
                 model_name: str,
                 service_account: str | dict = None,
                 response_schema=None):
        service_account_credentials = get_credentials(service_account)
        if service_account_credentials:
            aiplatform.init(project=project, location=location, credentials=service_account_credentials)
            vertexai.init(project=project, location=location, credentials=service_account_credentials,
                          api_transport="rest")
        else:
            aiplatform.init(project=project, location=location)
            vertexai.init(project=project, location=location, api_transport="rest")

        self.gemini_model = GenerativeModel(model_name=model_name)
        self.response_schema = response_schema

    def generate_content(self,
                         prompt: str,
                         images_path: List = None,
                         video_path: str = None
                         ) -> dict[str, str]:
        contents = []
        contents.append(prompt)
        if video_path:
            contents.append(Part.from_uri(video_path, mime_type="video/mp4"))
        if images_path:
            contents.extend([Part.from_uri(i, mime_type=get_mime_type(i)) for i in images_path])
        response = self.gemini_model.generate_content(
            contents,
            generation_config=GenerationConfig(response_mime_type="application/json",
                                               response_schema=self.response_schema)
        )
        replace = response.text.replace("```json", "").replace("```", "")
        try:
            loads = json.loads(replace)
            return loads
        except Exception as e:
            raise Exception(e)
