import IPython.display as ipd
import librosa
import librosa.display
import matplotlib.pyplot as plt


def get_sound_data(music):
    ipd.Audio(music)
    plt.figure(figsize=(15, 4))
    data = librosa.load(music,
                        sr=22050,
                        mono=True,
                        offset=0.0,
                        duration=50,
                        res_type='kaiser_best')
    return data
