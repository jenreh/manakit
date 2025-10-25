from manakit_user.authentication.backend.models import Role

ASSISTANT_ROLE = Role(name="assistant", label="Chat")
IMAGE_CREATOR_ROLE = Role(name="image_creator", label="Image Creator")

ALL_ROLES = [ASSISTANT_ROLE, IMAGE_CREATOR_ROLE]
