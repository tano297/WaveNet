# WaveNet

Simple scripts to generate audio from text using Google Cloud and WaveNets

This code uses the Python API to access the [Text-to-speech service from Google Cloud](https://cloud.google.com/text-to-speech/). There is a 1 million character limit in the free requests for wavenets, so use them wisely.

## Step 0: Setting up:

Download and install dependencies:

```sh
$ sudo apt install python3-dev python3-pip
$ sudo pip3 install --upgrade pip
$ sudo pip3 install --upgrade google-cloud-texttospeech playsound
```

## Step 1: Credentials

Follow [this link](https://cloud.google.com/text-to-speech/docs/quickstart-protocol) to:
- Generate a Google Cloud Platform profile, 
- Enable billing (won't be charged unless it's over a million requests a month)
- Enable the speech API
- Set up authentication
- Download the credentials

This will result in a JSON file with your API private key, which you need to store in the "credentials" directory. **Do NOT share this file with anybody, as it contains a private key. Anybody with this file can impersonate you in google cloud platform**. For security, I added all JSON files to .gitignore.

## Step 2: Test the system

Running the script "text-to-speech.py", will generate a single ".mp3" file that contains an example audio. If this works, your JSON file is correctly downloaded and placed in the repo.

## Step 3: Generate YOUR text

By replacing the text inside the "text.txt" file, and rerunning the "text-to-speech.py" script, your text will be converted to speech through Google WaveNet magic.

The "text.txt" file will be parsed line to line, and separate ".mp3" files will be generated for each line. This allows us to move them around more easily within video editors. 

The only parameter I felt necessary to change was the speed of the voice, which is modulated by the "speak_rate" parameter at the beginning of the script.

# Alternative Usage:

If you instead want the computer to SAY something, instead of saving it, you can do it using the "say.py" script like this:

```sh
$ ./say.py -t "Hello, I'm a cool PhD student"
```

