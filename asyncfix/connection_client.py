import asyncio
import sys
import time
import logging
from asyncfix import FTag, FMsg
from asyncfix.message import FIXMessage, MessageDirection
from asyncfix.protocol import FIXProtocolBase
from asyncfix.connection import ConnectionState, AsyncFIXConnection
from asyncfix.journaler import Journaler


class AsyncFIXClient(AsyncFIXConnection):
    def __init__(
        self,
        protocol: FIXProtocolBase,
        sender_comp_id: str,
        target_comp_id: str,
        journaler: Journaler,
        host: str,
        port: int,
        heartbeat_period: int = 30,
        logger: logging.Logger | None = None,
    ):
        super().__init__(
            protocol=protocol,
            sender_comp_id=sender_comp_id,
            target_comp_id=target_comp_id,
            journaler=journaler,
            host=host,
            port=port,
            heartbeat_period=heartbeat_period,
            logger=logger,
        )

    async def connect(self):
        assert self.connection_state == ConnectionState.DISCONNECTED
        self.socket_reader, self.socket_writer = await asyncio.open_connection(
            self.host, self.port
        )
        self.connection_state = ConnectionState.CONNECTED
        await self.on_connect()

