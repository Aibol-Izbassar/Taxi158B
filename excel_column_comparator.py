import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd


class ExcelComparer(tk.Tk):
    """Simple GUI to compare identical text across selected columns of three Excel files."""

    def __init__(self):
        super().__init__()
        self.title("Excel Column Comparator")

        self.files = [None, None, None]
        self.columns = [[], [], []]
        self.selected_cols = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.comboboxes = []

        for i in range(3):
            btn = tk.Button(self, text=f"Select Excel file {i+1}",
                             command=lambda idx=i: self.load_file(idx))
            btn.grid(row=0, column=i, padx=5, pady=5)
            combo = ttk.Combobox(self, textvariable=self.selected_cols[i], state='readonly')
            combo.grid(row=1, column=i, padx=5, pady=5)
            self.comboboxes.append(combo)

        compare_btn = tk.Button(self, text="Compare", command=self.compare)
        compare_btn.grid(row=2, column=0, columnspan=3, pady=10)

    def load_file(self, idx: int) -> None:
        """Prompt user to select an Excel file and populate its columns."""
        path = filedialog.askopenfilename(title=f"Select Excel file {idx+1}",
                                          filetypes=[("Excel files", "*.xlsx *.xls")])
        if not path:
            return
        self.files[idx] = path
        try:
            df = pd.read_excel(path)
            self.columns[idx] = list(df.columns)
            combo = self.comboboxes[idx]
            combo["values"] = self.columns[idx]
            if self.columns[idx]:
                self.selected_cols[idx].set(self.columns[idx][0])
        except Exception as exc:  # pragma: no cover - GUI error message
            messagebox.showerror("Error", f"Cannot read Excel file:\n{exc}")

    def compare(self) -> None:
        """Compare selected columns across the three files for identical text."""
        if not all(self.files):
            messagebox.showwarning("Missing files", "Please select all three files.")
            return
        try:
            dfs = [pd.read_excel(self.files[i], usecols=[self.selected_cols[i].get()])
                   for i in range(3)]
        except Exception as exc:  # pragma: no cover
            messagebox.showerror("Error", f"Cannot read selected columns:\n{exc}")
            return

        sets = [set(dfs[i].iloc[:, 0].dropna().astype(str)) for i in range(3)]
        duplicates = set.intersection(*sets)
        if duplicates:
            result = "\n".join(sorted(duplicates))
            messagebox.showinfo("Matches found",
                                f"Identical text across files in selected columns:\n{result}")
        else:
            messagebox.showinfo("Matches not found", "No identical text found across the selected columns.")


if __name__ == "__main__":
    app = ExcelComparer()
    app.mainloop()
