import reflex as rx

config = rx.Config(
    app_name="sales_brochure_generator",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)