import numpy as np
import matplotlib.pyplot as plt


sample_num = 2000  # Sampling points
total_time = 2  # Sampling number
sampling_rate = sample_num / total_time  # 取樣頻率

fs = [(20, 1), (100, 1), (250, 1)]  # sin 波的頻率與振幅組合。 (Hz, Amp)
noise_mag = 2

time = np.linspace(0, total_time, sample_num)

vib_data = [amp * np.sin(2*np.pi*hz*time) for hz, amp in fs]  # Original Signal

max_time = int(sample_num / 4)
# vib = sum(vib_data) + np.random.normal(0, noise_mag, sample_num)  # Original Signal + Add noise
vib = sum(vib_data)

# plot signal
# plt.figure(figsize=(12, 8))
# for idx, vib in enumerate(vib_data):
#     plt.subplot(2, 2, idx+1)
#     plt.plot(time[0:max_time], vib[0:max_time])
#     plt.xlabel('time')
#     plt.ylabel('vib_' + str(idx))
#     plt.ylim((-24, 24))
#
# plt.subplot(2, 2, 4)
# plt.plot(time[0:max_time], vib[0:max_time])
# plt.xlabel('time')
# plt.ylabel('vib(with noise)')
# plt.ylim((-24, 24))
# plt.show()

# fourier transform
freq_seq = np.linspace(0, sampling_rate, sample_num)
vib_fft = np.fft.fft(vib)
magnitude = 2 / sample_num * np.abs(vib_fft)

low_freq_index = np.argmax(magnitude[:sample_num//2])
print(time[1] - time[0])
print(low_freq_index, freq_seq[low_freq_index])
print(freq_seq[-1])

plt.plot(freq_seq[:sample_num//2], magnitude[:sample_num//2])
plt.xlabel('Hz')
plt.ylabel('Magnitude')
plt.show()


