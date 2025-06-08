import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")

        # Dark mode colors
        self.bg_color = "#2e2e2e"
        self.fg_color = "#e0e0e0"
        self.btn_bg = "#444444"
        self.entry_bg = "#3c3c3c"
        
        # Set root background
        self.root.configure(bg=self.bg_color)

        self.file_list = []

        # Lista plików
        self.listbox = tk.Listbox(root, width=60, height=15, bg=self.entry_bg, fg=self.fg_color, selectbackground="#555555")
        self.listbox.pack(padx=10, pady=10)

        # Info label
        self.info_label = tk.Label(root, text="No files selected", bg=self.bg_color, fg=self.fg_color)
        self.info_label.pack()

        btn_frame = tk.Frame(root, bg=self.bg_color)
        btn_frame.pack(pady=5)

        add_btn = tk.Button(btn_frame, text="Add Images", command=self.add_files, bg=self.btn_bg, fg=self.fg_color, activebackground="#666666", activeforeground=self.fg_color)
        add_btn.grid(row=0, column=0, padx=5)

        remove_btn = tk.Button(btn_frame, text="Remove Selected", command=self.remove_selected, bg=self.btn_bg, fg=self.fg_color, activebackground="#666666", activeforeground=self.fg_color)
        remove_btn.grid(row=0, column=1, padx=5)

        clear_btn = tk.Button(btn_frame, text="Clear List", command=self.clear_list, bg=self.btn_bg, fg=self.fg_color, activebackground="#666666", activeforeground=self.fg_color)
        clear_btn.grid(row=0, column=2, padx=5)

        convert_btn = tk.Button(root, text="Convert Images", command=self.convert_images, bg=self.btn_bg, fg=self.fg_color, activebackground="#666666", activeforeground=self.fg_color)
        convert_btn.pack(pady=10)

        format_frame = tk.Frame(root, bg=self.bg_color)
        format_frame.pack()

        tk.Label(format_frame, text="Convert to:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0)

        self.format_var = tk.StringVar(value="PNG")
        formats = ["PNG", "JPEG", "BMP", "GIF", "TIFF"]
        self.format_menu = tk.OptionMenu(format_frame, self.format_var, *formats)
        self.format_menu.config(bg=self.btn_bg, fg=self.fg_color, activebackground="#666666", activeforeground=self.fg_color)
        self.format_menu.grid(row=0, column=1)

        output_frame = tk.Frame(root, bg=self.bg_color)
        output_frame.pack(pady=5)

        tk.Label(output_frame, text="Output folder:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0)
        self.output_entry = tk.Entry(output_frame, width=40, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color)
        self.output_entry.grid(row=0, column=1, padx=5)

        browse_btn = tk.Button(output_frame, text="Browse", command=self.browse_folder, bg=self.btn_bg, fg=self.fg_color, activebackground="#666666", activeforeground=self.fg_color)
        browse_btn.grid(row=0, column=2)

        scale_frame = tk.Frame(root, bg=self.bg_color)
        scale_frame.pack(pady=5)

        tk.Label(scale_frame, text="Resize images (%):", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0)
        self.scale_var = tk.StringVar(value="100")
        self.scale_entry = tk.Entry(scale_frame, width=5, textvariable=self.scale_var, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color)
        self.scale_entry.grid(row=0, column=1, padx=5)

        self.overwrite_var = tk.BooleanVar(value=True)
        overwrite_check = tk.Checkbutton(root, text="Overwrite existing files", variable=self.overwrite_var, bg=self.bg_color, fg=self.fg_color, activebackground=self.bg_color, activeforeground=self.fg_color, selectcolor=self.bg_color)
        overwrite_check.pack()

    def update_info_label(self):
        count = len(self.file_list)
        size_mb = 0
        for f in self.file_list:
            if os.path.exists(f):
                size_mb += os.path.getsize(f)
        size_mb /= (1024 * 1024)
        self.info_label.config(text=f"{count} files selected | Total size: {size_mb:.2f} MB")

    def add_files(self):
        files = filedialog.askopenfilenames(title="Select images",
                                            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")])
        for f in files:
            if f not in self.file_list:
                self.file_list.append(f)
                self.listbox.insert(tk.END, f)
        self.update_info_label()

    def remove_selected(self):
        selected = list(self.listbox.curselection())
        selected.reverse()
        for i in selected:
            self.listbox.delete(i)
            del self.file_list[i]
        self.update_info_label()

    def clear_list(self):
        self.listbox.delete(0, tk.END)
        self.file_list.clear()
        self.update_info_label()

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)

    def convert_images(self):
        if not self.file_list:
            messagebox.showwarning("No files", "Please add some images to convert.")
            return

        output_folder = self.output_entry.get()
        if not output_folder or not os.path.isdir(output_folder):
            messagebox.showwarning("Invalid folder", "Please select a valid output folder.")
            return

        try:
            scale_percent = int(self.scale_var.get())
            if scale_percent <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid scale", "Resize percentage must be a positive integer.")
            return

        target_format = self.format_var.get().lower()
        overwrite = self.overwrite_var.get()

        for filepath in self.file_list:
            try:
                img = Image.open(filepath)
                if scale_percent != 100:
                    new_width = int(img.width * scale_percent / 100)
                    new_height = int(img.height * scale_percent / 100)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)

                base = os.path.basename(filepath)
                name, _ = os.path.splitext(base)
                out_path = os.path.join(output_folder, f"{name}.{target_format}")

                if os.path.exists(out_path) and not overwrite:
                    fight = messagebox.askyesno("File exists", f"{out_path} exists. Overwrite?")
                    if not fight:
                        continue

                img.convert("RGB").save(out_path, target_format.upper())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert {filepath}.\n{e}")
                return

        messagebox.showinfo("Success", "All images have been converted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
