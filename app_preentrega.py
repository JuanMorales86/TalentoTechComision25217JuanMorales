#App de administracion de productos OnthePointService

from colorama import Fore, Back, Style, init

init(autoreset=True)

products_storage = {}

#UI
def user_monitor () :
    print('Bienvenido al sistema de registro de OnthePointService Por favor escoja entre las siguientes opciones: ')
    
    program_options = ['Registrar un nuevo producto', 'Ver todos los productos', 'Consultar un producto', 'Actualizar un producto', 'Eliminar un producto', 'Ingrese "salir" para terminar del programa']

    for i, productos in enumerate(program_options):
        print(Style.BRIGHT + f'------{i}) {productos}')

#Manejador de opciones
def main():
    user_monitor()
    while True:
        
        print('\n' + 50*'-')
        user_input = input('Ingrese una opción: \t').lower().strip()
        print(Back.WHITE + Style.BRIGHT + Fore.GREEN + '(--> AYUDA => ("M"))')
        match user_input:
            case '0':
                new_products()
            case '1':
                show_products()
            case '2':
                find_product()
            case '3':
                update_product()
            case '4':
                eliminate_product()
            case 'm':
                user_monitor()
            case user_input if user_input.startswith('s'):
                print('Saliendo del programa...')
                break
            case _: 
                print(Back.BLACK + Fore.RED + 'Opción no válida')
                continue


#Agregar
def new_products ():
    while True:
        print('\n--- Registrar un nuevo producto ---')
        product_id = auto_id()
        while True:
            product_name = input('Ingrese el nombre del producto: ').lower().strip()
            if product_name:
                break
            print(Back.BLACK + Fore.RED + 'el nombre del producto no puede estar vacio')
        while True:
            product_category = input('Ingrese la categoria del producto: ').lower().strip()
            if product_category:
                break
            print(Back.BLACK + Fore.RED + 'la categoria del producto no puede estar vacio')
        while True:
            """con try valido si es un numero lo que me ingreso el usuario por q si no me daba un error con el simple comprobador == '' entra string directo en el input a pesar de que use el parse float , mas que todo es para evitar el crasheo de la app y controlar mejor el error  """
            try: 
                product_price = float(input('Ingrese el precio del producto: ').strip())
                if product_price > 0:
                    break
                print('El precio no puede ser negativo')
            except ValueError:
                print(Back.BLACK + Fore.RED + 'Error: Debe ingresar un monto valido (numero)')
        while True:
            try:
                product_quantity = int(input('Ingrese la cantidad del producto: ').strip())
                if product_quantity > 0:
                    break
                print(Back.BLACK + Fore.RED + 'La cantidad no debe ser negativa')
            except ValueError:
                print(Back.BLACK + Fore.RED + 'Error: Debe ingresar una cantidad valida (numero)')
        
        products_storage[product_id] = {
            'name': product_name,
            'category': product_category,
            'price': product_price,
            'quantity': product_quantity
        }
        print(f'\n¡Éxito! Producto "{product_name}" registrado con el ID: {product_id}')
        
        decision = input("¿Desea agregar otro producto? (si/no): ").lower()
        if decision.startswith('n'):
            print("Regresando al menú principal...")
            break

#Mostrar
def show_products():
    print('\n--- Lista de Productos ---')
    if not products_storage:
        print(Back.BLACK + Fore.RED + 'No hay productos registrados.')
        return
    for product_id, product_info in products_storage.items():
        print(f'ID: {product_id}, Nombre: {product_info["name"]}, Categoria: {product_info["category"]},Precio: {product_info['price']}, Cantidad: {product_info['quantity']}')
    input("\nPresione enter para volver al menu principal")

#Busqueda
def find_product():
    while True:
        print('\n consultar un producto')
        
        if not products_storage:
            print(Back.BLACK + Fore.RED + 'No hay productos registrados.')
            input("\nPresione enter para volver al menu principal")
            return
        
        user_product = input('Ingrese el nombre del producto: ').lower().strip()
        find_products = False
        for product_id, product_info in products_storage.items():
            if user_product in product_info['name']:
                print(f'Id: {product_id}, Nombre: {product_info["name"]}, Precio: {product_info["price"]}, Cantidad: {product_info["quantity"]}')
                find_products = True
        if not find_products:
            print(f'No se enconotraron productos que comienzen con {user_product}')
        
        desicion = input('Deseas buscar otro producto o quieres volver al menu principal? (si/no): ')
        if desicion.startswith('n'):
                break

#Actualizacion   
def update_product():
    print('\n--- Actualizar un producto ---')

    if not products_storage:
        print(Back.BLACK + Fore.RED + 'No hay productos registrados.')
        return
    
    search_product = input('Ingrese el nombre o el ID del producto a actualizar: ').lower().strip()

    found_products = {} #para manejar multiples coincidencias

    #Buscar el producto para recordarle el id o el nombre
    for product_id, product_info in products_storage.items():
        # si el input lo comparo con un numero pero es un string necesito convertir el product_id a str para que funcione la comparacion, entonces si es un 1 como string y la comparacion es correcta 
        if search_product == str(product_id) or search_product in product_info['name']:
            found_products[product_id] = product_info
    
    if not found_products:
        print(f'No se encontraron productos que coincidan con "{search_product}"')
        return
    
    #Mostrarle lo que se encontro y que verifique el id del producto que quiere modificar
    print('\nProductos encontrados:')
    for product_id, product_info in found_products.items():
        print(f'ID:{product_id} Nombre: {product_info["name"]} Precio: {product_info["price"]} Cantidad: {product_info["quantity"]}')

    #seleccionar el producto a modificar con el id
    try:
        id_to_update = int(input('Ingrese el ID del producto a modificar: ').strip())
        if id_to_update not in products_storage:
            print("ID no valido")
            return
    except ValueError:
        print(Back.BLACK + Fore.RED + 'Debe ingresar un ID valido')
        return
    
    product_to_update = products_storage[id_to_update]
    print('Por favor ingrese los nuevos datos para modificar el producto (presione enter para mantener el valor actual)')

    #para el nombre
    new_name = input(f'Ingrese la nueva descripcion para el ({product_to_update['name']}: ').lower().strip()
    if new_name:
        product_to_update['name'] = new_name 
    new_category = input(f'Ingrese la nueva descripcion para el ({product_to_update['category']}: ').lower().strip()
    #Para la categoria
    if new_category:
        product_to_update['category'] = new_category
    # para el precio
    while True:
        new_price = float(input(f"Ingrese el nuevo precio ({product_to_update['price']}): ").strip())
        if not new_price: 
            break
        try:
            if new_price > 0:
                product_to_update['price'] = new_price
                break
            else:
                print(Back.BLACK + Fore.RED + 'El precio no puede ser negativo')
        except ValueError:
            print(Back.BLACK + Fore.RED + 'Debe ingresar un monto valido') 

    #para la cantidad
    while True:
        new_quantity = int(input(f"Ingrese la nueva cantidad ({product_to_update['quantity']}): ").strip())
        if not new_quantity: 
            break
        try:
            if new_quantity > 0:
                product_to_update['quantity'] = new_quantity
                break
            else:
                print(Back.BLACK + Fore.RED + 'El precio no puede ser negativo')
        except ValueError:
            print(Back.BLACK + Fore.RED + 'Debe ingresar un monto valido') 
    

    print(Back.GREEN + Fore.WHITE + f'\nModificacion exitosa el Producto con ID {id_to_update} ha sido actualizado con exito')
    input("\nPresione enter para volver al menu principal")

#Eliminacion
def eliminate_product():
    print('\n--- Eliminar un producto ---')

    if not products_storage:
        print(Back.BLACK + Fore.RED + 'No hay productos registrados.')
        return
    
    search_product_elim = input('Ingrese el nombre o el ID del producto a eliminar: ').lower().strip()

    found_product_list = {}

    for product_id, product_info in products_storage.items():
        if search_product_elim == str(product_id) or search_product_elim in product_info['name']:
            found_product_list[product_id] = product_info
    if not found_product_list:
        print(Back.BLACK + Fore.RED + f'El producto no esta asociado al nombre o al id ingresado {search_product_elim}')
        return
    
    print('\nProductos Encontrados')
    for product_id, product_info in found_product_list.items():
        print(f'ID: {product_id} Nombre: {product_info["name"]}')

    try:
        id_to_delete = int(input('Ingrese el ID del producto: ').strip())
        if id_to_delete not in products_storage:
            print(Back.BLACK + Fore.RED + 'Producto no encontrado')
            return
    except ValueError:
        print(Back.BLACK + Fore.RED + 'Debe ingresar un ID valido')
        return
    
    product_eliminate = products_storage[id_to_delete]
    products_storage.pop(id_to_delete)

    print(Back.GREEN + Fore.WHITE + f'El registro {product_eliminate["name"]} se elimino con exito')
    print('\n-----------------')
    input("\nPresione enter para volver al menu principal")


#Incremento automtico de IDs
def auto_id ():
    if not products_storage:
        return 1
    return max(products_storage.keys()) + 1

#Ejecucion Principal
main()


