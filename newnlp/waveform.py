import os
import tkinter as tk
from tkinter import messagebox, ttk
import pyttsx3
import numpy as np
import pygame
from pydub import AudioSegment
from pydub.playback import play
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Global variable to store the current audio file
current_audio_file = None

# Function to generate audio using pyttsx3 and save it as MP3
def generate_audio(story_text, accent, gender):
    try:
        # Initialize pyttsx3 engine
        engine = pyttsx3.init()

        # Set properties for voice
        voices = engine.getProperty('voices')

        # Set gender based on the user's input
        if gender == "male":
            engine.setProperty('voice', voices[0].id)  # Male voice
        else:
            engine.setProperty('voice', voices[1].id)  # Female voice

        # Set the speech rate
        engine.setProperty('rate', 150)  # Speed of speech

        # Set the volume (0.0 to 1.0)
        engine.setProperty('volume', 1.0)

        # Define the output MP3 file path
        output_mp3_path = "static/audio/output.mp3"
        os.makedirs(os.path.dirname(output_mp3_path), exist_ok=True)

        # Save speech to MP3
        engine.save_to_file(story_text, output_mp3_path)

        # Run the engine to process the speech
        engine.runAndWait()

        print(f"Audio generated and saved as MP3 at: {output_mp3_path}")

        # Return the MP3 file path
        return output_mp3_path

    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return None

# Function to play audio using pydub
def play_audio_with_pydub(audio_file):
    try:
        if audio_file and os.path.exists(audio_file):
            # Convert MP3 to WAV (if required)
            audio = AudioSegment.from_mp3(audio_file)

            # Play the audio file using pydub
            play(audio)
        else:
            print(f"Audio file does not exist: {audio_file}")
            messagebox.showerror("Error", "Audio file not found!")

    except Exception as e:
        print(f"Error playing audio with pydub: {str(e)}")
        messagebox.showerror("Error", f"Error playing audio: {str(e)}")

# Function to extract waveform from audio
def extract_waveform(audio_file):
    try:
        # Load audio file
        audio = AudioSegment.from_mp3(audio_file)

        # Convert audio to numpy array (mono channel)
        samples = np.array(audio.get_array_of_samples())

        # Get the number of samples (for plotting)
        return samples

    except Exception as e:
        print(f"Error extracting waveform: {str(e)}")
        return None

# Function to update the waveform plot
def update_waveform_plot(samples, ax, line, current_sample_idx, max_samples):
    if current_sample_idx < max_samples:
        # Update the plot with new waveform data
        line.set_ydata(samples[:current_sample_idx])
        ax.relim()
        ax.autoscale_view()
        canvas.draw()

        # Continue updating at regular intervals
        root.after(20, update_waveform_plot, samples, ax, line, current_sample_idx + 100, max_samples)

# Function to handle the Generate button click
def on_generate_button_click():
    story_text = story_text_entry.get("1.0", "end-1c")
    accent = accent_var.get()
    gender = gender_var.get()

    if not story_text.strip():
        messagebox.showerror("Input Error", "Please enter a story text!")
        return

    try:
        # Generate audio via pyttsx3 and save as MP3
        audio_file = generate_audio(story_text, accent, gender)

        if audio_file:
            # Notify user that the audio was generated successfully
            messagebox.showinfo("Success", f"Audio generated successfully!\n{audio_file}")

            # Display the audio file path in the GUI
            audio_label.config(text=f"Audio File: {audio_file}")  # Update label with file path
            play_button.pack(pady=10)  # Show the play button

            # Store the audio filename in a global variable so we can play it later
            global current_audio_file
            current_audio_file = audio_file

            # Extract waveform data for plotting
            samples = extract_waveform(audio_file)
            if samples is not None:
                # Plot the waveform using matplotlib
                fig, ax = plt.subplots(figsize=(5, 2))
                ax.set_title("Audio Waveform")

                # Initialize line object
                line, = ax.plot(np.zeros_like(samples))

                # Embed the plot into the Tkinter GUI
                canvas = FigureCanvasTkAgg(fig, master=waveform_frame)  # Create canvas for the plot
                canvas.draw()
                canvas.get_tk_widget().pack(padx=10, pady=10)

                # Update the waveform plot in real-time
                max_samples = len(samples)
                update_waveform_plot(samples, ax, line, 0, max_samples)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to handle the Play button click
def on_play_button_click():
    try:
        if current_audio_file:
            # Play the generated audio with pydub
            play_audio_with_pydub(current_audio_file)
        else:
            messagebox.showerror("Error", "No audio generated to play.")
    except Exception as e:
        messagebox.showerror("Error", f"Error playing audio: {str(e)}")

# Set up the Tkinter root window
root = tk.Tk()
root.title("Story to Audio Desktop App")

# Set up the window size (initially at 500x600, but can resize)
root.geometry("500x600")

# Create a canvas widget for the background image
canvas = tk.Canvas(root, width=500, height=600)
canvas.pack(fill="both", expand=True)

# Frame for all widgets (to keep widgets on top of the background)
frame = tk.Frame(root, bg="#f0f0f0", bd=5)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title label
title_label = tk.Label(frame, text="Story to Audio Generator", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

# Story text input
story_text_label = tk.Label(frame, text="Story Text:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
story_text_label.pack(pady=(10, 5))

story_text_entry = tk.Text(frame, height=6, width=40, font=("Arial", 12), wrap=tk.WORD, bd=1, relief="solid", padx=10, pady=10)
story_text_entry.pack(pady=5)

# Accent selection
accent_label = tk.Label(frame, text="Accent:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
accent_label.pack(pady=5)

accent_var = tk.StringVar()
accent_var.set("us")  # Default accent is "us"

accent_menu = ttk.Combobox(frame, textvariable=accent_var, values=["us", "uk", "aus", "indian"], font=("Arial", 12), state="readonly")
accent_menu.pack(pady=5)

# Gender selection
gender_label = tk.Label(frame, text="Gender:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
gender_label.pack(pady=5)

gender_var = tk.StringVar()
gender_var.set("female")  # Default gender is "female"

gender_menu = ttk.Combobox(frame, textvariable=gender_var, values=["female", "male"], font=("Arial", 12), state="readonly")
gender_menu.pack(pady=5)

# Generate button
generate_button = tk.Button(frame, text="Generate Audio", command=on_generate_button_click, font=("Arial", 14), bg="#4CAF50", fg="white", relief="solid", bd=1, padx=20, pady=10)
generate_button.pack(pady=20)

# Label to show the generated audio file path
audio_label = tk.Label(frame, text="Audio File: ", font=("Arial", 12), bg="#f0f0f0", fg="#333")
audio_label.pack(pady=10)

# Play button (hidden initially, will be shown after generating audio)
play_button = tk.Button(frame, text="Play Audio", command=on_play_button_click, font=("Arial", 14), bg="#2196F3", fg="white", relief="solid", bd=1, padx=20, pady=10)
play_button.pack_forget()  # Hide the button initially

# Create a frame for waveform visualization
waveform_frame = tk.Frame(root)
waveform_frame.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
