import math

with open('inputs/input7.txt', 'r') as f:
    crabs = list(map(int, f.readline().split(",")))

# part 1: minimal movement to horizontally align
# median crab
crabs.sort()
median_crab = crabs[round(len(crabs)/2)]

def fuel_cost_linear(pos: int) -> int:
    return sum([abs(crab-pos) for crab in crabs])

print(f"Day 7, part 1: {fuel_cost_linear(median_crab)}")

# memoize triangle numbers
triangle_numbers = []
for i in range(max(crabs) - min(crabs) + 1):
    triangle_numbers.append(int((i * (i+1))/2))

def fuel_cost_triangular(pos: int) -> int:
    return sum([triangle_numbers[abs(crab-pos)] for crab in crabs])


# brute force solution
min_fuel = math.inf
best_pos = 0
for i in range(min(crabs), max(crabs) + 1):
    fuel_cost = fuel_cost_triangular(i)
    if fuel_cost < min_fuel:
        min_fuel = fuel_cost
        best_pos = i
    else:
        break # should be monotonic; once we start seeing increased cost we're done

print(f"Best crab position: {best_pos}")
print(f"Fuel cost at best position: {min_fuel}")
