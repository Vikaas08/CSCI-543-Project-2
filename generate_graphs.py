import matplotlib.pyplot as plt
import numpy as np

# Configure style
plt.style.use('seaborn-v0_8-whitegrid')
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# --- Graph 1: Selectivity & Data Distributions ---
labels_micro = ['Uniform\n(>500)', 'Uniform\n(<200)', 'Uniform\n(>800)', 'Uniform\n(>900)', 'Skewed\n(>800)', 'Bimodal\n(>800)']
io_red_micro = [43.75, 74.22, 73.51, 82.94, 34.45, 0.0]
speedup_micro = [1.53, 5.19, 3.59, 4.39, 1.49, 1.09]

x = np.arange(len(labels_micro))
width = 0.4

ax1_2 = ax1.twinx()
ax1.bar(x, io_red_micro, width, color='#3498db', alpha=0.8)
ax1_2.plot(x, speedup_micro, color='#e74c3c', marker='o', linewidth=2.5, markersize=8)

ax1.set_title('Micro-Benchmarks: Selectivity Impact', fontsize=13, pad=15)
ax1.set_ylabel('I/O Reduction (%)', color='#2980b9', fontweight='bold', fontsize=11)
ax1_2.set_ylabel('Latency Speedup (x)', color='#c0392b', fontweight='bold', fontsize=11)
ax1.set_xticks(x)
ax1.set_xticklabels(labels_micro, rotation=45, ha='right')
ax1.set_ylim(0, 100)
ax1_2.set_ylim(0, 6)
ax1.grid(axis='y', linestyle='--', alpha=0.5)

# --- Graph 2: Real-World Scenarios ---
labels_rw = ['IoT Temp\nAnomaly', 'Net Latency\nViolation', 'CPU High\nLoad', 'DB Slow\nQuery', 'App Memory\nLeak', 'High Disk\nI/O']
io_red_rw = [28.98, 4.03, 4.39, 0.0, 57.97, 89.38]
speedup_rw = [1.39, 1.48, 0.88, 0.92, 3.02, 10.19]

x_rw = np.arange(len(labels_rw))

ax2_2 = ax2.twinx()
ax2.bar(x_rw, io_red_rw, width, color='#2ecc71', alpha=0.8)
ax2_2.plot(x_rw, speedup_rw, color='#8e44ad', marker='s', linewidth=2.5, markersize=8)

ax2.set_title('Real-World Scenarios: Performance', fontsize=13, pad=15)
ax2.set_ylabel('I/O Reduction (%)', color='#27ae60', fontweight='bold', fontsize=11)
ax2_2.set_ylabel('Latency Speedup (x)', color='#8e44ad', fontweight='bold', fontsize=11)
ax2.set_xticks(x_rw)
ax2.set_xticklabels(labels_rw, rotation=45, ha='right')
ax2.set_ylim(0, 100)
ax2_2.set_ylim(0, 12)
ax2.grid(axis='y', linestyle='--', alpha=0.5)

# --- Graph 3: Scalability ---
labels_scale = ['1M', '10M', '50M', '100M', '500M']
speedup_scale = [1.31, 1.13, 1.25, 1.19, 1.09]

ax3.plot(labels_scale, speedup_scale, color='#f39c12', marker='^', linewidth=2.5, markersize=10)
ax3.fill_between(labels_scale, speedup_scale, 1.0, color='#f39c12', alpha=0.15)
ax3.axhline(1.0, color='gray', linestyle='dashed', alpha=0.7)

ax3.set_title('Scalability: Speedup Across Scales', fontsize=13, pad=15)
ax3.set_xlabel('Total Records', fontweight='bold', fontsize=11)
ax3.set_ylabel('Query Speedup (x)', color='#d68910', fontweight='bold', fontsize=11)
ax3.set_ylim(0.8, 1.5)
ax3.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('bitweave_performance.png', dpi=300, bbox_inches='tight')
print("Graph saved successfully as 'bitweave_performance.png'")