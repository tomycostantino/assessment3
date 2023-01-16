import tkinter as tk
from tkinter import filedialog  #Lets me open the audiofile
from modules.speech_recognition import Speech2Text


class FileSpeech2Text(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._perform_s2t = tk.Button(self, bg='white', fg='black', padx=5, pady=10,
                                      text='Select file and transform to text', command=self._transform)
        self._perform_s2t.pack()

    def _display_result(self, to_display):
        popup = tk.Toplevel(self)
        label = tk.Label(popup, text=to_display, padx=10, pady=10)
        label.pack()
        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack()

    def _transform(self):
        filename = filedialog.askopenfilename()
        s2t = Speech2Text()
        result = s2t.transform2text(filename)
        self._display_result(result)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileSpeech2Text(master=root)
    app.mainloop()
