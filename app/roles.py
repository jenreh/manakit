from manakit_user.authentication.backend.models import Role

ASSISTANT_ROLE = Role(
    id=1,
    name="assistant",
    label="Assistant",
    description="Access to the assistant features.",
)
IMAGE_GENERATOR_ROLE = Role(
    id=2,
    name="image_generator",
    label="Image Generator",
    description="Access to the image creation features.",
)

ALL_ROLES: list[Role] = [ASSISTANT_ROLE, IMAGE_GENERATOR_ROLE]
