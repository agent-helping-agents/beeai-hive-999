#!/usr/bin/env python3
"""
ELOHIM-FORGE: PVP Game Module
Multiplayer combat system with Elohim Shard powers
Based on original PVP game component
"""

import asyncio
import websockets
import json
import uuid
import time
import math
import random
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameMode(Enum):
    SHARD_HUNT = "shard_hunt"
    TEAM_DEATHMATCH = "team_deathmatch"
    KING_OF_HILL = "king_of_hill"
    CAPTURE_FLAG = "capture_flag"
    DREAM_DUEL = "dream_duel"

class PlayerClass(Enum):
    DREAM_WALKER = "dream_walker"
    SHARD_GUARDIAN = "shard_guardian"
    NIGHTMARE_HUNTER = "nightmare_hunter"
    VOID_MAGE = "void_mage"
    REALITY_ANCHOR = "reality_anchor"

class AbilityType(Enum):
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"
    UTILITY = "utility"
    ULTIMATE = "ultimate"

@dataclass
class Vector2D:
    x: float
    y: float
    
    def distance_to(self, other: 'Vector2D') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def normalize(self) -> 'Vector2D':
        magnitude = math.sqrt(self.x**2 + self.y**2)
        if magnitude > 0:
            return Vector2D(self.x / magnitude, self.y / magnitude)
        return Vector2D(0, 0)

@dataclass
class Ability:
    id: str
    name: str
    ability_type: AbilityType
    damage: int
    range: float
    cooldown: float
    energy_cost: int
    description: str
    shard_requirement: Optional[str] = None

@dataclass
class Player:
    id: str
    username: str
    player_class: PlayerClass
    position: Vector2D
    health: int
    max_health: int
    energy: int
    max_energy: int
    level: int
    experience: int
    kills: int
    deaths: int
    shards_collected: List[str]
    abilities: List[Ability]
    active_effects: List[str]
    last_action_time: float
    team: Optional[str] = None
    
    def is_alive(self) -> bool:
        return self.health > 0
    
    def take_damage(self, damage: int) -> bool:
        """Take damage and return True if player died"""
        self.health = max(0, self.health - damage)
        return self.health == 0
    
    def heal(self, amount: int):
        """Heal player"""
        self.health = min(self.max_health, self.health + amount)
    
    def use_energy(self, amount: int) -> bool:
        """Use energy, return True if successful"""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
    
    def add_experience(self, amount: int):
        """Add experience and handle level ups"""
        self.experience += amount
        new_level = 1 + (self.experience // 1000)
        if new_level > self.level:
            self.level = new_level
            self.max_health += 25
            self.max_energy += 15
            self.health = self.max_health
            self.energy = self.max_energy

class GameRoom:
    """PVP Game Room"""
    def __init__(self, room_id: str, game_mode: GameMode, max_players: int = 8):
        self.room_id = room_id
        self.game_mode = game_mode
        self.max_players = max_players
        self.players: Dict[str, Player] = {}
        self.websockets: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.game_state = "waiting"  # waiting, active, finished
        self.start_time = None
        self.match_duration = 600  # 10 minutes
        self.map_size = Vector2D(2000, 2000)
        self.shards_on_map: Dict[str, Vector2D] = {}
        self.spawn_points = self.generate_spawn_points()
        self.game_loop_task = None
        
        # Initialize game mode specific data
        self.initialize_game_mode()
    
    def initialize_game_mode(self):
        """Initialize game mode specific settings"""
        if self.game_mode == GameMode.SHARD_HUNT:
            self.spawn_shards()
        elif self.game_mode == GameMode.TEAM_DEATHMATCH:
            self.team_scores = {"red": 0, "blue": 0}
        elif self.game_mode == GameMode.KING_OF_HILL:
            self.hill_center = Vector2D(1000, 1000)
            self.hill_radius = 200
            self.hill_control_time = {"red": 0, "blue": 0}
    
    def generate_spawn_points(self) -> List[Vector2D]:
        """Generate spawn points around the map"""
        spawn_points = []
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            x = 1000 + 800 * math.cos(angle)
            y = 1000 + 800 * math.sin(angle)
            spawn_points.append(Vector2D(x, y))
        return spawn_points
    
    def spawn_shards(self):
        """Spawn Elohim Shards on the map for Shard Hunt mode"""
        shard_types = ["creation", "destruction", "time", "space", "mind"]
        for i, shard_type in enumerate(shard_types):
            x = random.uniform(200, 1800)
            y = random.uniform(200, 1800)
            self.shards_on_map[f"{shard_type}_shard"] = Vector2D(x, y)
    
    async def add_player(self, websocket: websockets.WebSocketServerProtocol, player_data: Dict):
        """Add a player to the room"""
        if len(self.players) >= self.max_players:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Room is full"
            }))
            return False
        
        player_id = str(uuid.uuid4())
        spawn_point = self.spawn_points[len(self.players) % len(self.spawn_points)]
        
        # Create player with class-specific stats
        player_class = PlayerClass(player_data.get("class", "dream_walker"))
        base_stats = self.get_class_stats(player_class)
        
        player = Player(
            id=player_id,
            username=player_data["username"],
            player_class=player_class,
            position=spawn_point,
            health=base_stats["health"],
            max_health=base_stats["health"],
            energy=base_stats["energy"],
            max_energy=base_stats["energy"],
            level=1,
            experience=0,
            kills=0,
            deaths=0,
            shards_collected=[],
            abilities=self.get_class_abilities(player_class),
            active_effects=[],
            last_action_time=time.time()
        )
        
        # Assign team for team-based modes
        if self.game_mode in [GameMode.TEAM_DEATHMATCH, GameMode.KING_OF_HILL]:
            player.team = "red" if len(self.players) % 2 == 0 else "blue"
        
        self.players[player_id] = player
        self.websockets[player_id] = websocket
        
        # Send welcome message
        await websocket.send(json.dumps({
            "type": "player_joined",
            "player_id": player_id,
            "player": asdict(player),
            "room_info": {
                "room_id": self.room_id,
                "game_mode": self.game_mode.value,
                "players_count": len(self.players),
                "max_players": self.max_players
            }
        }))
        
        # Broadcast to other players
        await self.broadcast_to_others(player_id, {
            "type": "player_joined",
            "player": asdict(player)
        })
        
        # Start game if enough players
        if len(self.players) >= 2 and self.game_state == "waiting":
            await self.start_game()
        
        logger.info(f"Player {player.username} joined room {self.room_id}")
        return True
    
    def get_class_stats(self, player_class: PlayerClass) -> Dict[str, int]:
        """Get base stats for player class"""
        stats = {
            PlayerClass.DREAM_WALKER: {"health": 100, "energy": 120},
            PlayerClass.SHARD_GUARDIAN: {"health": 150, "energy": 80},
            PlayerClass.NIGHTMARE_HUNTER: {"health": 120, "energy": 100},
            PlayerClass.VOID_MAGE: {"health": 80, "energy": 150},
            PlayerClass.REALITY_ANCHOR: {"health": 140, "energy": 90}
        }
        return stats.get(player_class, {"health": 100, "energy": 100})
    
    def get_class_abilities(self, player_class: PlayerClass) -> List[Ability]:
        """Get abilities for player class"""
        abilities = {
            PlayerClass.DREAM_WALKER: [
                Ability("phase_step", "Phase Step", AbilityType.UTILITY, 0, 300, 5.0, 20, "Teleport short distance"),
                Ability("dream_bolt", "Dream Bolt", AbilityType.OFFENSIVE, 35, 500, 2.0, 15, "Projectile attack"),
                Ability("lucid_shield", "Lucid Shield", AbilityType.DEFENSIVE, 0, 0, 8.0, 30, "Absorb next attack")
            ],
            PlayerClass.SHARD_GUARDIAN: [
                Ability("shard_slam", "Shard Slam", AbilityType.OFFENSIVE, 50, 200, 4.0, 25, "Melee area attack"),
                Ability("guardian_aura", "Guardian Aura", AbilityType.DEFENSIVE, 0, 300, 12.0, 40, "Heal nearby allies"),
                Ability("shard_barrier", "Shard Barrier", AbilityType.DEFENSIVE, 0, 0, 10.0, 35, "Create protective barrier")
            ],
            PlayerClass.NIGHTMARE_HUNTER: [
                Ability("shadow_strike", "Shadow Strike", AbilityType.OFFENSIVE, 45, 400, 3.0, 20, "High damage stealth attack"),
                Ability("fear_aura", "Fear Aura", AbilityType.UTILITY, 0, 250, 15.0, 50, "Slow nearby enemies"),
                Ability("nightmare_dash", "Nightmare Dash", AbilityType.UTILITY, 0, 600, 6.0, 25, "Fast movement ability")
            ],
            PlayerClass.VOID_MAGE: [
                Ability("void_blast", "Void Blast", AbilityType.OFFENSIVE, 40, 600, 3.5, 30, "Long range magic attack"),
                Ability("reality_tear", "Reality Tear", AbilityType.OFFENSIVE, 60, 400, 8.0, 50, "Area damage spell"),
                Ability("void_walk", "Void Walk", AbilityType.UTILITY, 0, 0, 12.0, 60, "Become untargetable briefly")
            ],
            PlayerClass.REALITY_ANCHOR: [
                Ability("anchor_strike", "Anchor Strike", AbilityType.OFFENSIVE, 40, 300, 3.0, 20, "Solid physical attack"),
                Ability("stability_field", "Stability Field", AbilityType.DEFENSIVE, 0, 400, 10.0, 45, "Reduce damage in area"),
                Ability("reality_bind", "Reality Bind", AbilityType.UTILITY, 0, 500, 7.0, 35, "Root enemy in place")
            ]
        }
        return abilities.get(player_class, [])
    
    async def start_game(self):
        """Start the game"""
        self.game_state = "active"
        self.start_time = time.time()
        
        await self.broadcast_to_all({
            "type": "game_started",
            "game_mode": self.game_mode.value,
            "match_duration": self.match_duration
        })
        
        # Start game loop
        self.game_loop_task = asyncio.create_task(self.game_loop())
        logger.info(f"Game started in room {self.room_id}")
    
    async def game_loop(self):
        """Main game loop"""
        while self.game_state == "active":
            try:
                # Update game state
                await self.update_game_state()
                
                # Send game state to all players
                await self.send_game_state()
                
                # Check win conditions
                if await self.check_win_conditions():
                    break
                
                # Check time limit
                if time.time() - self.start_time > self.match_duration:
                    await self.end_game("time_limit")
                    break
                
                await asyncio.sleep(1/30)  # 30 FPS update rate
                
            except Exception as e:
                logger.error(f"Game loop error: {e}")
                break
    
    async def update_game_state(self):
        """Update game state"""
        current_time = time.time()
        
        # Regenerate energy for all players
        for player in self.players.values():
            if player.is_alive():
                player.energy = min(player.max_energy, player.energy + 2)
        
        # Game mode specific updates
        if self.game_mode == GameMode.SHARD_HUNT:
            await self.update_shard_hunt()
        elif self.game_mode == GameMode.KING_OF_HILL:
            await self.update_king_of_hill()
    
    async def update_shard_hunt(self):
        """Update Shard Hunt game mode"""
        # Check for shard collection
        for player in self.players.values():
            if not player.is_alive():
                continue
                
            for shard_id, shard_pos in list(self.shards_on_map.items()):
                distance = player.position.distance_to(shard_pos)
                if distance < 50:  # Collection range
                    player.shards_collected.append(shard_id)
                    player.add_experience(100)
                    del self.shards_on_map[shard_id]
                    
                    await self.broadcast_to_all({
                        "type": "shard_collected",
                        "player_id": player.id,
                        "shard_id": shard_id,
                        "player_shards": len(player.shards_collected)
                    })
    
    async def update_king_of_hill(self):
        """Update King of Hill game mode"""
        # Check which team controls the hill
        red_players_in_hill = 0
        blue_players_in_hill = 0
        
        for player in self.players.values():
            if player.is_alive():
                distance = player.position.distance_to(self.hill_center)
                if distance <= self.hill_radius:
                    if player.team == "red":
                        red_players_in_hill += 1
                    elif player.team == "blue":
                        blue_players_in_hill += 1
        
        # Award control time
        if red_players_in_hill > blue_players_in_hill:
            self.hill_control_time["red"] += 1/30  # 1/30 second per update
        elif blue_players_in_hill > red_players_in_hill:
            self.hill_control_time["blue"] += 1/30
    
    async def handle_player_action(self, player_id: str, action: Dict):
        """Handle player action"""
        if player_id not in self.players:
            return
        
        player = self.players[player_id]
        if not player.is_alive():
            return
        
        action_type = action.get("type")
        
        if action_type == "move":
            await self.handle_move(player, action)
        elif action_type == "use_ability":
            await self.handle_ability_use(player, action)
        elif action_type == "attack":
            await self.handle_attack(player, action)
    
    async def handle_move(self, player: Player, action: Dict):
        """Handle player movement"""
        new_pos = Vector2D(action["x"], action["y"])
        
        # Validate movement (basic bounds checking)
        if 0 <= new_pos.x <= self.map_size.x and 0 <= new_pos.y <= self.map_size.y:
            # Check movement speed (prevent teleporting)
            distance = player.position.distance_to(new_pos)
            max_distance = 10  # Max pixels per update
            
            if distance <= max_distance:
                player.position = new_pos
                player.last_action_time = time.time()
    
    async def handle_ability_use(self, player: Player, action: Dict):
        """Handle ability usage"""
        ability_id = action.get("ability_id")
        target_pos = Vector2D(action.get("target_x", 0), action.get("target_y", 0))
        
        # Find the ability
        ability = None
        for ab in player.abilities:
            if ab.id == ability_id:
                ability = ab
                break
        
        if not ability:
            return
        
        # Check energy cost
        if not player.use_energy(ability.energy_cost):
            return
        
        # Check range
        if ability.range > 0:
            distance = player.position.distance_to(target_pos)
            if distance > ability.range:
                return
        
        # Execute ability
        await self.execute_ability(player, ability, target_pos)
    
    async def execute_ability(self, player: Player, ability: Ability, target_pos: Vector2D):
        """Execute an ability"""
        if ability.ability_type == AbilityType.OFFENSIVE:
            # Find targets in range
            targets = []
            for other_player in self.players.values():
                if other_player.id != player.id and other_player.is_alive():
                    distance = other_player.position.distance_to(target_pos)
                    if distance <= 100:  # Ability effect radius
                        targets.append(other_player)
            
            # Apply damage
            for target in targets:
                if target.take_damage(ability.damage):
                    # Player died
                    target.deaths += 1
                    player.kills += 1
                    player.add_experience(50)
                    
                    await self.broadcast_to_all({
                        "type": "player_killed",
                        "killer_id": player.id,
                        "victim_id": target.id
                    })
                    
                    # Respawn after delay
                    asyncio.create_task(self.respawn_player(target.id, 5.0))
        
        elif ability.ability_type == AbilityType.UTILITY:
            if ability.id == "phase_step":
                # Teleport to target position
                direction = (target_pos.x - player.position.x, target_pos.y - player.position.y)
                distance = math.sqrt(direction[0]**2 + direction[1]**2)
                if distance > 0:
                    max_distance = min(ability.range, distance)
                    normalized = (direction[0] / distance, direction[1] / distance)
                    player.position.x += normalized[0] * max_distance
                    player.position.y += normalized[1] * max_distance
        
        # Broadcast ability use
        await self.broadcast_to_all({
            "type": "ability_used",
            "player_id": player.id,
            "ability_id": ability.id,
            "target_x": target_pos.x,
            "target_y": target_pos.y
        })
    
    async def respawn_player(self, player_id: str, delay: float):
        """Respawn a player after delay"""
        await asyncio.sleep(delay)
        
        if player_id in self.players:
            player = self.players[player_id]
            spawn_point = random.choice(self.spawn_points)
            player.position = spawn_point
            player.health = player.max_health
            player.energy = player.max_energy
            
            await self.broadcast_to_all({
                "type": "player_respawned",
                "player_id": player_id,
                "position": asdict(player.position)
            })
    
    async def check_win_conditions(self) -> bool:
        """Check if game should end"""
        if self.game_mode == GameMode.SHARD_HUNT:
            # Check if any player collected all shards
            for player in self.players.values():
                if len(player.shards_collected) >= 5:
                    await self.end_game("shard_victory", player.id)
                    return True
        
        elif self.game_mode == GameMode.KING_OF_HILL:
            # Check if any team reached control time limit
            for team, control_time in self.hill_control_time.items():
                if control_time >= 180:  # 3 minutes
                    await self.end_game("hill_victory", team)
                    return True
        
        return False
    
    async def end_game(self, reason: str, winner: str = None):
        """End the game"""
        self.game_state = "finished"
        
        # Calculate final scores
        final_scores = {}
        for player in self.players.values():
            final_scores[player.id] = {
                "kills": player.kills,
                "deaths": player.deaths,
                "shards": len(player.shards_collected),
                "experience": player.experience
            }
        
        await self.broadcast_to_all({
            "type": "game_ended",
            "reason": reason,
            "winner": winner,
            "final_scores": final_scores
        })
        
        logger.info(f"Game ended in room {self.room_id}: {reason}")
    
    async def send_game_state(self):
        """Send current game state to all players"""
        game_state = {
            "type": "game_state",
            "players": {pid: asdict(player) for pid, player in self.players.items()},
            "shards": {sid: asdict(pos) for sid, pos in self.shards_on_map.items()},
            "time_remaining": max(0, self.match_duration - (time.time() - self.start_time)) if self.start_time else 0
        }
        
        if self.game_mode == GameMode.KING_OF_HILL:
            game_state["hill_control"] = self.hill_control_time
        
        await self.broadcast_to_all(game_state)
    
    async def broadcast_to_all(self, message: Dict):
        """Broadcast message to all players"""
        if self.websockets:
            await asyncio.gather(
                *[ws.send(json.dumps(message)) for ws in self.websockets.values()],
                return_exceptions=True
            )
    
    async def broadcast_to_others(self, exclude_player_id: str, message: Dict):
        """Broadcast message to all players except one"""
        websockets_to_send = [
            ws for pid, ws in self.websockets.items() 
            if pid != exclude_player_id
        ]
        if websockets_to_send:
            await asyncio.gather(
                *[ws.send(json.dumps(message)) for ws in websockets_to_send],
                return_exceptions=True
            )
    
    async def remove_player(self, player_id: str):
        """Remove a player from the room"""
        if player_id in self.players:
            player = self.players[player_id]
            del self.players[player_id]
            
            if player_id in self.websockets:
                del self.websockets[player_id]
            
            await self.broadcast_to_all({
                "type": "player_left",
                "player_id": player_id,
                "username": player.username
            })
            
            # End game if not enough players
            if len(self.players) < 2 and self.game_state == "active":
                await self.end_game("insufficient_players")
            
            logger.info(f"Player {player.username} left room {self.room_id}")

class PVPGameServer:
    """Main PVP Game Server"""
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.rooms: Dict[str, GameRoom] = {}
        self.player_to_room: Dict[str, str] = {}
    
    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle new client connection"""
        logger.info(f"New client connected from {websocket.remote_address}")
        
        try:
            async for message in websocket:
                data = json.loads(message)
                await self.handle_message(websocket, data)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            await self.cleanup_client(websocket)
    
    async def handle_message(self, websocket: websockets.WebSocketServerProtocol, data: Dict):
        """Handle message from client"""
        message_type = data.get("type")
        
        if message_type == "create_room":
            await self.create_room(websocket, data)
        elif message_type == "join_room":
            await self.join_room(websocket, data)
        elif message_type == "player_action":
            await self.handle_player_action(websocket, data)
        elif message_type == "list_rooms":
            await self.list_rooms(websocket)
    
    async def create_room(self, websocket: websockets.WebSocketServerProtocol, data: Dict):
        """Create a new game room"""
        room_id = str(uuid.uuid4())[:8]
        game_mode = GameMode(data.get("game_mode", "shard_hunt"))
        max_players = data.get("max_players", 8)
        
        room = GameRoom(room_id, game_mode, max_players)
        self.rooms[room_id] = room
        
        # Add creator as first player
        success = await room.add_player(websocket, data["player"])
        if success:
            # Find the player ID that was assigned
            for player_id, ws in room.websockets.items():
                if ws == websocket:
                    self.player_to_room[player_id] = room_id
                    break
        
        logger.info(f"Created room {room_id} with mode {game_mode.value}")
    
    async def join_room(self, websocket: websockets.WebSocketServerProtocol, data: Dict):
        """Join an existing room"""
        room_id = data.get("room_id")
        
        if room_id not in self.rooms:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Room not found"
            }))
            return
        
        room = self.rooms[room_id]
        success = await room.add_player(websocket, data["player"])
        
        if success:
            # Find the player ID that was assigned
            for player_id, ws in room.websockets.items():
                if ws == websocket:
                    self.player_to_room[player_id] = room_id
                    break
    
    async def handle_player_action(self, websocket: websockets.WebSocketServerProtocol, data: Dict):
        """Handle player action in game"""
        # Find which player this websocket belongs to
        player_id = None
        for pid, ws in [(pid, room.websockets.get(pid)) for room in self.rooms.values() for pid in room.websockets]:
            if ws == websocket:
                player_id = pid
                break
        
        if player_id and player_id in self.player_to_room:
            room_id = self.player_to_room[player_id]
            if room_id in self.rooms:
                await self.rooms[room_id].handle_player_action(player_id, data["action"])
    
    async def list_rooms(self, websocket: websockets.WebSocketServerProtocol):
        """List available rooms"""
        room_list = []
        for room in self.rooms.values():
            if room.game_state == "waiting":
                room_list.append({
                    "room_id": room.room_id,
                    "game_mode": room.game_mode.value,
                    "players": len(room.players),
                    "max_players": room.max_players
                })
        
        await websocket.send(json.dumps({
            "type": "room_list",
            "rooms": room_list
        }))
    
    async def cleanup_client(self, websocket: websockets.WebSocketServerProtocol):
        """Clean up when client disconnects"""
        # Find and remove player from room
        player_id = None
        room_id = None
        
        for room in self.rooms.values():
            for pid, ws in room.websockets.items():
                if ws == websocket:
                    player_id = pid
                    room_id = room.room_id
                    break
            if player_id:
                break
        
        if player_id and room_id:
            await self.rooms[room_id].remove_player(player_id)
            if player_id in self.player_to_room:
                del self.player_to_room[player_id]
            
            # Remove empty rooms
            if len(self.rooms[room_id].players) == 0:
                del self.rooms[room_id]
    
    async def start_server(self):
        """Start the PVP game server"""
        logger.info(f"Starting PVP Game Server on {self.host}:{self.port}")
        
        async with websockets.serve(self.handle_client, self.host, self.port):
            logger.info("PVP Game Server is running!")
            await asyncio.Future()  # Run forever

# Example usage
if __name__ == "__main__":
    print("🎮 ELOHIM-FORGE: PVP Game Server")
    print("=================================")
    print("Game Modes:")
    print("- Shard Hunt: Collect Elohim Shards to win")
    print("- Team Deathmatch: Team vs Team combat")
    print("- King of Hill: Control the hill to win")
    print("- Dream Duel: 1v1 combat")
    print()
    print("Player Classes:")
    print("- Dream Walker: Balanced mobility and magic")
    print("- Shard Guardian: Tank with healing abilities")
    print("- Nightmare Hunter: Stealth and high damage")
    print("- Void Mage: Long-range magical attacks")
    print("- Reality Anchor: Control and stability")
    print()
    
    # Start the server
    server = PVPGameServer()
    asyncio.run(server.start_server())