# Adaptive Batch Scheduling Architecture

## Background

The system runs batch jobs across heterogeneous compute nodes. Jobs differ in CPU, memory, I/O, GPU, and external service usage. Existing first-in-first-out scheduling causes resource fragmentation and unstable completion time when many jobs enter the queue at once.

## Components

1. **Job intake collector**: records declared resource needs, historical runtime, retry count, deadline class, and dependency state.
2. **Node resource profiler**: samples available CPU, memory, I/O pressure, GPU occupancy, and recent failure rate.
3. **Compatibility scorer**: computes a score between each pending job and each candidate node. The score considers resource fit, risk of memory pressure, queue age, and deadline class.
4. **Throttled reorderer**: reorders only a bounded window of pending jobs to avoid starvation and large scheduling oscillations.
5. **Feedback updater**: compares predicted runtime and actual runtime, then adjusts future scoring weights within a bounded range.

## Key Technical Detail

The reorderer does not globally sort the whole queue. It selects a sliding candidate window, filters jobs with unresolved dependencies, calculates job-node compatibility, and then applies a throttling factor to limit how far a job can move forward or backward. This reduces starvation risk while still improving resource utilization.

## Example Parameters

- Candidate window: 20 to 200 jobs.
- Weight adjustment range: 0.8 to 1.2.
- Starvation guard: a job exceeding the queue-age threshold receives a priority floor.
- Feedback update interval: every 5 to 30 minutes.

## Expected Technical Effects

- Higher node utilization under mixed CPU/GPU workloads.
- Lower tail latency for deadline-sensitive jobs.
- Lower retry rate caused by resource pressure mismatch.
- More stable scheduling behavior than full-queue resorting.
