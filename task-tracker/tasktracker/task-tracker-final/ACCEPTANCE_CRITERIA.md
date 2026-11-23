# Acceptance Criteria

These criteria are the project-level baseline used to assess the Task 03 decision and regression safety.

| ID | Acceptance criterion | Verification |
|---|---|---|
| AC-01 | Adding a task assigns a unique ID that is not reused after deletion. | `tests/test_tracker.py::test_id_not_reused_after_delete` |
| AC-02 | `add` accepts only `high`, `medium`, or `low` priority; invalid priority is rejected and no task is persisted. | `test_invalid_priority_rejected`, `test_rejected_task_is_not_stored`, `test_cli_rejects_invalid_priority` |
| AC-03 | A due date is either `None` or a real calendar date in exact `YYYY-MM-DD` format. | `test_invalid_due_rejected`, `test_valid_due_and_none_accepted` |
| AC-04 | Completing a task after a deletion/add sequence updates the task with the requested ID, not another task. | `test_complete_targets_correct_task_after_delete` |
| AC-05 | Existing list/filter/sort/summary behavior remains intact after the fixes. | Original nine tests in `tests/test_tracker.py`; compare baseline and post-fix logs. |

## Task 03 verification statement

The supplied post-fix log reports 20 passing tests, including AC-01 through AC-05 coverage. This is evidence from the included Linux/Python 3.13.18 run only. It does not establish a Windows/Python 3.12 result; that environment must be tested separately by the submitter.
