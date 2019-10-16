#!/usr/bin/env python3

"""
This script can be used to generate an audio from a ssml text file using google cloud services.
More information on https://github.com/tano297/WaveNet
Example:
>> python ssml-to-speech.py ssml.txt
"""


import os
import sys

# get text file
text_file = sys.argv[1]

# speak stuff
speak_rate = 1.0


def synthesize_ssml(ssml, client):
    """Synthesizes speech from the input string of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    Example: <speak>Hello there.</speak>
    """
    input_text = texttospeech.types.SynthesisInput(ssml=ssml)
    print(input_text)
    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
      language_code='en-US',
      ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
    audio_config = texttospeech.types.AudioConfig(
      audio_encoding=texttospeech.enums.AudioEncoding.MP3,
      speaking_rate=speak_rate)
    response = client.synthesize_speech(input_text, voice, audio_config)
    return response.audio_content


def write_to_file(audio, name):
    # The response's audio_content is binary.
    with open(str(name) + '.mp3', 'wb') as out:
        print('Audio content written to file', name)
        out.write(audio)


if __name__ == '__main__':

  # get the credentials
  pwd = os.getcwd()
  credential = ""
  for f in os.listdir("./credentials/"):
    if ".json" in f:
      credential = f
  if credential == "":
    print("No credentials json found in 'credentials' dir")
    quit()
  else:
    credential = os.path.join(pwd, "credentials", credential)
    print("Found credential file", credential)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

  # open ssml file as a list of lines
  with open(text_file) as f:
    content = f.read()
  print(content)
  audio = synthesize_ssml(content, client)
  write_to_file(audio, text_file.split('.')[0])
