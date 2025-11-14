"""WebSocket consumers for real-time updates."""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)


class NHLDataConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for NHL data updates."""

    async def connect(self):
        """Handle WebSocket connection."""
        self.room_group_name = 'nhl_updates'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"WebSocket disconnected: {self.channel_name}")

    async def receive(self, text_data):
        """Receive message from WebSocket."""
        data = json.loads(text_data)
        message_type = data.get('type', 'unknown')

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'nhl_update',
                'message': data
            }
        )

    async def nhl_update(self, event):
        """Send NHL update to WebSocket."""
        await self.send(text_data=json.dumps(event['message']))
