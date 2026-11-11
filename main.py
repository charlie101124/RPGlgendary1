import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    if not os.path.exists("game.html"):
        print("경고: 같은 폴더에 game.html 파일이 있는지 확인해주세요!")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"서버가 시작되었습니다: http://localhost:{PORT}")
        print("브라우저가 자동으로 열립니다. 종료하려면 Ctrl+C를 누르세요.")
        
        webbrowser.open(f"http://localhost:{PORT}/game.html")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n게임을 종료합니다.")

if __name__ == "__main__":
    run()