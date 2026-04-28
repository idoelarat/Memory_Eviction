# Memory Eviction: Vulnerability & Mitigation Report

**Author:** Ido Elarat  
**Project:** Memory Management Unit (MMU) Security Enhancements

---

## 1. Vulnerability Analysis

The original eviction strategy was based on a deterministic **"Cyclical Distance"** calculation. By measuring the maximum distance between a new page ($P_{in}$) and all resident pages ($P_{resident}$) on a fixed circular scale (0–99), the system follows a predictable pattern.

### The Exploitability
Because the algorithm is entirely deterministic, an adversary can predict the system's response to any specific input. 

In the proof-of-concept, `generate_attack_sequence` was able to iterate through possible pages until it identified the exact input required to force the distance calculation to target the frame holding **Page 50**. 
* **Real-world Impact:** This predictability allows an attacker to manipulate the cache state, perform side-channel attacks, or force-evict specific sensitive data at will.

---

## 2. Mitigation Strategy

To mitigate this vulnerability, the deterministic logic was replaced with a **Random Replacement** policy.

### The Logic
Instead of calculating distances, the system now selects a victim frame using a pseudorandom number generator:
`random.randint(0, NUM_FRAMES - 1)`

* **Entropy:** This introduces entropy into the memory management unit. 
* **Security Gain:** Even if an attacker possesses perfect knowledge of the RAM's current state, they can no longer calculate a "guaranteed" input to evict a specific target page. 
* **Outcome:** The probability of a successful targeted eviction is significantly reduced, rendering reliable, repeatable attacks impossible.

---

## 3. Empirical Results (Benchmark)

Both algorithms were tested against a trace of **1,000 random memory accesses** to evaluate the performance trade-offs of the security patch.

| Algorithm | Fault Count (1,000 runs) | Vulnerability Status |
| :--- | :--- | :--- |
| **Original (Cyclical)** | 962 | 🔴 High (Deterministic) |
| **Patched (Random)** | 970 | 🟢 Low (Secured) |

### Observations
The data indicates a **negligible performance delta** (approximately 0.8% – 1% increase in page faults). In randomized access patterns, a random eviction policy performs nearly as efficiently as the complex distance-based approach while providing significantly higher security by eliminating predictability.

---

## How to Run the Benchmark
1. Clone the repository.
2. Ensure you have Python installed.
3. Run the following command:
   ```bash
   python memory_benchmark.py
   ```
