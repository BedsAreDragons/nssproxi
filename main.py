import http.server
import socketserver
import urllib.parse

class ProxyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme == '':
            url = 'http://' + url

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        proxy_response = self.forward_request(url)
        self.wfile.write(proxy_response)

    def forward_request(self, url):
        import requests
        response = requests.get(url)
        return response.content

def run_proxy_server():
    port = 8080
    server_address = ('', port)
    httpd = socketserver.TCPServer(server_address, ProxyRequestHandler)
    print(f'Starting proxy server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_proxy_server()
