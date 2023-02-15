import scipy.signal
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Load the WAV file and apply the filter
fs, data = scipy.io.wavfile.read('Cascada - Everytime We Touch (Official Video).wav')
cutoff_hz = 300
order = 4
nyquist_hz = 0.5 * fs
cutoff_norm = cutoff_hz / nyquist_hz
b, a = scipy.signal.butter(order, cutoff_norm, btype='low', analog=False)
filtered_data = scipy.signal.lfilter(b, a, data).astype(np.int16)

# Define the length and overlap of the sliding window
window_length_sec = 0.1
window_overlap_sec = 0.05
window_length = int(window_length_sec * fs)
window_overlap = int(window_overlap_sec * fs)

# Calculate the power of the filtered signal using a sliding window approach
power = []
for i in range(0, len(filtered_data)-window_length, window_overlap):
    window = filtered_data[i:i+window_length]
    power.append(np.sum(window ** 2) / window_length)

# Calculate the corresponding time values
time = np.arange(len(power)) * (window_length - window_overlap) / float(fs)

# Define a function to animate the video
def animate(i):
    # Calculate the start and end indices of the audio segment to display
    audio_start = int(i * window_overlap)
    audio_end = int(audio_start + window_length)
    audio_segment = filtered_data[audio_start:audio_end]

    # Calculate the corresponding power values
    power_start = int(audio_start / window_overlap)
    power_end = int(power_start + window_length / window_overlap)
    power_segment = power[power_start:power_end]

    # print("power_segment shape:", power_segment.shape)
    # print("audio_segment shape:", audio_segment.shape)

    # Create a 2D plot with the audio waveform and the power as intensity
    plt.clf()
    plt.specgram(audio_segment, NFFT=256, Fs=fs, cmap='viridis')
    # power_segment_2d = np.reshape(power_segment, (1, -1))

    power_segment_2d = np.reshape(power_segment, (len(time), 1))
    audio_segment = np.reshape(audio_segment, (window_length,))

    # plt.imshow(power_segment_2d, cmap='plasma', extent=[0, window_length_sec, 0, np.max(time)], aspect='auto')
    plt.imshow(np.flipud(np.expand_dims(power_segment, axis=1)), cmap='plasma', extent=[0, window_length_sec, 0, np.max(time)], aspect='auto')


    # plt.imshow(np.flipud(np.array([power_segment])), cmap='plasma', extent=[0, window_length_sec, 0, np.max(time)], aspect='auto')
    plt.xlabel('Time (s)')
    plt.ylabel('Time (s)')

# Create the animated video and save it to a file
fig = plt.figure()
anim = animation.FuncAnimation(fig, animate, frames=int((len(filtered_data) - window_length) / window_overlap))
anim.save('animated_video.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
