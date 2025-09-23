import wave
import struct

def read_wav_as_float(path):
    wf = wave.open(path, 'rb')
    nchannels, sampwidth, framerate, nframes, comptype, compname = wf.getparams()
    data = wf.readframes(nframes)

    samples = []
    if sampwidth == 1:
        for i in range(0, len(data), nchannels):
            frame = []
            for c in range(nchannels):
                v = data[i + c]  
                x = (v - 128) / 128.0
                frame.append(x)
            samples.append(frame)
    else:
        for i in range(0, len(data), nchannels*2):
            frame = []
            for c in range(nchannels):
                off = i + 2 * c
                (val,) = struct.unpack_from('<h', data, off)  # -32768..32767
                x = val / 32768.0
                if x < -1.0:
                    x = -1.0
                if x > 1.0:
                    x = 1.0
                frame.append(x)
            samples.append(frame)
    return samples, framerate

def float_to_u8(x):
    q = int(round((x + 1.0) * 0.5 * 255.0))
    if q < 0: 
        q = 0
    if q > 255: 
        q = 255
    return q

def histogram_256(samples):
    nframes = len(samples)
    nch = len(samples[0]) if nframes else 1
    total = nframes * nch if nframes else 1
    counts = [0] * 256
    for frame in samples:
        for x in frame:
            q = float_to_u8(x)
            counts[q] += 1
    return {i: counts[i] / total for i in range(256)}

def quantize_to_u8(samples):
    q = []
    for frame in samples:
        q.append([float_to_u8(x) for x in frame])
    return q

def save_u8_wav(path, q_frames, samplerate):
    if not q_frames:
        nch = 1
        raw = b''
    else:
        nframes = len(q_frames)
        nch = len(q_frames[0])
        ba = bytearray()
        for i in range(nframes):
            for c in range(nch):
                v = q_frames[i][c]
                ba.append(v)
        raw = bytes(ba)

    wf = wave.open(path, 'wb')
    wf.setnchannels(nch)
    wf.setsampwidth(1)  
    wf.setframerate(samplerate)
    wf.writeframes(raw)
    wf.close()

if __name__ == "__main__":
    in_path = "python_elective/lesson_4/4_2_file_processing/input_data/sample-6s.wav"
    samples, sr = read_wav_as_float(in_path)  
    hist = histogram_256(samples)             
    q = quantize_to_u8(samples)               
    save_u8_wav("python_elective/lesson_4/4_2_file_processing/output_data/quantized.wav", q, sr) 
