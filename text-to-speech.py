#!/usr/bin/env python3
import os
import sys
import ffmpeg
import string

# speak stuff
speak_rate = 1.3


def synthesize_text(text, client):
  """Synthesizes speech from the input string of text."""

  # input format
  input_text = texttospeech.SynthesisInput(text=text)

  # Note: the voice can also be specified by name.
  # Names of voices can be retrieved with client.list_voices().
  voice = texttospeech.VoiceSelectionParams(
    language_code='en-GB',
    name='en-GB-Studio-B')

  audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.OGG_OPUS,
    speaking_rate=speak_rate)

  response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config})

  return response.audio_content


def write_to_file(audio, name):
    # The response's audio_content is binary.
    if not os.path.exists('RAW'):
      os.makedirs('RAW')
    os.chdir('RAW')
    with open(str(name) + '.ogg', 'wb') as out:
      print('Audio content written to file', name)
      out.write(audio)

def concat_oggs(oggs, output):
    input_args = []
    for ogg in oggs:
      input_args.append(ffmpeg.input(ogg))
    ffmpeg.concat(*input_args, v=0, a=1).output(output).run()

def trim_to_nearest_punctuation(input_str):
    # Set of punctuation marks
    punctuation_set = set(string.punctuation)

    # Iterate through the characters to find the nearest punctuation
    for i, char in enumerate(input_str):
        if char in punctuation_set:
            return input_str[:i]

    # If no punctuation is found, return the original string
    return input_str

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

  # open text file as a list of lines
  with open("text.txt") as f:
    content = f.readlines()

  # remove whitespace characters like `\n` at the end of each line
  content = [x.strip() for x in content]

  # remove empty lines
  content = [x for x in content if len(x) > 0]

  # download every line of text into a numbered ogg
  oggsname=[]
  title=trim_to_nearest_punctuation(content[0])
  if not os.path.exists(title):
    os.makedirs(title)
  os.chdir(title)
  for i, line in enumerate(content):
    audio = synthesize_text(line, client)
    write_to_file(audio, str(i))
    oggsname.append(str(i) + '.ogg')
  concat_oggs(oggsname, title+'.ogg')
