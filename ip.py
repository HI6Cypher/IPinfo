import http_request, re, random, sys, os

class IP :
    def __init__(self) :
        self.pass_ip = list()
        self.text = str()

    def req(self) :
        host = "208.95.112.1"
        end = "/json/"
        
        for IP in self.pass_ip :
            try :
                print(f"[*] check ip {IP}", end = "\r", flush = True)
                q = http_request.HTTP_request(host, 80, end + IP)
                q = q.send()
                if isinstance(q, tuple) and isinstance(q[0], dict) :
                    q = q
                elif "Error" in q :
                    q = ({"status" : "error"}, 200)
                else :
                    print(q)
                    sys.exit()
                if q[1] == 200 and q[0]["status"] == "success" :
                    print(f"[*] check ip {IP}  success")
                    text = "IP: %s  Country: %s  City: %s Timezone: %s\n\n" \
                        % (IP, q[0]["country"], q[0]["city"], q[0]["timezone"])
                    self.text = text
                    self.pass_ip.remove(IP)
                    self.save()
                elif q[0]["status"] == "fail" :
                    print(f"[*] check ip {IP}  fail")
                    self.pass_ip.remove(IP)
            except KeyboardInterrupt :
                sys.exit()
            except Exception :
                pass

    def save(self) :
        mode = "a" if os.path.exists(file) else "x"
        with open(file, mode) as f :
            f.write(self.text) 

if __name__ == "__main__" :
    i = input(">>>")
    file = f"{i}:/data{random.randint(500, 5000)}.txt"

    def extract(path) :
        with open(path, "r") as file :
            loads = file.read()
        IPs = [re.search(r"(?<=Destination : ).+?(?=\s)", load).group() for load in loads.split("[*]")[1:]]
        IPs = list(set(IPs))
        return IPs

    run = IP()
    path = input(">>>")
    run.pass_ip = extract(path)
    print(f"[*] {len(run.pass_ip)} IP address found")
    while run.pass_ip != [] :
        run.req()