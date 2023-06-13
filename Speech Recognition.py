import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox, filedialog

def save_file(text):
    # Open a file dialog to select the save location
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            # Save the recognized text to the selected file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)
            messagebox.showinfo("Save Successful", "Output saved to {}".format(file_path))
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

def start_recording(language):
    # Disable the start button
    start_button.config(state=tk.DISABLED)

    # Update the UI label
    status_label.config(text="Recording")

    # Create a recognizer object
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        # Adjust for ambient noise for better recognition
        recognizer.adjust_for_ambient_noise(source)

        try:
            # Listen to the user's input
            audio = recognizer.listen(source)

            # Update the UI label
            status_label.config(text="Processing...")

            # Use Google Speech Recognition to convert speech to text
            text = recognizer.recognize_google(audio, language=language)
            output_text.insert(tk.END, text + "\n")
            save_button.config(state=tk.NORMAL)

        except sr.UnknownValueError:
            messagebox.showwarning("Speech Recognition", "Could not understand audio.")

        except sr.RequestError as e:
            messagebox.showerror("Speech Recognition", "Error occurred: {}".format(str(e)))

        # Re-enable the start button
        start_button.config(state=tk.NORMAL)

        # Update the UI label
        status_label.config(text="Done")

def clear_text():
    output_text.delete("1.0", tk.END)
    save_button.config(state=tk.DISABLED)
    status_label.config(text="Start Recording")

# Create the main window
window = tk.Tk()
window.title("Speech to Text")
window.geometry("600x400")

# Create the user interface elements
status_label = tk.Label(window, text="Start Recording", font=("Arial", 12, "bold"))
status_label.pack(pady=10)

output_text = tk.Text(window, font=("Arial", 12), height=10, wrap=tk.WORD)
output_text.pack(padx=20, pady=10)

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start (English)", font=("Arial", 12), command=lambda: start_recording("en"))
start_button.grid(row=0, column=0, padx=5)

thai_button = tk.Button(button_frame, text="Start (Thai)", font=("Arial", 12), command=lambda: start_recording("th-TH"))
thai_button.grid(row=0, column=1, padx=5)

chinese_button = tk.Button(button_frame, text="Start (Chinese)", font=("Arial", 12), command=lambda: start_recording("zh-CN"))
chinese_button.grid(row=0, column=2, padx=5)

clear_button = tk.Button(button_frame, text="Clear", font=("Arial", 12), command=clear_text)
clear_button.grid(row=0, column=3, padx=5)

save_button = tk.Button(window, text="Save", font=("Arial", 12), state=tk.DISABLED, command=lambda: save_file(output_text.get("1.0", tk.END)))
save_button.pack(pady=10)

# Run the main window event loop
window.mainloop()
