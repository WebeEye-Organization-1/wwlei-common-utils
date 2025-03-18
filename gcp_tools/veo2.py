import time
from enum import Enum

from google import genai
from google.genai import types
from google.oauth2.service_account import Credentials
from credentials import get_credentials


class Veo2:
    class AspectRatio(Enum):
        RATIO_16_9 = "16:9"
        RATIO_9_16 = "9:16"

    class NumberOfVideos(Enum):
        ONE = 1
        FOUR = 4

    class DurationSeconds(Enum):
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8

    class PersonGeneration(Enum):
        DONT_ALLOW = 'dont_allow'
        ALLOW_ADULT = 'allow_adult'

    def __init__(self, project_id, location, bucket,
                 service_account: str | dict = None,
                 video_model='veo-2.0-generate-001'):
        self.video_model = video_model
        self.bucket = bucket
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        credentials = get_credentials(service_account, scopes)
        if credentials:
            self.client = genai.Client(vertexai=True, project=project_id, location=location,
                                       credentials=credentials)
        else:
            self.client = genai.Client(vertexai=True, project=project_id, location=location)

    def generate_video_from_text(self, prompt,
                                 aspect_ratio: AspectRatio = AspectRatio.RATIO_16_9,
                                 number_of_videos: NumberOfVideos = NumberOfVideos.ONE,
                                 duration_seconds: DurationSeconds = DurationSeconds.EIGHT,
                                 person_generation: PersonGeneration = PersonGeneration.DONT_ALLOW):
        operation = self.client.models.generate_videos(
            model=self.video_model,
            prompt=prompt,
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
                output_gcs_uri=self.bucket,
                number_of_videos=number_of_videos,
                duration_seconds=duration_seconds,
                person_generation=person_generation,
                enhance_prompt=True,
            ),
        )

        while not operation.done:
            time.sleep(10)
            operation = self.client.operations.get(operation)

        if operation.response:
            if operation.result.generated_videos:
                return [r.video.uri for r in operation.result.generated_videos]
            else:
                raise Exception(operation.result.rai_media_filtered_reasons)
        else:
            raise Exception(f'operation failed')

    def generate_video_from_image(self,
                                  prompt: str = None,
                                  image_path: str = None,
                                  image_bytes: str = None,
                                  image_type: str = None,
                                  aspect_ratio: AspectRatio = AspectRatio.RATIO_16_9,
                                  number_of_videos: NumberOfVideos = NumberOfVideos.ONE,
                                  duration_seconds: DurationSeconds = DurationSeconds.EIGHT,
                                  person_generation: PersonGeneration = PersonGeneration.ALLOW_ADULT):
        if image_bytes:
            image = types.Image(image_bytes=image_bytes, mime_type=image_type)
        else:
            image = types.Image.from_file(location=image_path)

        operation = self.client.models.generate_videos(
            model=self.video_model,
            prompt=prompt,
            image=image,
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
                output_gcs_uri=self.bucket,
                number_of_videos=number_of_videos,
                duration_seconds=duration_seconds,
                person_generation=person_generation,
            ),
        )

        while not operation.done:
            time.sleep(10)
            operation = self.client.operations.get(operation)

        if operation.response:
            if operation.result.generated_videos:
                return [r.video.uri for r in operation.result.generated_videos]
            else:
                raise Exception(operation.result.rai_media_filtered_reasons)
        else:
            raise Exception(f'operation failed')
