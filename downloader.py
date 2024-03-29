import os
import subprocess
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import END
from io import StringIO
import sys
from pytube import YouTube
from pytube import Playlist

DOWNLOADS = './Pyt2mp3_Downloads'
CWD = '.'

# Global variable to store the links
links = []
blocked_links = [] 

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, str):
        self.text_widget.insert(tk.END, str)
        self.text_widget.see(tk.END) 

    def flush(self):
        pass

def extract_from_list():
    global links, blocked_links

    print("Extracting from list...")
    root.update_idletasks()
    link_entries = link_entry.get("1.0", tk.END).splitlines()
    link_entry.delete("1.0", tk.END)

    if not link_entries:
        messagebox.showinfo("Info", "No links entered.")
        return

    print("Links entered:")
    root.update_idletasks()
    for link in link_entries:
        print(link)
        root.update_idletasks()
    
    # Add non-empty links to the global list
    for entry in link_entries:
        if entry.strip(): 
            links.append(entry.strip())
    
    print("Links in list:")
    root.update_idletasks()
    for link in links:
        print(link) 
        root.update_idletasks() 

    print("LOOP")
    root.update_idletasks()

    # Iterate over the links
    for link in links[:]:
        print("LOOP")
        root.update_idletasks()
        try:
            print("Checking Link:", link)
            root.update_idletasks()
            yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
            yt._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            video = yt.streams.filter(only_audio=True).first()

            final = yt.title + ".mp3"

            # Check if the final file already exists
            if os.path.exists(os.path.join(DOWNLOADS, final)):
                user_response = messagebox.askyesno("File Exists", f"File '{final}' already exists. Overwrite?")
                if not user_response:
                    print("Skipping download:", yt.title.upper(), "- Already downloaded")
                    root.update_idletasks()
                    links.remove(link)  # Remove link from list
                    continue
                else:
                    print("Overwriting existing file:", final)
                    root.update_idletasks()
                
            out_file = video.download(output_path=CWD)
            

            if not out_file:
                print("Download failed for:", yt.title.upper())
                root.update_idletasks()
                if os.path.exists(out_file):
                    os.remove(out_file)
                continue

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'

            os.rename(out_file, new_file)
            convert_final(os.path.join(CWD, new_file), os.path.join(DOWNLOADS, final))
            os.remove(new_file)
            print(yt.title.upper() + " has been successfully downloaded!")
            root.update_idletasks()
            links.remove(link)  # Remove link from list after successful download
        except Exception as e:
            print("Error:", e)
            if "age restricted" in str(e).lower():
                print("Skipping download of age-restricted video:", yt.title.upper())
                root.update_idletasks()
                blocked_links.append(link)
                continue
            messagebox.showerror("Error", "Error downloading: " + str(e))
            if os.path.exists(out_file):
                os.remove(out_file)
            continue

    links.clear()

    messagebox.showinfo("Info", "Downloads Complete")

    if blocked_links:
        blocked_links_msg = "\n".join(blocked_links)
        messagebox.showinfo("Age Restricted Videos", "The following videos are age-restricted and cannot be downloaded without logging in:\n" + blocked_links_msg)
        link_entry.delete("1.0", tk.END)
        link_entry.insert(tk.END, "\n".join(blocked_links))
    else:
        link_entry.delete("1.0", tk.END)

    download_button.config(state="normal")
    playlist_button.config(state="normal")

def extract_playlist():
    global links
    print("Extracting playlist...")
    root.update_idletasks()

    link_entries = link_entry.get("1.0", tk.END).splitlines()
    link_entry.delete("1.0", tk.END)
    
    # Append the links from the entry box to the existing links list
    for entry in link_entries:
        if entry.strip():  # Check if entry is not empty or whitespace
            links.append(entry.strip())

    if not links:
        messagebox.showinfo("Info", "No links remaining in the list.")
        return

    print("Links in list:", links)
    root.update_idletasks()

    playlist_link = links[0]
    try:
        playlist = Playlist(playlist_link)
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", "Invalid playlist link: " + playlist_link)
        return

    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    links.clear()

    for video in playlist.videos:
        links.append(video.watch_url)

    extract_from_list()

def convert_final(input_file, output_file):
    output_file = output_file.replace("//", "")

    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        output_file
    ])

def empty_downloads():
    for file in os.listdir(DOWNLOADS):
        os.remove(os.path.join(DOWNLOADS, file))
    messagebox.showinfo("Success", "Downloads folder has been emptied")

# Initialize downloader
def init_downloader():
    # if downloads folder doesn't exist, create it
    if not os.path.exists(DOWNLOADS):
        os.makedirs(DOWNLOADS)

def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 4
    window.geometry('+{}+{}'.format(x, y))

def process_list():
    global links
    # Process the links
    extract_from_list()
    messagebox.showinfo("Info", "All links processed.")

def download_list():
    download_button.config(state="disabled")
    playlist_button.config(state="disabled")
    extract_from_list()

def download_playlist():
    download_button.config(state="disabled")
    playlist_button.config(state="disabled")
    extract_playlist()

def on_button_click(event):
    button = event.widget
    x, y = event.x, event.y
    width, height = button.winfo_width(), button.winfo_height()

    if 0 <= x <= width and 0 <= y <= height:
        button.invoke() 

# Create the main window
root = tk.Tk()
root.title("YouTube Downloader")

window_width = 800  
window_height = 600 
root.geometry(f"{window_width}x{window_height}")

# Initialize downloader
init_downloader()

link_label = tk.Label(root, text="Enter YouTube link(s):")
link_label.pack()

link_entry = scrolledtext.ScrolledText(root, height=10, width=80)
link_entry.pack(fill="both", expand=True)

button_frame = tk.Frame(root)
button_frame.pack()

button_height = 2  # Adjust the height of the buttons

download_button = tk.Button(button_frame, text="Download", command=download_list, height=button_height)
download_button.pack(side="left", padx=5, pady=5, fill="both", expand=True)
download_button.bind("<Button-1>", on_button_click)  # Bind left-click event to the button

playlist_button = tk.Button(button_frame, text="Download Playlist", command=download_playlist, height=button_height)
playlist_button.pack(side="left", padx=5, pady=5, fill="both", expand=True)
playlist_button.bind("<Button-1>", on_button_click)  # Bind left-click event to the button

empty_button = tk.Button(button_frame, text="Empty Downloads Folder", command=empty_downloads, height=button_height)
empty_button.pack(side="left", padx=5, pady=5, fill="both", expand=True)
empty_button.bind("<Button-1>", on_button_click)  # Bind left-click event to the button

output_text = scrolledtext.ScrolledText(root, height=10, width=100)
output_text.pack(fill="both", expand=True)

sys.stdout = StdoutRedirector(output_text)

center_window(root)

root.mainloop()
