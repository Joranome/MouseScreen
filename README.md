# MouseScreen

Este es un script diseñado en python para utilizar la cámara de un dispositivo como si fuera una pantalla táctil.

Se puede personalizar la configuración y colores desde las líneas 15 a la 30

## Información sobre personalizaciones
**seg**: son los segmentos en los que el mouse puede recorrer la pantalla, como si fuera una cuadrícula recorriendo la pantalla, para mejorar la precisión ya que como humanos nuestras manos pueden temblar, la cámara puede que se mueva o simplemente hay errores al detectar nuestra mano

**Color**: son los colores de cada herramienta en la interfaz, en el código está bien definido

**SCREEN_INI**: son las coordenadas de límites iniciales de la pantalla, puedes configurar para limitar el espacio a donde puedes acceder con el mouse
**SCREEN_FIN**: son las coordenadas de límites finales de la pantalla, igual que las iniciales pero finales xd

**click_ratio_fingers**: son pixeles de diferencia entre el cursor y el índice, o sea, qué tanto necesitamos bajar el índice para poder dar click, mientras más alto sea necesitaremos bajar menos el dedo, y en caso contrario mientras más bajo necesitaremos bajar más el dedo


## Info versiones
Funciona con la versión de Python 3.8.5
### Librerías usadas:
- OpenCV          4.6.0.66
- Mediapipe       0.8.10.1
- PyAutoGUI       0.9.53
- Numpy           1.19.2
