import webbrowser
from threading import Thread

from .backend import PORT, run_server

Thread(target=run_server).start()
webbrowser.open(f'http://localhost:{PORT}')
