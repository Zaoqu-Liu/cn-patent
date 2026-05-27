# Inventor Meeting Notes

## Pain Points

- FIFO scheduling wastes resources when short CPU-only jobs wait behind long GPU-heavy jobs.
- A pure priority queue improves urgent jobs but causes low-priority jobs to starve.
- Global resorting can make the queue unstable because many jobs change position at the same time.
- Operators need a general mechanism that works across heterogeneous nodes without manually writing per-node rules.

## Candidate Invention Direction

Use resource profiles and job history to compute job-node compatibility. Reorder only a sliding window of pending jobs and apply a throttling factor so queue changes remain bounded. Add a feedback updater that adjusts scoring weights according to actual runtime and failure outcomes.

## Terms To Keep Generic

- Replace internal product names with "batch scheduling system".
- Replace concrete tenant names with "user group".
- Keep parameter values as examples or ranges.

## Disclosure Preference

Prefer a method-and-system disclosure. The technical effect should focus on resource utilization, tail latency, retry reduction, and scheduling stability.
