def puzzle3():
    with open('inputs/input3.txt', 'r') as f:
        readings = list(map(lambda x: list(x)[:-1], f.readlines())) # strip newline
    bit_values = list(map(list, zip(*readings)))
    most_common_bits = []
    least_common_bits = []
    for bit_pos in bit_values:
        most_common_bits.append("1" if (bit_pos.count("1") > len(bit_pos)/2) else "0")
        least_common_bits.append("1" if most_common_bits[-1] == "0" else "0")

    gamma = int(''.join(most_common_bits), 2)
    epsilon = int(''.join(least_common_bits), 2)
    # return gamma * epsilon // part 1

    def most_common_bit(readings: list, pos: int, default: str) -> str:
        bit_values = list(map(list, zip(*readings)))
        one_count = bit_values[pos].count("1")
        if one_count > len(readings)/2:
            return "1"
        if one_count == len(readings)/2:
            return default
        return "0"


    def oxygen_rating(readings: list, pos: int) -> str:
        return most_common_bit(readings, pos, "1")

    def co2_rating(readings: list, pos: int) -> str:
        return "1" if oxygen_rating(readings, pos) == "0" else "0"

    oxygen_readings = list(readings)
    pos = 0
    while len(oxygen_readings) > 1 and pos < len(oxygen_readings[0]):
        rating = oxygen_rating(oxygen_readings, pos)
        oxygen_readings = [x for x in oxygen_readings if x[pos] == rating]
        pos += 1
    oxygen = oxygen_readings[0]
    oxygen = int(''.join(oxygen), 2)

    co2_readings = list(readings)
    pos = 0
    while len(co2_readings) > 1 and pos < len(co2_readings[0]):
        rating = co2_rating(co2_readings, pos)
        co2_readings = [x for x in co2_readings if x[pos] == rating]
        pos += 1
    co2 = co2_readings[0]
    co2 = int(''.join(co2), 2)

    return oxygen * co2


print(f"Day 3: {puzzle3()}")
