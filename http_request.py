import socket
import json
import sys

class HTTP_request :
    def __init__(self, host, port, endpoint) :
        self.host = host
        self.port = int(port) if not isinstance(port, int) else port
        self.end = endpoint

    def send(self) :
        try :
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as flood :
                payload = f"GET /{self.end} HTTP/1.0\r\nHost: {self.host}\r\n\r\n"
                flood.connect((self.host, self.port))
                flood.send(payload.encode())
                response = b""
                while True :
                    data = flood.recv(4096)
                    if not data :
                        status = response.decode().split(" ")[1] if isinstance(response, bytes) else response.split(" ")[1]
                        response = response.decode().split("\r\n\r\n", 1)[-1] if isinstance(response, bytes) else response.split("\r\n\r\n", 1)[-1]
                        try :
                            data = json.loads(response)
                        except Exception:
                            return data.decode() if isinstance(data, bytes) else data
                        return data, int(status)
                    response += data
        except OSError as error :
            error = " ".join(str(error).split()[2:])
            return f"[!] Error - {error or None}"

if __name__ == "__main__" :
    if len(sys.argv) == 3 :
        run = HTTP_request(sys.argv[1], 80, sys.argv[2])
        print(run.send())