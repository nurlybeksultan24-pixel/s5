# Task Tracker — Tasks 01–10, AI Use Record and Evidence Appendix

**Project:** Task Tracker (Python CLI)  
**AI assistant:** Claude 
**Review status:** Documentation package prepared from the supplied repository archive and its logs.  
**Important environment boundary:** Included logs identify Linux, Python 3.13.18, pytest 9.1.1. They are not evidence of a run on the submitter's Windows/Python 3.12 environment.

---

## Task 01 — Repository map and initial inspection

### Repository map

| Path | Responsibility / entry point |
|---|---|
| `tasktracker/cli.py` | CLI entry point: `main(argv=None)`; argparse commands `add`, `list`, `done`, `delete`, `summary` |
| `tasktracker/tracker.py` | `TaskTracker`; add/complete/delete/list/summary; priority and due-date validation |
| `tasktracker/storage.py` | JSON persistence through `load()` and `save()`; default file is `tasks.json` |
| `tests/test_tracker.py` | Unit tests and Task 07 regression tests |
| `requirements.txt` | Test dependency (`pytest==9.1.1` in this package) |
| `README.md`, `AGENTS.md` | User and agent documentation |
| `logs/` | Supplied baseline, before-fix, after-fix logs and source diffs |

### Commands and recorded results

The archive contains test-session output, not a terminal transcript with every shell command. The logs show pytest sessions and their results:

| Evidence file | Environment stated in log | Collected | Result |
|---|---|---:|---|
| `logs/01_baseline.log` | Linux, Python 3.13.18, pytest 9.1.1 | 9 | 9 passed |
| `logs/02_before_fix.log` | Linux, Python 3.13.18, pytest 9.1.1 | 20 | 9 failed, 11 passed |
| `logs/03_after_fix.log` | Linux, Python 3.13.18, pytest 9.1.1 | 20 | 20 passed |

The archive also contains `logs/tracker.diff` and `logs/cli.diff`, which show the changes for the ID/validation and CLI error-handling fixes.

### Weaknesses observed

1. **Persistence robustness:** `storage.load()` directly parses JSON. Corrupted JSON can raise an exception and does not provide a recovery/backup flow.
2. **Write reliability:** `storage.save()` writes directly to the target file. There is no temporary-file plus atomic-replace strategy or file locking.
3. **Test/automation coverage:** `storage.py` has no dedicated tests; CLI coverage is limited. No CI workflow, lint configuration, type-check configuration, or build configuration is present in the supplied tree.

### Tooling checks not evidenced

- Lint: not run; no Ruff/Flake8 configuration is present.
- Type check: not run; no mypy configuration is present.
- Build/package: no build configuration or build step is present in the supplied repository.
- Windows/Python 3.12: not verified by the included logs.

Do not convert these “not run/not configured” items into passing results.

---

## Task 02 — Agent instructions

`AGENTS.md` is included and documents purpose, architecture, setup, safe commands, approval gates, forbidden actions, coding conventions, test expectations, and review gates.

**Instruction-loading evidence:** The file was manually opened/read during the review. The supplied evidence does not show that Claude automatically discovered or loaded `AGENTS.md`. Record this as: **manual read; automatic loading not verified / did not occur in the observed workflow**. Do not claim automatic loading.

---

## Task 03 — Design-pattern decision and acceptance criteria

### Decision

**Strategy: not required.** `tracker.py` already uses `SORT_KEYS` and `STATUS_FILTERS` lookup dictionaries. Adding a sort/filter option is a small mapping change; a class hierarchy would add complexity without a demonstrated need.

**Adapter: not required.** There is one JSON storage implementation. `TaskTracker` receives a list and does not directly depend on the storage module. An adapter should be reconsidered only if a second backend (for example SQLite or a remote API) is actually introduced.

### Acceptance criteria

See the separate `ACCEPTANCE_CRITERIA.md` file for AC-01 through AC-05 and their test mappings.

### Verification after the decision

The post-fix log reports 20/20 passing tests. In particular, the new regression tests cover ID non-reuse, correct completion after deletion, invalid priorities, invalid dates, rejected-task non-persistence, and CLI rejection. The original behavior tests also pass in that recorded run.

**Qualification:** this is evidence from the supplied Linux/Python 3.13.18 log, not a fresh Windows/Python 3.12 run.

**Additional packaging check in this assistant runtime:** `python -m pytest -v` was run against the extracted project and reported **20 passed in 0.08s** on Linux/Python 3.13.5 with the environment-provided pytest 9.0.2. The pinned `pytest==9.1.1` was not installed in that runtime, so this run does not verify installation from `requirements.txt` and is not a Windows/Python 3.12 result.

---

## Task 04 — Findings and categories

The table uses the required categories: **correctness, maintainability, security, dependency, agent operations**. Status meanings:

- **Confirmed:** directly visible in supplied source or logs.
- **Unverified:** plausible concern, but the supplied evidence is insufficient to establish it.
- **Unsupported:** checked against the supplied repository and not supported by the evidence.

| ID | Category | Finding | Status | Evidence / reasoning |
|---|---|---|---|---|
| F1 | correctness | Task IDs could be reused after deletion. | Confirmed; fixed in Task 07 | Before-fix regression log shows `test_id_not_reused_after_delete` failed (`2` was returned instead of `3`); `tracker.py` now uses `max(existing IDs) + 1`. |
| F2 | correctness | Invalid priority and due-date values were accepted by the add path. | Confirmed; fixed in Task 07 | Before-fix log shows validation tests failed; current `tracker.py` validates allowed priorities and exact real calendar dates. |
| F3 | correctness | Corrupted `tasks.json` can cause an unhandled JSON parsing error. | Confirmed from implementation; open | `storage.load()` calls `json.load()` without a recovery/error-handling path. No corrupted-file test is included. |
| F4 | correctness | A process interruption during a direct write may leave incomplete/corrupt data. | Confirmed design weakness; open | `storage.save()` opens the target with `"w"` and writes directly; no atomic replacement. Actual data-loss event not demonstrated. |
| F5 | maintainability | Storage path is tied to the current working directory; no `--file` option. | Confirmed; open | `DATA_FILE = "tasks.json"` in `storage.py`; README documents current-working-directory behavior. |
| F6 | security | A maliciously crafted local JSON file may contain unexpected shapes/types that later code assumes are valid task dictionaries. | Unverified | `storage.load()` trusts parsed JSON; no schema validation is shown. No exploit or malformed-structure test supplied. |
| F7 | maintainability | Persistence layer has no dedicated tests; CLI test coverage is limited. | Confirmed; open | Only `tests/test_tracker.py` is present; it has one CLI-focused test and no dedicated `storage.py` tests. |
| F8 | maintainability | Documentation can drift from implemented CLI behavior. | Confirmed as a documentation risk; corrected in this package | README now lists only the five implemented commands and explicitly says there is no `export` command. |
| F9 | dependency | The original requirements declaration did not pin pytest. | Confirmed in uploaded source; corrected in this package | Original `requirements.txt` contained only `pytest`. Updated file pins `pytest==9.1.1`, matching the supplied logs. |
| F10 | agent operations | Agent instructions may not be loaded automatically by the assistant/tool. | Unverified as a general tool capability; observed workflow was manual | The file was manually read; no evidence of automatic loading. This is explicitly disclosed rather than assumed. |
| F11 | agent operations | A documented/export feature might be assumed by an agent despite not existing. | Unsupported as an implemented feature; corrected documentation | The supplied code has no export command. README now states this clearly. |

No separate evidence in the supplied archive establishes a vulnerability involving network exposure, credentials, or deployment. The project appears local/offline in the inspected code, but this is not a full security certification.

---

## Task 05 — Risk register

Scales: Likelihood (L) and Impact (I) are 1–3; score = L × I. Scores are qualitative review estimates, not measured probabilities.

| Risk ID | Cause / event / consequence | Affected component | Owner | L×I (initial) | Mitigation | Verification plan | Residual risk |
|---|---|---|---|---:|---|---|---|
| F1 | Deletion changes list length; next ID based on list length can duplicate an existing ID; later completion/deletion may target the wrong task. | `tracker.py: TaskTracker.add/delete/complete` | Developer | 3×3=9 | Generate next ID from maximum existing ID plus one; add regression tests. | Run `test_id_not_reused_after_delete` and `test_complete_targets_correct_task_after_delete`; inspect diff. | Low; unusual imported data with duplicate IDs is not normalized. |
| F2 | Missing input validation allows invalid priority/date values; sorting or downstream use may fail or store inconsistent records. | `tracker.py: TaskTracker.add`; `cli.py: add` | Developer | 2×3=6 | Validate priority and real `YYYY-MM-DD` date before append; convert CLI `ValueError` into argparse error. | Run invalid/valid input tests and CLI test; confirm invalid task is not saved. | Low; title validation and loaded-file schema validation remain outside this fix. |
| F3 | JSON file is corrupted or truncated; `json.load` raises and CLI cannot recover gracefully. | `storage.py: load`; CLI startup | Developer | 2×3=6 | Add clear error handling, backup/recovery policy, and storage tests. | Test malformed JSON, empty file, missing file, and valid file; verify original data is preserved. | Medium until recovery behavior is implemented. |
| F4 | Process stops during direct write; target JSON may be truncated and tasks lost. | `storage.py: save` | Developer | 1×3=3 | Write to a temporary file in the same directory, flush/close, then `os.replace`; consider backup and locking if concurrent use is required. | Simulate write failure before replace; verify old file remains readable; test successful replacement. | Low–medium; filesystem and concurrent-process behavior still matter. |
| F5 | Running CLI from another directory reads/writes a different `tasks.json`; user may think tasks disappeared. | `storage.py: DATA_FILE`; CLI working directory | Developer / user | 2×2=4 | Add explicit `--file` option or document a stable absolute data location. | Run from two working directories and verify/document which file is used. | Medium while path remains CWD-relative. |
| F6 | Parsed JSON has wrong shape or field types; code indexing task keys may raise or behave unexpectedly. | `storage.py: load`; `tracker.py` consumers | Developer | 2×2=4 (provisional) | Validate top-level list and required task fields/types; reject safely. | Test object instead of list, missing keys, wrong types, duplicate IDs. | Medium; risk score provisional because no malformed-file test was supplied. |
| F7 | Storage/CLI regression goes unnoticed due to limited coverage. | `storage.py`, `cli.py`, `tests/` | Developer | 2×2=4 | Add focused storage and CLI tests. | Coverage checklist: missing file, valid load/save, malformed JSON, CLI add/list/done/delete/error. | Medium until new tests exist. |
| F8 | README/agent docs describe unsupported commands or stale behavior; user/agent follows wrong instructions. | `README.md`, `AGENTS.md` | Maintainer | 2×2=4 | Keep docs synchronized with CLI; review command list against argparse. | Compare README examples to `cli.py` parsers and run each documented command. | Low after this documentation correction; future drift remains possible. |
| F9 | Unpinned pytest can resolve to different versions across machines and produce different behavior. | `requirements.txt` | Maintainer | 2×2=4 | Pin the tested pytest version; update only with review and a test run. | Install from requirements in a clean environment; record Python and pytest versions. | Low for pytest version reproducibility; platform differences remain. |
| F10 | Agent may not know repository-specific rules if `AGENTS.md` is not loaded. | Agent workflow / repository root | Human operator | 2×2=4 (provisional) | Explicitly provide/read instructions at session start and verify tool support; require human diff review. | Record whether the assistant/tool confirms instruction loading; otherwise manually paste/read and record. | Medium until automatic loading is verified in the actual tool. |
| F11 | Agent assumes an export feature exists based on stale or mistaken context; may give invalid usage instructions. | README / agent context / CLI | Human operator | 1×2=2 | State that export is not implemented; keep supported commands explicit. | Check `argparse` subcommands and attempt no undocumented export claim. | Low; no export feature is claimed by current README. |

### Notes on evidence quality

- F1/F2 are backed by before/after regression logs and diffs.
- F3/F4/F5/F7/F8/F9 are grounded in the supplied source tree.
- F6/F10 are explicitly provisional/unverified concerns.
- F11 is a documentation/agent-operation guard, not a confirmed runtime defect.
- Scores are review estimates. Re-score if operational context or new test evidence changes.

---

## Task 06 — Agent-readiness audit

**Required level labels:** Level 1 Baseline, Level 2 Documented, Level 3 Agent-ready.  
**Verdict: Level 2 — Documented.**

| Measure | Status | Evidence / gap |
|---|---|---|
| Repository purpose and architecture | Documented | README and AGENTS.md identify CLI, tracker, storage, tests. |
| Agent instructions | Documented, loading not verified | AGENTS.md has safe/ask-first/forbidden actions; observed read was manual. |
| README accuracy | Improved / documented | Commands align with current `argparse` implementation; no export feature is claimed. |
| Tests | Partial | 20 passing in supplied historical Linux/Python 3.13.18 log; storage lacks dedicated tests. |
| Pinned dependencies | Yes in this package | `pytest==9.1.1`; the uploaded original requirements file was unpinned. |
| Logging | No | No application logging configuration or structured operational logs are shown. Test runner output exists, but that is not application logging. |
| Security safeguards | Partial | No secrets/network/deployment path is evident in the small CLI; JSON schema validation and robust error handling are missing. |
| Lint | No | No Ruff/Flake8 config and no lint run evidence. |
| Type check | No | No mypy config and no type-check evidence. |
| Build | Not applicable / not configured | No package build configuration or build command is present. |
| CI | No | No CI workflow is included. |
| Human review gate | Documented | AGENTS.md requires diff review and approval before risky changes. |

**Why not Level 1 Baseline:** repository structure, agent rules, and tests are documented.

**Why not Level 3 Agent-ready:** automatic instruction loading is unverified; there is no CI, lint/type-check gate, application logging, or adequate storage test coverage. Human supervision remains necessary.

---

## Task 07 — Fixes, mitigation records and regression evidence

### Historical test results supplied in the archive

| Stage | Tests | Result |
|---|---:|---|
| Baseline | 9 | 9 passed |
| Before fixes, with regression tests added | 20 | 9 failed, 11 passed |
| After fixes | 20 | 20 passed |

See `logs/01_baseline.log`, `logs/02_before_fix.log`, and `logs/03_after_fix.log`. These are historical Linux/Python 3.13.18 outputs.

### Mitigation record — F1

- **Risk ID:** F1 — task ID reuse after deletion.
- **Change:** `TaskTracker.add()` now calculates the next ID as `max(existing IDs, default=0) + 1`, rather than `len(tasks) + 1`.
- **Tests:** `test_id_not_reused_after_delete`; `test_complete_targets_correct_task_after_delete`.
- **Recorded result:** both tests pass in `logs/03_after_fix.log`; the first failed before the fix.
- **Updated score:** initial 9 (L3×I3); residual estimate 3 (L1×I3). This is a qualitative reassessment, not a measured probability.
- **Residual note:** pre-existing imported data with duplicate IDs is not repaired by this change.

### Mitigation record — F2

- **Risk ID:** F2 — invalid priority/date accepted.
- **Change:** `tracker.py` validates priority against `high/medium/low` and due date against a real `YYYY-MM-DD` calendar date. `cli.py` catches `ValueError` and reports it through `parser.error()`.
- **Tests:** `test_invalid_priority_rejected`; parameterized `test_invalid_due_rejected`; `test_rejected_task_is_not_stored`; `test_valid_due_and_none_accepted`; `test_cli_rejects_invalid_priority`.
- **Recorded result:** all related tests pass in `logs/03_after_fix.log`; the invalid-input tests failed before the fix.
- **Updated score:** initial 6 (L2×I3); residual estimate 3 (L1×I3). This is a qualitative reassessment.
- **Residual note:** title validation and validation of records loaded from an existing JSON file are not covered by this fix.

### Tests not run / not evidenced

- Windows + Python 3.12 full `pytest -v` run by the submitter.
- Ruff/Flake8 lint.
- mypy type checking.
- Build/package creation.
- Dedicated storage tests.
- Broader CLI tests beyond the single included CLI validation test.
- Corrupted JSON, interrupted write, file locking, and multi-process tests.
- CI pipeline.

### Screenshots still required from the submitter

Capture the actual local terminal after running:

```powershell
python --version
python -m pytest -v
```

If pytest is not installed in the active environment, install from the pinned file first:

```powershell
python -m pip install -r requirements.txt
python -m pytest -v
```

Take a screenshot showing the command, Python version if practical, and final pytest summary. Do not edit the supplied historical logs to make them look like a Windows run.

---

## Task 08 — Hypothetical background-agent plan

**Goal:** address F3/F4/F7 (storage error handling, atomic save, and storage tests).

### Allowed commands

- Read files in the repository.
- `git status`, `git diff`, `git log` (if a Git repository is present).
- `python --version`.
- `python -m pytest -v` and focused pytest node IDs.
- `python -m compileall -q tasktracker tests`.
- No package installation or network access without human approval.

### File permissions

| Permission | Paths |
|---|---|
| May edit | `tasktracker/storage.py`, new `tests/test_storage.py` |
| Read-only | `tasktracker/tracker.py`, `tasktracker/cli.py`, existing tests, README, AGENTS.md |
| Forbidden to edit | `requirements.txt`, `.venv/`, `tasks.json`, `.git/` internals, files outside repository |

### Controls and stop conditions

- Work on a separate branch `agent/storage-robustness`; never work directly on `main`.
- Maximum 20 minutes and at most 5 test runs.
- Stop if an existing test fails and cannot be fixed without changing that test, if a non-allowlisted file must change, or if the time limit is reached.
- Do not deploy, publish, push, access secrets, or run network commands.
- Produce a diff, exact before/after test output, and a list of unverified items.
- Human reviews the complete diff and reruns tests locally. Only the human merges.
- Rollback by discarding the agent branch; leave `main` untouched.

### Required output artifacts

1. **Build result:** no build is configured for this repository; report `Not configured / not run`, not “passed”.
2. **Risk notes:** updated F3/F4/F7 status, evidence, residual score, and unverified cases.
3. **Test evidence:** exact command, Python/pytest versions, output, and screenshots from the human's machine.
4. **Change record:** one focused commit per risk, only after human approval. No commit hash is supplied in this archive.

---

## Task 09 — Release decision

**CONDITIONAL GO** for v0.1 as a personal/learning tool only.

### Basis

- F1 and F2 fixes are present and regression-tested in the supplied log.
- The supplied after-fix test session reports 20 passed.
- README and requirements have been improved in this package.
- The app is a small local CLI; no deployment or network service is part of the supplied code.

### Conditions before wider or important-data use

1. Add a safe corrupted-JSON handling and recovery/backup strategy (F3).
2. Implement atomic save and define whether concurrent access is supported (F4).
3. Add storage and broader CLI tests (F7).
4. Validate loaded JSON structure and task records (F6).
5. Re-run tests on the actual target environment (Windows/Python 3.12).
6. Keep F5's working-directory behavior clearly documented or add a deliberate file-path option.

No claim is made that these open risks have been fixed.

---

## Task 10 — AI reflection draft

> **Please edit this into your own truthful account before submission.** The model/version and personal actions must not be claimed unless you can confirm them.

Бұл тапсырмада AI көмекшісі ретінде Claude қолданылды. Оған Task Tracker репозиторийінің файлдары, `README.md`, `AGENTS.md`, тесттер және бастапқы тест логтары контекст ретінде берілді. Нақты Claude моделінің нұсқасы жазылып алынбағандықтан, есепте тек Claude деп көрсетілді.

AI бастапқы кодты қарап, тәуекелдерді санаттауға және құжаттарды реттеуге көмектесті. Бірақ ұсыныстардың бәрін бірден дұрыс деп қабылдамадым. Мысалы, кодта жоқ `export` командасын құжаттауға болмайтыны тексерілді. Сондай-ақ `.venv` репозиторийге қосылады деген күдік `.gitignore` мазмұнымен салыстырылып, дәлелденбеген тұжырым ретінде қаралды.

Ең маңызды екі түзету Task ID қайталануын болдырмау және priority мен due date мәндерін тексеру болды. Бұлар үшін регрессиялық тесттер қосылған. Берілген логтарда бастапқы 9 тест өткен, жаңа тесттер қосылған кезде 9 тест құлаған, ал түзетуден кейін 20 тест өткен. Осы нәтижелер AI ұсынған өзгерістерді тест арқылы тексерудің маңызын көрсетті. Тесттер шешімге әсер етті: тек кодты өзгерту жеткіліксіз болды, өзгерістің бұрынғы функцияларды бұзбағанын да тексеру керек болды.

Менің тарапымнан тексерілуі тиіс нәрселердің бірі — өз Windows/Python 3.12 ортасында `pytest -v` командасын қайта орындау. Берілген логтар Linux/Python 3.13.18 ортасында жасалған, сондықтан оларды өз компьютерімдегі нәтиже ретінде көрсету дұрыс емес. Сонымен қатар lint, type check және build орындалған жоқ; репозиторийде оларға арналған конфигурация да жоқ.

`AGENTS.md` файлындағы қауіпсіз командалар, тыйым салынған әрекеттер және diff-ті адам тексеруі туралы ережелер жұмысты жүйелеуге көмектесті. Бірақ файл автоматты түрде жүктелгені дәлелденген жоқ: ол осы жұмыс барысында қолмен оқылды. Келесі жолы AI қолданғанда модель нұсқасын, нақты контексті, орындалған командаларды және тест нәтижелерін басынан бастап жазып отырамын. Сондай-ақ storage тесттерін, CI, lint және type checking қосу керек.

Негізгі қорытындым: AI кодты талдауды және құжат дайындауды жылдамдатады, бірақ дәлелді тексеру, тестті нақты ортада орындау және соңғы шешімді қабылдау адам жауапкершілігінде қалады.

---

## AI-use record

| Field | Record |
|---|---|
| AI assistant name | Claude |
| Exact model/version | Not recorded in supplied evidence |
| Context provided | Task Tracker repository files, README, AGENTS.md, tests, diffs, and historical test logs |
| Intended AI role | Code review, risk identification/classification, documentation and reflection drafting |
| Human verification expected | Inspect source and diffs; rerun tests; verify claims against repository; capture local evidence |
| AGENTS.md handling | Manually read during review; automatic loading not verified |
| AI limitations recorded | Model version absent; included logs are Linux/Python 3.13.18; Windows/Python 3.12 not verified |
| Human responsibility | Confirm factual accuracy, run local tests, take screenshots, verify submission format, and write personal reflection truthfully |

## AI evidence appendix

The following items are included in the archive:

- `AGENTS.md` — repository instructions and human approval gates.
- `README.md` — current usage and known limitations.
- `ACCEPTANCE_CRITERIA.md` — five measurable criteria and test mapping.
- `logs/01_baseline.log` — baseline test output (9 passed).
- `logs/02_before_fix.log` — regression test output before fixes (9 failed, 11 passed).
- `logs/03_after_fix.log` — test output after fixes (20 passed).
- `logs/tracker.diff` — core tracker changes.
- `logs/cli.diff` — CLI validation error handling change.

**Evidence not included / still to be supplied by the student:**

- Screenshot of the student's own Windows/Python 3.12 `python -m pytest -v` run.
- Baseline and final Git commit hashes or repository URL. The supplied ZIP does not contain a `.git` directory, so commit history cannot be verified from this archive.
- Separate F1 and F2 commit hashes. The supplied diffs show code changes but do not establish separate commits.
- Screenshot or transcript showing the exact AI model/version, if the platform exposes it.
- Instructor/Teams confirmation of required submission file format.

## Submission checklist

- [ ] Run `python --version` on the target Windows machine.
- [ ] Run `python -m pip install -r requirements.txt` if needed.
- [ ] Run `python -m pytest -v` and capture an authentic screenshot.
- [ ] If required, create/verify baseline, F1, F2, and final commits; record hashes.
- [ ] Confirm whether SIS #05 requires PDF, ZIP, or both.
- [ ] Edit Task 10 so it describes only actions personally performed.
- [ ] Review every claim and remove anything not personally verified.
