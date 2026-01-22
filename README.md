# 🛡️ Automated IP Incident Response System

Sistema de triaje automatizado para el análisis de amenazas de red, integrando múltiples capas de persistencia de datos.

## 🚀 Stack Tecnológico
* **Lenguaje:** Python (Requests, PyMongo, SQLite3)
* **Bases de Datos:** SQL (SQLite) y NoSQL (MongoDB)
* **Automatización:** Windows Batch Scripting
* **Integración:** AbuseIPDB API

## ⚙️ Arquitectura de Datos
El sistema procesa logs de IPs sospechosas y distribuye la información de la siguiente manera:
1. **Reportes Ejecutivos (CSV):** Segmentación automática para bloqueo inmediato o investigación.
2. **Historial de Reincidencia (SQL):** Almacenamiento estructurado para detectar ataques recurrentes.
3. **Metadata Forense (MongoDB):** Almacenamiento de la respuesta JSON cruda para análisis profundo.

## 🛠️ Instalación
```bash
pip install requests pymongo
python incident_response.py