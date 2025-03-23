import random

from google.cloud import texttospeech

from gcp_tools.credentials import get_credentials


class TTS:
    def __init__(self, service_account: str | dict = None):
        service_account_credentials = get_credentials(service_account)
        if service_account_credentials:
            self.tts_client = texttospeech.TextToSpeechClient(credentials=service_account_credentials)
        else:
            self.tts_client = texttospeech.TextToSpeechClient()

        self.lang_dict = {
            "en": "en-US",
            "ko": "ko-KR",
            "cn": "cmn-CN",
            "en-AU": "en-AU",
        }

        self.voice_dict = {
            "en": {
                "male": [
                    "Journey-D",
                ],
                "female": [
                    "Journey-F",
                    "Journey-O",
                ],
            },
            "ko": {
                "male": [
                    "Wavenet-C"
                ],
                "female": [
                    "Wavenet-B"
                ],
            },
            "cn": {
                "male": [
                    "Chirp3-HD-Charon"
                ],
                "female": [
                    "Chirp3-HD-Aoede"
                ],
            },
            "en-AU": {
                "male": [
                    "Chirp-HD-D"
                ],
                "female": [
                    "Chirp-HD-F",
                    "Chirp-HD-O"
                ],
            }
        }

        for lang in self.voice_dict:
            for gender in self.voice_dict[lang]:
                random.shuffle(self.voice_dict[lang][gender])

    def get_voice_config(self, lang, gender):
        language_code = self.lang_dict[lang]
        voice_id = self.voice_dict[lang][gender][0]
        voice_name = f"{language_code}-{voice_id}"
        voice_config = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )

        return voice_config

    def get_audio_config(self):
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        return audio_config

    def generate_voice(self, text, lang, gender):
        input_text = texttospeech.SynthesisInput(text=text)
        voice = self.tts_client.synthesize_speech(request={
            "input": input_text,
            "voice": self.get_voice_config(lang, gender),
            "audio_config": self.get_audio_config(),
        })
        return voice.audio_content
