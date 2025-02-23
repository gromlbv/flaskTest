import subprocess
import sys

def start_ngrok():
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(['open', '-a', 'Terminal', 'ngrok', 'http', '8000', '--url', 'https://maggot-patient-lamprey.ngrok-free.app'])
        elif sys.platform == "win32":  # Windows
            subprocess.run(['start', 'cmd', '/k', 'ngrok http 8000 --url https://maggot-patient-lamprey.ngrok-free.app'], shell=True)
        elif sys.platform == "linux":  # Linux
            subprocess.run(['gnome-terminal', '--', 'ngrok', 'http', '8000', '--url', 'https://maggot-patient-lamprey.ngrok-free.app'])
        else:
            print("Операционная система не поддерживается.")
    except Exception as e:
        print(f"Ошибка при запуске ngrok: {e}")

if __name__ == "__main__":
    start_ngrok()