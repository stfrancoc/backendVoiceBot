# app/data/customers.py

# Base de datos sintética de clientes
CUSTOMERS = [
    {
        "ID_Cliente": 1,
        "Nombre_Cliente": "Juan Perez",
        "Fecha_Nacimiento": "1985-07-23",
        "Número_Documento": "12345678",
        "Teléfono_Contacto": "123-456-789",
        "Correo_Electrónico": "juan.perez@email.com",
        "Monto_Deuda": 5000,
        "Fecha_Vencimiento": "2024-12-01",
        "Estado_Cuenta": "En mora",
        "Historial_Pagos": [
            {"fecha": "2024-01-15", "monto": 500},
            {"fecha": "2024-05-20", "monto": 700},
        ]
    },
    {
        "ID_Cliente": 2,
        "Nombre_Cliente": "María Rodríguez",
        "Fecha_Nacimiento": "1992-11-10",
        "Número_Documento": "87654321",
        "Teléfono_Contacto": "987-654-321",
        "Correo_Electrónico": "maria.rodriguez@example.com",
        "Monto_Deuda": 3000,
        "Fecha_Vencimiento": "2025-03-15",
        "Estado_Cuenta": "Pendiente",
        "Historial_Pagos": [
            {"fecha": "2024-09-05", "monto": 1000},
        ]
    },
    {
        "ID_Cliente": 3,
        "Nombre_Cliente": "Carlos López",
        "Fecha_Nacimiento": "1978-04-25",
        "Número_Documento": "54321678",
        "Teléfono_Contacto": "789-456-123",
        "Correo_Electrónico": "carlos.lopez@gmail.com",
        "Monto_Deuda": 800,
        "Fecha_Vencimiento": "2024-12-31",
        "Estado_Cuenta": "Pagada",
        "Historial_Pagos": [
            {"fecha": "2024-11-20", "monto": 800},
        ]
    },
]
