Does compressing an agent’s memory change which actions it approves?

I tested eight synthetic workflows with a two-part user constraint and repetitive progress notes. Each had four later candidate actions: one permitted, three forbidden. Qwen2.5 7B and Qwen3 8B each generated a summary, then classified the candidates in three fresh contexts.

Correct candidate sets, in the order full history → summary only → the same summary plus the original rule:
• Qwen2.5: 4/8 → 2/8 → 7/8.
• Qwen3: 6/8 → 5/8 → 6/8.

Forbidden actions selected, in the same order:
• Qwen2.5: 4/24 → 7/24 → 1/24.
• Qwen3: 2/24 → 6/24 → 2/24.

In one Qwen3 cleanup case, the summary dropped both restrictions. The next call approved all four actions. Adding back the rule reduced forbidden selections from 3/3 to 1/3; it still did not produce a correct set.

The full-history baseline also made mistakes. Retaining a rule and following it were separate problems in these outputs. Pinning improved five complete cases for Qwen2.5 and one for Qwen3, with no reverse transitions.

This was 64 local calls: 16 summaries and 48 simulated decision outputs. No actions executed. One summary prompt, one round and eight short authored histories; no real context overflow or production failure-rate estimate. The harness already knew the trusted rule, and pinning added information and length.

INVARIANT coordinated scorer implementation, eight fixed checks and implementation review. A separate auditor checked every request, summary reuse and score against the frozen protocol.

Code, raw outputs and chart:
https://github.com/Xenox-developer/compaction-constraint-lab

Tool — INVARIANT:
https://github.com/Xenox-developer/invariant

Research inspiration — The Compaction Cliff:
https://arxiv.org/abs/2608.22752
