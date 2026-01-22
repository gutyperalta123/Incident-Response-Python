import requests
import sqlite3
import pymongo
import csv
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
API_KEY = 'aqui iria tu key'
MONGO_URI = "mongodb://localhost:27017/"

# --- FUNCIONES DE BASE DE DATOS ---
def inicializar_sql():
    conn = sqlite3.connect('seguridad.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS historial_ips 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       fecha TEXT, ip TEXT, pais TEXT, score INTEGER, isp TEXT)''')
    conn.commit()
    conn.close()

def guardar_en_sql(dato):
    conn = sqlite3.connect('seguridad.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO historial_ips (fecha, ip, pais, score, isp) 
                      VALUES (?, ?, ?, ?, ?)''', 
                   (dato['fecha'], dato['ip'], dato['pais'], dato['score'], dato['isp']))
    conn.commit()
    conn.close()

def intentar_guardar_mongo(data):
    try:
        cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        db = cliente["Ciberseguridad_Data"]
        cliente.admin.command('ping') # Verifica si Mongo está activo
        data["fecha_captura"] = datetime.now()
        db["Reportes_Completos"].insert_one(data)
        print(f" [🍃] Guardado en MongoDB")
    except:
        print(f" [⚠️] MongoDB no disponible (paso omitido)")

# --- LÓGICA DE INVESTIGACIÓN ---
def investigar_ip(ip):
    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {'Accept': 'application/json', 'Key': API_KEY}
    params = {'ipAddress': ip, 'maxAgeInDays': '90'}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()['data']
            
            # 1. Guardar en NoSQL (Data Cruda)
            intentar_guardar_mongo(data)
            
            # 2. Estructurar para SQL y CSV
            res = {
                'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'ip': ip,
                'pais': data['countryCode'],
                'score': data['abuseConfidenceScore'],
                'reportes': data['totalReports'],
                'isp': data['isp']
            }
            
            # 3. Guardar en SQL (Historial)
            guardar_en_sql(res)
            print(f" [💾] Guardado en SQL (IP: {ip})")
            return res
    except Exception as e:
        print(f"Error con IP {ip}: {e}")
    return None

def ejecutar_sistema():
    inicializar_sql()
    if not os.path.exists('sospechosos.txt'):
        print("Error: No se encuentra sospechosos.txt")
        return

    with open('sospechosos.txt', 'r') as f:
        ips = [linea.strip() for linea in f if linea.strip()]

    print(f"\n--- Iniciando Patrullaje sobre {len(ips)} IPs ---")
    
    # Preparar CSVs
    f1 = open('1_BLOQUEAR_INMEDIATO.csv', 'w', newline='', encoding='utf-8')
    f2 = open('2_SOSPECHOSOS_A_INVESTIGAR.csv', 'w', newline='', encoding='utf-8')
    f3 = open('3_USUARIOS_LIMPIOS.csv', 'w', newline='', encoding='utf-8')
    
    campos = ['fecha', 'ip', 'pais', 'score', 'reportes', 'isp']
    w1, w2, w3 = csv.DictWriter(f1, fieldnames=campos), csv.DictWriter(f2, fieldnames=campos), csv.DictWriter(f3, fieldnames=campos)
    for w in [w1, w2, w3]: w.writeheader()

    for ip in ips:
        res = investigar_ip(ip)
        if res:
            if res['score'] >= 75: 
                w1.writerow(res); print(f" [❌] {ip} -> BLOQUEO")
            elif res['score'] >= 25: 
                w2.writerow(res); print(f" [⚠️] {ip} -> INVESTIGAR")
            else: 
                w3.writerow(res); print(f" [✅] {ip} -> LIMPIA")

    f1.close(); f2.close(); f3.close()
    print("\n--- Proceso Terminado: Reportes actualizados ---")

if __name__ == "__main__":
    ejecutar_sistema()







