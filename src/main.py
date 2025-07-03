import tkinter as tk
from tkinter import ttk, messagebox
import threading
from models.mus_game import MusGame

class MusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Mus")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Instancia del juego
        self.mus_game = MusGame()
        
        # Variables
        self.simulando = False
        
        # Crear la interfaz principal
        self.crear_interfaz_principal()
        
    def crear_interfaz_principal(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Simulador de Mus", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame para la jugada
        jugada_frame = ttk.LabelFrame(main_frame, text="Jugada", padding="10")
        jugada_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(jugada_frame, text="Introduce tu mano (4 cartas):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.jugada_entry = ttk.Entry(jugada_frame, width=10, font=("Arial", 12))
        self.jugada_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(jugada_frame, text="Cartas válidas: R, C, S, A, 7, 6, 5, 4", font=("Arial", 9)).grid(row=2, column=0, sticky=tk.W)
        
        # Frame para el orden
        orden_frame = ttk.LabelFrame(main_frame, text="Posición", padding="10")
        orden_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(orden_frame, text="Selecciona tu posición en la mesa:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.orden_var = tk.StringVar(value="1")
        orden_combo = ttk.Combobox(orden_frame, textvariable=self.orden_var, values=["1", "2", "3", "4"],
                                  state="readonly", width=10)
        orden_combo.grid(row=1, column=0, sticky=tk.W)
        
        # Frame para simulaciones
        sim_frame = ttk.LabelFrame(main_frame, text="Simulaciones", padding="10")
        sim_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(sim_frame, text="Número de simulaciones:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.simulaciones_var = tk.StringVar(value="1000")
        sim_entry = ttk.Entry(sim_frame, textvariable=self.simulaciones_var, width=10)
        sim_entry.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        ttk.Label(sim_frame, text="(Entre 1 y 10,000,000)", font=("Arial", 9)).grid(row=2, column=0, sticky=tk.W)
        
        # Botón simular
        self.simular_btn = ttk.Button(main_frame, text="Simular Mano", command=self.iniciar_simulacion)
        self.simular_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Configurar el grid
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def validar_jugada(self, jugada):
        """Valida que la jugada sea correcta"""
        # Verificar longitud
        if len(jugada) != 4:
            return False, "La jugada debe tener exactamente 4 cartas"
        
        # Verificar cartas válidas
        cartas_validas = {'R', 'C', 'S', 'A', '7', '6', '5', '4'}
        for carta in jugada:
            if carta not in cartas_validas:
                return False, f"Carta '{carta}' no válida. Usa: R, C, S, A, 7, 6, 5, 4"
        
        # Verificar que la jugada existe en el dataframe
        jugada_ordenada = ''.join(sorted(jugada, key=lambda x: "RCS7654A".index(x)))
        if jugada_ordenada not in self.mus_game.matriz_probabilidades['Mano'].values:
            return False, "Esta combinación de cartas no es válida en el juego"
        
        return True, jugada_ordenada
        
    def validar_simulaciones(self, num_sim_str):
        """Valida el número de simulaciones"""
        try:
            num_sim = int(num_sim_str)
            if num_sim < 1 or num_sim > 10000000:
                return False, "El número de simulaciones debe estar entre 1 y 10,000,000"
            return True, num_sim
        except ValueError:
            return False, "El número de simulaciones debe ser un entero"
    
    def iniciar_simulacion(self):
        """Inicia la simulación en un hilo separado"""
        # Validar jugada
        jugada = self.jugada_entry.get().upper().strip()
        es_valida, resultado = self.validar_jugada(jugada)
        
        if not es_valida:
            messagebox.showerror("Error", resultado)
            return
        
        jugada_ordenada = resultado
        
        # Validar número de simulaciones
        es_valido, num_sim = self.validar_simulaciones(self.simulaciones_var.get())
        
        if not es_valido:
            messagebox.showerror("Error", num_sim)
            return
        
        # Validar orden
        try:
            orden = int(self.orden_var.get())
        except ValueError:
            messagebox.showerror("Error", "Posición inválida")
            return
        
        # Deshabilitar botón y mostrar pantalla de carga
        self.simular_btn.config(state="disabled")
        self.mostrar_pantalla_carga()
        
        # Iniciar simulación en hilo separado
        self.simulando = True
        thread = threading.Thread(target=self.ejecutar_simulacion, 
                                args=(jugada_ordenada, orden, num_sim))
        thread.daemon = True
        thread.start()
    
    def mostrar_pantalla_carga(self):
        """Muestra la pantalla de carga"""
        self.ventana_carga = tk.Toplevel(self.root)
        self.ventana_carga.title("Simulando...")
        self.ventana_carga.geometry("300x150")
        self.ventana_carga.resizable(False, False)
        self.ventana_carga.transient(self.root)
        self.ventana_carga.grab_set()
        
        # Centrar ventana
        self.ventana_carga.geometry("+{}+{}".format(
            self.root.winfo_rootx() + 150,
            self.root.winfo_rooty() + 150
        ))
        
        # Contenido
        frame_carga = ttk.Frame(self.ventana_carga, padding="20")
        frame_carga.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame_carga, text="Simulando manos...", font=("Arial", 12)).pack(pady=(0, 20))
        
        # Barra de progreso indeterminada
        self.progress = ttk.Progressbar(frame_carga, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 20))
        self.progress.start()
        
        # Etiqueta de estado
        self.estado_label = ttk.Label(frame_carga, text="Preparando simulación...")
        self.estado_label.pack()
        
        # Protocolo de cierre
        self.ventana_carga.protocol("WM_DELETE_WINDOW", self.cancelar_simulacion)
    
    def ejecutar_simulacion(self, jugada, orden, num_sim):
        """Ejecuta la simulación en un hilo separado"""
        try:
            # Actualizar estado
            self.root.after(0, lambda: self.estado_label.config(text=f"Simulando {num_sim:,} manos..."))
            
            # Ejecutar simulación
            resultados = self.mus_game.simular_mano(jugada, orden, num_sim)
            
            # Mostrar resultados en el hilo principal
            self.root.after(0, lambda: self.mostrar_resultados(jugada, orden, resultados))
            
        except Exception as e:
            self.root.after(0, lambda: self.mostrar_error(str(e)))
        finally:
            self.simulando = False
    
    def mostrar_resultados(self, jugada, orden, resultados):
        """Muestra los resultados de la simulación"""
        # Cerrar ventana de carga
        if hasattr(self, 'ventana_carga'):
            self.ventana_carga.destroy()
        
        # Habilitar botón
        self.simular_btn.config(state="normal")
        
        # Crear ventana de resultados
        ventana_resultados = tk.Toplevel(self.root)
        ventana_resultados.title("Resultados de la Simulación")
        ventana_resultados.geometry("600x400")
        ventana_resultados.resizable(False, False)
        
        # Obtener información de la mano
        info_mano = self.mus_game.matriz_probabilidades[
            self.mus_game.matriz_probabilidades['Mano'] == jugada
        ].iloc[0]
        
        # Frame principal
        main_frame = ttk.Frame(ventana_resultados, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información de la mano
        info_frame = ttk.LabelFrame(main_frame, text="Información de la Mano", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(info_frame, text=f"Mano: {jugada}", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Orden: {orden}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Probabilidad de obtenerla: {info_mano['Probabilidad']*100:.4f}%").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Tipo de pares: {info_mano['Pares']}").pack(anchor=tk.W)
        
        # Tabla de resultados
        tabla_frame = ttk.LabelFrame(main_frame, text="% Victoria", padding="10")
        tabla_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview
        columns = ('Lance', 'Individual', 'Equipo')
        tree = ttk.Treeview(tabla_frame, columns=columns, show='headings', height=8)
        
        # Definir encabezados
        tree.heading('Lance', text='Lance')
        tree.heading('Individual', text='Individual')
        tree.heading('Equipo', text='Equipo')
        
        # Configurar ancho de columnas
        tree.column('Lance', width=150)
        tree.column('Individual', width=150)
        tree.column('Equipo', width=150)
        
        # Insertar datos
        lances = [
            ('Grande', 'grandes'),
            ('Chica', 'chicas'),
            ('Pares', 'pares'),
            ('Juego', 'juego')
        ]
        
        for lance_nombre, lance_key in lances:
            individual = f"{resultados[lance_key]['prob_victoria_individual']*100:.2f}%"
            equipo = f"{resultados[lance_key]['prob_victoria_equipo']*100:.2f}%"
            tree.insert('', tk.END, values=(lance_nombre, individual, equipo))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón cerrar
        ttk.Button(main_frame, text="Cerrar", command=ventana_resultados.destroy).pack(pady=10)
    
    def mostrar_error(self, mensaje):
        """Muestra un error y cierra la ventana de carga"""
        if hasattr(self, 'ventana_carga'):
            self.ventana_carga.destroy()
        
        self.simular_btn.config(state="normal")
        messagebox.showerror("Error", f"Error durante la simulación: {mensaje}")
    
    def cancelar_simulacion(self):
        """Cancela la simulación"""
        if self.simulando:
            resultado = messagebox.askyesno("Cancelar", "¿Estás seguro de que quieres cancelar la simulación?")
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