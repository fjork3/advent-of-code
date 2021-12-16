from __future__ import annotations

from typing import List
import math


class Packet:
    def __init__(self):
        self.packets: List[Packet]
        self.version: int

    def get_packet_size(self) -> int:
        raise NotImplementedError()

    def get_version_sum(self) -> int:
        raise NotImplementedError()

    def get_value(self) -> int:
        raise NotImplementedError()


class LiteralPacket(Packet):
    def __init__(self, packet: str):
        Packet.__init__(self)
        self.version = int(packet[0:3], 2)
        self.operator = int(packet[3:6], 2)  # should always be 4
        assert self.operator == 4
        chunk_start = 6
        chunks = 1
        value_str = packet[chunk_start:chunk_start+5]
        while packet[chunk_start] == "1":
            chunk_start += 5
            chunks += 1
            value_str += packet[chunk_start:chunk_start+5]
        self.value = int(value_str, 2)
        self.packet_size = 6 + (5*chunks)

    def get_packet_size(self) -> int:
        return self.packet_size

    def get_version_sum(self) -> int:
        return self.version

    def get_value(self):
        return self.value


class OperatorPacket(Packet):
    def __init__(self, packet: str):
        Packet.__init__(self)
        self.version = int(packet[0:3], 2)
        self.operator = int(packet[3:6], 2)
        self.packets: List[Packet] = []
        self.length_type_bit = packet[6] == "1"

        if self.length_type_bit:
            # 1: 11 bits with number of sub-packets
            num_packets = int(packet[7:18], 2)
            parsed_packets = 0
            subpackets = packet[18:]
            for _ in range(num_packets):
                p = parse_next_packet(subpackets)
                self.packets.append(p)
                parsed_packets += 1
                subpackets = subpackets[p.get_packet_size():]
        else:
            # 0: 15 bits with total length of sub-packets
            total_packet_length = int(packet[7:22], 2)
            parsed_packets_length = 0
            subpackets = packet[22:]
            while parsed_packets_length < total_packet_length:
                p = parse_next_packet(subpackets)
                self.packets.append(p)
                parsed_packets_length += p.get_packet_size()
                subpackets = subpackets[p.get_packet_size():]

    def get_packet_size(self) -> int:
        return 7 + (11 if self.length_type_bit else 15) + sum(p.get_packet_size() for p in self.packets)

    def get_version_sum(self) -> int:
        return self.version + sum(p.get_version_sum() for p in self.packets)

    def get_value(self) -> int:
        if self.operator == 0:
            print(f"sum operator: {[p.get_value() for p in self.packets]}")
            return sum(p.get_value() for p in self.packets)
        if self.operator == 1:
            print(f"prod operator: {[p.get_value() for p in self.packets]}")
            return math.prod(p.get_value() for p in self.packets)
        if self.operator == 2:
            print(f"min operator: {[p.get_value() for p in self.packets]}")
            return min(p.get_value() for p in self.packets)
        if self.operator == 3:
            print(f"max operator: {[p.get_value() for p in self.packets]}")
            return max(p.get_value() for p in self.packets)
        if self.operator == 5:
            return 1 if self.packets[0].get_value() > self.packets[1].get_value() else 0
        if self.operator == 6:
            return 1 if self.packets[0].get_value() < self.packets[1].get_value() else 0
        if self.operator == 7:
            return 1 if self.packets[0].get_value() == self.packets[1].get_value() else 0


def parse_next_packet(packet: str) -> Packet:
    if packet[3:6] == "100":
        return LiteralPacket(packet)
    else:
        return OperatorPacket(packet)


def read_input() -> Packet:
    with open("inputs/input16.txt", "r") as f:
        hex_input = f.readline().rstrip()
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    return parse_next_packet(binary_input)


def part_one_tests():
    hex_input = "8A004A801A8002F478"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_version_sum() == 16

    hex_input = "620080001611562C8802118E34"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_version_sum() == 12

    hex_input = "C0015000016115A2E0802F182340"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_version_sum() == 23

    hex_input = "A0016C880162017C3686B18A3D4780"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_version_sum() == 31

    print("part one tests passed!")


part_one_tests()


def part_one() -> int:
    packet = read_input()
    return packet.get_version_sum()


def part_two_tests():
    hex_input = "C200B40A82"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_value() == 3

    hex_input = "04005AC33890"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_value() == 54

    hex_input = "880086C3E88112"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_value() == 7

    hex_input = "CE00C43D881120"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_value() == 9

    hex_input = "D8005AC2A8F0"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_value() == 1

    hex_input = "F600BC2D8F"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_value() == 0

    hex_input = "9C005AC2F8F0"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_value() == 0

    hex_input = "9C0141080250320F1802104A08"
    binary_input = "".join(format(int(h, 16), "04b") for h in hex_input)
    p = parse_next_packet(binary_input)
    assert p.get_value() == 1

    print("part two tests passed!")


part_two_tests()


def part_two():
    packet = read_input()
    return packet.get_value()


print(f"Day 16, part 1: {part_one()}")
# print(f"Day 16, part 2: {part_two()}")
