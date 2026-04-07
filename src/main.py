import tkinter as tk
from tkinter import ttk, messagebox
import threading
from pathlib import Path
from models.mus_game import MusGame

# Color palette
BG_DARK = "#1a1a2e"
BG_CARD = "#16213e"
BG_INPUT = "#0f3460"
ACCENT = "#e94560"
ACCENT_HOVER = "#ff6b81"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#a0a0b8"
TEXT_MUTED = "#6c6c80"
GREEN = "#2ecc71"
GOLD = "#f1c40f"
CARD_BG = "#f5f5dc"
CARD_BORDER = "#8b4513"
CARD_TEXT = "#2c3e50"
BASE_DIR = Path(__file__).resolve().parent.parent
CARD_IMAGES_DIR = BASE_DIR / "card_images"


class MusGUI:
    CARD_NAMES = {
        'R': 'Rey', 'C': 'Caballo', 'S': 'Sota',
        'A': 'As', '7': '7', '6': '6', '5': '5', '4': '4'
    }
    CARD_IMAGE_FILES = {
        'R': 'R',
        'C': 'C',
        'S': 'S',
        'A': 'A',
        '7': '7',
        '6': '6',
        '5': '5',
        '4': '4',
    }
    CARD_ART = {
        'R': {'numero': '12', 'palo': 'Oros', 'simbolo': 'O', 'color': GOLD},
        'C': {'numero': '11', 'palo': 'Copas', 'simbolo': 'C', 'color': ACCENT},
        'S': {'numero': '10', 'palo': 'Espadas', 'simbolo': 'E', 'color': TEXT_PRIMARY},
        'A': {'numero': '1', 'palo': 'Bastos', 'simbolo': 'B', 'color': GREEN},
        '7': {'numero': '7', 'palo': 'Oros', 'simbolo': 'O', 'color': GOLD},
        '6': {'numero': '6', 'palo': 'Copas', 'simbolo': 'C', 'color': ACCENT},
        '5': {'numero': '5', 'palo': 'Espadas', 'simbolo': 'E', 'color': TEXT_PRIMARY},
        '4': {'numero': '4', 'palo': 'Bastos', 'simbolo': 'B', 'color': GREEN},
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Mus")
        self.root.geometry("720x620")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DARK)

        self.mus_game = MusGame()
        self.simulando = False
        self.card_image_cache = {}

        self._configure_styles()
        self._crear_interfaz()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Dark.TFrame', background=BG_DARK)
        style.configure('Card.TFrame', background=BG_CARD, relief='flat')
        style.configure('Dark.TLabel', background=BG_DARK, foreground=TEXT_PRIMARY, font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=BG_DARK, foreground=TEXT_PRIMARY, font=('Segoe UI', 22, 'bold'))
        style.configure('Subtitle.TLabel', background=BG_DARK, foreground=TEXT_SECONDARY, font=('Segoe UI', 10))
        style.configure('Section.TLabel', background=BG_CARD, foreground=TEXT_PRIMARY, font=('Segoe UI', 11, 'bold'))
        style.configure('Info.TLabel', background=BG_CARD, foreground=TEXT_SECONDARY, font=('Segoe UI', 9))
        style.configure('CardFrame.TFrame', background=BG_CARD)

        style.configure('Accent.TButton',
                        background=ACCENT, foreground=TEXT_PRIMARY,
                        font=('Segoe UI', 12, 'bold'), padding=(20, 10))
        style.map('Accent.TButton',
                  background=[('active', ACCENT_HOVER), ('disabled', TEXT_MUTED)])

        style.configure('Dark.TEntry', fieldbackground=BG_INPUT, foreground=TEXT_PRIMARY,
                        insertcolor=TEXT_PRIMARY, font=('Segoe UI', 13))

        style.configure('Dark.TCombobox', fieldbackground=BG_INPUT, foreground=TEXT_PRIMARY,
                        background=BG_INPUT, font=('Segoe UI', 12))
        style.map('Dark.TCombobox', fieldbackground=[('readonly', BG_INPUT)])

        style.configure('Dark.TLabelframe', background=BG_CARD, foreground=TEXT_PRIMARY,
                        font=('Segoe UI', 10, 'bold'))
        style.configure('Dark.TLabelframe.Label', background=BG_CARD, foreground=ACCENT,
                        font=('Segoe UI', 10, 'bold'))

        style.configure('Results.Treeview',
                        background=BG_CARD, foreground=TEXT_PRIMARY,
                        fieldbackground=BG_CARD, font=('Segoe UI', 11),
                        rowheight=36)
        style.configure('Results.Treeview.Heading',
                        background=BG_INPUT, foreground=ACCENT,
                        font=('Segoe UI', 11, 'bold'))
        style.map('Results.Treeview', background=[('selected', ACCENT)])

        style.configure('Loading.Horizontal.TProgressbar',
                        background=ACCENT, troughcolor=BG_INPUT)

    def _crear_interfaz(self):
        # Main container
        main = ttk.Frame(self.root, style='Dark.TFrame', padding=30)
        main.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Frame(main, style='Dark.TFrame')
        header.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(header, text="Simulador de Mus", style='Title.TLabel').pack(side=tk.LEFT)
        ttk.Label(header, text="Monte Carlo", style='Subtitle.TLabel').pack(side=tk.RIGHT, anchor=tk.S, pady=(0, 4))

        # Separator
        sep = tk.Frame(main, height=2, bg=ACCENT)
        sep.pack(fill=tk.X, pady=(0, 20))

        # Content area - two columns
        content = ttk.Frame(main, style='Dark.TFrame')
        content.pack(fill=tk.BOTH, expand=True)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)

        # Left column: inputs
        left = ttk.Frame(content, style='Dark.TFrame')
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 15))

        self._crear_seccion_mano(left)
        self._crear_seccion_config(left)
        self._crear_boton_simular(left)

        # Right column: card preview
        right = ttk.Frame(content, style='Dark.TFrame')
        right.grid(row=0, column=1, sticky='nsew')

        self._crear_preview_cartas(right)

    def _crear_seccion_mano(self, parent):
        frame = ttk.LabelFrame(parent, text=" Tu Mano ", style='Dark.TLabelframe', padding=15)
        frame.pack(fill=tk.X, pady=(0, 15))

        inner = ttk.Frame(frame, style='CardFrame.TFrame')
        inner.pack(fill=tk.X)

        ttk.Label(inner, text="Introduce 4 cartas:", style='Section.TLabel').pack(anchor=tk.W)

        self.jugada_entry = tk.Entry(inner, font=('Segoe UI', 18), width=8,
                                     bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                                     relief='flat', justify='center')
        self.jugada_entry.pack(fill=tk.X, pady=(8, 6))
        self.jugada_entry.bind('<KeyRelease>', self._on_hand_change)

        ttk.Label(inner, text="R  C  S  A  7  6  5  4", style='Info.TLabel').pack(anchor=tk.CENTER)

        # Quick buttons for card input
        btn_frame = ttk.Frame(inner, style='CardFrame.TFrame')
        btn_frame.pack(fill=tk.X, pady=(8, 0))
        for carta in ['R', 'C', 'S', 'A', '7', '6', '5', '4']:
            btn = tk.Button(btn_frame, text=carta, width=3, font=('Segoe UI', 9, 'bold'),
                           bg=BG_INPUT, fg=TEXT_PRIMARY, activebackground=ACCENT,
                           activeforeground=TEXT_PRIMARY, relief='flat', cursor='hand2',
                           command=lambda c=carta: self._insert_card(c))
            btn.pack(side=tk.LEFT, padx=2)

    def _crear_seccion_config(self, parent):
        frame = ttk.LabelFrame(parent, text=" Configuracion ", style='Dark.TLabelframe', padding=15)
        frame.pack(fill=tk.X, pady=(0, 15))

        inner = ttk.Frame(frame, style='CardFrame.TFrame')
        inner.pack(fill=tk.X)

        # Position
        row1 = ttk.Frame(inner, style='CardFrame.TFrame')
        row1.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(row1, text="Posicion:", style='Section.TLabel').pack(side=tk.LEFT)
        self.orden_var = tk.StringVar(value="1")
        pos_frame = ttk.Frame(row1, style='CardFrame.TFrame')
        pos_frame.pack(side=tk.RIGHT)

        self.pos_buttons = {}
        for i in range(1, 5):
            btn = tk.Button(pos_frame, text=str(i), width=3, font=('Segoe UI', 10, 'bold'),
                           bg=ACCENT if i == 1 else BG_INPUT,
                           fg=TEXT_PRIMARY, activebackground=ACCENT_HOVER,
                           activeforeground=TEXT_PRIMARY, relief='flat', cursor='hand2',
                           command=lambda p=i: self._select_position(p))
            btn.pack(side=tk.LEFT, padx=2)
            self.pos_buttons[i] = btn

        # Simulations
        row2 = ttk.Frame(inner, style='CardFrame.TFrame')
        row2.pack(fill=tk.X)

        ttk.Label(row2, text="Simulaciones:", style='Section.TLabel').pack(side=tk.LEFT)
        self.simulaciones_var = tk.StringVar(value="10000")

        sim_entry = tk.Entry(row2, textvariable=self.simulaciones_var,
                            font=('Segoe UI', 12), width=10,
                            bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                            relief='flat', justify='center')
        sim_entry.pack(side=tk.RIGHT)

    def _crear_boton_simular(self, parent):
        btn_frame = ttk.Frame(parent, style='Dark.TFrame')
        btn_frame.pack(fill=tk.X, pady=(5, 0))

        self.simular_btn = tk.Button(btn_frame, text="SIMULAR MANO",
                                     font=('Segoe UI', 13, 'bold'),
                                     bg=ACCENT, fg=TEXT_PRIMARY,
                                     activebackground=ACCENT_HOVER,
                                     activeforeground=TEXT_PRIMARY,
                                     relief='flat', cursor='hand2',
                                     padx=20, pady=12,
                                     command=self.iniciar_simulacion)
        self.simular_btn.pack(fill=tk.X)

    def _crear_preview_cartas(self, parent):
        ttk.Label(parent, text="Vista previa", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 8))

        self.preview_frame = ttk.Frame(parent, style='Dark.TFrame')
        self.preview_frame.pack(fill=tk.BOTH, expand=True)

        self._update_card_preview("")

    def _insert_card(self, card):
        current = self.jugada_entry.get()
        if len(current) < 4:
            self.jugada_entry.insert(tk.END, card)
            self._on_hand_change(None)

    def _select_position(self, pos):
        self.orden_var.set(str(pos))
        for i, btn in self.pos_buttons.items():
            btn.configure(bg=ACCENT if i == pos else BG_INPUT)

    def _on_hand_change(self, event):
        hand = self.jugada_entry.get().upper()
        self._update_card_preview(hand)

    def _update_card_preview(self, hand):
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        cards_frame = ttk.Frame(self.preview_frame, style='Dark.TFrame')
        cards_frame.pack(expand=True)

        if not hand:
            for i in range(4):
                self._draw_empty_card(cards_frame, i)
            return

        valid_cards = {'R', 'C', 'S', 'A', '7', '6', '5', '4'}
        for i in range(4):
            if i < len(hand) and hand[i] in valid_cards:
                self._draw_card(cards_frame, i, hand[i])
            else:
                self._draw_empty_card(cards_frame, i)

    def _draw_card(self, parent, col, card):
        card_frame = tk.Frame(parent, bg=BG_DARK)
        card_frame.grid(row=0, column=col, padx=4, pady=4)
        self._create_spanish_card_widget(card_frame, card, small=False).pack()

    def _draw_empty_card(self, parent, col):
        card_frame = tk.Frame(parent, bg=BG_INPUT, relief='flat', bd=1,
                             highlightbackground=TEXT_MUTED, highlightthickness=1)
        card_frame.grid(row=0, column=col, padx=4, pady=4)

        tk.Label(card_frame, text="?", font=('Segoe UI', 24),
                bg=BG_INPUT, fg=TEXT_MUTED, width=3, height=1).pack(pady=(8, 0))
        tk.Label(card_frame, text="", font=('Segoe UI', 8),
                bg=BG_INPUT, fg=TEXT_MUTED).pack(pady=(0, 8))

    def _create_spanish_card_widget(self, parent, card, small=False):
        image = self._get_card_image(card, small=small)
        if image is not None:
            label = tk.Label(parent, image=image, bg=BG_DARK, bd=0, highlightthickness=0)
            label.image = image
            return label

        art = self.CARD_ART.get(card, {
            'numero': card,
            'palo': 'Mus',
            'simbolo': card,
            'color': CARD_TEXT,
        })
        nombre = self.CARD_NAMES.get(card, card)

        width = 74 if small else 94
        height = 106 if small else 134
        font_num = ('Georgia', 12 if small else 14, 'bold')
        font_symbol = ('Georgia', 18 if small else 28, 'bold')
        font_name = ('Segoe UI', 7 if small else 8, 'bold')
        font_suit = ('Segoe UI', 7 if small else 8)

        container = tk.Frame(parent, bg=CARD_BG, relief='raised', bd=1,
                             highlightbackground=CARD_BORDER, highlightthickness=2)

        canvas = tk.Canvas(container, width=width, height=height, bg=CARD_BG,
                           highlightthickness=0, bd=0)
        canvas.pack()

        accent_color = art['color']
        canvas.create_rectangle(8, 8, width - 8, height - 8, outline=accent_color, width=2)
        canvas.create_text(18, 18, text=art['numero'], font=font_num,
                           fill=accent_color, anchor='nw')
        canvas.create_text(width - 18, height - 18, text=art['numero'], font=font_num,
                           fill=accent_color, anchor='se')
        canvas.create_text(width / 2, height / 2 - 12, text=art['simbolo'],
                           font=font_symbol, fill=accent_color)
        canvas.create_text(width / 2, height / 2 + 18, text=nombre,
                           font=font_name, fill=CARD_TEXT)
        canvas.create_text(width / 2, height / 2 + 34, text=art['palo'],
                           font=font_suit, fill=CARD_TEXT)

        return container

    def _get_card_image(self, card, small=False):
        path = self._find_card_image_path(card)
        if path is None:
            return None

        cache_key = (card, small)
        if cache_key in self.card_image_cache:
            return self.card_image_cache[cache_key]

        try:
            image = tk.PhotoImage(file=str(path))
            if small:
                image = image.subsample(2, 2)
            self.card_image_cache[cache_key] = image
            return image
        except tk.TclError:
            return None

    def _find_card_image_path(self, card):
        base_name = self.CARD_IMAGE_FILES.get(card)
        if not base_name:
            return None

        for extension in ('.png', '.gif', '.ppm', '.pgm'):
            candidate = CARD_IMAGES_DIR / f"{base_name}{extension}"
            if candidate.exists():
                return candidate
        return None

    def validar_jugada(self, jugada):
        if len(jugada) != 4:
            return False, "La jugada debe tener exactamente 4 cartas"

        cartas_validas = {'R', 'C', 'S', 'A', '7', '6', '5', '4'}
        for carta in jugada:
            if carta not in cartas_validas:
                return False, f"Carta '{carta}' no valida. Usa: R, C, S, A, 7, 6, 5, 4"

        jugada_ordenada = ''.join(sorted(jugada, key=lambda x: "RCS7654A".index(x)))
        if jugada_ordenada not in self.mus_game.matriz_probabilidades['Mano'].values:
            return False, "Esta combinacion de cartas no es valida en el juego"

        return True, jugada_ordenada

    def validar_simulaciones(self, num_sim_str):
        try:
            num_sim = int(num_sim_str)
            if num_sim < 1 or num_sim > 10000000:
                return False, "El numero de simulaciones debe estar entre 1 y 10,000,000"
            return True, num_sim
        except ValueError:
            return False, "El numero de simulaciones debe ser un entero"

    def iniciar_simulacion(self):
        jugada = self.jugada_entry.get().upper().strip()
        es_valida, resultado = self.validar_jugada(jugada)

        if not es_valida:
            messagebox.showerror("Error", resultado)
            return

        jugada_ordenada = resultado

        es_valido, num_sim = self.validar_simulaciones(self.simulaciones_var.get())
        if not es_valido:
            messagebox.showerror("Error", num_sim)
            return

        try:
            orden = int(self.orden_var.get())
        except ValueError:
            messagebox.showerror("Error", "Posicion invalida")
            return

        self.simular_btn.config(state="disabled")
        self.mostrar_pantalla_carga()

        self.simulando = True
        thread = threading.Thread(target=self.ejecutar_simulacion,
                                  args=(jugada_ordenada, orden, num_sim))
        thread.daemon = True
        thread.start()

    def mostrar_pantalla_carga(self):
        self.ventana_carga = tk.Toplevel(self.root)
        self.ventana_carga.title("Simulando...")
        self.ventana_carga.geometry("360x160")
        self.ventana_carga.resizable(False, False)
        self.ventana_carga.transient(self.root)
        self.ventana_carga.grab_set()
        self.ventana_carga.configure(bg=BG_DARK)

        self.ventana_carga.geometry("+{}+{}".format(
            self.root.winfo_rootx() + 180,
            self.root.winfo_rooty() + 200
        ))

        frame_carga = tk.Frame(self.ventana_carga, bg=BG_DARK, padx=30, pady=20)
        frame_carga.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame_carga, text="Simulando manos...",
                font=('Segoe UI', 13, 'bold'), bg=BG_DARK, fg=TEXT_PRIMARY).pack(pady=(0, 15))

        self.progress = ttk.Progressbar(frame_carga, mode='indeterminate',
                                        style='Loading.Horizontal.TProgressbar')
        self.progress.pack(fill=tk.X, pady=(0, 15))
        self.progress.start(15)

        self.estado_label = tk.Label(frame_carga, text="Preparando simulacion...",
                                    font=('Segoe UI', 9), bg=BG_DARK, fg=TEXT_SECONDARY)
        self.estado_label.pack()

        self.ventana_carga.protocol("WM_DELETE_WINDOW", self.cancelar_simulacion)

    def ejecutar_simulacion(self, jugada, orden, num_sim):
        try:
            self.root.after(0, lambda: self.estado_label.config(text=f"Simulando {num_sim:,} manos..."))
            resultados = self.mus_game.simular_mano(jugada, orden, num_sim)
            self.root.after(0, lambda: self.mostrar_resultados(jugada, orden, resultados))
        except Exception as e:
            self.root.after(0, lambda: self.mostrar_error(str(e)))
        finally:
            self.simulando = False

    def mostrar_resultados(self, jugada, orden, resultados):
        if hasattr(self, 'ventana_carga'):
            self.ventana_carga.destroy()
        self.simular_btn.config(state="normal")

        ventana = tk.Toplevel(self.root)
        ventana.title("Resultados")
        ventana.geometry("680x520")
        ventana.resizable(False, False)
        ventana.configure(bg=BG_DARK)

        main = tk.Frame(ventana, bg=BG_DARK, padx=25, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        # Header
        tk.Label(main, text="Resultados de la Simulacion",
                font=('Segoe UI', 18, 'bold'), bg=BG_DARK, fg=TEXT_PRIMARY).pack(anchor=tk.W)

        sep = tk.Frame(main, height=2, bg=ACCENT)
        sep.pack(fill=tk.X, pady=(8, 15))

        # Hand info
        info_mano = self.mus_game.matriz_probabilidades[
            self.mus_game.matriz_probabilidades['Mano'] == jugada
        ].iloc[0]

        info_frame = tk.Frame(main, bg=BG_CARD, padx=15, pady=12)
        info_frame.pack(fill=tk.X, pady=(0, 15))

        # Cards display in results
        cards_row = tk.Frame(info_frame, bg=BG_CARD)
        cards_row.pack(fill=tk.X)

        left_info = tk.Frame(cards_row, bg=BG_CARD)
        left_info.pack(side=tk.LEFT)

        for i, card in enumerate(jugada):
            self._create_spanish_card_widget(left_info, card, small=True).pack(side=tk.LEFT, padx=2)

        right_info = tk.Frame(cards_row, bg=BG_CARD)
        right_info.pack(side=tk.RIGHT)

        prob_pct = info_mano['Probabilidad'] * 100
        tk.Label(right_info, text=f"Prob: {prob_pct:.4f}%",
                font=('Segoe UI', 10), bg=BG_CARD, fg=GOLD).pack(anchor=tk.E)
        tk.Label(right_info, text=f"Pares: {info_mano['Pares']}  |  Pos: {orden}",
                font=('Segoe UI', 10), bg=BG_CARD, fg=TEXT_SECONDARY).pack(anchor=tk.E)

        # Results table
        table_frame = tk.Frame(main, bg=BG_DARK)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('Lance', 'Individual', 'Equipo')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                           height=4, style='Results.Treeview')

        tree.heading('Lance', text='Lance')
        tree.heading('Individual', text='Individual')
        tree.heading('Equipo', text='Equipo')

        tree.column('Lance', width=180, anchor='w')
        tree.column('Individual', width=200, anchor='center')
        tree.column('Equipo', width=200, anchor='center')

        lances = [
            ('Grande', 'grandes', '\u2191'),
            ('Chica', 'chicas', '\u2193'),
            ('Pares', 'pares', '\u2261'),
            ('Juego', 'juego', '\u2605')
        ]

        for lance_nombre, lance_key, icon in lances:
            ind = resultados[lance_key]['prob_victoria_individual'] * 100
            eq = resultados[lance_key]['prob_victoria_equipo'] * 100
            tree.insert('', tk.END, values=(
                f"  {icon}  {lance_nombre}",
                f"{ind:.2f}%",
                f"{eq:.2f}%"
            ))

        tree.pack(fill=tk.BOTH, expand=True)

        # Bar chart visualization
        chart_frame = tk.Frame(main, bg=BG_DARK)
        chart_frame.pack(fill=tk.X, pady=(15, 0))

        tk.Label(chart_frame, text="Victoria Individual por Lance",
                font=('Segoe UI', 10, 'bold'), bg=BG_DARK, fg=TEXT_SECONDARY).pack(anchor=tk.W, pady=(0, 5))

        for lance_nombre, lance_key, icon in lances:
            prob = resultados[lance_key]['prob_victoria_individual'] * 100
            row = tk.Frame(chart_frame, bg=BG_DARK)
            row.pack(fill=tk.X, pady=2)

            tk.Label(row, text=f"{icon} {lance_nombre}", font=('Segoe UI', 9),
                    bg=BG_DARK, fg=TEXT_SECONDARY, width=10, anchor='w').pack(side=tk.LEFT)

            bar_bg = tk.Frame(row, bg=BG_INPUT, height=16)
            bar_bg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
            bar_bg.update_idletasks()

            bar_width = max(1, prob / 100)
            bar_color = GREEN if prob >= 50 else ACCENT if prob >= 25 else TEXT_MUTED
            bar = tk.Frame(bar_bg, bg=bar_color, height=16)
            bar.place(relwidth=bar_width, relheight=1.0)

            tk.Label(row, text=f"{prob:.1f}%", font=('Segoe UI', 9, 'bold'),
                    bg=BG_DARK, fg=TEXT_PRIMARY, width=7, anchor='e').pack(side=tk.RIGHT)

        # Close button
        close_btn = tk.Button(main, text="Cerrar", font=('Segoe UI', 10),
                             bg=BG_INPUT, fg=TEXT_PRIMARY,
                             activebackground=ACCENT, activeforeground=TEXT_PRIMARY,
                             relief='flat', padx=20, pady=6, cursor='hand2',
                             command=ventana.destroy)
        close_btn.pack(pady=(15, 0))

    def mostrar_error(self, mensaje):
        if hasattr(self, 'ventana_carga'):
            self.ventana_carga.destroy()
        self.simular_btn.config(state="normal")
        messagebox.showerror("Error", f"Error durante la simulacion: {mensaje}")

    def cancelar_simulacion(self):
        if self.simulando:
            resultado = messagebox.askyesno("Cancelar", "Estas seguro de que quieres cancelar la simulacion?")
            if resultado:
                self.simulando = False
                self.ventana_carga.destroy()
                self.simular_btn.config(state="normal")
        else:
            self.ventana_carga.destroy()


def main():
    root = tk.Tk()
    app = MusGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
