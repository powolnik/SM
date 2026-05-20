from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, RichLog, Label
from textual.containers import Horizontal, Vertical
from src.content.plan_store import PlanStore
from src.content.content_executor import ContentExecutor
from src.social.instagram_client import InstagramClient
import os

class TUIApp(App):
    BINDINGS = [("q", "quit", "Quit"), ("e", "execute_selected", "Execute Selected"), ("r", "refresh", "Refresh")]

    def __init__(self, character_name):
        super().__init__()
        self.character_dir = os.path.join("characters", character_name)
        self.plan_store = PlanStore(self.character_dir)
        self.ig_client = InstagramClient()
        self.executor = ContentExecutor(self.plan_store, self.ig_client)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            Vertical(Label("Plans"), DataTable(id="plan-table"), id="sidebar"),
            Vertical(Label("Logs"), RichLog(id="log-viewer"), id="main-view"),
        )
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Filename", "Status")
        self.refresh_plans()

    def refresh_plans(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        plans = self.plan_store.load_all_plans()
        for filename, plan in plans.items():
            table.add_row(filename, plan.get("execution_status", "unknown"))

    def action_refresh(self) -> None:
        self.refresh_plans()
        self.query_one(RichLog).write("Refreshed plan list.")

    def action_execute_selected(self) -> None:
        table = self.query_one(DataTable)
        cursor_row = table.cursor_row
        if cursor_row >= 0:
            filename = table.get_row_at(cursor_row)[0]
            self.query_one(RichLog).write(f"Starting execution: {filename}")
            self.run_worker(self.execute_task(filename), name="executor")

    async def execute_task(self, filename):
        try:
            self.executor.execute_plan(filename, dry_run=True)
            self.query_one(RichLog).write(f"Finished: {filename}")
            self.refresh_plans()
        except Exception as e:
            self.query_one(RichLog).write(f"Error executing {filename}: {str(e)}")

    def action_quit(self) -> None:
        self.ig_client.close()
        self.exit()
