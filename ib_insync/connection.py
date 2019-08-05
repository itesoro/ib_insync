import asyncio


def _default_callback(*args):
    pass


def _tmp_str_data(data):
    n = 10
    if len(data) < n:
        return str(data)
    return str(data[:n]) + '...'


class Connection(asyncio.Protocol):
    """
    Socket connection.
    """
    __slots__ = '_transport', 'on_data_received', 'on_connection_lost'

    @staticmethod
    async def create_async(host, port, on_data_received=_default_callback, on_connection_lost=_default_callback):
        c = Connection()
        c.transport = None
        c.on_data_received = on_data_received
        c.on_connection_lost = on_connection_lost
        loop = asyncio.get_event_loop()
        await loop.create_connection(lambda: c, host, port)
        return c if c.is_connected else None

    def close(self):
        if self._transport is not None:
            self._transport.close()

    @property
    def is_connected(self) -> bool:
        return self._transport is not None

    def write(self, data):
        # print('<<', _tmp_str_data(data))
        # print('<<', data)
        self._transport.write(data)

    def connection_made(self, transport):
        self._transport = transport

    def connection_lost(self, exc):
        self.on_connection_lost(exc)
        self._transport = None

    def data_received(self, data):
        # print('>>', _tmp_str_data(data))
        # print('>>', data)
        self.on_data_received(data)
