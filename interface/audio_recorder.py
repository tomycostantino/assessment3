import tkinter as tk
from tkinter import messagebox
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AudioRecorder(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callback_data = None
        self.stream_open = None
        self.master.geometry("700x550")
        self.master.title("Audio Recorder")

        self.pack()

        self.start_recording_button = tk.Button(self, text="Start Recording", command=self.start_recording)
        self.start_recording_button.pack()

        self.stop_recording_button = tk.Button(self, text="Stop Recording", command=self.stop_recording)
        self.stop_recording_button.pack()

        self.recording_label = tk.Label(self, text="Not Recording", fg="red")
        self.recording_label.pack()

        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = None

        self.fig, self.ax = plt.subplots()
        self.fig, self.ax = plt.subplots()
        self.fig.set_tight_layout(True)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.ax.set_ylim(-32768, 32767)
        self.ax.set_xlim(0, 1024)
        self.ax.set_xlabel("Samples")
        self.ax.set_ylabel("Amplitude")
        self.line, = self.ax.plot([], [])
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack()

    def start_recording(self):
        self.frames = []
        self.recording_label.config(text="Recording", fg="green")
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=1024,
                                  stream_callback=self.callback)
        self.stream.start_stream()
        self.start_recording_button.config(state="disable")
        self.stream_open = True
        self.update_waveform()

    def stop_recording(self):
        self.stream_open = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.recording_label.config(text="Not Recording", fg="red")
        self.start_recording_button.config(state="normal")

        filename = "recorded_audio.wav"
        if self.frames:
            wf = wave.open(filename, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            messagebox.showinfo("Info", "Recording done!")
        else:
            messagebox.showerror("Error", "No audio data recorded.")

    def update_waveform(self):
        if self.stream_open:
            data = self.callback_data
            if data:  # check whether data is not None
                self.callback_data = None
                self.frames.append(data)
                data = np.frombuffer(data, dtype=np.int16)
                self.line.set_data(range(len(data)), data)
                self.ax.set_xlim(0, len(data))
                self.canvas.draw()
        self.after(10, self.update_waveform)

    def callback(self, in_data, frame_count, time_info, status):
        self.callback_data = in_data
        return in_data, pyaudio.paContinue


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")  # Assign the size of the window
    app = AudioRecorder(master=root)
    app.mainloop()

