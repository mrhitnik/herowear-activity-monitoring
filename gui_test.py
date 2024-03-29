import tkinter as tk
from tkinter import font
import sys
import time

def redirect_output(text_widget, numbers, font_size=12):
    class StdoutRedirector:
        def __init__(self, text_widget, numbers, font_size):
            self.text_widget = text_widget
            self.numbers = numbers
            self.current_index = 0
            self.font = font.Font(size=font_size)

        def write(self, message):
            self.text_widget.delete("1.0", tk.END)  # Clear previous content
            self.text_widget.tag_configure("big", font=self.font)
            self.text_widget.insert(tk.END, f"Current Number: {self.numbers[self.current_index]}\n", "big")
            self.text_widget.insert(tk.END, message, "big")
            self.text_widget.see(tk.END)  # Auto-scroll to the bottom
            self.text_widget.update()

    sys.stdout = StdoutRedirector(text_widget, numbers, font_size)

def run_while_loop():
    while sys.stdout.current_index < len(sys.stdout.numbers):
        # Your logic here...
        print(f"Output for Number: {sys.stdout.numbers[sys.stdout.current_index]}")
        time.sleep(2)  # Add delay to make it visible in the GUI
        sys.stdout.current_index += 1

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Print Output Viewer")

    numbers = [1, 2, 3, 4, 5]  # Replace with your list of numbers
    font_size = 16  # Adjust the font size as needed
    window_size = (800, 600)

    output_text = tk.Text(root, wrap=tk.WORD, width=60, height=20)
    output_text.pack(expand=True, fill=tk.BOTH)

    redirect_output(output_text, numbers, font_size)

    root.after(0, run_while_loop)  # Run the while loop in the GUI event loop

    root.mainloop()
