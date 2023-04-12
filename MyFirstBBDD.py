#MENUS EN INFERFAZ GRAFICA
from tkinter import *
#ABRIR Y GUARDAR ARCHIVOS
from tkinter import filedialog 

#IMPORTAR LAS VENTANAS
from tkinter import messagebox

import tkinter as tk

#IMPORTAR LIBRERIA BBDD
import sqlite3


#-------INTERFAZ-----------------------------------------------------------------------------------


root_inicio=Tk()

#VARIABLES DATOS VENTANA CREACION#    
DATONOMBRE=StringVar()
DATOAPELLIDO=StringVar()
DATODIR=StringVar()
DATOPASS=StringVar()
#VARIABLES DATOS VENTANA CREACION# 


DATOID=StringVar()   

root_inicio.title("BBDD Usuarios v0.01")
root_inicio.iconbitmap("boll.ico")
root_inicio.geometry("480x480")

ventana_seleccion=Frame(root_inicio)
ventana_seleccion.pack()


Label(root_inicio,text="¿Que accion desea realizar en la Base de Datos de Usuarios?\nLa primera vez que añada un usuario estara creando la BBDD",fg="black",font=("Times New Roman",14)).pack()

fotoVoli=PhotoImage(file="Voli.png")
Label(root_inicio,image=fotoVoli).pack()


#---VARIABLE GLOBAL PARA EVITAR CREAR BBDD 2 VECES Y FLAGS DE VENTANAS---

VENTANACREACIONONESTADO=False

def limpiar_campos(variableTexto):

	DATONOMBRE.set("")
	DATOAPELLIDO.set("")
	DATODIR.set("")
	DATOPASS.set("")
	variableTexto.config(state=NORMAL)
	variableTexto.delete(1.0,END)
	variableTexto.config(state=DISABLED)

#VENTANA EMERGENTE Predeterminada (AVISO)

def info_emergente(nombreVentana,contenidoVentanaEmergente):

	messagebox.showinfo(nombreVentana,contenidoVentanaEmergente)


def conectar_BBDD():
	
	excepcion_activada=False
	
	try:
		mi_conexion=sqlite3.connect("Usuarios")
		mi_cursor=mi_conexion.cursor()
		mi_cursor.execute('''
				CREATE TABLE DATOS_USUARIOS(
				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				NOMBRE_USUARIO VARCHAR(50),
				PASSWORD VARCHAR(50),
				APELLIDO VARCHAR(30),
				DIRECCION VARCHAR(25),
				COMENTARIOS VARCHAR(200)
				)
				''')
	except:
		info_emergente("BBDD","La BBDD ya existe, no necesita conectar")
		excepcion_activada=True


	if excepcion_activada==False:
		info_emergente("BBDD","BBDD Conectada y creada con éxito")



def cerrar_BBDD():
	valorElegido=messagebox.askokcancel("Salir","¿Quieres salir sin guardar? tu trabajo no se guardara")
	
	if valorElegido==True:
		root_inicio.destroy()

def eliminar_usuario():
	try:

		miConexion=sqlite3.connect("Usuarios")
		miCursor=miConexion.cursor()	

		miCursor.execute("DELETE FROM DATOS_USUARIOS WHERE ID= ?",DATOID.get())

		miConexion.commit()

		info_emergente("Usuario Removido","El usuario ha sido removido con exito")
	except:
		info_emergente("BBDD","El usuario no existe o el archivo ha fallado")




def chupar_info():


	banderaDatoVacio=0
	i=0
	

	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()
	
	tuplaCarga=(DATONOMBRE.get(),DATOPASS.get(),DATOAPELLIDO.get(),DATODIR.get(),cuadro_texto_comentario.get(1.0,END))

	for data in tuplaCarga:
		if data=="":
			banderaDatoVacio=1




	if banderaDatoVacio==0:	
		miCursor.execute("INSERT INTO DATOS_USUARIOS VALUES(NULL,?,?,?,?,?)",tuplaCarga)

		miConexion.commit()

		info_emergente("Usuario Creado","El usuario ha sido añadido con exito")
		limpiar_campos(cuadro_texto_comentario)

	else:
		info_emergente("ERROR","Existen uno o mas campos vacios")



def ventana_seleccion_ID(StringTitulo,StringSub,StringBuscar,comando,posicionX,posicionY):

	global ventanaSeleccionID

	ventanaSeleccionID=Toplevel()

	ventanaSeleccionID.title("BBDD Usuarios v0.01 - "+StringTitulo)
	ventanaSeleccionID.iconbitmap("boll.ico")

	ventanaSeleccionID.geometry("520x480+600+150")

	Label(ventanaSeleccionID,text="Ingrese la ID del usuario a "+StringSub,fg="black",font=("Times New Roman",20)).pack()

	BBDD_frame=Frame(ventanaSeleccionID)
	BBDD_frame.pack()

	cuadro_texto_ID=Entry(BBDD_frame,width=40,textvariable=DATOID)
	cuadro_texto_ID.grid(row=3,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_ID.config(fg="red",justify="left")

	indicadorIDACT=Label(BBDD_frame,text="Codigo ID:",fg="black",font=("Times New Roman",16),cursor="hand2")
	indicadorIDACT.grid(row=3,column=0,padx=10,pady=10,sticky="w")

	botonBuscarID=Button(ventanaSeleccionID,text=StringBuscar,font=("Times New Roman",20),cursor="hand2",command=comando)
	botonBuscarID.place(x=posicionX,y=posicionY)

	botonVolver=Button(ventanaSeleccionID,text="Volver",font=("Times New Roman",16),cursor="hand2",command=ventanaSeleccionID.destroy)
	botonVolver.place(x=380,y=300)

	#botonBuscarID=Button(ventanaSeleccionID,text="Buscar y traer usuario por ID para leer",font=("Times New Roman",20),cursor="hand2",command=ventana_leer)
	#botonBuscarID.place(x=10,y=330)

def modificar_usuario():

	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()
	tuplaCarga=(DATONOMBRE.get(),DATOPASS.get(),DATOAPELLIDO.get(),DATODIR.get(),cuadro_texto_comentarioACT.get(1.0,END),DATOID.get())

	miCursor.execute("UPDATE DATOS_USUARIOS SET NOMBRE_USUARIO = ?, PASSWORD = ?, APELLIDO=?,DIRECCION=?,COMENTARIOS=? WHERE ID =?",tuplaCarga)

	miConexion.commit()

	info_emergente("Actualizacion Usuario","Usuario modificado con exito")


def ventana_leer():

	global cuadro_texto_comentarioACT
	global DATOID


	ventanaLeer=Toplevel()
	ventanaSeleccionID.destroy()

	ventanaLeer.title("BBDD Usuarios v0.01 - Leer usuario")
	ventanaLeer.iconbitmap("boll.ico")

	ventanaLeer.geometry("520x480+600+150")


	BBDD_frame=Frame(ventanaLeer)
	BBDD_frame.pack()

	#CUADROS DE TEXTO DONDE ESCRIBIR------------------------------


	cuadro_texto_nombreLeer=Entry(BBDD_frame,width=40,textvariable=DATONOMBRE,state= "disabled")
	cuadro_texto_nombreLeer.grid(row=1,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_nombreLeer.config(fg="red",justify="left")


	cuadro_texto_pssLeer=Entry(BBDD_frame,width=40,textvariable=DATOPASS,state= "disabled")
	cuadro_texto_pssLeer.grid(row=2,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_pssLeer.config(show="*",fg="red",justify="left")

	cuadro_texto_apeLeer=Entry(BBDD_frame,width=40,textvariable=DATOAPELLIDO,state= "disabled")
	cuadro_texto_apeLeer.grid(row=3,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_apeLeer.config(fg="red",justify="left")

	cuadro_texto_dirLeer=Entry(BBDD_frame,width=40,textvariable=DATODIR,state= "disabled")
	cuadro_texto_dirLeer.grid(row=4,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_dirLeer.config(fg="red",justify="left")

	cuadro_texto_comentarioLeer=Text(BBDD_frame,width=30,height=5)
	cuadro_texto_comentarioLeer.grid(row=5,column=1,padx=5,pady=20,sticky="w")

	#Caja comentario sub elemento en esta seccion----->

	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()
	
	miCursor.execute("SELECT * FROM DATOS_USUARIOS WHERE ID = ?",DATOID.get())

	
	usuario=miCursor.fetchall()
	if usuario:
		DATONOMBRE.set(usuario[0][1])
		DATOPASS.set(usuario[0][2])
		DATOAPELLIDO.set(usuario[0][3])
		DATODIR.set(usuario[0][4])
		cuadro_texto_comentarioLeer.insert(1.0,usuario[0][5])
		DATOID.set("")
	else:
		limpiar_campos(cuadro_texto_comentarioLeer)
		info_emergente("ERROR","El usuario no existe")
		DATOID.set("")
	
	miConexion.commit()
	cuadro_texto_comentarioLeer.config(fg="red",state=DISABLED)

	#Scrollbar de caja de comentarios

	scroll_barLeer=Scrollbar(BBDD_frame,command=cuadro_texto_comentarioLeer.yview,cursor="hand2")
	scroll_barLeer.grid(row=5,column=2,sticky="nsew")

	cuadro_texto_comentarioLeer.config(yscrollcommand=scroll_barLeer.set)

	#FIN CUADROS DE TEXTO DONDE ESCRIBIR---------------------------

	#TEXTOS INDICADORES--------------------------------------------


	indicadorNombreLeer=Label(BBDD_frame,text="Nombre:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorNombreLeer.grid(row=1,column=0,padx=10,pady=10,sticky="w")

	indicadorPssLeer=Label(BBDD_frame,text="Contraseña:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorPssLeer.grid(row=2,column=0,padx=10,pady=10,sticky="w")

	indicadorApeLeer=Label(BBDD_frame,text="Apellido:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorApeLeer.grid(row=3,column=0,padx=10,pady=10,sticky="w")

	indicadorDirLeer=Label(BBDD_frame,text="Direccion:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorDirLeer.grid(row=4,column=0,padx=10,pady=10,sticky="w")

	indicadorDirLeer=Label(BBDD_frame,text="Comentarios:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorDirLeer.grid(row=5,column=0,padx=10,pady=10,sticky="w")

	#FIN TEXTOS INDICADORES-----------------------------------------

	#BOTONES DE INTERFAZ--------------------------------------------

	botonVolver=Button(ventanaLeer,text="Volver",font=("Times New Roman",16),cursor="hand2",command=ventanaLeer.destroy)
	botonVolver.place(x=380,y=410)



	#FIN BOTONES DE INTERFAZ----------------------------------------



def ventana_actualizar_usuario():

	global cuadro_texto_comentarioACT

	ventanaActualizar=Toplevel()
	ventanaSeleccionID.destroy()

	ventanaActualizar.title("BBDD Usuarios v0.01 - Actualizar usuario")
	ventanaActualizar.iconbitmap("boll.ico")

	ventanaActualizar.geometry("520x480+600+150")


	BBDD_frame=Frame(ventanaActualizar)
	BBDD_frame.pack()

	#CUADROS DE TEXTO DONDE ESCRIBIR------------------------------


	cuadro_texto_nombreACT=Entry(BBDD_frame,width=40,textvariable=DATONOMBRE)
	cuadro_texto_nombreACT.grid(row=1,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_nombreACT.config(fg="red",justify="left")


	cuadro_texto_pssACT=Entry(BBDD_frame,width=40,textvariable=DATOPASS)
	cuadro_texto_pssACT.grid(row=2,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_pssACT.config(show="*",fg="red",justify="left")

	cuadro_texto_apeACT=Entry(BBDD_frame,width=40,textvariable=DATOAPELLIDO)
	cuadro_texto_apeACT.grid(row=3,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_apeACT.config(fg="red",justify="left")

	cuadro_texto_dirACT=Entry(BBDD_frame,width=40,textvariable=DATODIR)
	cuadro_texto_dirACT.grid(row=4,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_dirACT.config(fg="red",justify="left")

	#Caja comentario sub elemento en esta seccion----->

	cuadro_texto_comentarioACT=Text(BBDD_frame,width=30,height=5)
	cuadro_texto_comentarioACT.grid(row=5,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_comentarioACT.config(fg="red")



	#Scrollbar de caja de comentarios

	scroll_barACT=Scrollbar(BBDD_frame,command=cuadro_texto_comentarioACT.yview,cursor="hand2")
	scroll_barACT.grid(row=5,column=2,sticky="nsew")

	cuadro_texto_comentarioACT.config(yscrollcommand=scroll_barACT.set)


	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()
	try:
		miCursor.execute("SELECT * FROM DATOS_USUARIOS WHERE ID = ?",DATOID.get())
	except:
		info_emergente("ERROR","ID incorrecta")
	
	usuario=miCursor.fetchall()
		
	if usuario:
		DATONOMBRE.set(usuario[0][1])
		DATOPASS.set(usuario[0][2])
		DATOAPELLIDO.set(usuario[0][3])
		DATODIR.set(usuario[0][4])
		cuadro_texto_comentarioACT.insert(1.0,usuario[0][5])
		DATOID.set("")
	else:
		limpiar_campos(cuadro_texto_comentarioACT)
		info_emergente("BBDD","El usuario no existe o el archivo ha fallado")
		DATOID.set("")



	miConexion.commit()


	#FIN CUADROS DE TEXTO DONDE ESCRIBIR---------------------------

	#TEXTOS INDICADORES--------------------------------------------


	indicadorNombreACT=Label(BBDD_frame,text="Nombre:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorNombreACT.grid(row=1,column=0,padx=10,pady=10,sticky="w")

	indicadorPssACT=Label(BBDD_frame,text="Contraseña:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorPssACT.grid(row=2,column=0,padx=10,pady=10,sticky="w")

	indicadorApeACT=Label(BBDD_frame,text="Apellido:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorApeACT.grid(row=3,column=0,padx=10,pady=10,sticky="w")

	indicadorDirACT=Label(BBDD_frame,text="Direccion:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorDirACT.grid(row=4,column=0,padx=10,pady=10,sticky="w")

	indicadorDirACT=Label(BBDD_frame,text="Comentarios:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorDirACT.grid(row=5,column=0,padx=10,pady=10,sticky="w")

	#FIN TEXTOS INDICADORES-----------------------------------------

	#BOTONES DE INTERFAZ--------------------------------------------


	botonActualizar=Button(ventanaActualizar,text="Actualizar usuario",font=("Times New Roman",20),cursor="hand2",command=modificar_usuario)
	botonActualizar.place(x=150,y=400)
	botonVolver=Button(ventanaActualizar,text="Volver",font=("Times New Roman",16),cursor="hand2",command=ventanaActualizar.destroy)
	botonVolver.place(x=380,y=410)

	#FIN BOTONES DE INTERFAZ----------------------------------------

	#MENU SUPERIOR--------------------------------------------------

	barra_menu=Menu(ventanaActualizar)
	ventanaActualizar.config(menu=barra_menu)



	#AGREGAR OPCIONES SUBMENU

	borrar=Menu(barra_menu,tearoff=0)

	borrar.add_command(label="Borrar campos",command=lambda:limpiar_campos(cuadro_texto_comentarioACT))


	#PARA QUE SE VEAN EN LA VENTANA

	barra_menu.add_cascade(label="Borrar", menu=borrar)



def ventana_creacion_usuario():

	global VENTANACREACIONONESTADO
	global root_creacion
	global cuadro_texto_comentario
	
	root_creacion=Toplevel()

	VENTANACREACIONONESTADO=True

	root_creacion.title("BBDD Usuarios v0.01 - Creacion Usuario")
	root_creacion.iconbitmap("boll.ico")

	root_creacion.geometry("520x480+600+150")


	BBDD_frame=Frame(root_creacion)
	BBDD_frame.pack()

#CUADROS DE TEXTO DONDE ESCRIBIR------------------------------


	cuadro_texto_nombre=Entry(BBDD_frame,width=40,textvariable=DATONOMBRE)
	cuadro_texto_nombre.grid(row=1,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_nombre.config(fg="red",justify="left")


	cuadro_texto_pss=Entry(BBDD_frame,width=40,textvariable=DATOPASS)
	cuadro_texto_pss.grid(row=2,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_pss.config(show="*",fg="red",justify="left")

	cuadro_texto_ape=Entry(BBDD_frame,width=40,textvariable=DATOAPELLIDO)
	cuadro_texto_ape.grid(row=3,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_ape.config(fg="red",justify="left")

	cuadro_texto_dir=Entry(BBDD_frame,width=40,textvariable=DATODIR)
	cuadro_texto_dir.grid(row=4,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_dir.config(fg="red",justify="left")

	#Caja comentario sub elemento en esta seccion----->

	cuadro_texto_comentario=Text(BBDD_frame,width=30,height=5)
	cuadro_texto_comentario.grid(row=5,column=1,padx=5,pady=20,sticky="w")
	cuadro_texto_comentario.config(fg="red")

	#Scrollbar de caja de comentarios

	scroll_bar=Scrollbar(BBDD_frame,command=cuadro_texto_comentario.yview,cursor="hand2")
	scroll_bar.grid(row=5,column=2,sticky="nsew")

	cuadro_texto_comentario.config(yscrollcommand=scroll_bar.set)

	#FIN CUADROS DE TEXTO DONDE ESCRIBIR---------------------------

	#TEXTOS INDICADORES--------------------------------------------


	indicadorNombre=Label(BBDD_frame,text="Nombre:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorNombre.grid(row=1,column=0,padx=10,pady=10,sticky="w")

	indicadorPss=Label(BBDD_frame,text="Contraseña:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorPss.grid(row=2,column=0,padx=10,pady=10,sticky="w")

	indicadorApe=Label(BBDD_frame,text="Apellido:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorApe.grid(row=3,column=0,padx=10,pady=10,sticky="w")

	indicadorDir=Label(BBDD_frame,text="Direccion:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorDir.grid(row=4,column=0,padx=10,pady=10,sticky="w")

	indicadorComment=Label(BBDD_frame,text="Comentarios:",fg="black",font=("Times New Roman",12),cursor="hand2")
	indicadorComment.grid(row=5,column=0,padx=10,pady=10,sticky="w")

	#FIN TEXTOS INDICADORES-----------------------------------------

	#BOTONES DE INTERFAZ--------------------------------------------


	boton_crear=Button(root_creacion,text="Crear usuario",font=("Times New Roman",20),cursor="hand2",command=chupar_info)
	boton_crear.place(x=180,y=400)
	boton_volver=Button(root_creacion,text="Volver",font=("Times New Roman",16),cursor="hand2",command=root_creacion.destroy)
	boton_volver.place(x=380,y=410)

	#FIN BOTONES DE INTERFAZ----------------------------------------

	#MENU SUPERIOR--------------------------------------------------

	barra_menu=Menu(root_creacion)
	root_creacion.config(menu=barra_menu)



	#AGREGAR OPCIONES SUBMENU

	borrar=Menu(barra_menu,tearoff=0)

	borrar.add_command(label="Borrar campos",command=lambda:limpiar_campos(cuadro_texto_comentario))


	#PARA QUE SE VEAN EN LA VENTANA

	barra_menu.add_cascade(label="Borrar", menu=borrar)





#BOTONES DE INTERFAZ--------------------------------------------


boton_crear=Button(root_inicio,text="Crear",font=("Times New Roman",14),cursor="hand2",command=ventana_creacion_usuario)
boton_crear.place(x=80,y=200)

botonActualizar=Button(root_inicio,text="Actualizar",font=("Times New Roman",14),cursor="hand2",command=lambda:ventana_seleccion_ID("Modificar Usuario","modificar","Buscar y traer usuario por ID para modificar",ventana_actualizar_usuario,10,400))
botonActualizar.place(x=210,y=200)

botonLeer=Button(root_inicio,text="Leer",font=("Times New Roman",14),cursor="hand2",command=lambda:ventana_seleccion_ID("Leer Usuario","leer","Buscar y traer usuario por ID para leer",ventana_leer,40,400))
botonLeer.place(x=150,y=200)
boton_eliminar=Button(root_inicio,text="Eliminar",font=("Times New Roman",14),cursor="hand2",command=lambda:ventana_seleccion_ID("Remover Usuario","remover","Buscar y traer usuario por ID para eliminar",eliminar_usuario,15,400))
boton_eliminar.place(x=320,y=200)

#FIN BOTONES DE INTERFAZ----------------------------------------

#MENU SUPERIOR--------------------------------------------------

barra_menu=Menu(root_inicio)
root_inicio.config(menu=barra_menu)

BBDD=Menu(barra_menu, tearoff=0)


#AGREGAR OPCIONES SUBMENU
BBDD.add_command(label="Conectar",command=conectar_BBDD)
BBDD.add_separator()
BBDD.add_command(label="Salir",command=cerrar_BBDD)


ayuda=Menu(barra_menu,tearoff=0)

ayuda.add_command(label="Licencia")
ayuda.add_separator()
ayuda.add_command(label="Acerca de")

#PARA QUE SE VEAN EN LA VENTANA

barra_menu.add_cascade(label="BBDD", menu=BBDD)

barra_menu.add_cascade(label="Ayuda", menu=ayuda)


root_inicio.mainloop()

#-------FIN CREAR BASE DE DATOS--------------------------------------------------------------------
