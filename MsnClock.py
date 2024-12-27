# Mission Clock
# Version 1.0


import tkinter as tk
from datetime import datetime, timedelta, timezone

class MultiTimezoneClock:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove title bar
        self.root.attributes('-topmost', False)  # Keep window on top
        # self.root.title("Multi-Timezone Clock")
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        # screen_height = root.winfo_screenheight()

        self.timezones = [
            ('Hawaii', -10),
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
        
        self.clock_frames = {}
        self.date_frames = {}

        # Add drag functionality
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.on_drag)

        # Add right-click to close
        self.root.bind('<Button-3>', lambda e: root.destroy())
        
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
        
        self.update_time()

    def update_time(self):
        # utc = datetime.utcnow()
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

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiTimezoneClock(root)
    root.mainloop()