import librosa
import numpy as np
from PIL import Image
import librosa.display

def mel_spectrogram_to_image(mel_spectrogram):
    # Normalize to 0-255
    mel_spectrogram -= np.min(mel_spectrogram)
    mel_spectrogram /= np.max(mel_spectrogram)
    mel_spectrogram *= 255
    mel_spectrogram = np.uint8(mel_spectrogram)

    # Convert to PIL image
    image = Image.fromarray(mel_spectrogram)

    return image

def compute_mel_spectrogram(wav_file, n_fft=2048, hop_length=512, n_mels=128):
    # Load audio file
    y, sr = librosa.load(wav_file, sr=None)

    # Compute Mel spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)

    # Convert to decibels
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

    return mel_spectrogram_db
def test_mel():
    # Example usage
    wav_file = 'example.wav'
    mel_spectrogram = compute_mel_spectrogram(wav_file)
    print(mel_spectrogram.shape)  # Print the shape of the computed Mel spectrogram
