import selectors

from . import http


class IO:

    def __init__(self, mode):
        print("mode: " + mode)

        if mode == 'poll':
            self.sel = selectors.PollSelector()
        elif mode == 'epoll':
            self.sel = selectors.EpollSelector()
        else:
            self.sel = selectors.SelectSelector()

    def accept(self, server, mask):
        client, addr = server.accept()
        self.sel.register(client, selectors.EVENT_READ, self.read)

    def read(self, client, mask):
        request = http.get_request(client)

        if not request:
            self.sel.unregister(client)
            client.close()
            return
        http.send_response(client, request)
        if not http.is_keep_alive(request):
            self.sel.unregister(client)
            client.close()

    def wait(self, server):
        self.sel.register(server, selectors.EVENT_READ, self.accept)
        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
