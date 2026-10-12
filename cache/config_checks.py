import config


def is_power_of_two(value):
    return isinstance(value, int) and value > 0 and (value & (value - 1)) == 0


def inspect_submission_cache(cache):
    failures = []

    if cache is None:
        return False, ["submission_cache is missing"], {}

    directory = getattr(cache, "directory", None)
    if not directory:
        return False, ["directory is empty or missing"], {}

    block_size = getattr(cache, "block_size", None)
    if not is_power_of_two(block_size):
        failures.append(f"block_size={block_size} must be a positive power of two")

    row_lengths = [len(row) for row in directory]
    if len(set(row_lengths)) != 1:
        failures.append("directory rows have inconsistent associativity")
        return False, failures, {}

    associativity = row_lengths[0]
    sets = len(directory)

    if associativity < 1:
        failures.append(f"associativity={associativity} must be a positive integer")

    if getattr(cache, "associativity", None) != associativity:
        failures.append(
            f"cache.associativity={getattr(cache, 'associativity', None)} does not match "
            f"directory associativity ({associativity})"
        )

    declared_sets = getattr(cache, "sets", None)
    if declared_sets is not None and declared_sets != sets:
        failures.append(f"cache.sets={declared_sets} does not match directory sets ({sets})")

    if not is_power_of_two(sets):
        failures.append(f"number of sets ({sets}) must be a power of two")

    footprint = sets * associativity * block_size if is_power_of_two(block_size) else 0
    if footprint != config.CACHE_CAPACITY:
        failures.append(
            f"footprint={footprint} bytes must equal CACHE_CAPACITY ({config.CACHE_CAPACITY})"
        )

    if failures:
        return False, failures, {}

    metrics = {
        "block_size": block_size,
        "associativity": associativity,
        "sets": sets,
        "footprint": footprint,
        "hit_cost": config.HIT_LATENCY + (associativity - 1),
        "miss_cost": config.MISS_PENALTY,
    }
    return True, [], metrics
