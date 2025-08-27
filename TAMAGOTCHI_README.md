# 🐾 Tamagotchi Game

A fun, interactive terminal-based Tamagotchi virtual pet simulation with beautiful UI!

## 🎮 Features

- **Virtual Pet Care**: Feed, play, clean, and care for your Tamagotchi
- **Life Stages**: Watch your pet evolve from egg → baby → child → teen → adult
- **Real-time Stats**: Monitor hunger, happiness, energy, health, and hygiene
- **Personality System**: Each pet has unique personality traits
- **Beautiful UI**: Rich terminal interface with emojis and colorful displays
- **Save/Load System**: Your progress is automatically saved
- **Mood System**: Pet mood changes based on care and stats

## 🚀 How to Run

```bash
python tamagotchi.py
```

## 🎯 How to Play

### Basic Actions:
1. **Feed** - Choose from different food types:
   - Normal: Basic nutrition
   - Treat: Increases happiness and energy
   - Healthy: Boosts health
   - Special: Best overall effects

2. **Play** - Different games for different effects:
   - Normal: Standard play
   - Active: More fun but uses more energy
   - Gentle: Less energy consumption
   - Training: Increases care score

3. **Sleep/Wake** - Put your pet to sleep or wake it up
4. **Clean** - Clean your pet to restore hygiene
5. **Heal** - Heal your pet if it gets sick
6. **Save Game** - Manually save your progress
7. **Exit** - Exit the game (with save option)

### Pet Stats:
- **Hunger** 🍽️: Increases over time, feed to reduce
- **Happiness** 😊: Decreases over time, play to increase
- **Energy** ⚡: Decreases with activities, sleep to restore
- **Health** ❤️: Affected by other stats, heal when sick
- **Hygiene** 🧼: Decreases over time, clean to restore

### Life Stages:
- 🥚 **Egg**: Newborn stage
- 👶 **Baby**: Young and growing
- 🧒 **Child**: More active and playful
- 👱 **Teen**: Adolescent stage
- 👨 **Adult**: Fully grown

### Tips:
- Keep all stats balanced for optimal health
- Your pet will automatically sleep when energy is low
- Sick pets need healing to recover
- Different personalities may prefer different activities
- Care score increases with good care practices

## 🎨 UI Features

- **Color-coded stat bars**: Green (good), Yellow (warning), Red (critical)
- **Emoji indicators**: Visual status and mood representation
- **Interactive menus**: Easy navigation with arrow keys
- **Real-time updates**: Stats change based on elapsed time
- **Beautiful layouts**: Organized information display

## 💾 Save System

Your game automatically saves to `tamagotchi_save.json`. The game will:
- Load your previous save when starting
- Update stats based on time passed since last play
- Save automatically after actions
- Offer manual save option

## 🎉 Enjoy Your Tamagotchi!

Take good care of your virtual pet and watch it grow and evolve! The better you care for it, the happier and healthier it will be.

---

*Made with ❤️ using Python, Rich, and Questionary*