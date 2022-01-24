#!/usr/bin/env python3
import os
import argparse
import playsound
import time

# speak stuff
speak_rate = 1.2


def synthesize_text(text, client):
  """Synthesizes speech from the input string of text."""

  # input format
  input_text = texttospeech.SynthesisInput(text=text)

  # Note: the voice can also be specified by name.
  # Names of voices can be retrieved with client.list_voices().
  voice = texttospeech.VoiceSelectionParams(
      language_code='en-US',
      ssml_gender=texttospeech.SsmlVoiceGender.MALE)

  audio_config = texttospeech.AudioConfig(
      audio_encoding=texttospeech.AudioEncoding.MP3,
      speaking_rate=speak_rate)

  response = client.synthesize_speech(
      request={"input": input_text, "voice": voice, "audio_config": audio_config})

  return response.audio_content


def play_mp3(audio):
  # The response's audio_content is binary. Write to temp
  name = '/tmp/temp.mp3'
  with open(name, 'wb') as out:
    print('Audio content written to file', name)
    out.write(audio)
  # play
  p = playsound.playsound(name)


if __name__ == '__main__':

  parser = argparse.ArgumentParser("./say.py")
  parser.add_argument(
      '-t', '--text',
      type=str,
      required=False,
      default="This is the default text. For other text use the minus t option.",
      help='Text to speak. Defaults to "%(default)s"',
  )
  FLAGS, unparsed = parser.parse_known_args()

  # print summary of what we will do
  print("----------")
  print("Saying: ", FLAGS.text)
  print("----------\n")

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

  # get mp3 from google cloud
  audio = synthesize_text(FLAGS.text, client)

  # play
  play_mp3(audio)
