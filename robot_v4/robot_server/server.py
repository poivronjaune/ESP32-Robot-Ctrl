import socket
import os
import gc
import time
import camera

routes = {}

def route(path):
    def decorator(func):
        routes[path] = func
        return func
    return decorator

# --- TEMPLATE ENGINE (very basic) ---
def render_template(filename, context=None):
    context = context or {}   # If context is None, then not variables are passed to the html page

    try:
        base_dir = "/".join(__file__.split("/")[:-1])
        template_path = "/".join([base_dir, "templates", filename])

        with open(template_path, "r") as f:
            content = f.read()

        for key, value in context.items():
            content = content.replace("{{ " + key + " }}", str(value))

        return content

    except Exception as e:
        # TODO: Improve response to be a valide HTML File
        return "<h1>Template Error: {}</h1>".format(e)

# --- WEB SERVER LOOP ---
def start_server(port=80):
    from . import routes as route_defs  # Triggers registration of all defined routes
    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
    
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    server_on = True
    while server_on:
        cl, addr = s.accept()
        print(' 🌐 Client connected from', addr)
        try:
            request = cl.recv(1024)
            request = request.decode('utf-8')
        except Exception as e:
            print(" 🛑 Error: ",e)
        #finally:
        #    cl.close()            
            
        path = "/"
        try:
            line = request.split("\r\n")[0]
            path = line.split(" ")[1]
            path = path.split("?")[0]    # QUESTION: Do we need get parameters?
            print(f" 🛠 Debug path received: {path}")
        except:
            pass # Defaults to /
        
        if path in routes:
            http_response = routes[path]()  # Call the route handler to get the HTML Part of the response based on the URL command path
            cl.sendall(http_response)
        else:
            if path == '/exit':
                # Return control back to web_server calling function
                server_on = False
                print(" ⛔ Shuting down server")
                cl.send("HTTP/1.1 503 Service Unavailable\r\n\r\n <p>&nbsp;&nbsp;</p>Error 503 - Robot controller was shutdown or is unavailable.")
            else:
                cl.send("HTTP/1.1 404 Not Found\r\n\r\n <p>&nbsp;&nbsp;</p>Error 404 - Page Not Found")

        cl.close()    # Flush connection
        del cl        # Freeup memory
        gc.collect()  # Manually launch garbage collection
