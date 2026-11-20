# Compaction constraint lab

A preregistered synthetic diagnostic of user-constraint retention after one continuation summary. Eight authored workflow histories, four later candidate actions per history, and two already-installed local Ollama models. No action is executed. This is an independent adaptation inspired by *The Compaction Cliff in Long-Running AI Agent Memory*, not a reproduction of Knowledge Triage, Claude /compact, an attack benchmark or a production deployment.

## Comparison

Each model writes one summary for each history, before seeing any candidates. Three fresh consumers receive: the full history; that summary alone; or the **same saved summary** plus the original trusted user constraint copied verbatim. Consumer instructions, schema and candidates are identical. Pinning changes both information availability and length. The harness already knows the authoritative rule; extracting trusted rules automatically is not tested. Each rule has two conjunctive predicates, and the four candidates cover all combinations with one permitted and three forbidden actions. First/middle rule placement is balanced across the histories. Neutral progress text is deliberately repetitive.

See PROTOCOL.md, fixtures.json and schedule.json. Fixed settings: temperature0, seed20261120, num_ctx8192, num_predict384, think=false; 90-second timeout, no retries/repair/tuning. Qwen2.5 7B then Qwen3 8B run sequentially, never resident together. Per model8 summary and24 consumer calls:64 total. Exact installed digests/templates/versions are saved. These short synthetic contexts do not trigger real context overflow or simulate extended autonomous operation.

## Metrics and checks

Exact allowed-ID set /8 cases per condition; binary candidate decisions /32; unsafe admissions /24 forbidden actions; false denials /8 allowed actions; invalid outputs /8 and unknown-ID count. Output order/duplicates are accepted. Denying everything is not task completion, and invalid format is reported separately. One seed, eight authored rules, one summary prompt and older local models cannot estimate real-world failure rates or establish general model rankings. Pinning makes the rule available but does not guarantee model compliance.

Eight fixed acceptance checks cover every domain/predicate, threshold endpoints, positive and negative controls, empty/all/unknown selections, strict parsing and alternative valid output order/duplicates. INVARIANT implements evaluation.py, runs the protected controls, obtains semantic implementation review and applies the reviewed scorer. The host issues the local requests. audit.py separately derives predicate gold/scores, reconstructs exact prompts from frozen literal data without executing the request builder, verifies summary reuse and all64 issuance/response records, settings, digests, coverage and scientific hashes. It imports neither runner nor evaluator. Same-model development review is not an independent scientific replication.

```sh
python3 -B tests/run_checks.py
python3 -B audit.py
python3 plot.py
```

Python3.11+ standard library suffices for tests and stored-data audit. Figure generation additionally uses the existing Matplotlib installation. For a new explicitly requested measurement, use a separate working copy and preserve published results before moving the results/primary folder; then `python3 -B run.py measure`. It refuses an existing run directory. Use the already-installed matching model digests, without other resident models. Do not regenerate evidence to obtain a preferred outcome. Fresh serving/hardware need not produce byte-identical text. The scientific freeze and premeasurement commit are preserved separately from later README/results additions.

## Tool use and usage

[INVARIANT](https://github.com/Xenox-developer/invariant) coordinates scorer implementation, eight protected checks, semantic review and guarded application through the current Codex subscription. Save actual native receipts/IDs/version and all available worker/reviewer usage in evidence. Distinguish native sessions from individual model responses; cached input/reasoning are subsets of totals. Local Ollama token counters are separate. Outer chat usage is unavailable. No paid APIs, rented GPU or model downloads. No real transactions, network calls proposed by models, third-party attacks or commands from research materials are executed.

## Sources and provenance

- Saber Zerhoudi, Jelena Mitrovic and Michael Granitzer, *The Compaction Cliff in Long-Running AI Agent Memory*, submitted August24,2026: https://arxiv.org/abs/2608.22752 . Read scope: abstract, introduction and knowledge-type/compaction framework sections. We did not reproduce their full experiments/code or use their released corpus/classifier. No paper benchmark numbers are our measurements.
- Anthropic, *Effective context engineering for AI agents*, September29,2025: https://www.anthropic.com/research/effective-context-engineering-for-ai-agents . Read scope: context engineering and compaction sections. No Claude API/product evaluation here.

SOURCES.json describes internal discovery scope and CANDIDATES.json records alternatives. All code, histories, rules and outputs in this repository are authored/collected for this project and available under MIT. Third-party papers are linked, not redistributed. Telegram exports, credentials, sessions, private UI state and unrelated Docker/container inventories stay outside the public repository.
