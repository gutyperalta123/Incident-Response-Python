import sqlite3

def consultar():
    conn = sqlite3.connect('seguridad.db')
    cursor = conn.cursor()

    print("\n" + "="*50)
    print("📋 HISTORIAL COMPLETO DE INVESTIGACIONES (SQL)")
    print("="*50)
    
    query_todas = "SELECT fecha, ip, score, pais FROM historial_ips ORDER BY fecha DESC LIMIT 20"
    rows = cursor.execute(query_todas).fetchall()

    if not rows:
        print("La base de datos está vacía.")
    else:
        for f in rows:
            print(f"🕒 {f[0]} | 🌐 {f[1]} | ⭐ Score: {f[2]} | 📍 {f[3]}")

    print("\n" + "="*50)
    print("🚨 IPs REINCIDENTES (Más de 1 aparición)")
    print("="*50)
    
    query_reincidentes = '''SELECT ip, COUNT(*) as total, MAX(fecha) 
                            FROM historial_ips 
                            GROUP BY ip 
                            HAVING total > 1 
                            ORDER BY total DESC'''
    
    reincidencias = cursor.execute(query_reincidentes).fetchall()
    
    if not reincidencias:
        print("No se encontraron IPs repetidas todavía.")
    else:
        for r in reincidencias:
            print(f"🔥 IP: {r[0]} | 🔄 Veces detectada: {r[1]} | 📅 Última: {r[2]}")

    conn.close()

if __name__ == "__main__":
    consultar()










