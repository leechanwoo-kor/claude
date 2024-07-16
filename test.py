import threading
from flask_app import run_flask
import streamlit.web.cli as stcli
import sys

if __name__ == '__main__':
    # Flask 서버를 별도의 스레드에서 실행
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Streamlit 앱 실행
    sys.argv = ["streamlit", "run", "app.py"]
    stcli.main()
