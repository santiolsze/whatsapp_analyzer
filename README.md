# WHATSAPP ANALYZER

Este es un pequeño proyecto personal con el objetivo de familiarizarme con el lenguaje de programación Python y varias de las librerías más usadas en ciencia de datos. El código está disponible en el repositorio. Este es un ejemplo de la evolución de mis chats en el grupo LPB desde que fue creado.  

![](daily_plot_LPB.jpg)


Con este código, solo se requiere darle al programa:

* El nombre del archivo que sale de _Whatsapp -> Exportar chat
 * filename = "LPB.txt"
* El nombre de la otra persona (str) o la lista de nombres en un grupo, así como el nombre de uno.
 * others = ["Oco","Nacho","Mauro","Lorant"....]
 * me = "Santiago Olszevicki"

* El color con el que graficar. 
 *"indigo"


Para un grupo de amigos llamado LPB, se exporta un archivo de Whatsapp llamado "LPB.txt". Se pueden generar diversos gráficos, como mensajes agrupados por hora, por mes, por usuario y hasta una nube de palabras. 



filename = "LPB.txt"
color  = "lightblue"
me = "Santiago Olszevicki"
others = ["Oco", "Mauro"....] _y todos los otros miembros del grupo_

file_stripped = read_file(filename)
df = create_df(file_stripped)
df = add_msj_writer_groups(df, others)



