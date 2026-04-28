import os
import pygame
import gtts
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pygame import mixer
from PIL import Image, ImageTk

# Initialize pygame mixer for playing audio
mixer.init()

# Function to generate audio using gTTS (Google Text-to-Speech)
def generate_audio(story_text, accent, gender):
    try:
        # Create a TTS object with the selected language and accent
        tts = gtts.gTTS(text=story_text, lang='en', slow=False)

        # Define the output file path
        output_path = "static/audio/output.mp3"

        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the audio to the specified path
        tts.save(output_path)

        print(f"Audio generated and saved at: {output_path}")  # Debug line
        return output_path  # Return the audio file path

    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return None


# Function to play audio
def play_audio(audio_file):
    try:
        # Check if the file exists before trying to play it
        if os.path.exists(audio_file):
            print(f"Playing audio: {audio_file}")  # Debug line
            mixer.music.load(audio_file)
            mixer.music.play()
        else:
            print(f"Audio file does not exist: {audio_file}")
            messagebox.showerror("Error", "Audio file not found!")

    except Exception as e:
        print(f"Error playing audio: {str(e)}")
        messagebox.showerror("Error", f"Error playing audio: {str(e)}")

# Function to handle the Generate button click
def on_generate_button_click():
    story_text = story_text_entry.get("1.0", "end-1c")
    accent = accent_var.get()
    gender = gender_var.get()

    if not story_text.strip():
        messagebox.showerror("Input Error", "Please enter a story text!")
        return

    try:
        # Generate audio via gTTS
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

            # Update the background image to be full-screen
            resize_background(None)  # Call to resize background image after audio generation

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to handle the Play button click
def on_play_button_click():
    try:
        if 'current_audio_file' in globals():
            # Play the generated audio
            play_audio(current_audio_file)
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

# Function to resize background image dynamically
def resize_background(event):
    # Get the new size of the window
    new_width = event.width if event else root.winfo_width()
    new_height = event.height if event else root.winfo_height()
    
    # Load the background image (ensure you have an image file at the specified path)
    bg_image = Image.open("background.jpg")  # Replace 'background.jpg' with your image file
    bg_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resize image to window size
    bg_image = ImageTk.PhotoImage(bg_image)

    # Update the canvas background image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    canvas.image = bg_image  # Keep a reference to avoid garbage collection

# Bind the resize event to the resize_background function
root.bind("<Configure>", resize_background)

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

# Run the Tkinter event loop
root.mainloop()
