import cv2
import mediapipe as mp
import time
import math
import pyautogui
import webbrowser
import streamlit as st

# ----------------- CONFIG -----------------
CAMERA_ID = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
DWELL_TIME = 0.9
PINCH_THRESH = 0.04
FONT = cv2.FONT_HERSHEY_SIMPLEX

pyautogui.FAILSAFE = False

# keyboard layout
KEYS_ALPHA = [
    list("1234567890"),
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    ["Caps","Z","X","C","V","B","N","M","Back"],
    ["Symbols","Space","Enter","Send"]
]

KEYS_SYMBOLS = [
    list("!@#$%^&*()"),
    ["-","/",":",";","(",")","$","&","@","\""],
    [".",",","?","'","#","%","+","=","_"],
    ["ABC","Space","Enter","Send"]
]

# visual settings
KEY_W = 90
KEY_H = 70
KEY_MARGIN_X = 10
KEY_MARGIN_Y = 10

# state
caps = False
use_symbols = False
typed_buffer = ""
last_pressed_time = 0
hover_key = None
hover_start = 0

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def draw_keyboard(img, keys_layout, hover_key_name=None):
    key_boxes = {}
    img_h, img_w = img.shape[:2]
    y = 50
    for row in keys_layout:
        row_width = len(row) * (KEY_W + KEY_MARGIN_X) - KEY_MARGIN_X
        x = int((img_w - row_width) / 2)
        for key in row:
            w = KEY_W
            h = KEY_H
            if key == "Space":
                w = KEY_W * 4 + KEY_MARGIN_X * 3
            box = (x, y, x + w, y + h)
            key_boxes[key] = box
            color = (200, 200, 200)
            thickness = 2
            if hover_key_name == key:
                color = (0, 255, 255)
                thickness = 3
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, thickness)
            text = key
            font_scale = 1.0
            text_size = cv2.getTextSize(text, FONT, font_scale, 2)[0]
            text_x = box[0] + (w - text_size[0]) // 2
            text_y = box[1] + (h + text_size[1]) // 2
            cv2.putText(img, text, (text_x, text_y), FONT, font_scale, (255, 255, 255), 2)
            x += w + KEY_MARGIN_X
        y += KEY_H + KEY_MARGIN_Y
    return key_boxes


def point_in_box(x, y, box):
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]


def normalized_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def send_whatsapp_message(message, contact):
    if not contact.startswith("+"):
        st.error("❌ Please enter number with country code (e.g. +9230093823422)")
        return
    
    url = f"https://web.whatsapp.com/send?phone={contact}&text={message}"
    webbrowser.open(url)
    time.sleep(12)
    pyautogui.press("enter")
    st.success(f"✅ Message sent to {contact}: {message}")


def press_key(key, contact):
    global caps, use_symbols, typed_buffer, last_pressed_time
    now = time.time()
    if now - last_pressed_time < 0.25:
        return
    last_pressed_time = now

    if key == "Space":
        typed_buffer += " "
    elif key == "Enter":
        typed_buffer += "\n"
    elif key == "Back":
        typed_buffer = typed_buffer[:-1]
    elif key == "Caps":
        caps = not caps
    elif key == "Symbols":
        use_symbols = True
    elif key == "ABC":
        use_symbols = False
    elif key == "Send":
        if typed_buffer.strip():
            send_whatsapp_message(typed_buffer, contact)
            typed_buffer = ""
    else:
        char = key
        if not use_symbols:
            char = char.upper() if caps else char.lower()
        typed_buffer += char


def main(contact_number):
    global hover_key, hover_start, typed_buffer
    cap = cv2.VideoCapture(CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    with mp_hands.Hands(max_num_hands=1,
                        min_detection_confidence=0.6,
                        min_tracking_confidence=0.6) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            img_h, img_w = frame.shape[:2]

            layout = KEYS_SYMBOLS if use_symbols else KEYS_ALPHA
            hover_this_frame = None
            key_boxes = draw_keyboard(frame, layout, hover_key_name=hover_key)

            if results.multi_hand_landmarks:
                handLms = results.multi_hand_landmarks[0]
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

                lm = handLms.landmark
                index_tip = (lm[8].x, lm[8].y)
                thumb_tip = (lm[4].x, lm[4].y)
                ix, iy = int(index_tip[0] * img_w), int(index_tip[1] * img_h)
                tx, ty = int(thumb_tip[0] * img_w), int(thumb_tip[1] * img_h)

                cv2.circle(frame, (ix, iy), 8, (0,255,0), cv2.FILLED)

                pinch_dist_norm = normalized_distance(index_tip, thumb_tip)
                is_pinch = pinch_dist_norm < PINCH_THRESH
                if is_pinch:
                    cv2.circle(frame, (tx, ty), 8, (0,0,255), cv2.FILLED)

                for k, box in key_boxes.items():
                    if point_in_box(ix, iy, box):
                        hover_this_frame = k
                        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0,255,255), 3)
                        break

                current_time = time.time()
                if hover_this_frame is not None:
                    if hover_key != hover_this_frame:
                        hover_key = hover_this_frame
                        hover_start = current_time
                    else:
                        elapsed = current_time - hover_start
                        box = key_boxes[hover_key]
                        progress_w = int(((elapsed) / DWELL_TIME) * (box[2]-box[0]))
                        progress_w = max(0, min(progress_w, box[2]-box[0]))
                        cv2.rectangle(frame, (box[0], box[3]+5),(box[0]+progress_w, box[3]+12),(0,255,0), cv2.FILLED)
                        if elapsed >= DWELL_TIME:
                            press_key(hover_key, contact_number)
                            hover_key = None
                            hover_start = 0
                else:
                    hover_key = None
                    hover_start = 0

                if is_pinch and hover_this_frame is not None:
                    press_key(hover_this_frame, contact_number)
                    time.sleep(0.25)

            # Show info
            mode = "SYMBOLS" if use_symbols else "ALPHA"
            caps_text = "ON" if caps else "OFF"
            cv2.putText(frame, f"Mode: {mode}    Caps: {caps_text}",
                        (20, FRAME_HEIGHT-20), FONT, 0.8, (255,255,255), 2)

            # Show current typed buffer (last 40 chars)
            cv2.putText(frame, "Buffer: " + typed_buffer[-40:],
                        (20, FRAME_HEIGHT-80), FONT, 0.7, (0,255,0), 2)

            cv2.imshow('Virtual Hand Keyboard', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

    cap.release()
    cv2.destroyAllWindows()


# ================= STREAMLIT UI =================
st.title("🖐️ Virtual Hand Keyboard with WhatsApp Sender")

contact_number = st.text_input("Enter WhatsApp Number (with country code):", "+923001234567")

if st.button("Start Virtual Keyboard"):
    if contact_number.strip():
        st.write("🎥 Virtual Keyboard starting... Press ESC to stop.")
        main(contact_number)
    else:
        st.error("❌ Please enter a valid WhatsApp number")
