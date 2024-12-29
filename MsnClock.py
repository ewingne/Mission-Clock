# Mission Clock
# Version 1.5

import pystray
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta, timezone
from PIL import Image
from os import _exit

class ConfigWindow:
    def __init__(self, parent, current_timezones, update_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Edit Timezones")
        self.window.geometry("300x450")
        self.update_callback = update_callback
        
        # Tuple that holds the Cities and UTC offset by order of the offset.
        self.timezones = sorted(list(current_timezones), key=lambda x: x[1])
        
        # Create a label for the input box to collect the City name
        tk.Label(self.window, text="City:").pack(pady=5)
        self.city_entry = tk.Entry(self.window)
        self.city_entry.pack(pady=5)
        
        # Create a label for the input box to collect the UTC offset
        tk.Label(self.window, text="UTC Offset:").pack(pady=5)
        self.offset_entry = tk.Entry(self.window)
        self.offset_entry.pack(pady=5)
        
        # A button to add an entry for a new clock based off the inputs above
        tk.Button(self.window, text="Add Clock", command=self.add_timezone).pack(pady=10)
        
        # The list box showing the current clocks which will be generated when the save button is pressed
        self.listbox = tk.Listbox(self.window, width=40, height=10)
        self.listbox.pack(pady=10)
        
        # Button to remove an item selected inside the above listbox
        tk.Button(self.window, text="Remove Selected", command=self.remove_timezone).pack(pady=10)
        
        # Button to generate the clock based on the list from the above listbox
        tk.Button(self.window, text="Save Changes", command=self.save_changes).pack(pady=10)
        
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        self.timezones.sort(key=lambda x: x[1])
        for city, offset in self.timezones:
            self.listbox.insert(tk.END, f"{city} (UTC{offset:+d})")

    def add_timezone(self):
        if len(self.timezones) >= 9:
            messagebox.showwarning("Limit Reached", "Maximum of 9 clocks allowed")
            return
        
        city = self.city_entry.get().strip()
        try:
            offset = int(self.offset_entry.get())
            if city and -12 <= offset <= 14:
                self.timezones.append((city, offset))
                self.timezones.sort(key=lambda x: x[1])
                self.update_listbox()
                self.city_entry.delete(0, tk.END)
                self.offset_entry.delete(0, tk.END)
        except ValueError:
            pass

    def remove_timezone(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.timezones.pop(index)
            self.update_listbox()

    def save_changes(self):
        self.update_callback(self.timezones)
        self.window.destroy()

class MissionClock:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove title bar
        self.root.attributes('-topmost', False)  # Keep window on top
        self.root.attributes('-alpha', 0.99) # turn the window just a bit transparent to allow the screensave/lock to take affect.
        self.setup_tray() # Setup the tray icon

        self.is_on_top = tk.BooleanVar(value=False) # Variable to track if the application is always on top or not
        
        screen_width = root.winfo_screenwidth() # Get screen width dimensions for centering application

        self.timezones = [ # Beginning Timezones
            ('Honolulu', -10),
            ('San Antonio', -6),
            ('Zulu', 0),
            ('Berlin', 1),
            ('Tokyo', 9),
            ('Sydney', 10)
        ]

        # Set initial window size
        window_width = 155 * len(self.timezones)
        window_height = 85

        # Calculate center position
        x = (screen_width - window_width) // 2
        y = 0  # Top of screen

        # Set window geometry
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        self.create_clock_widgets()
        self.update_time()
        
    def create_clock_widgets(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.clock_frames = {}
        self.date_frames = {}

        # Add drag functionality
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.on_drag)

        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Edit", command=self.open_config)
        self.menu.add_checkbutton(label="Always on Top", variable=self.is_on_top, command=self.toggle_position)
        self.menu.add_command(label="Close", command=self.quit_app)

        # Add right-click to close
        self.root.bind('<Button-3>', self.show_menu)
        
        for city, _ in self.timezones:
            frame = tk.Frame(root, bg='black', padx=5)
            frame.pack(side='left', fill='both', expand=True)
            
            city_label = tk.Label(frame, text=city, font=('Helvetica', 12), bg='black', fg='white')
            city_label.pack(pady=1)
            
            time_label = tk.Label(frame, font=('Digital Display Regular', 24, 'bold'), bg='black', fg='#b5041a')
            time_label.pack(pady=1)
            
            date_label = tk.Label(frame, font=('Helvetica', 10), bg='black', fg='white')
            date_label.pack(pady=1)
            
            self.clock_frames[city] = time_label
            self.date_frames[city] = date_label

    def update_window_size(self):
        window_width = 155 * len(self.timezones)
        window_height = 85
        screen_width = self.root.winfo_screenwidth()
        x = (screen_width - window_width) // 2
        y = self.root.winfo_y()
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
    def toggle_position(self):
        if self.is_on_top.get():
            self.root.attributes('-topmost', True)
        else:
            self.root.attributes('-topmost', False)
    
    def update_timezones(self, new_timezones):
        self.timezones = new_timezones
        self.create_clock_widgets()
        self.update_window_size() # Resize the window based on the number of mission clocks.

    def open_config(self):
        ConfigWindow(self.root, self.timezones, self.update_timezones)        

    def update_time(self):
        utc = datetime.now(timezone.utc)
        for city, offset in self.timezones:
            local_time = utc + timedelta(hours=offset)
            self.clock_frames[city].config(text=local_time.strftime('%H:%M:%S'))
            self.date_frames[city].config(text=local_time.strftime('%A, %B %d'))
        self.root.after(1000, self.update_time)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f'+{x}+{y}')

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def setup_tray(self):
        # Create blank 32x32 image for tray icon
        icon_image = Image.open('resources/MsnClock_128.ico')

        self.tray_menu = pystray.Menu( # Create system try icon menu
            # Checks the status of "is_on_top" and toggles the position then sets the menu item to checked or not.
            pystray.MenuItem('Always on Top', lambda: (self.is_on_top.set(not self.is_on_top.get()), self.toggle_position()), checked=lambda item: self.is_on_top.get()),
            pystray.MenuItem('Close', self.quit_app)
        )

        # Create system tray icon
        self.tray_icon = pystray.Icon('mission_clock', icon_image, 'Mission Clock', self.tray_menu)

        self.tray_icon.run_detached() # start tray icon in separate thread

    def quit_app(self):
        _exit(0)
        self.tray_icon.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MissionClock(root)
    root.mainloop()