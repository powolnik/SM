# TUI Implementation Plan

## Phase 1: Architecture & Dependency Setup
1. Install `textual`.
2. Decouple logic: Move `AgentOrchestrator` loop into an `async` worker to prevent blocking the UI.
3. Define State Management: Use `Reactive` variables to track plan statuses.

## Phase 2: TUI Layout Design
1. Main Layout:
    - Sidebar: `DataTable` for plan management.
    - Main View: `RichLog` widget for debug output.
    - Footer: Keybindings for [G]enerate, [E]xecute, [Q]uit.
2. Components:
    - `PlanList`: Displays plans from `PlanStore`.
    - `LogViewer`: Captures output from `debug_log`.

## Phase 3: Integration
1. Event Binding: Map UI actions to `PlanStore` and `ContentExecutor` methods.
2. Logging Redirection: Create a custom handler to pipe `debug_log` into the `RichLog` widget.
3. Threading: Use `run_in_executor` for network-heavy `InstagramClient` operations to keep the UI responsive.

## Phase 4: Testing Strategy
1. Unit Tests: Use `textual.pilot` to simulate user interactions.
2. Mocking: Use `MockInstagramClient` and `MockPlanStore` to verify UI state transitions without network/file side effects.
3. Integration Tests: Verify that selecting a plan in the TUI correctly updates the `PlanStore` status.

## Phase 5: Refinement
1. Error Handling: Implement modal dialogs for API/execution failures.
2. Configuration: Ensure TUI respects existing `.env` and character directory structures.
