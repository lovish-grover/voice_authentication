# audio_processing.py
from pydub import AudioSegment
from audiomentations import AddGaussianNoise, PitchShift, TimeStretch
import librosa
import soundfile as sf

def split_and_augment(audio_file, prefix):
    # Load and split audio into 3-second segments
    audio = AudioSegment.from_file(audio_file)
    segment_length = 3000  # 3 seconds in milliseconds
    segments = [audio[i:i + segment_length] for i in range(0, len(audio), segment_length)]
    
    # Save original segments
    original_files = []
    for i, segment in enumerate(segments):
        file_path = f"{prefix}_segment_{i}.wav"
        segment.export(file_path, format="wav")
        original_files.append(file_path)
    
    # Define individual augmentation transformations
    augmentations = [
        AddGaussianNoise(min_amplitude=0.01, max_amplitude=0.015, p=1.0),  # Noise only
        PitchShift(min_semitones=-2, max_semitones=-1, p=1.0),            # Pitch down
        PitchShift(min_semitones=1, max_semitones=2, p=1.0),              # Pitch up
        TimeStretch(min_rate=0.9, max_rate=0.95, p=1.0),                  # Slow down
        TimeStretch(min_rate=1.05, max_rate=1.1, p=1.0),                  # Speed up
        AddGaussianNoise(min_amplitude=0.005, max_amplitude=0.01, p=1.0), # Light noise
    ]
    
    # Apply augmentations to each segment
    augmented_files = []
    for i in range(len(segments)):
        audio_data, sr = librosa.load(f"{prefix}_segment_{i}.wav", sr=16000)
        for j, aug in enumerate(augmentations):
            augmented_audio = aug(samples=audio_data, sample_rate=sr)
            aug_file = f"{prefix}_augmented_segment_{i}_aug{j}.wav"
            sf.write(aug_file, augmented_audio, sr)
            augmented_files.append(aug_file)
    
    return original_files + augmented_files

if __name__ == "__main__":
    # Test the function
    files = split_and_augment("input_audio.wav", "target")
    print(f"Total files generated: {len(files)}")