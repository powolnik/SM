# Development Roadmap: Agent Orchestrator

This document outlines the next 10 steps to evolve the Agent Orchestrator into a robust, production-ready system.

1. **Implement Error Handling in `InstagramClient`**: Add `try-except` blocks around login and posting selectors to handle UI changes or network timeouts gracefully.
2. **Add Logging Infrastructure**: Replace `print` statements with the `logging` module to capture execution history, errors, and status changes in a persistent log file.
3. **Enhance `PlanStore` Validation**: Add schema validation in `PlanStore.save_plan` to ensure plans are always in the correct format.
4. **Implement "Dry Run" Logic in `InstagramClient`**: Update `post_content` to respect the `dry_run` flag by logging intended actions instead of interacting with the browser.
5. **Add Unit Tests for `PlanStore`**: Use `pytest` to verify that `get_due_plans` correctly filters by status and that `update_plan_status` persists changes.
6. **Create a "Plan Generator" CLI**: Add a TUI command that triggers `PlanGenerator.create_new_plan` to generate content without manual JSON editing.
7. **Improve `InstagramClient` Session Persistence**: Ensure `user_data_dir` is managed to minimize re-login/2FA requirements.
8. **Add Content Validation/Review Step**: Introduce a "Review" status in the `PlanStore` to prevent the agent from posting unverified AI content.
9. **Implement Media Handling**: Update `InstagramClient.post_content` to support uploading images and videos.
10. **Add Monitoring/Alerting**: Integrate a notification system (e.g., Telegram or email) to alert on execution failures or session expiration.
