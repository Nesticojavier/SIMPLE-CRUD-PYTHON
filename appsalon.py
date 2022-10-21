import pymysql


print("GESTOR DE BASE DE DATOS")

try:
    conexion = pymysql.connect( host="localhost",
                                user="root",
                                password="",
                                db="appsalon")

    try:
        while True:
            print("Menú se uso: \n"
                "CREATE para crear una nueva cita \n"
                "READ para ver los servicios disponibles \n"
                "UPDATE para cambiar una fecha, hora o servicio \n"
                "DELETE para cancelar una cita \n"
                "EXIT para salir del interprete \n"
                )
            entrada = input("> ")
            
            if entrada == "CREATE":

                # Pedir datos de entrada
                ci = int(input("ci: "))
                nombre = input("nombre: ")
                apellido = input("apellido: ")
                fecha = input("fecha: ")
                hora = input("hora: ")
                servicio = int(input("servicio: "))

                # insertar cliente
                with conexion.cursor() as cursor:
                    
                    # cosultas
                    consultaCLiente = "INSERT INTO clientes (ci, nombre, apellido) VALUES (%s, %s, %s);"
                    consultaCita = "INSERT INTO citas (fecha, hora, cliente_ci) VALUES (%s, %s, %s);"
                    consultaCitasServicios = "INSERT INTO citasServicios (citaId, serviciosId) VALUES (%s, %s);"
                    
                    # llamadas a las tablas de clientes y citas
                    cursor.execute(consultaCLiente, (ci, nombre, apellido))
                    conexion.commit()
                    cursor.execute(consultaCita, (fecha, hora, ci))
                    conexion.commit()

                    # obtener id de la ultima cita insertada en citaId
                    cursor.execute("SELECT last_insert_id();")
                    citaId = cursor.fetchone()
                    
                    # agregar a la tabla de citasServicios
                    consultaCitaServicio = "INSERT INTO citasServicios (citaId, servicioId) VALUES (%s, %s);"
                    cursor.execute(consultaCitaServicio, (citaId, servicio))
                    conexion.commit()

            elif entrada == "READ":

                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM servicios")
                    servicios = cursor.fetchall()

                for servicio in servicios:
                    print(servicio)
            
            elif entrada == "UPDATE":
                ci = int(input("ci: "))

                with conexion.cursor() as cursor:
                    consulta = "UPDATE citas SET fecha = %s WHERE cliente_ci = %s;"
                    nuevaFecha = input("nueva fecha: ")
                    cursor.execute(consulta, (nuevaFecha, ci))
                    conexion.commit()

            # elif entrada == "DELETE":
            #     ci = int(input("ci: "))

            #     with conexion.cursor() as cursor:
            #         consultaCitaServicio = "DELETE FROM citasServicios WHERE "
            #         nuevaFecha = input("nueva fecha: ")
            #         cursor.execute(consulta, (nuevaFecha, ci))
            #         conexion.commit()


            elif entrada == "EXIT":
                break

    finally:
        conexion.close()

except Exception as e:
    print("Error al conectar: ", e)
    exit()

