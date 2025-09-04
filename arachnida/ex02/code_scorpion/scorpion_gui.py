import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from metadata_handler import (
    get_image_metadata,
    set_image_tag,
    remove_image_tag,
    remove_all_metadata
)

class ScorpionGUI:
    def __init__(self, master_window):
        self.root = master_window
        self.root.title("Scorpion Metadata Editor")
        self.root.geometry("700x500")

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        self.open_button = ttk.Button(main_frame, text="Ouvrir une image...", command=self.open_image_file)
        self.open_button.grid(row=0, column=0, sticky="ew", pady=5)

        columns = ('key', 'value')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        self.tree.heading('key', text='Clé')
        self.tree.heading('value', text='Valeur')
        self.tree.grid(row=1, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        self.set_button = ttk.Button(action_frame, text="Modifier Tag...", command=self.set_tag_dialog)
        self.set_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(action_frame, text="Supprimer Tag...", command=self.remove_tag_dialog)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.remove_all_button = ttk.Button(action_frame, text="Tout Supprimer...", command=self.remove_all_tags)
        self.remove_all_button.pack(side=tk.LEFT, padx=5)

        self.current_filepath = None

    def refresh_display(self):
        if self.current_filepath:
            metadata = get_image_metadata(self.current_filepath)
            self.display_metadata(metadata)

    def open_image_file(self):
        filepath = filedialog.askopenfilename(
            title='Ouvrir une image',
            filetypes=(('Images', '*.jpg *.jpeg *.png *.bmp *.gif'), ('Tous les fichiers', '*.*'))
        )
        if filepath:
            self.current_filepath = filepath
            self.refresh_display()

    def display_metadata(self, metadata):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if metadata:
            for key, value in metadata.items():
                self.tree.insert('', tk.END, values=(key, str(value)))
        else:
            self.tree.insert('', tk.END, values=("Erreur", "Impossible de lire les métadonnées."))

    def set_tag_dialog(self):
        if not self.current_filepath: 
            return
        tag = simpledialog.askstring("Modifier", "Nom du tag à modifier :")
        if not tag:
            return
        value = simpledialog.askstring("Modifier", f"Nouvelle valeur pour le tag '{tag}':")
        if value is not None:
            set_image_tag(self.current_filepath, tag, value)
            self.refresh_display()

    def remove_tag_dialog(self):
        if not self.current_filepath:
            return
        tag = simpledialog.askstring("Supprimer", "Nom du tag à supprimer :")
        if tag:
            remove_image_tag(self.current_filepath, tag)
            self.refresh_display()

    def remove_all_tags(self):
        if not self.current_filepath:
            return
        if messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir supprimer TOUTES les métadonnées EXIF ?\nCette action est irréversible."):
            remove_all_metadata(self.current_filepath)
            self.refresh_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScorpionGUI(root)
    root.mainloop()
