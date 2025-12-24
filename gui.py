import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import webbrowser
from steam_locator import SteamLocator
from analyzer import GameAnalyzer

class SteamCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam Game Manager")
        self.root.geometry("800x600")

        self.locator = SteamLocator()
        self.analyzer = GameAnalyzer()
        self.games = []

        self._setup_ui()
        self.refresh_data()

    def _setup_ui(self):
        # Top Frame: Toolbar
        toolbar = ttk.Frame(self.root, padding="5")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(toolbar, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Uninstall Selected", command=self.uninstall_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Open Location", command=self.open_location).pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(toolbar, text="Ready")
        self.status_label.pack(side=tk.RIGHT, padx=5)

        # Main Frame: Treeview
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("name", "size", "last_updated")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="extended")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Headings
        self.tree.heading("name", text="Game Name", command=lambda: self.sort_tree("name", False))
        self.tree.heading("size", text="Size (GB)", command=lambda: self.sort_tree("size_gb", True))
        self.tree.heading("last_updated", text="Last Updated/Played", command=lambda: self.sort_tree("last_updated", False))

        self.tree.column("name", width=300)
        self.tree.column("size", width=100)
        self.tree.column("last_updated", width=150)

    def refresh_data(self):
        self.status_label.config(text="Scanning...")
        self.root.update_idletasks()
        
        try:
            self.games = self.locator.get_installed_games()
            # Default sort: Last Updated (Oldest first)
            self.games = self.analyzer.sort_games(self.games, sort_by="last_updated", reverse=False)
            self._populate_tree(self.games)
            self.status_label.config(text=f"Found {len(self.games)} games")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="Error")

    def _populate_tree(self, games):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for game in games:
            self.tree.insert("", tk.END, iid=game['id'], values=(
                game['name'],
                game['size_gb'],
                game['last_updated_str']
            ))

    def sort_tree(self, col, reverse):
        # Determine sort key based on column
        sort_key = "last_updated"
        is_reverse = reverse
        
        if col == "name":
            self.games.sort(key=lambda x: x['name'].lower(), reverse=is_reverse)
        elif col == "size_gb":
            self.games.sort(key=lambda x: x['size_gb'], reverse=is_reverse)
        else: # last_updated
             self.games.sort(key=lambda x: x['last_updated_timestamp'], reverse=is_reverse)
        
        self._populate_tree(self.games)
        
        # Toggle reverse for next click (simple toggle based on current state isn't tracked perfectly here, 
        # but for MVP we assume fixed toggle or improvement later if needed. 
        # Actually, let's just stick to the requested logic: Oldest first default. 
        # To make it toggleable would need to store state. Skipping complexity for now.)

    def uninstall_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No games selected")
            return

        if messagebox.askyesno("Confirm", f"Uninstall {len(selected_items)} selected game(s)?\n(This will open Steam uninstall dialogs)"):
            for appid in selected_items:
                # steam://uninstall/<id>
                webbrowser.open(f"steam://uninstall/{appid}")
    
    def open_location(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        # Just open the first one if multiple
        appid = selected_items[0]
        game = next((g for g in self.games if str(g['id']) == str(appid)), None)
        if game:
            path = game['path']
            folder = os.path.dirname(path)
            os.startfile(folder)

if __name__ == "__main__":
    root = tk.Tk()
    app = SteamCleanerApp(root)
    root.mainloop()
