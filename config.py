# The device to record sound from. Run `python listDevices.py` to list devices and their indecies
# You should use the index of the device you want to record from.
microphone_device = 1

# The blocksize to use when recording the audio.
# Default: 4096
blocksize = 2048

# The sample rate to use when recording the audio.
# Default: 16000
sample_rate = 16000

# The maximum amount of silent frames before stopping the recording.
# Default: 10
max_silent_frames = 10

# The lowest volume to consider as silence.
# Default: 0.5
silence_threshold = 0.5
