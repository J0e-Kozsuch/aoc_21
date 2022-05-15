from collections import defaultdict


def calculate_volume(cuboid_ranges):
    product = 1
    for axis_range in cuboid_ranges:
        product *= axis_range[1] - axis_range[0] + 1

    return product


class Reactor_Grid:
    def __init__(self):
        self.cuboids = defaultdict(int)

    def _point_combinations(self, cuboid1: tuple, cuboid2: tuple) -> tuple:
        """
        given cuboids, find all possible points where their extended planes could interesect
        """
        points = []

        for x in set(cuboid1[0] + cuboid2[0]):
            for y in set(cuboid1[1] + cuboid2[1]):
                for z in set(cuboid1[2] + cuboid2[2]):

                    points.append((x, y, z))

        return tuple(points)

    def _is_cuboid_in_cuboid(self, cuboid1: tuple, cuboid2: tuple) -> str:
        """
        given two cuboids, determine if the first is within second
        """

        one_in_two = (
            sum(
                [
                    point_range1[0] >= point_range2[0]
                    and point_range1[1] <= point_range2[1]
                    for point_range1, point_range2 in zip(cuboid1, cuboid2)
                ]
            )
            == 3
        )

        two_in_one = (
            sum(
                [
                    point_range1[0] <= point_range2[0]
                    and point_range1[1] >= point_range2[1]
                    for point_range1, point_range2 in zip(cuboid1, cuboid2)
                ]
            )
            == 3
        )

        if one_in_two and two_in_one:
            return "identical"
        elif one_in_two:
            return "one_in_two"
        elif two_in_one:
            return "two_in_one"
        else:
            return "neither"

    def find_intersect(self, cuboid1: tuple, cuboid2: tuple) -> tuple:
        """
        receive two cuboids and find all possible cuboids
        return null if no cuboid in both of others
        return cuboid object with value = 1 if it is in both
        """

        points = self._point_combinations(cuboid1, cuboid2)

        for first_index, first_point in enumerate(points[:-1]):
            for second_point in points[first_index + 1 :]:

                matching_point_elements = [
                    i for i, j in zip(first_point, second_point) if i == j
                ]

                if matching_point_elements == []:

                    sub_cuboid = (
                        tuple(sorted((first_point[0], second_point[0]))),
                        tuple(sorted((first_point[1], second_point[1]))),
                        tuple(sorted((first_point[2], second_point[2]))),
                    )

                    in_first = self._is_cuboid_in_cuboid(sub_cuboid, cuboid1)
                    in_second = self._is_cuboid_in_cuboid(sub_cuboid, cuboid2)

                    if in_first in ["identical", "one_in_two"] and in_second in [
                        "identical",
                        "one_in_two",
                    ]:
                        return sub_cuboid

        return None

    def process_line(self, line: str):

        value, ranges = self.interpret_line(line)

        new_cuboids = defaultdict(int)

        for prev_cube, prev_cube_value in self.cuboids.items():

            intersect = self.find_intersect(ranges, prev_cube)

            if intersect is None:
                continue
            elif intersect is not None:
                new_cuboids[intersect] -= prev_cube_value

        if value == 1:
            new_cuboids[ranges] += 1

        for cuboid in new_cuboids:
            self.cuboids[cuboid] += new_cuboids[cuboid]

    def interpret_line(self, line: str) -> tuple:
        """
        given line of input, interpret and convert cube values
        """
        instruction = line.split(" ")[0]

        if instruction == "on":
            value = 1
        elif instruction == "off":
            value = 0

        ranges = [
            tuple([int(i) for i in min_max.split("=")[1].split("..")])
            for min_max in line.split(",")
        ]

        return (value, tuple(ranges))


# Read in text file
file = open(r".\Puzzle_Input\aoc22_cube_steps.txt")
by = file.read()
file.close()

text_lines = by.split("\n")

reactor_grid = Reactor_Grid()

count = 0
for line in text_lines:
    print(count)
    count += 1
    reactor_grid.process_line(line)

total_volume = 0
for cuboid_ranges, value in reactor_grid.cuboids.items():
    total_volume += calculate_volume(cuboid_ranges) * value

print(total_volume)
