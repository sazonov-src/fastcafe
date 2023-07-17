import uuid

from mixer.backend.django import mixer

mixer.register("auth.user", username=lambda: str(uuid.uuid4()))

__all__ = [
    "mixer",
    ]
