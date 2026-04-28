import random

class MemorySimulation:
    def __init__(self, num_frames, num_pages, secure_mode=False):
        self.num_frames = num_frames
        self.num_pages = num_pages
        self.ram = [-1] * num_frames
        self.page_faults = 0
        self.secure_mode = secure_mode

    def get_cyclical_distance(self, p_in, p_resident):
        if p_resident is -1:
            return -1
        diff = abs(p_in - p_resident)
        return min(diff, self.num_pages - diff)

    def find_victim_idx(self, p_in):
        if self.secure_mode:
            return random.randint(0, self.num_frames - 1)
        
        max_dist = -1
        victim_idx = -1

        for i in range(self.num_frames):
            dist = self.get_cyclical_distance(p_in, self.ram[i])
            if dist > max_dist:
                max_dist = dist
                victim_idx = i
        return victim_idx

    def access(self, page_id):
        if page_id in self.ram:
            return "HIT"

        self.page_faults += 1
        if -1 in self.ram:
            v_idx = self.ram.index(-1)
        else:
            v_idx = self.find_victim_idx(page_id)
            
        self.ram[v_idx] = page_id
        return "MISS"


if __name__ == "__main__":
    sim = MemorySimulation(num_frames=4, num_pages=100)

    pages_to_load = [10, 20, 30, 40]
    for p in pages_to_load:
        sim.access(p)

    print(f"Current RAM: {sim.ram}")

    sim.access(85)
    print(f"Final RAM State: {sim.ram}")
