import tkinter as tk
from tkinter import filedialog
from os import makedirs
import os.path
import subprocess


def main():
	root = tk.Tk()
	Extractor(root)
	root.mainloop()


class Extractor(tk.Frame):
	def __init__(self, root, *args, **kwargs):
		super().__init__(root, *args, **kwargs)
		self.root = root
		self.configure()
		self.create_widgets()
		self.pack_widgets()

	def configure(self):
		self.root.resizable(0, 0)
		self.root.title("Extractor")

	def create_widgets(self):
		self.file_input = tk.StringVar()
		self.label_file_input = tk.Label(self, text="Video path:")
		self.label_frame_rate = tk.Label(self, text="Frame rate:")
		self.entry_file_input = tk.Entry(self, textvariable=self.file_input)
		self.entry_frame_rate = tk.Entry(self)
		self.btn_choose_input_path = tk.Button(self, text="...", command=self.choose_input_path)
		self.btn_ok = tk.Button(self, text="OK", command=self.extract_video)

	def pack_widgets(self):
		self.grid()
		self.label_file_input.grid(row=1, column=1)
		self.entry_file_input.grid(row=1, column=2)
		self.btn_choose_input_path.grid(row=1, column=3)
		self.label_frame_rate.grid(row=2, column=1)
		self.entry_frame_rate.grid(row=2, column=2)
		self.btn_ok.grid(row=3, column=3)

	def choose_input_path(self):
		path = self.open_file()
		if path != "":
			self.file_input.set(path)

	def open_file(self):
		ftypes = [('Video files', '*.mp4'), ('All files', '*')]
		dlg = filedialog.Open(self, filetypes=ftypes)
		return dlg.show()

	def extract_video(self):
		file_path = self.file_input.get()
		dir_path = os.path.dirname(os.path.realpath(file_path))
		frame_rate = self.entry_frame_rate.get().strip()
		if os.path.exists(file_path) and os.path.isfile(file_path) and is_int(frame_rate):
			extracted_frames_dir = os.path.join(dir_path, os.path.basename(file_path) + "_extracted")
			extracted_frame_template = os.path.join(extracted_frames_dir, "%04d.png")
			fps_arg = "fps=" + frame_rate
			makedirs(extracted_frames_dir, exist_ok=True)
			os.chdir(extracted_frames_dir)
			subprocess.run(["ffmpeg", "-i", file_path, "-vf", fps_arg, extracted_frame_template])

def is_int(x):
	try:
		x = int(x)
		return True
	except:
		return False


if __name__ == "__main__":
	main()