import wave

def bin_to_wav(bin_file, wav_file):
    with open(bin_file, 'rb') as f:
        data = f.read()

    with wave.open(wav_file, 'wb') as wf:
        wf.setnchannels(1)  # 单声道
        wf.setsampwidth(2)  # 采样宽度为2字节（16位）
        wf.setframerate(88200)  # 采样率为44100Hz
        wf.writeframes(data)

bin_file = 'input.wav'
wav_file = 'output.wav'
bin_to_wav(bin_file,wav_file)