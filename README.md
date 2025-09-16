# 🖐️ Virtual Hand Keyboard with WhatsApp Sender  

This project is an **AI-powered Virtual Hand-Controlled Keyboard** that allows users to **type without touching a physical keyboard**.  
Using **Computer Vision (OpenCV + Mediapipe)** for hand tracking, the system recognizes **finger positions and gestures** to interact with an on-screen virtual keyboard.  

It also integrates with **WhatsApp Web** so that typed text can be directly **sent as a message** to a selected phone number.  
The project includes a **Streamlit-based UI** for entering phone numbers and controlling the keyboard.  


## ✨ Features  

✅ **Virtual Keyboard** controlled by hand gestures  
✅ **Hand Tracking** using Mediapipe + OpenCV  
✅ **Typing by hovering & pinching** over keys  
✅ **Caps Lock / Symbols / Backspace** support  
✅ **Buffer preview** for typed text  
✅ **Dwell-Time Selection** → Hold on a key for selection  
✅ **WhatsApp Web Integration** → Send messages directly  
✅ **Streamlit UI** → Enter phone numbers & control keyboard  
✅ **Cross-platform** (Windows, Linux, Mac with camera + browser)  


## ⚙️ How It Works  

1. **Hand Detection**  
   - Mediapipe identifies hand landmarks (index fingertip, thumb, etc.).  
   - The index finger is used as the **cursor**.  

2. **Key Selection**  
   - Hover your finger over a virtual key.  
   - If you hold for `0.9 seconds` (dwell time), the key is automatically pressed.  
   - Alternatively, make a **pinch gesture** (thumb + index) to select instantly.  

3. **Typing**  
   - Typed characters are stored in a **buffer** displayed on screen.  

4. **WhatsApp Integration**  
   - Enter the phone number (with country code) in the UI.  
   - Press **Send** → The message is typed into **WhatsApp Web** and sent automatically.  


## 🛠️ Tech Stack  

- **Python 3.8+**  
- **OpenCV** → For video frame processing  
- **Mediapipe** → For real-time hand tracking  
- **PyAutoGUI** → To automate keystrokes & sending messages  
- **Streamlit** → For user interface (enter WhatsApp number, start app)  
- **WebBrowser API** → To open WhatsApp Web automatically  


## 🚀 Installation  

Clone the repository:  
```bash
git clone https://github.com/YOUR-USERNAME/virtual-hand-keyboard-whatsapp.git
cd virtual-hand-keyboard-whatsapp

#Install dependencies:
pip install -r requirements.txt

#Run the Streamlit app:
streamlit run app.py


📖 Future Improvements

🔹 Add support for multiple contacts from a UI list
🔹 Voice-to-text input as an alternative
🔹 Dark mode keyboard theme
🔹 Support for emojis & multimedia sharing
🔹 Mobile camera integration (IP Webcam)

👨‍💻 Author

Developed by Muhammad Sufyan🎓
This project was built as part of an AI + Computer Vision learning journey to explore gesture-based interfaces and real-world automation with WhatsApp.
