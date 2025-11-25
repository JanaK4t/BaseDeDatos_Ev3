import pymongo
from datetime import datetime
from bson.objectid import ObjectId
import sys

URI = "mongodb+srv://baabello_db_user:EaQrEapWte3r0b5F@clusterpulento.hvytzul.mongodb.net/?appName=ClusterPulento"

try:
    client = pymongo.MongoClient(URI)
    db = client["BookStore_Evaluacion"] 
    
    col_tipos = db["tipos"]
    col_productos = db["productos"]
    col_clientes = db["clientes"]
    col_resenas = db["resenas"]
    
    print("Conexión exitosa a MongoDB Atlas")
except Exception as e:
    print(f"Error de conexión: {e}")
    sys.exit()


def inicializar_datos():
    if col_tipos.count_documents({}) == 0:
        print("Migrando datos: Tipos de producto...")
        lista_tipos = [
            {"codigo": "LIB", "descripcion": "Libro"},
            {"codigo": "REV", "descripcion": "Revista"},
            {"codigo": "SEP", "descripcion": "Separata"}
        ]
        col_tipos.insert_many(lista_tipos)

    if col_productos.count_documents({}) == 0:
        print("Migrando datos: Productos BookStore...")
        
        id_lib = col_tipos.find_one({"codigo": "LIB"})["_id"]
        id_rev = col_tipos.find_one({"codigo": "REV"})["_id"]
        id_sep = col_tipos.find_one({"codigo": "SEP"})["_id"]
        
        lista_productos = [
            {"sku": "LIB00001", "titulo": "Power Builder", "autor": "William B. Heys", "precio": 5000, "id_tipo": id_lib},
            {"sku": "LIB00002", "titulo": "Visual Basic", "autor": "Joel Carrasco", "precio": 4000, "id_tipo": id_lib},
            {"sku": "LIB00003", "titulo": "Programación C/S con VB", "autor": "Kenneth L. Spenver", "precio": 4000, "id_tipo": id_lib},
            {"sku": "LIB00004", "titulo": "JavaScript a través de Ejemplos", "autor": "Jery Honeycutt", "precio": 3000, "id_tipo": id_lib},
            {"sku": "LIB00005", "titulo": "UNIX en 12 lecciones", "autor": "Juan Matías Matías", "precio": 2000, "id_tipo": id_lib},
            {"sku": "LIB00006", "titulo": "Visual Basic y SQL Server", "autor": "Eric G. Coronel Castillo", "precio": 3000, "id_tipo": id_lib},
            {"sku": "LIB00007", "titulo": "Power Builder y SQL Server", "autor": "Eric G. Coronel Castillo", "precio": 3000, "id_tipo": id_lib},
            {"sku": "LIB00008", "titulo": "PHP y MySQL", "autor": "Eric G. Coronel", "precio": 5000, "id_tipo": id_lib},

            {"sku": "REV00001", "titulo": "Eureka", "autor": "GrapPeru", "precio": 4000, "id_tipo": id_rev},
            {"sku": "REV00002", "titulo": "El Programador", "autor": "Desarrolla Software SAC", "precio": 6000, "id_tipo": id_rev},
            {"sku": "REV00003", "titulo": "La Revista del Programador", "autor": "DotNET SAC", "precio": 10000, "id_tipo": id_rev},

            {"sku": "SEP00001", "titulo": "Java Orientado a Objetos", "autor": "Eric G. Coronel C.", "precio": 1000, "id_tipo": id_sep},
            {"sku": "SEP00002", "titulo": "Desarrollo Web con Java", "autor": "Eric G. Coronel C.", "precio": 1000, "id_tipo": id_sep},
            {"sku": "SEP00003", "titulo": "Electrónica Aplicada", "autor": "Hugo Valencia M.", "precio": 2000, "id_tipo": id_sep},
            {"sku": "SEP00004", "titulo": "Circuitos Digitales", "autor": "Hugo Valencia M.", "precio": 2000, "id_tipo": id_sep},
            {"sku": "SEP00005", "titulo": "SQL Server Básico", "autor": "Sergio Matsukawa", "precio": 2000, "id_tipo": id_sep},
            {"sku": "SEP00006", "titulo": "SQL Server Avanzado", "autor": "Sergio Matsukawa", "precio": 2000, "id_tipo": id_sep},
            {"sku": "SEP00007", "titulo": "Windows Server Fundamentos", "autor": "Hugo Valencia M.", "precio": 1000, "id_tipo": id_sep},
            {"sku": "SEP00008", "titulo": "windows Server Administración", "autor": "Sergio Matsukawa", "precio": 1000, "id_tipo": id_sep}
        ]
        col_productos.insert_many(lista_productos)

    if col_clientes.count_documents({}) == 0:
        
        print("Migrando datos: Clientes...")
        lista_clientes = [
            {"nombre": "Manuel", "apellido": "Zambrano Sanchez", "usuario": "Manuuel"},
            {"nombre": "Selma", "apellido": "Wilson", "usuario": "SelmmaW"},
            {"nombre": "Carlos", "apellido": "Hernandez Garcia", "usuario": "Karlitox"},
            {"nombre": "Lucia", "apellido": "Rodriguez Gonzalez", "usuario": "Lucy234"},
            {"nombre": "Francisco", "apellido": "Sanchez Garcia", "usuario": "Panxito"},
            {"nombre": "Almendra", "apellido": "Quispe Flores", "usuario": "Almendritaa"}
        ]
        col_clientes.insert_many(lista_clientes)
    
    if col_resenas.count_documents({}) == 0:
        print("Generando reseña de prueba...")
        cli = col_clientes.find_one({"usuario": "Manuuel"})["_id"]
        prod = col_productos.find_one({"sku": "LIB00001"})["_id"]
        
        col_resenas.insert_one({
            "id_cliente": cli,
            "id_producto": prod,
            "valoracion": 5,
            "comentario": "Excelente libro para aprender.",
            "fecha": datetime.now()
        })

inicializar_datos()


def ver_resenas():
    print("\n--- LISTADO DE RESEÑAS ---")
    resenas = col_resenas.find()

    for r in resenas:
        cliente = col_clientes.find_one({"_id": r["id_cliente"]})
        producto = col_productos.find_one({"_id": r["id_producto"]})

        if not cliente or not producto:
            print(f"Error: Reseña {r['_id']} tiene datos corruptos (cliente o producto no encontrado).")
            continue

        tipo = col_tipos.find_one({"_id": producto["id_tipo"]})
        
        desc_tipo = tipo['descripcion'] if tipo else "Tipo desconocido"

        print(f"ID: {r['_id']}")
        print(f"Cliente: {cliente['nombre']} {cliente['apellido']}")
        print(f"Producto: {producto['titulo']} ({desc_tipo})")
        print(f"Precio: ${producto['precio']}")
        print(f"Nota: {r['valoracion']}/5")
        print(f"Opinión: {r['comentario']}")
        print("-----------------------------------------")

def nueva_resena():
    print("\n--- NUEVA RESEÑA ---")
    
    print("¿Quién eres?")
    clientes = list(col_clientes.find())
    for i, c in enumerate(clientes):
        print(f"{i+1}. {c['nombre']} {c['apellido']}")
    idx_c = int(input("Número de cliente: ")) - 1
    id_cliente_sel = clientes[idx_c]["_id"]

    print("\n¿Qué leíste?")
    productos = list(col_productos.find())
    for i, p in enumerate(productos):
        print(f"{i+1}. {p['titulo']} (Autor: {p['autor']})")
    idx_p = int(input("Número de producto: ")) - 1
    id_producto_sel = productos[idx_p]["_id"]

    nota = int(input("Calificación (1-5): "))
    texto = input("Tu comentario: ")

    col_resenas.insert_one({
        "id_cliente": id_cliente_sel,
        "id_producto": id_producto_sel,
        "valoracion": nota,
        "comentario": texto,
        "fecha": datetime.now()
    })
    print("Reseña guardada.")

def actualizar_resena():
    ver_resenas()
    id_str = input("\nCopia el ID de la reseña a editar: ")
    nuevo_txt = input("Nuevo comentario: ")
    try:
        col_resenas.update_one(
            {"_id": ObjectId(id_str)}, 
            {"$set": {"comentario": nuevo_txt}}
        )
        print("Editado correctamente.")
    except:
        print("Error de ID.")

def eliminar_resena():
    ver_resenas()
    id_str = input("\nCopia el ID de la reseña a borrar: ")
    try:
        col_resenas.delete_one({"_id": ObjectId(id_str)})
        print("Eliminado correctamente.")
    except:
        print("Error de ID.")

def menu():
    op = 0
    while op != 5:
        print("\n=== BOOKSTORE ===")
        print("1. Ver Reseñas")
        print("2. Agregar Reseña")
        print("3. Editar Reseña")
        print("4. Eliminar Reseña")
        print("5. Salir")
        
        op = input("Seleccione: ")
        if op == '1': ver_resenas()
        elif op == '2': nueva_resena()
        elif op == '3': actualizar_resena()
        elif op == '4': eliminar_resena()
        elif op == '5': break

if __name__ == "__main__":
    menu()