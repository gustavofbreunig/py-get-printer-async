import unittest

from main import get_counter

class TestCounter(unittest.IsolatedAsyncioTestCase):
    async def testa_contador(self):
        r = await get_counter("192.168.0.1")
        self.assertIsNotNone(r)


if __name__ == '__main__':
    unittest.main()