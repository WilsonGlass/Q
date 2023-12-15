import unittest
import asyncio
from Q.Server.server import main as run_server
from Q.Client.client import main as run_client

class testTCPConnection(unittest.TestCase):
    def setUp(self):
        self.server_task = asyncio.ensure_future(run_server(port="localhost"))
        self.client_task = asyncio.ensure_future(run_client(port="localhost"))

    def tearDown(self):
        self.server_task.cancel()
        self.client_task.cancel()

    def test_tcp_connection(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(self.server_task, self.client_task))

