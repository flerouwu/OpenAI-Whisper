import whisper
import sounddevice as sd
from pydub import AudioSegment
from pydub.silence import split_on_silence
import numpy as np
import config
from scipy.io.wavfile import write as WAVWrite


def record_audio(device_index: int = 0):
    recording = []
    silence_counter = 0

    def callback(indata, frames, time, status):
        nonlocal recording, silence_counter
        if status:
            print(status)

        volume_norm = np.linalg.norm(indata) * 10
        print(
            f"Volume Normal: {volume_norm}. {volume_norm < config.silence_threshold}. {config.silence_threshold}"
        )
        if volume_norm < config.silence_threshold:
            silence_counter += 1
        else:
            silence_counter = 0

        recording.append(indata.copy())  # append a copy of indata to recording

    with sd.InputStream(
        channels=2,
        samplerate=config.sample_rate,
        blocksize=config.blocksize,
        device=device_index,
        callback=callback,
    ):
        while silence_counter < config.max_silent_frames:
            pass

    return np.concatenate(recording)


if __name__ == "__main__":
    #############################
    ## PROCESS AUDIO RECORDING ##
    #############################

    # start recording
    print("Recording...")
    recording = record_audio(device_index=config.microphone_device)
    print("Done recording.")

    # save recording
    print("Saving recording...")
    WAVWrite("recording.wav", config.sample_rate, recording)
    print("Done saving recording.")

    # start transcribing
    print("Transcribing...")
    model = whisper.load_model("small")
    audio = whisper.load_audio("recording.wav", sr=config.sample_rate)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")  # type: ignore

    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    print("Done transcribing.")

    # print result
    print(f"Result: {result}")
