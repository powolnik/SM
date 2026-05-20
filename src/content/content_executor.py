class ContentExecutor:
    def __init__(self, plan_store, instagram_client):
        self.plan_store = plan_store
        self.ig = instagram_client

    def execute_plan(self, filename):
        self.plan_store.update_plan_status(filename, "in_progress")
        try:
            plan = self.plan_store.load_plan(filename)
            browser, page = self.ig.get_authenticated_page()
            try:
                for step in plan.get("steps", []):
                    if step.get("platform") == "instagram":
                        self.ig.post_content(page, step.get("content"))
            finally:
                browser.close()
                self.ig.close()
            self.plan_store.update_plan_status(filename, "completed")
        except Exception as e:
            self.plan_store.update_plan_status(filename, "pending")
            raise e
