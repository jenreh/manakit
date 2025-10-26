import reflex as rx


class KeyboardShortcuts(rx.Component):
    library = None  # No external library needed
    tag = None

    def add_imports(self) -> dict:
        return {
            "react": [rx.ImportVar(tag="useEffect")],
        }

    def add_hooks(self) -> list[str]:
        return [
            """
useEffect(() => {
    const textarea = document.getElementById('composer-area');
    const submitBtn = document.getElementById('composer-submit');

    if (textarea && submitBtn) {
        const handleKeydown = (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (textarea.value.trim() && !submitBtn.disabled) {
                    submitBtn.click();
                }
            }
        };
        textarea.addEventListener('keydown', handleKeydown);
        return () => textarea.removeEventListener('keydown', handleKeydown);
    }
}, []);
            """
        ]


# Create an instance function
keyboard_shortcuts = KeyboardShortcuts.create
