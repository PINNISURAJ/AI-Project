import sounddevice as sd
from scipy.io.wavfile import write

def record_admin_voice(filename="admin_voice_sample.wav", duration=5, fs=44100):
    print("Recording admin's voice...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, recording)  # Save as WAV file
    print(f"Admin voice sample saved as {filename}")

# Record a 5-second voice sample
record_admin_voice()
