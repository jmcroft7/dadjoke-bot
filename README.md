<div align="center">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python Logo" width="80" height="80" />
  <h2 align="center">DadJoke Bot</h2>
  <p align="center">
    A feature-rich Discord bot that brings humor and fitness tracking to your server.
    <br />
    <a href="https://github.com/jmcroft7/dadjoke-bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/jmcroft7/dadjoke-bot/issues">Request Feature</a>
  </p>
</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Discord](https://img.shields.io/badge/Discord-API-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/developers/docs/intro)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://github.com/jmcroft7/dadjoke-bot/blob/main/LICENSE.txt)
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

---

## 📖 About The Project

DadJoke Bot (affectionately known as **Gooby Bot** in some circles) is designed to keep your Discord community engaged and active. Whether you need a quick laugh from a curated list of dad jokes or want to track your fitness goals with your friends, this bot has you covered.

### Key Features
- **Dad Jokes**: Fetches fresh, groan-worthy dad jokes using the [icanhazdadjoke API](https://icanhazdadjoke.com/).
- **Exercise Tracking**: Support for Pushups, Pullups, Squats, and Crunches.
- **Daily Goals**: Set collective daily targets for the server.
- **Personal Progress**: Track your individual lifetime stats, daily progress, and streaks.
- **Leaderboards**: Compete with friends on lifetime leaderboards.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- A Discord Bot Token (obtainable from the [Discord Developer Portal](https://discord.com/developers/applications))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jmcroft7/dadjoke-bot.git
   cd dadjoke-bot
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure `discord.py` and `python-dotenv` are installed)*

4. **Configure environment variables**
   Create a `.env` file in the root directory and add your bot token:
   ```env
   Token1=YOUR_DISCORD_BOT_TOKEN
   ```

5. **Run the bot**
   ```bash
   python __app__.py
   ```

---

## 🛠 Command Reference

The default command prefix is `!`.

### General Commands
| Command | Alias | Description |
| :--- | :--- | :--- |
| `!joke` | `!j` | Fetches a random dad joke. |
| `!gooby` | `!g` | Responds with a random "Gooby" quote. |
| `!help` | `!h` | Displays the help menu. |

### Exercise & Fitness
| Command | Alias | Description |
| :--- | :--- | :--- |
| `!add <ex> <amt>` | `!a` | Add to the daily collective goal (default: pushups). |
| `!total [ex]` | `!t` | View daily goal progress. |
| `!setTotal <ex> <amt>` | `!st` | Manually set the daily goal total. |
| `!done [ex] [amt]` | `!d` | Log your completed exercises (defaults: pushups, 10). |
| `!setDone <ex> <amt>` | `!sd` | Manually set your daily completed count. |
| `!progress [ex]` | `!p` | View current progress of all active users. |
| `!myProgress` | `!mp` | View your personal stats, started date, and streaks. |
| `!lifetime [ex]` | `!l` | View the top 10 lifetime leaderboard. |

**Supported Exercises**: `pushups`, `pullups`, `squats`, `crunches`.

---

## 📄 License

Distributed under the MIT License. See `LICENSE.txt` for more information.

---

## 🤝 Contact

Johnathan Croft - [@devJohnathan](https://twitter.com/devJohnathan) - croftmjohn@gmail.com

Project Link: [https://github.com/jmcroft7/dadjoke-bot](https://github.com/jmcroft7/dadjoke-bot)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/devjohnathan/
