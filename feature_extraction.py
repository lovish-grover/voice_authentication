# feature_extraction.py
import numpy as np
import librosa

def extract_features(file_path, sr=16000, n_mfcc=40, n_chroma=36):  # Increased n_mfcc to 40, n_chroma to 36
    audio, sr = librosa.load(file_path, sr=sr)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr, n_chroma=n_chroma)  # Increased chroma bins
    chroma_mean = np.mean(chroma.T, axis=0)
    spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)
    spec_cent_mean = np.mean(spectral_centroid.T, axis=0)
    spec_roll_mean = np.mean(spectral_rolloff.T, axis=0)
    features = np.concatenate([mfcc_mean, chroma_mean, spec_cent_mean, spec_roll_mean])
    return features