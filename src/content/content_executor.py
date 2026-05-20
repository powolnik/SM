class ContentExecutor:
    def __init__(self, plan_store, clients: dict):
        self.plan_store = plan_store
        self.clients = clients

    def execute_plan(self, filename, dry_run=False):
        self.plan_store.update_plan_status(filename, "in_progress")
        try:
            plan = self.plan_store.load_plan(filename)
            platform = plan.get("platform", "instagram")
            client = self.clients.get(platform)

            if not client:
                raise ValueError(f"No client configured for platform: {platform}")

            if dry_run:
                print(f"--- DRY RUN: Executing {filename} on {platform} ---")
                for post in plan.get("posts", []):
                    content = post.get("caption")
                    if content:
                        print(f"Would post to {platform}: {content}")
                print("--- DRY RUN COMPLETE ---")
            else:
                for post in plan.get("posts", []):
                    content = post.get("caption")
                    if content:
                        client.post_content(content)
            
            self.plan_store.update_plan_status(filename, "completed")
        except Exception as e:
            self.plan_store.update_plan_status(filename, "confirmed")
            raise e
