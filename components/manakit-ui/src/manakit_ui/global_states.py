import reflex as rx


class LoadingState(rx.State):
    is_loading: bool = False
    is_loading_message: str = "Lade..."

    def set_is_loading(self, is_loading: bool) -> None:
        self.is_loading = is_loading
