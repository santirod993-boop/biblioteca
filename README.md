# Sistema de Gestión de Biblioteca

Trabajo Final Integrador - Algoritmos y Estructuras de Datos - ISI - Ciclo 2026

## Integrantes del grupo

- Alejo Arias 
- Nayhara Romero 
- Santiago Rodriguez
- Fabrizio Zanier 

- (agregar el resto de los integrantes)

## Comisión



## Descripción general del sistema

Este sistema simula el funcionamiento de una biblioteca mediante una aplicación
de consola desarrollada en Python. Permite:

- Registrar usuarios.
- Registrar libros (incluyendo suma de ejemplares si el libro ya existe).
- Realizar préstamos de libros, controlando la disponibilidad de ejemplares.
- Realizar devoluciones, calculando automáticamente una multa si el libro se
  devuelve fuera del plazo permitido (7 días).
- Consultar la disponibilidad actual de todos los libros.
- Consultar los préstamos que todavía no fueron devueltos.
- Ver estadísticas generales: cantidad total de préstamos, devoluciones,
  dinero recaudado en multas y el libro más solicitado.

El sistema aplica validaciones sobre todos los datos ingresados por el
usuario (por ejemplo, no permite ingresar texto donde se espera un número,
ni continuar si un DNI o código de libro no existe), y utiliza contadores y
acumuladores para llevar el registro de préstamos, devoluciones y multas.

## Instrucciones de ejecución

1. Tener instalado Python 3 en la computadora.
2. Descargar o clonar este repositorio.
3. Abrir una terminal en la carpeta del proyecto.
4. Se mostrará un menú por consola. Ingresar el número de la opción deseada
   y seguir las instrucciones en pantalla.

### Ejemplo de uso básico

1. Registrar un usuario (opción 1).
2. Registrar un libro (opción 2).
3. Prestar el libro al usuario (opción 3), indicando el día actual (por
   ejemplo, día 1).
4. Devolver el libro (opción 4), indicando el día de devolución. Si pasaron
   más de 7 días desde el préstamo, el sistema calculará una multa
   automáticamente.
5. Consultar estadísticas (opción 7) para ver el resumen general.

## Diseño previo (pseudocódigo)

Antes de programar, el equipo diseñó la lógica del sistema en pseudocódigo con ayuda de IA
(formato Ambiente/Proceso). El archivo se encuentra en


## Uso de Inteligencia Artificial

Durante el desarrollo del proyecto se utilizó **Claude (Anthropic)** como
herramienta de apoyo, específicamente para:

- Generar una primera versión del pseudocódigo (formato Ambiente/Proceso)
  a partir de la consigna de la cátedra.
- Generar una primera versión del código en Python con la estructura general
  del sistema (funciones, validaciones, manejo de errores).
- Resolver dudas puntuales sobre manejo de excepciones  y
  buenas prácticas de modularización.

Todo el código generado fue **revisado, probado y comprendido por todos los
integrantes del grupo**, quienes pueden explicar el funcionamiento de cada
función, las validaciones implementadas y las decisiones tomadas durante el
desarrollo. Se realizaron ajustes propios del equipo sobre la propuesta
inicial (detallar aquí qué cambiaron, si corresponde).


```
