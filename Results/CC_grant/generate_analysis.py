import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data
base = pd.read_csv(os.path.join(OUTPUT_DIR, 'base_summary-original.csv'))
np_at = pd.read_csv(os.path.join(OUTPUT_DIR, 'np_at_rt_summary.csv'))

users = base['Concurrent Users'].values
labels = [str(u) for u in users]

# Key metrics extraction
base_tps = base['Throughput (Requests/sec)'].values
np_tps = np_at['Throughput (Requests/sec)'].values

base_avg_rt = base['Average Response Time (ms)'].values
np_avg_rt = np_at['Average Response Time (ms)'].values

base_p95 = base['95th Percentile of Response Time (ms)'].values
np_p95 = np_at['95th Percentile of Response Time (ms)'].values

base_p99 = base['99th Percentile of Response Time (ms)'].values
np_p99 = np_at['99th Percentile of Response Time (ms)'].values

base_samples = base['# Samples'].values
np_samples = np_at['# Samples'].values

base_stddev = base['Standard Deviation of Response Time (ms)'].values
np_stddev = np_at['Standard Deviation of Response Time (ms)'].values

base_max = base['Maximum Response Time (ms)'].values
np_max = np_at['Maximum Response Time (ms)'].values

base_min = base['Minimum Response Time (ms)'].values
np_min = np_at['Minimum Response Time (ms)'].values

# Compute percentage differences (np vs base, positive = np is better)
tps_diff_pct = ((np_tps - base_tps) / base_tps) * 100
avg_rt_diff_pct = ((np_avg_rt - base_avg_rt) / base_avg_rt) * 100  # negative = np is better
p95_diff_pct = ((np_p95 - base_p95) / base_p95) * 100
p99_diff_pct = ((np_p99 - base_p99) / base_p99) * 100

# ── Color scheme ──
COLOR_BASE = '#2196F3'
COLOR_NP = '#FF9800'
COLOR_IMPROVEMENT = '#4CAF50'
COLOR_DEGRADATION = '#F44336'

bar_width = 0.35
x = np.arange(len(users))

# ═══════════════════════════════════════════════════════════════
# GRAPH 1 — Throughput Comparison
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - bar_width/2, base_tps, bar_width, label='Base (Persistent AT)', color=COLOR_BASE)
bars2 = ax.bar(x + bar_width/2, np_tps, bar_width, label='Non-Persistent AT', color=COLOR_NP)
ax.set_xlabel('Concurrent Users', fontsize=12)
ax.set_ylabel('Throughput (Requests/sec)', fontsize=12)
ax.set_title('Throughput Comparison — Client Credential Grant (15 min)', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{bar.get_height():.0f}', ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{bar.get_height():.0f}', ha='center', va='bottom', fontsize=8)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'graph_throughput_comparison.png'), dpi=150)
plt.close(fig)

# ═══════════════════════════════════════════════════════════════
# GRAPH 2 — Average Response Time Comparison
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(users, base_avg_rt, 'o-', color=COLOR_BASE, label='Base (Persistent AT)', linewidth=2, markersize=8)
ax.plot(users, np_avg_rt, 's-', color=COLOR_NP, label='Non-Persistent AT', linewidth=2, markersize=8)
for i, (b, n) in enumerate(zip(base_avg_rt, np_avg_rt)):
    ax.annotate(f'{b:.1f}', (users[i], b), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color=COLOR_BASE)
    ax.annotate(f'{n:.1f}', (users[i], n), textcoords="offset points", xytext=(0, -15), ha='center', fontsize=8, color=COLOR_NP)
ax.set_xlabel('Concurrent Users', fontsize=12)
ax.set_ylabel('Avg Response Time (ms)', fontsize=12)
ax.set_title('Average Response Time — Client Credential Grant (15 min)', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'graph_avg_response_time.png'), dpi=150)
plt.close(fig)

# ═══════════════════════════════════════════════════════════════
# GRAPH 3 — P95 & P99 Latency Comparison
# ═══════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
# P95
ax1.bar(x - bar_width/2, base_p95, bar_width, label='Base (Persistent AT)', color=COLOR_BASE)
ax1.bar(x + bar_width/2, np_p95, bar_width, label='Non-Persistent AT', color=COLOR_NP)
ax1.set_xlabel('Concurrent Users')
ax1.set_ylabel('P95 Response Time (ms)')
ax1.set_title('95th Percentile Response Time', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.legend()
# P99
ax2.bar(x - bar_width/2, base_p99, bar_width, label='Base (Persistent AT)', color=COLOR_BASE)
ax2.bar(x + bar_width/2, np_p99, bar_width, label='Non-Persistent AT', color=COLOR_NP)
ax2.set_xlabel('Concurrent Users')
ax2.set_ylabel('P99 Response Time (ms)')
ax2.set_title('99th Percentile Response Time', fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(labels)
ax2.legend()
plt.suptitle('Tail Latency Comparison — Client Credential Grant (15 min)', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'graph_p95_p99_latency.png'), dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════════════════════
# GRAPH 4 — % Improvement in Throughput & Avg RT
# ═══════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
colors_tps = [COLOR_IMPROVEMENT if v > 0 else COLOR_DEGRADATION for v in tps_diff_pct]
bars = ax1.bar(labels, tps_diff_pct, color=colors_tps, edgecolor='white')
for bar, val in zip(bars, tps_diff_pct):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'+{val:.1f}%', ha='center', fontsize=9, fontweight='bold')
ax1.set_xlabel('Concurrent Users')
ax1.set_ylabel('% Change in Throughput')
ax1.set_title('Throughput Improvement (Non-Persistent vs Base)', fontweight='bold')
ax1.axhline(y=0, color='black', linewidth=0.5)
ax1.grid(axis='y', alpha=0.3)

colors_rt = [COLOR_IMPROVEMENT if v < 0 else COLOR_DEGRADATION for v in avg_rt_diff_pct]
bars = ax2.bar(labels, avg_rt_diff_pct, color=colors_rt, edgecolor='white')
for bar, val in zip(bars, avg_rt_diff_pct):
    offset = -3 if val < 0 else 1
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + offset, f'{val:.1f}%', ha='center', fontsize=9, fontweight='bold')
ax2.set_xlabel('Concurrent Users')
ax2.set_ylabel('% Change in Avg Response Time')
ax2.set_title('Avg Response Time Reduction (Non-Persistent vs Base)', fontweight='bold')
ax2.axhline(y=0, color='black', linewidth=0.5)
ax2.grid(axis='y', alpha=0.3)

plt.suptitle('Performance Gains — Non-Persistent AT vs Base', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'graph_percentage_improvement.png'), dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════════════════════
# GRAPH 5 — Total Samples (Requests Served in 15 min)
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - bar_width/2, base_samples, bar_width, label='Base (Persistent AT)', color=COLOR_BASE)
bars2 = ax.bar(x + bar_width/2, np_samples, bar_width, label='Non-Persistent AT', color=COLOR_NP)
ax.set_xlabel('Concurrent Users', fontsize=12)
ax.set_ylabel('Total Requests Served', fontsize=12)
ax.set_title('Total Requests Served in 15 Minutes — Client Credential Grant', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000, f'{bar.get_height()/1000:.0f}K', ha='center', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000, f'{bar.get_height()/1000:.0f}K', ha='center', fontsize=8)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'graph_total_samples.png'), dpi=150)
plt.close(fig)

# ═══════════════════════════════════════════════════════════════
# GRAPH 6 — Response Time Distribution (Min/Avg/P95/P99/Max)
# ═══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 5, figsize=(20, 5), sharey=False)
for i, (u, ax_i) in enumerate(zip(users, axes)):
    categories = ['Min', 'Avg', 'P95', 'P99', 'Max']
    base_vals = [base_min[i], base_avg_rt[i], base_p95[i], base_p99[i], base_max[i]]
    np_vals = [np_min[i], np_avg_rt[i], np_p95[i], np_p99[i], np_max[i]]
    bx = np.arange(len(categories))
    bw = 0.35
    ax_i.bar(bx - bw/2, base_vals, bw, label='Base', color=COLOR_BASE)
    ax_i.bar(bx + bw/2, np_vals, bw, label='Non-Persistent', color=COLOR_NP)
    ax_i.set_title(f'{u} Users', fontweight='bold')
    ax_i.set_xticks(bx)
    ax_i.set_xticklabels(categories, fontsize=8, rotation=45)
    ax_i.set_ylabel('Response Time (ms)' if i == 0 else '')
    if i == 0:
        ax_i.legend(fontsize=7)
plt.suptitle('Response Time Distribution by Concurrency Level', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'graph_response_time_distribution.png'), dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════════════════════
# Generate Markdown Analysis Report
# ═══════════════════════════════════════════════════════════════
report = """# Performance Analysis: Client Credential Grant (15-minute test)

## Test Configuration
| Parameter | Value |
|-----------|-------|
| **Grant Type** | Client Credentials |
| **Test Duration** | 15 minutes |
| **Heap Size** | 4G |
| **Concurrent User Levels** | 50, 100, 150, 300, 500 |
| **Error Rate** | 0% (both configurations) |

## Configurations Compared
| Label | Description |
|-------|-------------|
| **Base (Persistent AT)** | Base pack with persistent access token |
| **Non-Persistent AT** | Non-persistent access token feature enabled |

---

## Executive Summary

The **Non-Persistent Access Token** configuration delivers a **major performance improvement** across all concurrency levels compared to the base persistent access token setup.

### Key Highlights
- **Throughput doubled**: Non-persistent AT achieves ~2x the throughput of the base at every concurrency level
- **Response times halved**: Average response times are ~40-54% lower across all loads
- **2x more requests served**: In the same 15-minute window, non-persistent AT served roughly double the total requests
- **Zero errors**: Both configurations maintained 0% error rate throughout
- **Higher load tolerance at lower concurrency** observed in non-persistent AT with significantly better min response times (2ms vs 6-7ms)

---

## Detailed Metrics Comparison

### Throughput (Requests/sec)

| Concurrent Users | Base (Persistent AT) | Non-Persistent AT | Improvement |
|:---:|:---:|:---:|:---:|
"""

for i, u in enumerate(users):
    report += f"| {u} | {base_tps[i]:.2f} | {np_tps[i]:.2f} | **+{tps_diff_pct[i]:.1f}%** |\n"

report += """
![Throughput Comparison](graph_throughput_comparison.png)
![Percentage Improvement](graph_percentage_improvement.png)

**Analysis:**
"""

report += f"""
- Throughput improvement ranges from **+{tps_diff_pct.min():.1f}%** (at {users[np.argmin(tps_diff_pct)]} users) to **+{tps_diff_pct.max():.1f}%** (at {users[np.argmax(tps_diff_pct)]} users).
- The base configuration scales from {base_tps[0]:.0f} to {base_tps[-1]:.0f} TPS ({((base_tps[-1]-base_tps[0])/base_tps[0]*100):.1f}% increase) as users grow from 50 to 500.
- The non-persistent configuration stays remarkably stable: {np_tps[0]:.0f} to {np_tps[-1]:.0f} TPS — only a {((np_tps[0]-np_tps[-1])/np_tps[0]*100):.1f}% drop, indicating **superior scalability under load**.
- At 500 concurrent users, non-persistent AT delivers **{np_tps[-1]/base_tps[-1]:.2f}x** the throughput of the base.

"""

report += """### Average Response Time (ms)

| Concurrent Users | Base (Persistent AT) | Non-Persistent AT | Improvement |
|:---:|:---:|:---:|:---:|
"""

for i, u in enumerate(users):
    report += f"| {u} | {base_avg_rt[i]:.2f} | {np_avg_rt[i]:.2f} | **{avg_rt_diff_pct[i]:.1f}%** |\n"

report += """
![Average Response Time](graph_avg_response_time.png)

**Analysis:**
"""

report += f"""
- Average response time is consistently lower for non-persistent AT across all concurrency levels.
- The improvement ranges from **{abs(avg_rt_diff_pct).min():.1f}%** to **{abs(avg_rt_diff_pct).max():.1f}%** reduction.
- At 500 users, base averages {base_avg_rt[-1]:.1f}ms vs non-persistent at {np_avg_rt[-1]:.1f}ms — a **{base_avg_rt[-1] - np_avg_rt[-1]:.1f}ms** reduction.
- Non-persistent AT's response time growth is more linear — from {np_avg_rt[0]:.1f}ms to {np_avg_rt[-1]:.1f}ms — suggesting **predictable latency scaling**.

"""

report += """### Tail Latency (P95 & P99)

| Concurrent Users | Base P95 | NP P95 | Base P99 | NP P99 |
|:---:|:---:|:---:|:---:|:---:|
"""

for i, u in enumerate(users):
    report += f"| {u} | {base_p95[i]:.0f} | {np_p95[i]:.0f} | {base_p99[i]:.0f} | {np_p99[i]:.0f} |\n"

report += """
![P95 and P99 Latency](graph_p95_p99_latency.png)

**Analysis:**
"""

report += f"""
- At low concurrency (50 users), non-persistent AT has significantly lower tail latency: P95 = {np_p95[0]:.0f}ms vs {base_p95[0]:.0f}ms.
- At high concurrency (500 users), non-persistent AT P95 ({np_p95[-1]:.0f}ms) **exceeds** base P95 ({base_p95[-1]:.0f}ms) — a **{((np_p95[-1]-base_p95[-1])/base_p95[-1]*100):.1f}%** increase.
- Similarly, P99 at 500 users: non-persistent = {np_p99[-1]:.0f}ms vs base = {base_p99[-1]:.0f}ms — a **{((np_p99[-1]-base_p99[-1])/base_p99[-1]*100):.1f}%** increase.
- **Critical observation**: While average and median response times are far superior for non-persistent AT, the **tail latency (P95/P99) degrades significantly at 300+ concurrent users**. This suggests occasional long-running requests, likely due to token generation overhead without caching.

"""

report += """### Response Time Variability (Standard Deviation)

| Concurrent Users | Base StdDev (ms) | NP StdDev (ms) |
|:---:|:---:|:---:|
"""

for i, u in enumerate(users):
    report += f"| {u} | {base_stddev[i]:.2f} | {np_stddev[i]:.2f} |\n"

report += f"""
**Analysis:**
- Non-persistent AT shows **higher variability** at elevated concurrency levels.
- At 50 users: base StdDev = {base_stddev[0]:.1f}ms vs NP = {np_stddev[0]:.1f}ms — NP is **more consistent**.
- At 500 users: base StdDev = {base_stddev[-1]:.1f}ms vs NP = {np_stddev[-1]:.1f}ms — NP has **{np_stddev[-1]/base_stddev[-1]:.1f}x higher variance**.
- The growing variance correlates with the tail latency spikes observed above, indicating that while most requests complete very fast, a small fraction experience significant delays under high load.

"""

report += """### Maximum Response Time

| Concurrent Users | Base Max (ms) | NP Max (ms) |
|:---:|:---:|:---:|
"""

for i, u in enumerate(users):
    report += f"| {u} | {base_max[i]} | {np_max[i]} |\n"

report += f"""
**Analysis:**
- Maximum response times for non-persistent AT are dramatically higher at elevated loads.
- At 500 users: base max = {base_max[-1]}ms vs NP max = {np_max[-1]}ms — **{np_max[-1]/base_max[-1]:.1f}x higher**.
- This indicates rare but severe latency spikes in the non-persistent configuration, likely from token generation contention or GC pauses under high throughput.

"""

report += """### Total Requests Served (15 minutes)

| Concurrent Users | Base | Non-Persistent AT | Multiplier |
|:---:|:---:|:---:|:---:|
"""

for i, u in enumerate(users):
    report += f"| {u} | {base_samples[i]:,} | {np_samples[i]:,} | **{np_samples[i]/base_samples[i]:.2f}x** |\n"

report += """
![Total Samples](graph_total_samples.png)

"""

report += """### Response Time Distribution by Concurrency
![Response Time Distribution](graph_response_time_distribution.png)

---

## Server Load Analysis

| Concurrent Users | Base IS1 Load (1m) | NP IS1 Load (1m) | Base IS2 Load (1m) | NP IS2 Load (1m) |
|:---:|:---:|:---:|:---:|:---:|
"""

base_is1_load = base['WSO2 Identity Server 1 Load Average - Last 1 minute'].values
np_is1_load = np_at['WSO2 Identity Server 1 Load Average - Last 1 minute'].values
base_is2_load = base['WSO2 Identity Server 2 Load Average - Last 1 minute'].values
np_is2_load = np_at['WSO2 Identity Server 2 Load Average - Last 1 minute'].values

for i, u in enumerate(users):
    report += f"| {u} | {base_is1_load[i]:.2f} | {np_is1_load[i]:.2f} | {base_is2_load[i]:.2f} | {np_is2_load[i]:.2f} |\n"

report += f"""
**Analysis:**
- At low concurrency (50-150 users), server load is comparable between configurations.
- At high concurrency (300-500 users), the base configuration shows **dramatically higher server load** (IS1: {base_is1_load[-1]:.1f} vs {np_is1_load[-1]:.1f}).
- The base configuration's IS1 load spikes to {base_is1_load[-1]:.1f} at 500 users, while non-persistent stays at {np_is1_load[-1]:.1f} — suggesting that **persistent token storage creates significant I/O and CPU overhead** at scale.
- The non-persistent configuration maintains **stable, moderate load** across all concurrency levels, indicating better resource efficiency.

---

## Critical Findings & Recommendations

### Strengths of Non-Persistent AT
1. **~2x throughput** across all concurrency levels — the most significant finding
2. **~40-54% lower average response times** — consistently faster for the majority of requests
3. **Dramatically lower server load** at high concurrency — better resource utilization
4. **Stable throughput** that doesn't degrade much as users increase (2163 → 2075 TPS)
5. **Zero errors** maintained throughout — reliability is not compromised
6. **Lower minimum response times** (2ms vs 6-7ms) — faster best-case performance

### Concerns with Non-Persistent AT
1. **Higher tail latency (P95/P99) at 300+ users** — occasional slow requests
2. **Higher response time variance** under load — less predictable for individual requests
3. **Significantly higher max response times** (up to {np_max[-1]}ms vs {base_max[-1]}ms at 500 users) — rare but severe outliers
4. **Higher server load on IS2** — load is shifted/distributed differently

### Recommendations
1. **Non-persistent AT is recommended for production** — the throughput gains far outweigh the tail latency concerns for most use cases
2. **Monitor P99 latency** in production at high concurrency — set alerts for response times exceeding 2000ms
3. **Investigate max response time outliers** — the 8563ms max at 500 users may indicate a specific bottleneck (e.g., connection pool exhaustion, GC pause)
4. **Consider connection pooling tuning** to reduce tail latency spikes under high concurrency
5. **Test at higher concurrency levels** (750, 1000 users) to understand the upper scaling limit of non-persistent AT
"""

with open(os.path.join(OUTPUT_DIR, 'analysis_report.md'), 'w') as f:
    f.write(report)

print("Analysis complete. Generated files:")
print("  - analysis_report.md")
print("  - graph_throughput_comparison.png")
print("  - graph_avg_response_time.png")
print("  - graph_p95_p99_latency.png")
print("  - graph_percentage_improvement.png")
print("  - graph_total_samples.png")
print("  - graph_response_time_distribution.png")
