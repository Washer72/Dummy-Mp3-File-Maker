import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, USLT, TCOP
import wave

def create_dummy_mp3(file_path, duration=1):
    sample_rate = 44100
    n_channels = 2
    n_frames = duration * sample_rate
    silence = (b'\x00\x00' * n_channels * sample_rate) * duration

    wav_file = wave.open('silence.wav', 'wb')
    wav_file.setnchannels(n_channels)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(silence)
    wav_file.close()

    os.system(f'ffmpeg -i silence.wav -codec:a libmp3lame -qscale:a 2 "{file_path}"')
    os.remove('silence.wav')

def add_tags(file_path, tags, lyrics=None, cover_image_path=None):
    audio = MP3(file_path, ID3=EasyID3)
    for tag, value in tags.items():
        audio[tag] = value
    audio.save()

    id3 = ID3(file_path)
    id3.delall('APIC')

    if lyrics:
        id3.add(USLT(
            encoding=3,
            lang='eng',
            desc=u'Lyrics',
            text=lyrics
        ))

    if cover_image_path:
        with open(cover_image_path, 'rb') as img_file:
            img_data = img_file.read()
            id3.add(APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc=u'Cover',
                data=img_data
            ))

    if 'copyright' in tags:
        id3.add(TCOP(
            encoding=3,
            text=tags['copyright']
        ))

    id3.save(v2_version=3)

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)

def browse_cover_image():
    cover_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if cover_image_path:
        entry_cover_image.delete(0, tk.END)
        entry_cover_image.insert(0, cover_image_path)

def create_file():
    directory = entry_directory.get()
    filename = entry_filename.get()
    duration_str = entry_duration.get()
    cover_image_path = entry_cover_image.get()
    
    try:
        minutes, seconds = map(int, duration_str.split(':'))
        duration = minutes * 60 + seconds
    except ValueError:
        messagebox.showerror("Error", "Please enter duration in mm:ss format.")
        return

    file_path = os.path.join(directory, f'{filename}.mp3')
    create_dummy_mp3(file_path, duration)

    if os.path.exists(file_path):
        tags = {
            'title': entry_title.get(),
            'artist': entry_artist.get(),
            'album': entry_album.get(),
            'genre': entry_genre.get(),
            'date': entry_date.get(),
            'tracknumber': entry_tracknumber.get(),
            'copyright': entry_copyright.get()
        }
        lyrics = entry_lyrics.get("1.0", tk.END).strip()
        add_tags(file_path, tags, lyrics, cover_image_path)
        messagebox.showinfo("Success", f'Dummy MP3 file created and tagged: {file_path}')
    else:
        messagebox.showerror("Error", "Failed to create MP3 file.")

root = tk.Tk()
root.title("Dummy MP3 File Maker by Washer")
root.geometry("500x600")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

root.configure(bg='#f0f0f0')

style.configure("TLabel", font=('Arial', 10), background='#f0f0f0')
style.configure("TEntry", font=('Arial', 10), fieldbackground='#ffffff')
style.configure("TButton", font=('Arial', 10, 'bold'), background='#4caf50', foreground='white')
style.map("TButton",
    foreground=[('active', 'black')],
    background=[('active', '#3e8e41')]
)
style.configure("TText", font=('Arial', 10), background='#ffffff')

tk.Label(root, text="Output Directory:", bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=5, sticky='w')
entry_directory = ttk.Entry(root, width=40)
entry_directory.grid(row=0, column=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=browse_directory).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Filename:", bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=5, sticky='w')
entry_filename = ttk.Entry(root, width=40)
entry_filename.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Duration (mm:ss):", bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=5, sticky='w')
entry_duration = ttk.Entry(root, width=40)
entry_duration.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Title:", bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=5, sticky='w')
entry_title = ttk.Entry(root, width=40)
entry_title.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Artist:", bg='#f0f0f0').grid(row=4, column=0, padx=10, pady=5, sticky='w')
entry_artist = ttk.Entry(root, width=40)
entry_artist.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Album:", bg='#f0f0f0').grid(row=5, column=0, padx=10, pady=5, sticky='w')
entry_album = ttk.Entry(root, width=40)
entry_album.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Genre:", bg='#f0f0f0').grid(row=6, column=0, padx=10, pady=5, sticky='w')
entry_genre = ttk.Entry(root, width=40)
entry_genre.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Date:", bg='#f0f0f0').grid(row=7, column=0, padx=10, pady=5, sticky='w')
entry_date = ttk.Entry(root, width=40)
entry_date.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Cover Image:", bg='#f0f0f0').grid(row=8, column=0, padx=10, pady=5, sticky='w')
entry_cover_image = ttk.Entry(root, width=40)
entry_cover_image.grid(row=8, column=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=browse_cover_image).grid(row=8, column=2, padx=10, pady=5)

tk.Label(root, text="Track Number:", bg='#f0f0f0').grid(row=9, column=0, padx=10, pady=5, sticky='w')
entry_tracknumber = ttk.Entry(root, width=40)
entry_tracknumber.grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="Copyright:", bg='#f0f0f0').grid(row=10, column=0, padx=10, pady=5, sticky='w')
entry_copyright = ttk.Entry(root, width=40)
entry_copyright.grid(row=10, column=1, padx=10, pady=5)

tk.Label(root, text="Message as Lyrics:", bg='#f0f0f0').grid(row=11, column=0, padx=10, pady=5, sticky='w')
entry_lyrics = tk.Text(root, width=40, height=10, bg='#ffffff', font=('Arial', 10))
entry_lyrics.grid(row=11, column=1, padx=10, pady=5, columnspan=2)

ttk.Button(root, text="Create File", command=create_file).grid(row=12, columnspan=3, pady=10)

root.mainloop()
