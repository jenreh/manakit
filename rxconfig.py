import reflex as rx

config = rx.Config(
    app_name="reflex_mantine",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
