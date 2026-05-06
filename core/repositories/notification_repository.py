# File: core/repositories/notification_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from core.notification import Notification


class NotificationRepository(ABC):
    """
    Interfaz abstracta para el repositorio de notificaciones.
    Define los métodos que deben ser implementados por cualquier repositorio
    concreto para interactuar con la persistencia de datos de las notificaciones.
    """

    @abstractmethod
    async def save(self, notification: Notification) -> None:
        """
        Guarda una nueva notificación en el repositorio.

        Args:
            notification: La instancia de Notification a guardar.
        """
        ...

    @abstractmethod
    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """
        Obtiene una notificación por su identificador único.

        Args:
            notification_id: El UUID de la notificación a buscar.

        Returns:
            Una instancia de Notification si se encuentra, de lo contrario None.
        """
        ...

    @abstractmethod
    async def get_all(self) -> List[Notification]:
        """
        Obtiene todas las notificaciones del repositorio.

        Returns:
            Una lista de instancias de Notification.
        """
        ...

    @abstractmethod
    async def update(self, notification: Notification) -> None:
        """
        Actualiza una notificación existente en el repositorio.

        Args:
            notification: La instancia de Notification con los datos actualizados.
        """
        ...

    @abstractmethod
    async def delete(self, notification_id: UUID) -> None:
        """
        Elimina una notificación del repositorio por su identificador único.

        Args:
            notification_id: El UUID de la notificación a eliminar.
        """
        ...

# File: core/repositories/notification_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from core.notification import Notification


class NotificationRepository(ABC):
    """
    Interfaz abstracta para el repositorio de notificaciones.
    Define los métodos que deben ser implementados por cualquier repositorio
    concreto para interactuar con la persistencia de datos de las notificaciones.
    """

    @abstractmethod
    async def save(self, notification: Notification) -> None:
        """
        Guarda una nueva notificación en el repositorio.

        Args:
            notification: La instancia de Notification a guardar.
        """
        ...

    @abstractmethod
    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """
        Obtiene una notificación por su identificador único.

        Args:
            notification_id: El UUID de la notificación a buscar.

        Returns:
            Una instancia de Notification si se encuentra, de lo contrario None.
        """
        ...

    @abstractmethod
    async def get_all(self) -> List[Notification]:
        """
        Obtiene todas las notificaciones del repositorio.

        Returns:
            Una lista de instancias de Notification.
        """
        ...

    @abstractmethod
    async def update(self, notification: Notification) -> None:
        """
        Actualiza una notificación existente en el repositorio.

        Args:
            notification: La instancia de Notification con los datos actualizados.
        """
        ...

    @abstractmethod
    async def delete(self, notification_id: UUID) -> None:
        """
        Elimina una notificación del repositorio por su identificador único.

        Args:
            notification_id: El UUID de la notificación a eliminar.
        """
        ...