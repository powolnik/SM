from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Log
from src.content.content_planner import ContentPlannerService

class PlannerApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Generate New Plan", id="generate")
        yield Log(id="log")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "generate":
            self.query_one(Log).write("Generating plan... please wait.")
            try:
                service = ContentPlannerService()
                path = service.run_planner()
                self.query_one(Log).write(f"Success! Saved to: {path}")
            except Exception as e:
                self.query_one(Log).write(f"Error: {str(e)}")

if __name__ == "__main__":
    app = PlannerApp()
    app.run()
