import random
from part1.simulation import MemorySimulation

def generate_attack_sequence(target_page):
    target_idx = sim.ram.index(target_page)
    for p_in in range(sim.num_pages):
        if sim.find_victim_idx(p_in) == target_idx:
            return p_in
    return -1

print("\n--- Part 1.2: Vulnerability Demonstration ---\n")
sim = MemorySimulation(4, 100, secure_mode=False)

for p in [10, 20, 50, 30]: 
    sim.access(p)
print(f"Initial RAM: {sim.ram}")

attacker_page = generate_attack_sequence(30)
print(f"Attacker requests Page: {attacker_page}")

result = sim.access(attacker_page)
print(f"System Response: {result}")
print(f"Final RAM State: {sim.ram}")

if 30 not in sim.ram:
    print("Result: Success! Page 30 was evicted.")


print("\n--- Part 1.3: Performance Benchmark (1,000 accesses) ---\n")

orig_sim = MemorySimulation(4, 100, secure_mode=False)
sec_sim = MemorySimulation(4, 100, secure_mode=True)

random_accesses = [random.randint(0, 99) for _ in range(1000)]

for p in random_accesses:
    if p not in orig_sim.ram:
        orig_sim.page_faults += 1
        if -1 in orig_sim.ram:
            target_idx = orig_sim.ram.index(-1)
        else:
            target_idx = orig_sim.find_victim_idx(p)
        
        orig_sim.ram[target_idx] = p
        
    if p not in sec_sim.ram:
        sec_sim.page_faults += 1
        if -1 in sec_sim.ram:
            target_idx = sec_sim.ram.index(-1)
        else:
            target_idx = sec_sim.find_victim_idx(p)
            
        sec_sim.ram[target_idx] = p

print(f"Original Algorithm Faults: {orig_sim.page_faults}")
print(f"Secured Algorithm Faults: {sec_sim.page_faults}")