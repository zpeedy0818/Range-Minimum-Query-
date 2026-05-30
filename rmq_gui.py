import tkinter as tk
import random
import math

class RMQVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador RMQ - Sparse Table (O(n) -> O(1))")
        
        # Paleta de colores oscura, estética "Catppuccin Macchiato" / moderna
        self.bg_color = "#24273A"      # Fondo principal
        self.box_color = "#363A4F"     # Cajas neutras
        self.text_color = "#CAD3F5"    # Texto normal
        self.cyan_color = "#8AADF4"    # Primer bloque potencia de 2
        self.magenta_color = "#C6A0F6" # Segundo bloque potencia de 2
        self.green_color = "#A6DA95"   # Respuesta correcta

        self.root.configure(bg=self.bg_color)
        self.root.geometry("1000x550")
        self.root.resizable(False, False)

        # Título
        title = tk.Label(root, text="Demostración Sparse Table - RMQ", font=("Consolas", 24, "bold"), bg=self.bg_color, fg=self.text_color)
        title.pack(pady=(20, 0))

        # Canvas para dibujar
        self.canvas = tk.Canvas(root, width=950, height=350, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack()

        # Etiqueta de información matemática
        self.info_label = tk.Label(root, text="Construyendo estructura...", font=("Consolas", 14), bg=self.bg_color, fg=self.green_color)
        self.info_label.pack(pady=(0, 20))

        # Variables lógicas
        self.n = 16 # Tamaño del arreglo
        self.arr = [random.randint(10, 99) for _ in range(self.n)]
        self.st = self.build_sparse_table(self.arr)
        
        # Variables de dibujo
        self.block_size = 45
        self.padding = 10
        self.total_w = self.n * (self.block_size + self.padding)
        self.start_x = (950 - self.total_w) // 2 + 5
        self.start_y = 150

        # Iniciar el bucle de animación
        self.root.after(1000, self.animate_query)

    def build_sparse_table(self, arr):
        n = len(arr)
        max_pow = math.floor(math.log2(n)) + 1
        st = [[0] * max_pow for _ in range(n)]
        for i in range(n):
            st[i][0] = arr[i]
        j = 1
        while (1 << j) <= n:
            i = 0
            while (i + (1 << j) - 1) < n:
                st[i][j] = min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1])
                i += 1
            j += 1
        return st

    def draw_base_array(self):
        self.canvas.delete("all")
        for i in range(self.n):
            x = self.start_x + i * (self.block_size + self.padding)
            y = self.start_y
            
            # Dibujar Índice
            self.canvas.create_text(x + self.block_size//2, y - 20, text=str(i), fill="#8087A2", font=("Consolas", 11, "bold"))
            
            # Dibujar Caja
            self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill=self.box_color, outline="#494D64", width=2, tags="box")
            
            # Dibujar Número
            self.canvas.create_text(x + self.block_size//2, y + self.block_size//2, text=str(self.arr[i]), fill=self.text_color, font=("Consolas", 16, "bold"), tags="text")

    def animate_query(self):
        self.draw_base_array()
        
        # Generar rango aleatorio (L, R)
        L = random.randint(0, self.n - 3)
        R = random.randint(L + 2, self.n - 1) # Aseguramos un rango de al menos 3 para que se note el solapamiento

        length = R - L + 1
        j = math.floor(math.log2(length))
        pow_size = 1 << j # 2^j

        val1 = self.st[L][j]
        val2 = self.st[R - pow_size + 1][j]
        ans = min(val1, val2)

        # Actualizar texto explicativo
        explicacion = (
            f"Consulta Rango: [{L}, {R}]  |  Longitud: {length}\n"
            f"Usando solapamiento de dos bloques precalculados de tamaño 2^{j} = {pow_size}"
        )
        self.info_label.config(text=explicacion, fg=self.text_color)

        # ====== Dibujar Bloque Izquierdo (Cyan) ======
        x1_left = self.start_x + L * (self.block_size + self.padding) - 5
        x2_left = self.start_x + (L + pow_size) * (self.block_size + self.padding) - self.padding + 5
        y1_left = self.start_y - 40
        y2_left = self.start_y + self.block_size + 10
        
        # Recuadro Punteado
        self.canvas.create_rectangle(x1_left, y1_left, x2_left, y2_left, outline=self.cyan_color, width=3, dash=(6, 4))
        # Etiqueta
        self.canvas.create_text(x1_left + (x2_left-x1_left)//2, y1_left - 15, text=f"st[{L}][{j}] = {val1}", fill=self.cyan_color, font=("Consolas", 13, "bold"))

        # ====== Dibujar Bloque Derecho (Magenta) ======
        x1_right = self.start_x + (R - pow_size + 1) * (self.block_size + self.padding) - 5
        x2_right = self.start_x + (R + 1) * (self.block_size + self.padding) - self.padding + 5
        y1_right = self.start_y - 10
        y2_right = self.start_y + self.block_size + 40
        
        # Recuadro Punteado
        self.canvas.create_rectangle(x1_right, y1_right, x2_right, y2_right, outline=self.magenta_color, width=3, dash=(6, 4))
        # Etiqueta
        self.canvas.create_text(x1_right + (x2_right-x1_right)//2, y2_right + 15, text=f"st[{R - pow_size + 1}][{j}] = {val2}", fill=self.magenta_color, font=("Consolas", 13, "bold"))

        # ====== Resaltar la Respuesta (Caja Verde) ======
        ans_idx = -1
        # Buscamos la posición del mínimo en el rango para pintarlo
        for i in range(L, R + 1):
            if self.arr[i] == ans:
                ans_idx = i
                break
        
        if ans_idx != -1:
            x = self.start_x + ans_idx * (self.block_size + self.padding)
            y = self.start_y
            self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill=self.green_color, outline="#8BD5CA", width=3)
            self.canvas.create_text(x + self.block_size//2, y + self.block_size//2, text=str(self.arr[ans_idx]), fill="#181825", font=("Consolas", 16, "bold"))

        # Agregar el resultado final al texto explicativo
        self.info_label.config(text=explicacion + f"\nResultado Final: min({val1}, {val2}) = {ans}")

        # Programar la siguiente animación en 5 segundos
        self.root.after(5000, self.animate_query)

if __name__ == "__main__":
    root = tk.Tk()
    app = RMQVisualizer(root)
    root.mainloop()
