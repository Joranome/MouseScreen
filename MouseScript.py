import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import ctypes

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Configuración incremento del mouse
# Esto es para mejorar la precisión del cursor al ignorar los temblores o movimientos minimos en la mano
# Mientras más grande, más precisión habrá pero no se podrá dar clicks en algunos lugares de la pantalla
# 25 es el valor que yo encontré más cómodo
seg = 25

# Personalizar colores (B, G, R)
color_mouse_pointer = (0, 0, 0)     # Color del puntero del mouse
color_mouse_normal = (64, 64, 64)   # Color del mouse
color_mouse_click = (255, 64, 64)   # Color del mouse al dar click
color_screen = (255, 0, 0)          # Color de la pantalla
screen_opacity = 0.5                # Opacidad de la pantalla

# Personalizar pantalla (por defecto pantalla completa)
SCREEN_X_INI, SCREEN_Y_INI = (0, 0)
SCREEN_X_FIN, SCREEN_Y_FIN = pyautogui.size()
X_Y_INI = 100

# Mientras más grande, menos tendrás que doblar el dedo índice para dar click
click_ratio_fingers = 50

# Codigo
aspect_ratio_screen = (SCREEN_X_FIN - SCREEN_X_INI) / \
    (SCREEN_Y_FIN - SCREEN_Y_INI)
print("aspect_ratio_screen:", aspect_ratio_screen)


def calculate_distance(x1, y1, x2, y2):
    return np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))


def detect_finger_down(hand_landmarks):
    finger_down = False
    color = color_mouse_normal

    x1 = int(hand_landmarks.landmark[0].x * width)
    y1 = int(hand_landmarks.landmark[0].y * height)

    x2 = int(hand_landmarks.landmark[9].x * width)
    y2 = int(hand_landmarks.landmark[9].y * height)

    x_index = int(hand_landmarks.landmark[8].x * width)
    y_index = int(hand_landmarks.landmark[8].y * height)

    d = calculate_distance(x1, y1, x2-click_ratio_fingers, y2-click_ratio_fingers)
    d_index = calculate_distance(x1, y1, x_index, y_index)

    if d_index < d:
        finger_down = True
        color = color_mouse_click

    cv2.circle(output, (x1, y1), 5, color, 2)
    cv2.circle(output, (x_index, y_index), 5, color, 2)
    cv2.line(output, (x1, y1), (x2, y2), color, 3)
    cv2.line(output, (x1, y1), (x_index, y_index), color, 3)

    return finger_down


with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.05) as hands:

    while True:
        ret, frame = video.read()
        if ret == False:
            break

        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)

        area_w = width - X_Y_INI * 2
        area_h = int(area_w / aspect_ratio_screen)
        aux_img = np.zeros(frame.shape, np.uint8)
        aux_img = cv2.rectangle(aux_img, (X_Y_INI, X_Y_INI), (X_Y_INI + area_w, X_Y_INI + area_h), color_screen, -1)
        output = cv2.addWeighted(frame, 1, aux_img, screen_opacity, 0)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                x = int(hand_landmarks.landmark[9].x * width)
                y = int(hand_landmarks.landmark[9].y * height)
                xm = np.interp(x, (X_Y_INI, X_Y_INI + area_w), (SCREEN_X_INI, SCREEN_X_FIN))
                ym = np.interp(y, (X_Y_INI, X_Y_INI + area_h), (SCREEN_Y_INI, SCREEN_Y_FIN))
                xm = int(xm/seg)*seg
                ym = int(ym/seg)*seg
                try:
                    pyautogui.moveTo(int(xm), int(ym))
                    if detect_finger_down(hand_landmarks):
                        pyautogui.click()
                except:
                    print('error xd')
                cv2.circle(output, (x, y), 10, color_mouse_pointer, 3)
                cv2.circle(output, (x, y), 5, color_mouse_pointer, -1)

        cv2.imshow('Joranome Mouse', output)
        if cv2.waitKey(1) & 0xFF == 27:
            break
video.release()
cv2.destroyAllWindows()
