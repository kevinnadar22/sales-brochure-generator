"""Sales Brochure Generator - A minimal, clean UI."""

import reflex as rx
from loguru import logger

from .services import generate_brochure
from .utils import make_pdf


class State(rx.State):
    """App state."""
    url: str = ""
    brochure: str = ""
    loading: bool = False
    
    async def generate(self):
        """Generate brochure from URL."""
        if not self.url:
            return
        
        self.loading = True
        yield
        
        try:
            self.brochure = await generate_brochure(self.url)
        except Exception as e:
            logger.exception(e)
            self.brochure = f"Error: {str(e)}"
        finally:
            self.loading = False
    
    async def download_pdf(self):
        """Generate PDF from brochure and download it."""
        if not self.brochure:
            return
        
        try:
            pdf_path = make_pdf(self.brochure)
            return rx.download(pdf_path)
        except Exception as e:
            logger.exception(e)
            return rx.window_alert(f"Error generating PDF: {str(e)}")


def index() -> rx.Component:
    """Main page."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Sales Brochure Generator", size="9"),
            rx.text("Enter a company website URL to generate a brochure", size="5", color="gray"),
            
            rx.hstack(
                rx.input(
                    placeholder="https://example.com",
                    value=State.url,
                    on_change=State.set_url,
                    width="100%",
                    size="3",
                ),
                rx.button(
                    "Generate",
                    on_click=State.generate,
                    loading=State.loading,
                    size="3",
                ),
                width="100%",
                spacing="3",
            ),
            
            rx.cond(
                State.brochure,
                rx.vstack(
                    rx.hstack(
                        rx.heading("Generated Brochure", size="6"),
                        rx.button(
                            rx.icon("download"),
                            "Download PDF",
                            on_click=State.download_pdf,
                            variant="soft",
                            size="2",
                        ),
                        width="100%",
                        justify="between",
                        align="center",
                    ),
                    rx.box(
                        rx.markdown(State.brochure),
                        width="100%",
                        padding="4",
                        border_radius="8px",
                        border="1px solid var(--gray-6)",
                    ),
                    width="100%",
                    spacing="3",
                ),
            ),
            
            spacing="6",
            width="100%",
            max_width="800px",
            padding="8",
            min_height="85vh",
        ),
        size="4",
    )


app = rx.App()
app.add_page(index)
