import requests
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import threading

def load_logo_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        logo_image = Image.open(image_data)
        return ImageTk.PhotoImage(logo_image)
    else:
        return None

def getheaders(token):
    return {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

def setTitle(title):
    root.title(title)

def start_mass_dm_thread():
    threading.Thread(target=start_mass_dm).start()

def MassDM(token, channels, Message, delay, output_text, message_count_label):
    contacted_users = set()  
    message_count = 0  
    for channel in channels:
        for user in [x["username"]+"#"+x["discriminator"] for x in channel["recipients"]]:
            if user not in contacted_users:  
                try:
                    setTitle(f"Messaging {user}")
                    output_text.insert(tk.END, f"Message envoyé à : {user}\n")
                    contacted_users.add(user)  
                    message_count += 1  
                    message_count_label.config(text=f"Messages envoyés : {message_count}")
                    root.update_idletasks()  
                    requests.post(f"https://discord.com/api/v9/channels/{channel['id']}/messages", headers={'Authorization': token}, data={"content": f"{Message}"})
                    time.sleep(delay)
                except Exception as e:
                    output_text.insert(tk.END, f"Une erreur s'est produite lors de l'envoi à {user}: {e}\n")
                    output_text.see(tk.END)
                    root.update_idletasks()  

def start_mass_dm():
    token = token_entry.get()
    message = message_entry.get("1.0", tk.END).strip()
    delay = float(delay_entry.get())  
    
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
    if validityTest.status_code != 200:
        output_text.insert(tk.END, "Token invalide\n")
        output_text.see(tk.END)
        return
    
    channelIds = requests.get("https://discord.com/api/v9/users/@me/channels", headers=getheaders(token)).json()
    if not channelIds:
        output_text.insert(tk.END, "Ce compte n'a pas de messages privés\n")
        output_text.see(tk.END)
        return
    
    MassDM(token, channelIds, message, delay, output_text, message_count_label)

root = tk.Tk()
root.title("Mass DM by Furkan-FRTR")
root.geometry("600x500")

logo_url = "https://i.goopics.net/kgyjqw.png"

logo_photo = load_logo_from_url(logo_url)

if logo_photo:
    root.iconphoto(True, logo_photo)

input_frame = ttk.Frame(root, padding="20")
input_frame.pack(pady=(20, 10), padx=20)

token_label = ttk.Label(input_frame, text="Token:")
token_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

token_entry = ttk.Entry(input_frame, width=40)
token_entry.grid(row=1, column=1, padx=5, pady=5)

message_label = ttk.Label(input_frame, text="Message:")
message_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

message_entry = tk.Text(input_frame, width=30, height=5)
message_entry.grid(row=2, column=1, padx=5, pady=5)

delay_label = ttk.Label(input_frame, text="Délai (en secondes):") 
delay_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

delay_entry = ttk.Entry(input_frame, width=10)  
delay_entry.grid(row=3, column=1, padx=5, pady=5)

start_button = ttk.Button(input_frame, text="Commencer", command=start_mass_dm_thread)
start_button.grid(row=4, columnspan=2, padx=5, pady=5)

output_frame = ttk.Frame(root, padding="20")
output_frame.pack(fill="both", expand=True)

output_text = tk.Text(output_frame, wrap="word", width=40, height=10)
output_text.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=output_text.yview)
scrollbar.pack(side="right", fill="y")

output_text.config(yscrollcommand=scrollbar.set)

message_count_label = ttk.Label(root, text="Messages envoyés : 0")
message_count_label.pack(side="bottom", pady=5)

root.mainloop()
