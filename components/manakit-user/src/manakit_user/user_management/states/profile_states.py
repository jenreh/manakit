import re
from typing import Final

import reflex as rx
from reflex.components.sonner.toast import Toaster

from manakit_commons.database.session import get_asyncdb_session
from manakit_user.authentication.backend import user_repository
from manakit_user.authentication.states import UserSession

MIN_PASSWORD_LENGTH: Final[int] = 12

# Compile a regex pattern that ensures the password has:
# - At least MIN_PASSWORD_LENGTH characters
# - At least one uppercase letter
# - At least one lowercase letter
# - At least one digit
# - At least one special character (anything other than letters and digits)
PASSWORD_REGEX = re.compile(
    r"^(?=.{"
    + str(MIN_PASSWORD_LENGTH)
    + r",})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).*$"
)


class ProfileState(rx.State):
    new_password: str = ""
    confirm_password: str = ""
    current_password: str = ""
    name: str = ""

    async def handle_password_update(self) -> Toaster:
        if not PASSWORD_REGEX.match(self.new_password):
            return rx.toast.error(
                "Password must meet the following criteria: "
                f"At least {MIN_PASSWORD_LENGTH} characters, "
                "one UPPERCASE letter, "
                "one lowercase letter, "
                "1 number, "
                "one special! character",
                position="top-right",
            )

        if self.new_password != self.confirm_password:
            return rx.toast.error("New passwords do not match", position="top-right")

        user_session = await self.get_state(UserSession)
        user_id = user_session.user_id

        try:
            async with get_asyncdb_session() as session:
                user_repository.update_password(
                    session,
                    user_id=user_id,
                    old_password=self.current_password,
                    new_password=self.new_password,
                )
        except ValueError:
            return rx.toast.error("Incorrect current password", position="top-right")

        self.current_password = ""
        self.new_password = ""
        self.confirm_password = ""
        return rx.toast.info("Password updated successfully", position="top-right")

    def set_name(self, name: str) -> None:
        self.name = name

    def set_new_password(self, password: str) -> None:
        self.new_password = password

    def set_confirm_password(self, password: str) -> None:
        self.confirm_password = password

    def set_current_password(self, password: str) -> None:
        self.current_password = password
