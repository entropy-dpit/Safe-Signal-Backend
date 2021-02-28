# Copyright (c) prisma.ai 2021
# All rights reserved

__author__ = 'Ioana Gabor'
# Refactor: David Pescariu

from typing import List, Tuple

class ZoneBuilder:
    """
    Generates the zones

    Params:
        marker_data (list): The list of markers, ex: [46.7874&23.6018&robbery&2020-08-17&10:32:55, end]
        threshold (float, optional): Threshold for the zone creation. Defaults to 0.004.
    """
    def __init__(self, marker_data: list, threshold: float = 0.004) -> None:
        self.threshold = threshold
        self.markers = self.__parse_input(marker_data)
        self.sets = {}
        self.__disjoint_sets(self.markers, self.sets)
        self.zones = self.__get_zones(self.sets)

    def get_zones(self) -> List[List[Tuple[float, float]]]:
        """
        Get zones

        Returns:
            List[List[Tuple[float, float]]]: List containing zones(lists), with their coords(tuples)
        """
        return self.zones

    def __parse_input(self, marker_data: list) -> List[Tuple[float, float]]:
        """
        Parse the marker data and return a list of tuples with coords

        Args:
            marker_data (list): Raw data

        Returns:
            List[Tuple[float, float]]: Parsed data, like [(46.7945, 23.5986), (46.7933, 23.6017)]
        """
        _markers = []
        
        for marker in marker_data:
            if marker == "end":
                return _markers
            else:
                parsed = marker.split('&', 2)
                _markers.append((float(parsed[0]), float(parsed[1])))

    def __disjoint_sets(self, markers: list, sets: dict) -> None:
        """
        Ask Ioana :)

        Args:
            markers (list): Parsed list of markers
            sets (dict): Ask Ioana :)
        """
        n = len(markers)
        _labels = []
        for i in range(0, n):
            _labels.append(i)

        for i in range(0, n):
            for j in range(0, i):
                if self.__proximal_zones(markers[i], markers[j], self.threshold):
                    self.__normalize_label(i, _labels)
                    self.__normalize_label(j, _labels)
                    if(_labels[i] < _labels[j]):
                        _labels[j] = _labels[i]
                    elif(_labels[i] > _labels[j]):
                        _labels[i] = _labels[j]
        
        for i in range(0, n):
            self.__normalize_label(i, _labels)
            if bool(sets.get(_labels[i])) == False:
                sets[_labels[i]] = []
            sets[_labels[i]].append(markers[i])
        
    def __proximal_zones(self, zone1: Tuple, zone2: Tuple, threshold: float) -> bool:
        """
            Checks, using the Euclidean Distance Formula if two zones are within 
        the set threshold

        Args:
            zone1 (Tuple): First zone
            zone2 (Tuple): Second zone
            threshold (float): The threshold

        Returns:
            bool: True / False
        """
        return (
            (zone1[0] - zone2[0]) **2 + 
            (zone1[1] - zone2[1]) **2 <= threshold ** 2
        )

    def __normalize_label(self, index: int, labels: list) -> float:
        """
        Doing some kind of normalizing, ask Ioana

        Args:
            index (int): ?
            labels (list): Labels list from disjoint_sets

        Returns:
            float: ?
        """
        if(labels[index] != index):
            labels[index] = self.__normalize_label(labels[index], labels)    
        return labels[index]

    def __counterclockwise_order(self, point1: Tuple, point2: Tuple, point3: Tuple) -> bool:
        """
        Checks if 3 given points are in a counter clockwise order

        Args:
            point1 (Tuple): Point 1
            point2 (Tuple): Point 2
            point3 (Tuple): Point 3

        Returns:
            bool: True / False
        """
        return (
            point1[0] * point2[1] + 
            point2[0] * point3[1] + 
            point3[0] * point1[1] - 
            point1[0] * point3[1] - 
            point3[0] * point2[1] -
            point2[0] * point1[1] > 0
        )

    def __convex_hull(self, zone) -> list:
        """
        Honestly I really dont know... ask Ioana

        Args:
            zone ([type]): ?

        Returns:
            list: ?
        """
        zone.sort()
        n = len(zone)
        stack = []
        size_of_stack = 0
        for i in range(0,n):
            if size_of_stack > 1 and self.__counterclockwise_order(stack[size_of_stack-2], stack[size_of_stack-1], zone[i]):
                size_of_stack = size_of_stack - 1
                stack.pop(size_of_stack)
            stack.append(zone[i])
            size_of_stack = size_of_stack + 1

        for i in range(n-2,-1,-1):
            if size_of_stack > 1 and self.__counterclockwise_order(stack[size_of_stack-2], stack[size_of_stack-1], zone[i]):
                size_of_stack = size_of_stack - 1
                stack.pop(size_of_stack)
            stack.append(zone[i])
            size_of_stack = size_of_stack + 1
            
        stack.pop(size_of_stack-1)
        return stack

    def __get_border(self, zone) -> list:
        """
        Get some zone border

        Args:
            zone ([type]): ?

        Returns:
            list: ?
        """
        if len(zone) < 4:
            return zone
        else:
            return self.__convex_hull(zone)

    def __get_zones(self, sets: dict) -> List[List[Tuple[float, float]]]:
        """
        Build final zones

        Args:
            sets (dict): Sets of coords (I think)

        Returns:
            List[List[Tuple[float, float]]]: Explained in get_zones
        """
        _zones = []
        for x in sets:
            zone = sets[x]
            zone = self.__get_border(zone)
            _zones.append(zone)
        return _zones

# EOF
