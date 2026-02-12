"""
Hive AI Core - Hexagonal Geometry Layer

Implements hexagonal grid mathematics for agent cell distribution.
Uses axial coordinates (q, r) with cube coordinate constraints (q + r + s = 0).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum, auto
from datetime import datetime
import math


class HexDirection(Enum):
    """Six hexagonal directions using axial coordinates."""

    NORTH = 0  # (0, -1)
    NORTHEAST = 1  # (+1, -1)
    SOUTHEAST = 2  # (+1, 0)
    SOUTH = 3  # (0, +1)
    SOUTHWEST = 4  # (-1, +1)
    NORTHWEST = 5  # (-1, 0)


@dataclass(frozen=True)
class HexCoords:
    """Axial coordinates for hexagonal grid.

    q + r + s = 0 where s = -q - r (cube coordinate conversion)
    """

    q: int  # Column (pointy-top orientation)
    r: int  # Row

    @property
    def s(self) -> int:
        """Cube coordinate s (computed, not stored)."""
        return -self.q - self.r

    def __add__(self, other: "HexCoords") -> "HexCoords":
        return HexCoords(q=self.q + other.q, r=self.r + other.r)

    def __sub__(self, other: "HexCoords") -> "HexCoords":
        return HexCoords(q=self.q - other.q, r=self.r - other.r)

    def __hash__(self):
        return hash((self.q, self.r))

    def __eq__(self, other):
        if not isinstance(other, HexCoords):
            return False
        return self.q == other.q and self.r == other.r

    def distance_to(self, other: "HexCoords") -> int:
        """Manhattan distance in hex grid (cube distance)."""
        return (
            abs(self.q - other.q)
            + abs(self.q + self.r - other.q - other.r)
            + abs(self.r - other.r)
        ) // 2

    def neighbor(self, direction: HexDirection) -> "HexCoords":
        """Get neighbor in given direction."""
        deltas = {
            HexDirection.NORTH: (0, -1),
            HexDirection.NORTHEAST: (1, -1),
            HexDirection.SOUTHEAST: (1, 0),
            HexDirection.SOUTH: (0, 1),
            HexDirection.SOUTHWEST: (-1, 1),
            HexDirection.NORTHWEST: (-1, 0),
        }
        dq, dr = deltas[direction]
        return HexCoords(q=self.q + dq, r=self.r + dr)

    def all_neighbors(self) -> List["HexCoords"]:
        """Get all 6 neighbors."""
        return [self.neighbor(d) for d in HexDirection]

    def within_radius(self, radius: int) -> Set["HexCoords"]:
        """Get all hexes within radius (inclusive)."""
        results = set()
        for q in range(-radius, radius + 1):
            for r in range(max(-radius, -q - radius), min(radius, -q + radius) + 1):
                results.add(HexCoords(q=self.q + q, r=self.r + r))
        return results

    def ring(self, radius: int) -> Set["HexCoords"]:
        """Get hexes exactly at radius distance."""
        results = set()
        current = self.neighbor(HexDirection.SOUTHWEST)
        for _ in range(6):
            for _ in range(radius):
                results.add(current)
                current = current.neighbor(HexDirection.NORTH)
            current = current.neighbor(HexDirection.NORTHEAST)
        return results

    def to_tuple(self) -> Tuple[int, int]:
        return (self.q, self.r)

    def __repr__(self):
        return f"HexCoords({self.q}, {self.r})"


class ResourceState(Enum):
    """Compute/resource states using glass transition analogy."""

    COLD = auto()  # Stored, no model attached
    WARM = auto()  # Model attached, idle
    HOT = auto()  # Active streaming


@dataclass
class Cell:
    """A single hexagonal cell in the hive comb.

    Represents an agent context: research thread, code agent, log, or dataset.
    """

    coords: HexCoords
    cell_id: str
    name: str

    # Agent/role info
    agent_role: Optional["AgentRole"] = None
    agent_id: Optional[str] = None

    # Resource state
    resource_state: ResourceState = ResourceState.COLD

    # Content
    content: Dict = field(default_factory=dict)
    messages: List[Dict] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)

    # Junction info (standardized interfaces)
    junction_with: Set[HexCoords] = field(default_factory=set)
    shared_artifacts: Dict[str, str] = field(default_factory=dict)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    status: str = "initialized"

    def to_dict(self) -> Dict:
        return {
            "cell_id": self.cell_id,
            "coords": self.coords.to_tuple(),
            "name": self.name,
            "role": self.agent_role.value if self.agent_role else None,
            "state": self.resource_state.name,
            "status": self.status,
            "messages": len(self.messages),
            "artifacts": len(self.artifacts),
        }


class HexGrid:
    """Manages a hexagonal grid of cells.

    Implements honeycomb theorem: minimizes perimeter for equal-area partitions.
    """

    def __init__(self, radius: int = 5):
        self.radius = radius  # Grid radius from center
        self.cells: Dict[HexCoords, Cell] = {}
        self.cell_index: Dict[str, HexCoords] = {}  # cell_id -> coords

        # Initialize grid
        self._initialize_grid()

    def _initialize_grid(self):
        """Create hex grid within radius."""
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, -q - self.radius)
            r2 = min(self.radius, -q + self.radius)
            for r in range(r1, r2 + 1):
                coords = HexCoords(q=q, r=r)
                cell_id = f"cell_{q}_{r}"
                cell = Cell(coords=coords, cell_id=cell_id, name=f"Hex[{q},{r}]")
                self.cells[coords] = cell
                self.cell_index[cell_id] = coords

    def get_cell(self, coords: HexCoords) -> Optional[Cell]:
        """Get cell at coordinates."""
        return self.cells.get(coords)

    def get_cell_by_id(self, cell_id: str) -> Optional[Cell]:
        """Get cell by ID."""
        coords = self.cell_index.get(cell_id)
        return self.get_cell(coords) if coords else None

    def add_neighbor_connection(self, coords1: HexCoords, coords2: HexCoords):
        """Add junction connection between two cells."""
        if coords1 in self.cells and coords2 in self.cells:
            self.cells[coords1].junction_with.add(coords2)
            self.cells[coords2].junction_with.add(coords1)

    def get_neighbors(self, coords: HexCoords) -> List[Cell]:
        """Get all neighboring cells."""
        return [self.cells[n] for n in coords.all_neighbors() if n in self.cells]

    def navigate(
        self, from_coords: HexCoords, direction: HexDirection
    ) -> Optional[Cell]:
        """Navigate to neighbor in direction."""
        target = from_coords.neighbor(direction)
        return self.get_cell(target)

    def find_path(self, start: HexCoords, end: HexCoords) -> List[HexCoords]:
        """A* pathfinding through hex grid."""
        if start == end:
            return [start]

        open_set = {start}
        came_from: Dict[HexCoords, HexCoords] = {}
        g_score: Dict[HexCoords, float] = {start: 0}
        f_score: Dict[HexCoords, float] = {start: start.distance_to(end)}

        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float("inf")))

            if current == end:
                return self._reconstruct_path(came_from, current)

            open_set.discard(current)

            for neighbor in current.all_neighbors():
                if neighbor not in self.cells:
                    continue

                tentative_g = g_score[current] + 1

                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + neighbor.distance_to(end)
                    open_set.add(neighbor)

        return []  # No path found

    def _reconstruct_path(self, came_from: Dict, current: HexCoords) -> List[HexCoords]:
        """Reconstruct path from A* search."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))

    def get_grid_stats(self) -> Dict:
        """Get grid statistics."""
        role_counts = {}
        state_counts = {}
        total_messages = 0
        total_artifacts = 0

        for cell in self.cells.values():
            if cell.agent_role:
                role_counts[cell.agent_role.value] = (
                    role_counts.get(cell.agent_role.value, 0) + 1
                )
            state_counts[cell.resource_state.name] = (
                state_counts.get(cell.resource_state.name, 0) + 1
            )
            total_messages += len(cell.messages)
            total_artifacts += len(cell.artifacts)

        return {
            "total_cells": len(self.cells),
            "cells_with_agents": sum(1 for c in self.cells.values() if c.agent_id),
            "role_distribution": role_counts,
            "state_distribution": state_counts,
            "total_messages": total_messages,
            "total_artifacts": total_artifacts,
        }


if __name__ == "__main__":
    # Test hex grid
    grid = HexGrid(radius=3)

    center = HexCoords(q=0, r=0)
    print(f"HexGrid initialized with {len(grid.cells)} cells")

    # Test navigation
    neighbor = grid.navigate(center, HexDirection.NORTH)
    print(f"North neighbor of {center}: {neighbor.coords if neighbor else 'None'}")

    # Test pathfinding
    target = HexCoords(q=2, r=-1)
    path = grid.find_path(center, target)
    print(f"Path from {center} to {target}: {[c.to_tuple() for c in path]}")

    # Stats
    stats = grid.get_grid_stats()
    print(f"Grid stats: {stats}")
