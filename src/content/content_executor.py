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
                # Changed 'steps' to 'posts' to match PlanGenerator output
                for post in plan.get("posts", []):
                    # Assuming content is in the 'caption' field for now
                    content = post.get("caption")
                    if content:
                        self.ig.post_content(page, content)
            finally:
                browser.close()
                self.ig.close()
            self.plan_store.update_plan_status(filename, "completed")
        except Exception as e:
            self.plan_store.update_plan_status(filename, "pending")
            raise e
