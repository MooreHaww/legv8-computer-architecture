class CacheBlock:
    def __init__(self):
        self.valid = False  # True if this cache line holds valid data
        self.tag = 0  # Tag bits of the address stored in this line
        self.lru_counter = 0  # Higher = more recently used


class Cache:
    def __init__(self, capacity, block_size, associativity):
        self.capacity = capacity  # Total cache size in bytes (4096 for submission)
        self.block_size = block_size  # Bytes per cache block (must be power of 2)
        self.associativity = associativity  # Ways per set (blocks per set)

        self.sets = capacity // (block_size * associativity)
        self.offset_bits = self.block_size.bit_length() - 1
        self.index_bits = self.sets.bit_length() - 1

        self.directory = [
            [CacheBlock() for _ in range(associativity)]
            for _ in range(self.sets)
        ]

        self._clock = 0  # global access counter, used to track LRU recency

    def access(self, address: int) -> bool:
        self._clock += 1

        offset_mask = self.block_size - 1
        index_mask = self.sets - 1

        # offset = address & offset_mask              (unused beyond split, block-level cache)
        index = (address >> self.offset_bits) & index_mask
        tag = address >> (self.offset_bits + self.index_bits)

        row = self.directory[index]

        # --- Check for a hit ---
        for block in row:
            if block.valid and block.tag == tag:
                block.lru_counter = self._clock
                return True

        # --- Miss: install the new block ---
        victim = None
        for block in row:
            if not block.valid:
                victim = block
                break

        if victim is None:
            # No free way in this set -> evict the least-recently-used block
            victim = min(row, key=lambda b: b.lru_counter)

        victim.valid = True
        victim.tag = tag
        victim.lru_counter = self._clock

        return False


# 4096-byte submission cache.
# Design: block_size=1024 bytes, 2-way set associative (sets=2).
# Chosen by exhaustively testing every valid (block_size, associativity)
# combination under the 4096-byte budget against traces/benchmark.txt.
# This config gives the lowest total_cycles (3392) of any valid design --
# wide 1024-byte blocks absorb the sequential/strided regions (data init,
# matrix row/column, stack frame) via spatial locality, while 2-way
# associativity prevents the ping-pong region (0x40000000 / 0x40010000)
# from thrashing a single set.
block_size = 1024
associativity = 2
submission_cache = Cache(4096, block_size, associativity)
