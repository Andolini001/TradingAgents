#!/usr/bin/env python3
"""
Tamagotchi Game - A virtual pet simulation
A fun terminal-based Tamagotchi game with beautiful UI
"""

import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import random

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.align import Align
from rich.live import Live
from rich import box
import questionary

console = Console()

class Tamagotchi:
    def __init__(self, name: str = "Tamagotchi"):
        self.name = name
        self.birth_time = datetime.now()
        self.last_update = datetime.now()
        
        # Stats (0-100)
        self.hunger = 50
        self.happiness = 80
        self.energy = 100
        self.health = 100
        self.hygiene = 80
        
        # Life stage
        self.age_hours = 0
        self.stage = "egg"  # egg -> baby -> child -> teen -> adult
        self.evolution_progress = 0
        
        # Personality traits
        self.personality = random.choice(["playful", "lazy", "hungry", "clean", "energetic"])
        
        # Status effects
        self.is_sick = False
        self.is_sleeping = False
        self.mood = "happy"
        
        # Achievements
        self.achievements = []
        self.care_score = 0
        
    def update_stats(self, elapsed_hours: float):
        """Update pet stats based on elapsed time"""
        if self.is_sleeping:
            # Sleeping reduces hunger and increases energy
            self.hunger = max(0, self.hunger - elapsed_hours * 2)
            self.energy = min(100, self.energy + elapsed_hours * 5)
        else:
            # Normal stat changes
            self.hunger = min(100, self.hunger + elapsed_hours * 3)
            self.happiness = max(0, self.happiness - elapsed_hours * 1.5)
            self.energy = max(0, self.energy - elapsed_hours * 2)
            self.hygiene = max(0, self.hygiene - elapsed_hours * 1)
        
        # Health depends on other stats
        if self.hunger > 80 or self.happiness < 20 or self.hygiene < 20:
            self.health = max(0, self.health - elapsed_hours * 2)
        else:
            self.health = min(100, self.health + elapsed_hours * 0.5)
        
        # Update age and evolution
        self.age_hours += elapsed_hours
        self.evolution_progress += elapsed_hours * 0.1
        
        # Evolution stages
        if self.evolution_progress >= 10 and self.stage == "egg":
            self.stage = "baby"
            self.evolution_progress = 0
        elif self.evolution_progress >= 20 and self.stage == "baby":
            self.stage = "child"
            self.evolution_progress = 0
        elif self.evolution_progress >= 40 and self.stage == "child":
            self.stage = "teen"
            self.evolution_progress = 0
        elif self.evolution_progress >= 60 and self.stage == "teen":
            self.stage = "adult"
            self.evolution_progress = 0
        
        # Update mood based on stats
        self._update_mood()
        
        # Check for sickness
        if self.health < 30 and not self.is_sick:
            self.is_sick = True
        
        # Auto-sleep when energy is low
        if self.energy < 20 and not self.is_sleeping:
            self.is_sleeping = True
    
    def _update_mood(self):
        """Update pet mood based on current stats"""
        avg_stats = (self.hunger + self.happiness + self.energy + self.health + self.hygiene) / 5
        
        if avg_stats >= 80:
            self.mood = "ecstatic"
        elif avg_stats >= 60:
            self.mood = "happy"
        elif avg_stats >= 40:
            self.mood = "neutral"
        elif avg_stats >= 20:
            self.mood = "sad"
        else:
            self.mood = "miserable"
    
    def feed(self, food_type: str = "normal"):
        """Feed the pet"""
        if self.is_sleeping:
            return "Your pet is sleeping! Let it rest."
        
        food_effects = {
            "normal": {"hunger": 30, "happiness": 5},
            "treat": {"hunger": 20, "happiness": 15, "energy": 10},
            "healthy": {"hunger": 25, "health": 10, "happiness": 5},
            "special": {"hunger": 40, "happiness": 20, "energy": 15, "health": 15}
        }
        
        effects = food_effects.get(food_type, food_effects["normal"])
        
        for stat, value in effects.items():
            if hasattr(self, stat):
                current_value = getattr(self, stat)
                setattr(self, stat, min(100, current_value + value))
        
        self.care_score += 5
        self._update_mood()
        return f"Yum! {self.name} enjoyed the {food_type} food!"
    
    def play(self, game_type: str = "normal"):
        """Play with the pet"""
        if self.is_sleeping:
            return "Your pet is sleeping! Let it rest."
        
        if self.energy < 20:
            return f"{self.name} is too tired to play!"
        
        game_effects = {
            "normal": {"happiness": 20, "energy": -10},
            "active": {"happiness": 30, "energy": -20, "hunger": 10},
            "gentle": {"happiness": 15, "energy": -5},
            "training": {"happiness": 25, "energy": -15, "care_score": 10}
        }
        
        effects = game_effects.get(game_type, game_effects["normal"])
        
        for stat, value in effects.items():
            if hasattr(self, stat):
                current_value = getattr(self, stat)
                if stat == "energy" or stat == "hunger":
                    setattr(self, stat, max(0, current_value + value))
                else:
                    setattr(self, stat, min(100, current_value + value))
        
        self.care_score += 8
        self._update_mood()
        return f"Fun! {self.name} loved playing {game_type}!"
    
    def sleep(self):
        """Put pet to sleep or wake it up"""
        if self.is_sleeping:
            self.is_sleeping = False
            return f"{self.name} woke up feeling refreshed!"
        else:
            self.is_sleeping = True
            return f"{self.name} went to sleep. Sweet dreams!"
    
    def clean(self):
        """Clean the pet"""
        if self.is_sleeping:
            return "Your pet is sleeping! Let it rest."
        
        self.hygiene = 100
        self.happiness += 10
        self.care_score += 3
        self._update_mood()
        return f"{self.name} is now clean and happy!"
    
    def heal(self):
        """Heal the pet if sick"""
        if not self.is_sick:
            return f"{self.name} is not sick!"
        
        self.is_sick = False
        self.health = min(100, self.health + 30)
        self.care_score += 15
        return f"{self.name} is feeling better!"
    
    def get_status_emoji(self):
        """Get emoji representation of pet status"""
        if self.is_sleeping:
            return "😴"
        elif self.is_sick:
            return "🤒"
        elif self.mood == "ecstatic":
            return "🤩"
        elif self.mood == "happy":
            return "😊"
        elif self.mood == "neutral":
            return "😐"
        elif self.mood == "sad":
            return "😢"
        else:
            return "😭"
    
    def get_stage_emoji(self):
        """Get emoji for life stage"""
        stage_emojis = {
            "egg": "🥚",
            "baby": "👶",
            "child": "🧒",
            "teen": "👱",
            "adult": "👨"
        }
        return stage_emojis.get(self.stage, "🐾")

class TamagotchiGame:
    def __init__(self):
        self.pet = None
        self.save_file = "tamagotchi_save.json"
        self.console = Console()
    
    def create_new_pet(self):
        """Create a new Tamagotchi pet"""
        name = Prompt.ask("What would you like to name your Tamagotchi?", default="Tamagotchi")
        self.pet = Tamagotchi(name)
        self.save_game()
        self.console.print(f"🎉 Welcome {name}! Your new Tamagotchi is ready!", style="bold green")
    
    def load_game(self):
        """Load saved game"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                
                self.pet = Tamagotchi(data['name'])
                self.pet.__dict__.update(data)
                self.pet.birth_time = datetime.fromisoformat(data['birth_time'])
                self.pet.last_update = datetime.fromisoformat(data['last_update'])
                
                # Update stats since last save
                elapsed = datetime.now() - self.pet.last_update
                elapsed_hours = elapsed.total_seconds() / 3600
                self.pet.update_stats(elapsed_hours)
                
                return True
            except Exception as e:
                self.console.print(f"Error loading save file: {e}", style="red")
                return False
        return False
    
    def save_game(self):
        """Save current game state"""
        if self.pet:
            data = self.pet.__dict__.copy()
            data['birth_time'] = self.pet.birth_time.isoformat()
            data['last_update'] = datetime.now().isoformat()
            
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=2)
    
    def display_status(self):
        """Display current pet status"""
        if not self.pet:
            return
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        # Header with name and status
        header = Panel(
            Align.center(
                Text(f"{self.pet.get_status_emoji()} {self.pet.name} {self.pet.get_stage_emoji()}", style="bold blue")
            ),
            title="[bold cyan]Tamagotchi Status[/bold cyan]",
            border_style="blue"
        )
        
        # Main content with stats
        stats_table = Table(title="Pet Statistics", box=box.ROUNDED)
        stats_table.add_column("Stat", style="cyan", no_wrap=True)
        stats_table.add_column("Value", style="magenta")
        stats_table.add_column("Bar", style="green")
        
        stats = [
            ("Hunger", self.pet.hunger, "🍽️"),
            ("Happiness", self.pet.happiness, "😊"),
            ("Energy", self.pet.energy, "⚡"),
            ("Health", self.pet.health, "❤️"),
            ("Hygiene", self.pet.hygiene, "🧼")
        ]
        
        for stat_name, value, emoji in stats:
            bar_length = int(value / 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            color = "green" if value > 70 else "yellow" if value > 40 else "red"
            stats_table.add_row(f"{emoji} {stat_name}", f"{value}/100", f"[{color}]{bar}[/{color}]")
        
        # Additional info
        info_table = Table(box=box.SIMPLE)
        info_table.add_column("Info", style="cyan")
        info_table.add_column("Value", style="white")
        
        age_days = int(self.pet.age_hours / 24)
        age_hours = int(self.pet.age_hours % 24)
        
        info_table.add_row("Age", f"{age_days} days, {age_hours} hours")
        info_table.add_row("Stage", self.pet.stage.title())
        info_table.add_row("Mood", self.pet.mood.title())
        info_table.add_row("Personality", self.pet.personality.title())
        info_table.add_row("Care Score", str(self.pet.care_score))
        
        if self.pet.is_sleeping:
            info_table.add_row("Status", "[yellow]Sleeping[/yellow]")
        elif self.pet.is_sick:
            info_table.add_row("Status", "[red]Sick[/red]")
        else:
            info_table.add_row("Status", "[green]Active[/green]")
        
        main_content = Layout()
        main_content.split_row(
            Layout(Panel(stats_table, title="[bold]Stats[/bold]", border_style="green")),
            Layout(Panel(info_table, title="[bold]Info[/bold]", border_style="blue"))
        )
        
        # Footer with actions
        actions_text = Text()
        actions_text.append("Actions: ", style="bold")
        actions_text.append("1-Feed 2-Play 3-Sleep 4-Clean 5-Heal 6-Save 7-Exit", style="cyan")
        
        footer = Panel(
            Align.center(actions_text),
            title="[bold]Available Actions[/bold]",
            border_style="yellow"
        )
        
        layout["header"].update(header)
        layout["main"].update(main_content)
        layout["footer"].update(footer)
        
        self.console.print(layout)
    
    def get_action_choice(self):
        """Get user action choice"""
        choices = [
            "Feed",
            "Play", 
            "Sleep/Wake",
            "Clean",
            "Heal",
            "Save Game",
            "Exit"
        ]
        
        action = questionary.select(
            "What would you like to do?",
            choices=choices
        ).ask()
        
        return action
    
    def handle_action(self, action: str):
        """Handle user action"""
        if not self.pet:
            return
        
        result = ""
        
        if action == "Feed":
            food_choice = questionary.select(
                "What type of food?",
                choices=["normal", "treat", "healthy", "special"]
            ).ask()
            result = self.pet.feed(food_choice)
        
        elif action == "Play":
            if self.pet.energy < 20:
                result = f"{self.pet.name} is too tired to play!"
            else:
                game_choice = questionary.select(
                    "What type of game?",
                    choices=["normal", "active", "gentle", "training"]
                ).ask()
                result = self.pet.play(game_choice)
        
        elif action == "Sleep/Wake":
            result = self.pet.sleep()
        
        elif action == "Clean":
            result = self.pet.clean()
        
        elif action == "Heal":
            result = self.pet.heal()
        
        elif action == "Save Game":
            self.save_game()
            result = "Game saved successfully!"
        
        elif action == "Exit":
            if Confirm.ask("Save before exiting?"):
                self.save_game()
            return "exit"
        
        if result:
            self.console.print(f"💬 {result}", style="bold green")
        
        return "continue"
    
    def run(self):
        """Main game loop"""
        self.console.print(Panel.fit(
            "🐾 Welcome to Tamagotchi! 🐾",
            title="[bold cyan]Tamagotchi Game[/bold cyan]",
            border_style="blue"
        ))
        
        # Load or create new game
        if self.load_game():
            self.console.print("📂 Loaded saved game!", style="green")
        else:
            self.console.print("🆕 Starting new game...", style="yellow")
            self.create_new_pet()
        
        # Main game loop
        while True:
            # Update pet stats
            if self.pet:
                elapsed = datetime.now() - self.pet.last_update
                elapsed_hours = elapsed.total_seconds() / 3600
                self.pet.update_stats(elapsed_hours)
                self.pet.last_update = datetime.now()
            
            # Clear screen and display status
            self.console.clear()
            self.display_status()
            
            # Get and handle action
            action = self.get_action_choice()
            result = self.handle_action(action)
            
            if result == "exit":
                break
            
            # Brief pause
            time.sleep(1)

def main():
    """Main entry point"""
    game = TamagotchiGame()
    try:
        game.run()
    except KeyboardInterrupt:
        console.print("\n👋 Thanks for playing Tamagotchi!", style="bold green")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")

if __name__ == "__main__":
    main()