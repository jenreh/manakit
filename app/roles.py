from manakit_user.authentication.backend.models import Role

ASSISTANT_ROLE = Role(
    id=1,
    name="assistant",
    label="Assistent",
    description="Berechtigung für den Chat-Assistenten",
)
IMAGE_GENERATOR_ROLE = Role(
    id=2,
    name="image_generator",
    label="Bildgenerator",
    description="Berechtigung für die Bildgenerierung",
)


ALL_ROLES: list[Role] = [
    ASSISTANT_ROLE,
    IMAGE_GENERATOR_ROLE,
]
