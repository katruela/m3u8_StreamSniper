import json
import os
import subprocess

def main():
    # Cargar los canales desde tu archivo canales.json
    with open("canales.json", "r", encoding="utf-8") as f:
        canales = json.load(f)

    m3u_content = "#EXTM3U\n"
    print(f"--- Iniciando extracción para {len(canales)} canales de Argentina ---")

    for canal in canales:
        nombre = canal["name"]
        url = canal["url"]
        print(f"\nProcesando: {nombre} ({url})...")
        
        # Ejecutamos el script optimizado (fetch_stream.py) pasándole la URL de cada canal
        env = os.environ.copy()
        env["TARGET_URL"] = url
        
        try:
            # Corre el script optimizado
            res = subprocess.run(
                ["python", "fetch_stream.py"],
                env=env,
                capture_output=True,
                text=True,
                timeout=45
            )
            
            # Buscar el enlace .m3u8 en la salida de la consola
            m3u8_link = None
            for line in res.stdout.splitlines():
                if "http" in line and ".m3u8" in line and "Found" not in line:
                    m3u8_link = line.strip()
                    break
            
            if m3u8_link:
                print(f"  [OK] Enlace capturado: {m3u8_link}")
                m3u_content += f'#EXTINF:-1 tvg-name="{nombre}",{nombre}\n{m3u8_link}\n'
            else:
                print(f"  [X] No se encontró enlace para {nombre}")

        except Exception as e:
            print(f"  [X] Error al procesar {nombre}: {e}")

    # Guardar la lista M3U final
    with open("argentina.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print("\n==========================================")
    print("¡Proceso finalizado! Archivo 'argentina.m3u' creado.")
    print("==========================================")

if __name__ == "__main__":
    main()
