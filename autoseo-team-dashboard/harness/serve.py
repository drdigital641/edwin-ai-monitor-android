import http.server,os,sys
class H(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        p=self.path.split('?')[0]
        if not os.path.exists('.'+p) or p in('/billing','/sales'): self.path='/index.html'
        return super().send_head()
    def log_message(self,*a): pass
http.server.ThreadingHTTPServer(('127.0.0.1',8765),H).serve_forever()
