"""Test script to validate refactored structure"""
import sys

print('Testing refactored structure...\n')

# Testar todos os imports
print('1. Testing core imports...')
from src.core import Game
print('   ✓ src.core.Game')

print('2. Testing entity imports...')
from src.entities import Heroi, Enemy, Bullet
print('   ✓ src.entities.Heroi')
print('   ✓ src.entities.Enemy')
print('   ✓ src.entities.Bullet')

print('3. Testing system imports...')
from src.systems import Direction
print('   ✓ src.systems.Direction')

print('4. Testing world imports...')
from src.world import Map, Tile
print('   ✓ src.world.Map')
print('   ✓ src.world.Tile')

print('5. Testing level imports...')
from levels.level1 import tile_data, tile_images, solid_tiles
print('   ✓ levels.level1')

print('\n✅ All imports successful!')
print('✅ Structure is ready for development')
print('\n📂 Directory structure:')
print('   src/core/     - Game engine')
print('   src/entities/ - Game objects (Heroi, Enemy, Bullet)')
print('   src/systems/  - Auxiliary systems (Direction)')
print('   src/world/    - Map and Tile classes')
print('   levels/       - Level data')
