import tkinter as tk
from tkinter import ttk
from qm_auto import QuineMcCluskeyPyEDA

class QMApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Configurations
        self.title("Simplificador Quine-McCluskey")
        self.geometry("650x500")
        self.configure(bg="#2c3e50")

        # Styles
        style = ttk.Style()
        style.configure("TFrame", background="#2c3e50")
        style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 14))
        style.configure("TButton", font=("Arial", 14), padding=(10, 5))
        style.configure("TEntry", font=("Arial", 14))

        # Configure button colors
        style.map('TButton',
                  foreground=[('pressed', '#ecf0f1'), ('active', '#2c3e50')],
                  background=[('pressed', '!disabled', '#2c3e50'), ('active', '#27ae60')],
                  highlightcolor=[('focus', '#27ae60'), ('!focus', '#2c3e50')]
                  )

        # Canvas and scrollbar
        self.canvas = tk.Canvas(self, bg="#2c3e50")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Minterms label and entry
        self.label_minterms = ttk.Label(self.scrollable_frame, text="Minterminos (separados por comas):")
        self.label_minterms.pack(pady=30)

        self.minterms = tk.StringVar()
        self.entry_minterms = ttk.Entry(self.scrollable_frame, textvariable=self.minterms, width=50)
        self.entry_minterms.pack(pady=10, padx=40, ipady=5)

        # Buttons
        self.btn_simplify = ttk.Button(self.scrollable_frame, text="Simplificar", command=self.simplify_expression)
        self.btn_simplify.pack(pady=20)

        self.btn_clear = ttk.Button(self.scrollable_frame, text="Limpiar", command=self.clear_fields)
        self.btn_clear.pack(pady=10)

        # Result label and text box
        self.label_result = ttk.Label(self.scrollable_frame, text="Resultado:")
        self.label_result.pack(pady=30)

        self.result_text = tk.Text(self.scrollable_frame, width=50, height=10, font=("Arial", 14), state='disabled', bg="#34495e", fg="#ecf0f1")
        self.result_text.pack(pady=10, padx=40)

    def simplify_expression(self):
        try:
            minterms_list = [int(x.strip()) for x in self.minterms.get().split(',')]
            
            qm = QuineMcCluskeyPyEDA(minterms=minterms_list)
            result = qm.simplify(minterms_list)

            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)

            def insert_result(index=0):
                if index < len(result):
                    self.result_text.insert(tk.END, result[index])
                    self.after(50, insert_result, index+1)  # 50 ms delay between characters
                else:
                    self.result_text.config(state='disabled')

            insert_result()

        except Exception as e:
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error: {str(e)}")
            self.result_text.config(state='disabled')


    def clear_fields(self):
        self.minterms.set("")
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state='disabled')

if __name__ == "__main__":
    app = QMApp()
    app.mainloop()
