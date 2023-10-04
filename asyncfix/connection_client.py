import asyncio
import logging

from asyncfix.connection import AsyncFIXConnection, ConnectionRole, ConnectionState
from asyncfix.errors import FIXConnectionError
from asyncfix.journaler import Journaler
from asyncfix.protocol import FIXProtocolBase


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
        start_tasks: bool = True,
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
            start_tasks=start_tasks,
        )
        self._connection_role = ConnectionRole.INITIATOR

    async def connect(self):
        if self._socket_reader:
            raise FIXConnectionError("Socket already connected")

        self._socket_reader, self._socket_writer = await asyncio.open_connection(
            self._host, self._port
        )

        self._connection_state = ConnectionState.NETWORK_CONN_ESTABLISHED

        await self.on_connect()
