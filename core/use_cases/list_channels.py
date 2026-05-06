# File: core/use_cases/list_channels.py
"""
Caso de uso para listar todos los canales de notificación disponibles.
"""
from typing import List

from core.channel import Channel
from core.repositories.channel_repository import ChannelRepository
from core.exceptions import ChannelError


class ListChannels:
    """
    Caso de uso para obtener una lista de todos los canales de notificación.

    Este caso de uso interactúa con el repositorio de canales para recuperar
    la información.
    """

    def __init__(self, channel_repository: ChannelRepository):
        """
        Inicializa el caso de uso con una instancia del repositorio de canales.

        Args:
            channel_repository: Una implementación de la interfaz ChannelRepository.
        """
        self.channel_repository = channel_repository

    async def execute(self) -> List[Channel]:
        """
        Ejecuta el caso de uso para listar todos los canales.

        Returns:
            Una lista de objetos Channel.

        Raises:
            ChannelError: Si ocurre un error al intentar recuperar los canales
                          desde el repositorio.
        """
        try:
            return await self.channel_repository.list_all()
        except Exception as e:
            # Captura cualquier excepción del repositorio y la encapsula en un
            # error de dominio específico.
            raise ChannelError(f"Error listing channels: {e}") from e