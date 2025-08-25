import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
import os
import sys
import json

from main_logic import analisar_edital, limpar_e_extrair_json, preencher_documento

COLORS = {
    "bg_dark": "#2c313c",
    "bg_medium": "#454952",
    "bg_light": "#5a5f6a",
    "text_light": "#f0f0f0",
    "accent_green": "#0a3b1e"
}

class PrintLogger:
    def __init__(self, text_widget, root):
        self.text_widget = text_widget
        self.root = root

    def write(self, text):
        # Usa root.after para garantir que a UI seja atualizada na thread principal
        self.root.after(0, lambda: self._update_text(text))

    def _update_text(self, text):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, text)
        self.text_widget.configure(state='disabled')
        self.text_widget.see(tk.END) # Rola para o final

    def flush(self):
        pass

class AnalisadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume AI")
        self.root.geometry("700x600")
        self.root.configure(bg=COLORS["bg_dark"])

        self.setup_styles()
        self.create_widgets()
        
        sys.stdout = PrintLogger(self.log_textbox, self.root)
        print("Bem-vindo! Selecione o edital e o local para salvar.\n")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TButton',
                        background=COLORS["bg_light"],
                        foreground=COLORS["text_light"],
                        bordercolor=COLORS["bg_medium"],
                        padding=8,
                        font=('Arial', 10, 'bold'))
        style.map('TButton',
                  background=[('active', COLORS["bg_medium"])])

        style.configure('Accent.TButton',
                        background=COLORS["accent_green"],
                        font=('Arial', 12, 'bold'))
        style.map('Accent.TButton',
                  background=[('active', '#2ecc71')])

        style.configure('TLabel', background=COLORS["bg_dark"], foreground=COLORS["text_light"], font=('Arial', 12, 'bold'))
        style.configure('TFrame', background=COLORS["bg_dark"])

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill='both')

        pdf_label = ttk.Label(main_frame, text="1. Selecione o Edital (.pdf)")
        pdf_label.pack(fill='x', pady=(0, 5))
        
        pdf_frame = ttk.Frame(main_frame)
        pdf_frame.pack(fill='x', pady=(0, 20))
        
        self.pdf_path_var = tk.StringVar()
        pdf_entry = ttk.Entry(pdf_frame, textvariable=self.pdf_path_var, state='readonly', font=('Arial', 10))
        pdf_entry.pack(side='left', expand=True, fill='x', ipady=4)

        self.pdf_browse_button = ttk.Button(pdf_frame, text="Procurar...", command=self.select_pdf)
        self.pdf_browse_button.pack(side='right', padx=(10, 0))

        save_label = ttk.Label(main_frame, text="2. Escolha onde salvar o Resumo (.docx)")
        save_label.pack(fill='x', pady=(0, 5))

        save_frame = ttk.Frame(main_frame)
        save_frame.pack(fill='x', pady=(0, 20))

        self.save_path_var = tk.StringVar()
        save_entry = ttk.Entry(save_frame, textvariable=self.save_path_var, state='readonly', font=('Arial', 10))
        save_entry.pack(side='left', expand=True, fill='x', ipady=4)

        self.save_browse_button = ttk.Button(save_frame, text="Salvar como...", command=self.select_save_path)
        self.save_browse_button.pack(side='right', padx=(10, 0))

        self.analyze_button = ttk.Button(main_frame, text="Analisar Edital", style='Accent.TButton', command=self.start_analysis_thread, state='disabled')
        self.analyze_button.pack(fill='x', pady=10)

        log_label = ttk.Label(main_frame, text="Log de Atividade:")
        log_label.pack(fill='x', pady=(10, 5))
        
        self.log_textbox = scrolledtext.ScrolledText(main_frame, state='disabled', height=10, bg=COLORS["bg_medium"], fg=COLORS["text_light"], font=('Courier New', 10), relief='flat')
        self.log_textbox.pack(expand=True, fill='both')

    def select_pdf(self):
        filepath = filedialog.askopenfilename(title="Selecionar Edital PDF", filetypes=[("Arquivos PDF", "*.pdf")])
        if filepath:
            self.pdf_path_var.set(filepath)
            self.check_paths()

    def select_save_path(self):
        filepath = filedialog.asksaveasfilename(title="Salvar Resumo Como", filetypes=[("Documentos Word", "*.docx")], defaultextension=".docx")
        if filepath:
            self.save_path_var.set(filepath)
            self.check_paths()

    def check_paths(self):
        if self.pdf_path_var.get() and self.save_path_var.get():
            self.analyze_button.config(state='normal')
        else:
            self.analyze_button.config(state='disabled')

    def toggle_ui_elements(self, enabled):
        state = 'normal' if enabled else 'disabled'
        self.analyze_button.config(state=state)
        self.pdf_browse_button.config(state=state)
        self.save_browse_button.config(state=state)

    def start_analysis_thread(self):
        self.toggle_ui_elements(False)
        thread = threading.Thread(target=self.run_analysis)
        thread.start()

    def run_analysis(self):
        pdf_path = self.pdf_path_var.get()
        save_path = self.save_path_var.get()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, 'RESUMO_SMP..docx')

        try:
            resposta_bruta_ia = analisar_edital(pdf_path)
            if resposta_bruta_ia:
                json_limpo = limpar_e_extrair_json(resposta_bruta_ia)
                if json_limpo:
                    dados_edital = json.loads(json_limpo)
                    preencher_documento(dados_edital, template_path, save_path)
                else:
                    print("\n--- ERRO: Não foi possível extrair um JSON da resposta da IA ---\n")
        except Exception as e:
            print(f"\n--- UM ERRO INESPERADO OCORREU ---\n{e}\n")
        finally:
            print("\n--- Processo Finalizado ---\n")
            self.toggle_ui_elements(True)


if __name__ == "__main__":
    root = tk.Tk()
    app = AnalisadorApp(root)
    root.mainloop()