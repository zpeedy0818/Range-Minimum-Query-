import math
import random
import time
import matplotlib.pyplot as plt

def build_sparse_table(arr):
    n = len(arr)
    # log2(n) tells us the maximum power of 2 needed
    max_pow = math.floor(math.log2(n)) + 1
    # st[i][j] will store the minimum in the range [i, i + 2^j - 1]
    st = [[0] * max_pow for _ in range(n)]
    
    # Base case: intervals of length 1 (2^0)
    for i in range(n):
        st[i][0] = arr[i]
        
    # Dynamic programming to fill the rest of the table
    j = 1
    while (1 << j) <= n:
        i = 0
        # The interval must fit within the array boundaries
        while (i + (1 << j) - 1) < n:
            st[i][j] = min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1])
            i += 1
        j += 1
        
    return st

def query_sparse_table(st, L, R):
    # Length of the interval
    length = R - L + 1
    # Find the largest power of 2 that fits in the interval
    j = math.floor(math.log2(length))
    # We overlap two intervals of length 2^j
    # First interval starts at L: [L, L + 2^j - 1]
    # Second interval ends at R: [R - 2^j + 1, R]
    return min(st[L][j], st[R - (1 << j) + 1][j])

def naive_query(arr, L, R):
    res = arr[L]
    for i in range(L + 1, R + 1):
        if arr[i] < res:
            res = arr[i]
    return res

def interactive_demo():
    print("\n" + "="*50)
    print("  Modo Demostración Interactiva (RMQ Sparse Table)")
    print("="*50)
    try:
        entrada = input("Ingresa una lista de números separados por espacio\n(o presiona Enter para usar uno aleatorio de 15 elementos): ")
        if entrada.strip():
            arr = [int(x) for x in entrada.split()]
        else:
            n = 15
            arr = [random.randint(1, 100) for _ in range(n)]
            
        print(f"\nArreglo a evaluar (índices 0 a {len(arr)-1}):")
        for i, val in enumerate(arr):
            print(f"[{i}]:{val}", end="  ")
        print("\n")
        
        # Construimos Sparse Table
        start_build = time.time()
        st = build_sparse_table(arr)
        print(f"-> ¡Sparse Table construida en {time.time() - start_build:.6f} segundos!\n")
        
        while True:
            rango = input(f"Ingresa el rango L y R separados por espacio (ej. '2 8') o 'q' para salir: ")
            if rango.lower() == 'q':
                break
            try:
                partes = rango.split()
                if len(partes) != 2:
                    raise ValueError
                L, R = int(partes[0]), int(partes[1])
                
                if L < 0 or R >= len(arr) or L > R:
                    print(f"  [Error]: Rango inválido. Asegúrate de que 0 <= L <= R < {len(arr)}")
                    continue
                
                # Consultas
                res_st = query_sparse_table(st, L, R)
                res_naive = naive_query(arr, L, R)
                
                print(f"  => Mínimo en rango [{L}, {R}] es: {res_st} (Búsqueda ingenua coincide: {res_st == res_naive})\n")
            except ValueError:
                print("  [Error]: Entrada no válida. Ingresa dos números enteros separados por espacio.")
    except KeyboardInterrupt:
        pass
    print("\nSaliendo de la demostración. ¡Gracias!")

def benchmark():
    print("Iniciando Benchmarking para Range Minimum Query (RMQ)...")
    sizes = [1000, 5000, 10000, 20000, 50000, 100000]
    num_queries = 10000
    
    naive_times = []
    st_build_times = []
    st_query_times = []
    st_total_times = []
    
    print(f"\nGenerando resultados para {num_queries} consultas (queries):")
    print(f"{'n':>8} | {'Naive Total (s)':>16} | {'ST Build (s)':>15} | {'ST Query Total (s)':>18} | {'ST Total (s)':>15}")
    print("-" * 83)
    
    for n in sizes:
        arr = [random.randint(1, 10**9) for _ in range(n)]
        
        # Generar queries aleatorios
        queries = []
        for _ in range(num_queries):
            L = random.randint(0, n - 1)
            R = random.randint(L, n - 1)
            queries.append((L, R))
            
        # Benchmark Naive
        start_naive = time.time()
        for L, R in queries:
            naive_query(arr, L, R)
        end_naive = time.time()
        naive_time = end_naive - start_naive
        
        # Benchmark Sparse Table
        start_build = time.time()
        st = build_sparse_table(arr)
        end_build = time.time()
        st_build_time = end_build - start_build
        
        start_query = time.time()
        for L, R in queries:
            query_sparse_table(st, L, R)
        end_query = time.time()
        st_query_time = end_query - start_query
        
        st_total_time = st_build_time + st_query_time
        
        naive_times.append(naive_time)
        st_build_times.append(st_build_time)
        st_query_times.append(st_query_time)
        st_total_times.append(st_total_time)
        
        print(f"{n:>8} | {naive_time:>16.6f} | {st_build_time:>15.6f} | {st_query_time:>18.6f} | {st_total_time:>15.6f}")

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, naive_times, marker='o', label=f'Ingenua $O(n)$ - {num_queries} queries', color='#e74c3c', linewidth=2)
    plt.plot(sizes, st_total_times, marker='s', label=f'Sparse Table (Build + {num_queries} queries)', color='#2980b9', linewidth=2)
    plt.plot(sizes, st_query_times, marker='^', linestyle='--', label=f'Sparse Table (Solo {num_queries} queries) $O(1)$', color='#2ecc71', linewidth=2)
    
    plt.title('Comparativa de Tiempos en Range Minimum Query (RMQ)\nBúsqueda Ingenua $O(n)$ vs Sparse Table $O(1)$', fontsize=14, fontweight='bold')
    plt.xlabel('Tamaño del Arreglo (n)', fontsize=12)
    plt.ylabel('Tiempo (Segundos)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('rmq_benchmark_plot.png', dpi=300)
    print("\nGráfico generado exitosamente y guardado como 'rmq_benchmark_plot.png'.")

if __name__ == "__main__":
    import sys
    # Fijamos la semilla para hacer los resultados predecibles en la comparación masiva
    random.seed(42) 
    
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        interactive_demo()
    else:
        print("Tip: Puedes ejecutar 'python rmq_benchmark.py --demo' para probar tus propios datos de manera interactiva.\n")
        benchmark()
