
import pygame
import numpy as np
import random
from collections import defaultdict
import sys

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 4
GRID_WIDTH = 200  # Adjustable grid dimensions
GRID_HEIGHT = 150
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 150  # Extra space for stats and toggle

# Colors
RED = (255, 0, 0)      # Bad
GREEN = (0, 255, 0)    # Good
BLACK = (0, 0, 0)      # Empty
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
TOGGLE_ON = (0, 255, 0)
TOGGLE_OFF = (255, 0, 0)

# Cell states
EMPTY = 0
BAD = 1
GOOD = 2

# Population limits
MAX_POPULATION = int(GRID_WIDTH * GRID_HEIGHT * 0.4)  # 40% max density
INITIAL_POPULATION = int(GRID_WIDTH * GRID_HEIGHT * 0.15)  # 15% initial density

class HumanSimulation:
    def __init__(self):
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Human Behavior Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Statistics
        self.generation = 0
        self.conversions = 0
        self.deaths = 0
        self.births = 0
        
        # Kill toggle
        self.kills_allowed = True
        self.toggle_rect = pygame.Rect(10, GRID_HEIGHT * CELL_SIZE + 110, 100, 25)
        
        self.initialize_population()
    
    def initialize_population(self):
        """Initialize population with Gaussian distribution"""
        center_x, center_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
        
        for _ in range(INITIAL_POPULATION):
            # Gaussian distribution around center
            x = int(np.random.normal(center_x, GRID_WIDTH * 0.2))
            y = int(np.random.normal(center_y, GRID_HEIGHT * 0.2))
            
            # Clamp to grid bounds
            x = max(0, min(GRID_WIDTH - 1, x))
            y = max(0, min(GRID_HEIGHT - 1, y))
            
            if self.grid[y, x] == EMPTY:
                self.grid[y, x] = random.choice([BAD, GOOD])
    
    def get_neighbors(self, y, x, radius=1):
        """Get all neighbors within radius"""
        neighbors = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dy == 0 and dx == 0:
                    continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                    neighbors.append((ny, nx))
        return neighbors
    
    def count_neighbors(self, y, x, radius=1):
        """Count neighbors by type"""
        neighbors = self.get_neighbors(y, x, radius)
        bad_count = sum(1 for ny, nx in neighbors if self.grid[ny, nx] == BAD)
        good_count = sum(1 for ny, nx in neighbors if self.grid[ny, nx] == GOOD)
        return bad_count, good_count
    
    def get_group_size(self, y, x, cell_type):
        """Get size of connected group of same type"""
        if self.grid[y, x] != cell_type:
            return 0
        
        visited = set()
        stack = [(y, x)]
        count = 0
        
        while stack and count < 20:  # Limit search for performance
            cy, cx = stack.pop()
            if (cy, cx) in visited:
                continue
            visited.add((cy, cx))
            
            if self.grid[cy, cx] == cell_type:
                count += 1
                for ny, nx in self.get_neighbors(cy, cx):
                    if (ny, nx) not in visited:
                        stack.append((ny, nx))
        
        return count
    
    def handle_kill_event(self, y, x, new_grid, kill_probability):
        """Handle kill events based on toggle setting"""
        if self.kills_allowed:
            if random.random() < kill_probability:
                new_grid[y, x] = EMPTY
                self.deaths += 1
                return True
        else:
            # When kills not allowed, convert kill probability to 50% conversion, 50% nothing
            if random.random() < kill_probability:
                if random.random() < 0.5:
                    # Convert instead of kill
                    new_grid[y, x] = GOOD if self.grid[y, x] == BAD else BAD
                    self.conversions += 1
                    return True
                # Else: nothing happens (50% chance)
        return False
    
    def individual_interactions(self, new_grid):
        """Handle individual cell interactions"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y, x] == EMPTY:
                    continue
                
                current_type = self.grid[y, x]
                neighbors = self.get_neighbors(y, x)
                
                # Get neighbor types
                bad_neighbors = []
                good_neighbors = []
                
                for ny, nx in neighbors:
                    if self.grid[ny, nx] == BAD:
                        bad_neighbors.append((ny, nx))
                    elif self.grid[ny, nx] == GOOD:
                        good_neighbors.append((ny, nx))
                
                # Individual interaction rules
                if current_type == GOOD:
                    if len(bad_neighbors) >= 3:
                        # 3+ red meet green: 75% kill, 25% convert
                        if not self.handle_kill_event(y, x, new_grid, 0.75):
                            if random.random() < 0.25:
                                new_grid[y, x] = BAD
                                self.conversions += 1
                    elif len(bad_neighbors) == 2:
                        # 2 red + 1 green: 50% kill, 50% convert
                        if not self.handle_kill_event(y, x, new_grid, 0.5):
                            new_grid[y, x] = BAD
                            self.conversions += 1
                    elif len(bad_neighbors) == 1:
                        # 1 red + 1 green: 50% both become good or bad
                        if random.random() < 0.5:
                            new_grid[y, x] = BAD
                            self.conversions += 1
                
                elif current_type == BAD:
                    if len(good_neighbors) >= 3:
                        # 3+ green meet red: 90% convert, 10% kill
                        if random.random() < 0.9:
                            new_grid[y, x] = GOOD
                            self.conversions += 1
                        else:
                            self.handle_kill_event(y, x, new_grid, 1.0)  # 10% kill probability handled above
                    elif len(good_neighbors) == 2:
                        # 2 green + 1 red: convert
                        new_grid[y, x] = GOOD
                        self.conversions += 1
                    elif len(good_neighbors) == 1:
                        # 1 green + 1 red: 50% both become good or bad
                        if random.random() < 0.5:
                            new_grid[y, x] = GOOD
                            self.conversions += 1
    
    def group_interactions(self, new_grid):
        """Handle group-based interactions"""
        processed = set()
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if (y, x) in processed or self.grid[y, x] == EMPTY:
                    continue
                
                current_type = self.grid[y, x]
                group_size = self.get_group_size(y, x, current_type)
                
                if group_size >= 4:
                    # Large group can spawn new member
                    empty_neighbors = []
                    for ny, nx in self.get_neighbors(y, x, radius=2):
                        if self.grid[ny, nx] == EMPTY:
                            empty_neighbors.append((ny, nx))
                    
                    if empty_neighbors and self.count_total_population() < MAX_POPULATION:
                        spawn_y, spawn_x = random.choice(empty_neighbors)
                        if current_type == BAD:
                            prob_coming = 0.6
                        if current_type == GOOD:
                            prob_coming = 0.3
                        if random.random() < prob_coming:  # 30% chance to spawn
                            new_grid[spawn_y, spawn_x] = current_type
                            self.births += 1
                
                # Group competition
                bad_neighbors, good_neighbors = self.count_neighbors(y, x, radius=2)
                
                if current_type == BAD and good_neighbors >= bad_neighbors:
                    self.handle_kill_event(y, x, new_grid, 0.5)
                elif current_type == GOOD and bad_neighbors >= good_neighbors:
                    self.handle_kill_event(y, x, new_grid, 0.5)
                
                processed.add((y, x))

    def handle_overpopulation(self, new_grid):
        """Kill random cells if population exceeds limit, with higher probability in crowded/grouped areas."""
        total_pop = self.count_total_population()
        if total_pop <= MAX_POPULATION:
            return

        # Calculate how many need to die
        excess = total_pop - MAX_POPULATION + np.random.randint(1000,total_pop-1000)

        # Build a list of all living cells with their 'crowdedness' score
        candidates = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y, x] != EMPTY:
                    # Crowdedness: number of non-empty neighbors + group size
                    neighbors = self.get_neighbors(y, x)
                    crowded = sum(1 for ny, nx in neighbors if self.grid[ny, nx] != EMPTY)
                    group_size = self.get_group_size(y, x, self.grid[y, x])
                    # The more crowded/grouped, the higher the score
                    score = crowded + group_size
                    candidates.append((score, y, x))

        # Normalize scores to probabilities
        if not candidates:
            return
        scores = np.array([score for score, _, _ in candidates], dtype=float)
        if np.sum(scores) == 0:
            probs = np.ones(len(scores)) / len(scores)
        else:
            probs = scores / np.sum(scores)

        # Randomly select cells to kill, weighted by crowdedness/group size
        indices = np.random.choice(len(candidates), size=excess, replace=True, p=probs)
        for idx in indices:
            _, y, x = candidates[idx]
            new_grid[y, x] = EMPTY
            self.deaths += 1

    
    def random_events(self, new_grid):
        """Handle random conversions and isolation deaths"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if new_grid[y, x] == EMPTY:
                    continue
                
                current_type = new_grid[y, x]
                bad_neighbors, good_neighbors = self.count_neighbors(y, x)
                
                # Isolation death (surrounded by same type)
                if current_type == BAD and bad_neighbors >= 6 and good_neighbors == 0:
                    self.handle_kill_event(y, x, new_grid, 0.1)
                elif current_type == GOOD and good_neighbors >= 6 and bad_neighbors == 0:
                    self.handle_kill_event(y, x, new_grid, 0.1)
                
                # Random conversion (very low probability)
                if random.random() < 0.01:  # 1% chance
                    new_grid[y, x] = GOOD if current_type == BAD else BAD
                    self.conversions += 1
    
    def count_total_population(self):
        """Count total living cells"""
        return np.sum(self.grid != EMPTY)
    
    def update(self):
        """Update simulation by one generation"""
        new_grid = self.grid.copy()
        
        # Reset statistics
        self.conversions = 0
        self.deaths = 0
        self.births = 0
        
        # Apply all interaction rules
        self.individual_interactions(new_grid)
        self.group_interactions(new_grid)
        self.random_events(new_grid)
        self.handle_overpopulation(new_grid)
        
        if random.random() < 0.8:
            self.random_movement(new_grid)
        
        self.grid = new_grid
        self.generation += 1
    
    def random_movement(self, grid):
        """Randomly move some cells"""
        for _ in range(max(1, self.count_total_population() // 50)):
            y, x = random.randint(0, GRID_HEIGHT-1), random.randint(0, GRID_WIDTH-1)
            if grid[y, x] != EMPTY:
                neighbors = self.get_neighbors(y, x)
                empty_neighbors = [(ny, nx) for ny, nx in neighbors if grid[ny, nx] == EMPTY]
                if empty_neighbors:
                    ny, nx = random.choice(empty_neighbors)
                    grid[ny, nx] = grid[y, x]
                    grid[y, x] = EMPTY
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        if self.toggle_rect.collidepoint(pos):
            self.kills_allowed = not self.kills_allowed
    
    def draw(self):
        """Draw the simulation"""
        self.screen.fill(BLACK)
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y, x] == BAD:
                    color = RED
                elif self.grid[y, x] == GOOD:
                    color = GREEN
                else:
                    continue
                
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect)
        
        bad_count = np.sum(self.grid == BAD)
        good_count = np.sum(self.grid == GOOD)
        total_pop = bad_count + good_count
        
        stats = [
            f"Generation: {self.generation}",
            f"Population: {total_pop}/{MAX_POPULATION}",
            f"Bad: {bad_count} Good: {good_count}",
            f"Conversions: {self.conversions} Deaths: {self.deaths} Births: {self.births}",
            f"Press R to reset, SPACE to pause, +/- to change speed"
        ]
        
        y_offset = GRID_HEIGHT * CELL_SIZE + 10
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, WHITE)
            self.screen.blit(text, (10, y_offset + i * 20))
        
        # Draw kill toggle
        toggle_color = TOGGLE_ON if self.kills_allowed else TOGGLE_OFF
        pygame.draw.rect(self.screen, toggle_color, self.toggle_rect)
        pygame.draw.rect(self.screen, WHITE, self.toggle_rect, 2)
        
        toggle_text = "Kills: ON" if self.kills_allowed else "Kills: OFF"
        text_surface = self.small_font.render(toggle_text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.toggle_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        # Add instruction text
        instruction_text = "Click toggle to enable/disable kills"
        instruction_surface = self.small_font.render(instruction_text, True, LIGHT_GRAY)
        self.screen.blit(instruction_surface, (120, GRID_HEIGHT * CELL_SIZE + 115))
        
        pygame.display.flip()
    
    def reset(self):
        """Reset the simulation"""
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.generation = 0
        self.conversions = 0
        self.deaths = 0
        self.births = 0
        self.initialize_population()
    
    def run(self):
        """Main simulation loop"""
        running = True
        paused = False
        speed = 5  # Updates per second
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        speed = min(60, speed + 1)
                    elif event.key == pygame.K_MINUS:
                        speed = max(1, speed - 1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
            
            if not paused:
                self.update()
            
            self.draw()
            self.clock.tick(speed)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # GRID_WIDTH = 300 
    # GRID_HEIGHT = 200
    
    sim = HumanSimulation()
    sim.run()



