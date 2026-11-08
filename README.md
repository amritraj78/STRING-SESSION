<p align="center">
  <img src="https://files.catbox.moe/0kpdw9.jpg" alt="StringGen">
</p>

### 🤤 Features

- [»] **Pyrogram v2, Pyrogram v1 & Telethon** string session generator
- [»] **BotFather Bots Session** generation support
- [»] **Session String Validator & Checker (`/check`)** - safely verifies active/revoked sessions in-memory
- [»] **Broadcast System (`/broadcast`)** - broadcast text & media to all bot users with `-copy` & `-pin` options
- [»] **Ping & Uptime Monitor (`/ping`, `/uptime`, `/alive`)** - live latency, RAM usage & uptime stats
- [»] **Admin User Moderation (`/ban`, `/unban`, `/banned`)** - complete control over malicious users
- [»] **System Dashboard (`/stats`)** - real-time served users and resource analytics
- [»] **24/7 Koyeb Keep-Alive Auto-Pinger** - prevents free-tier deep sleep
- [»] **Interactive Menus (`/help`, `/about`)** with smooth inline navigation
- [»] Pure in-memory session operations - **100% safe & private**

---

### 🚀 Deploy to Koyeb

Deploy directly to Koyeb using the button below:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=string-session&type=git&repository=amritraj78%2FSTRING-SESSION&branch=main&builder=dockerfile&ports=8000%3Bhttp%3B%2F)

> **Important for Koyeb:**
> - **Builder:** Dockerfile (or Buildpack).
> - **Port:** Set port to `8000`, Protocol `HTTP`, Path `/`. The bot automatically serves a lightweight HTTP health check endpoint on `$PORT` to ensure Koyeb marks the service Healthy.

---

### 🚀 Deploy to Heroku
  
<p align="center"><a href="https://dashboard.heroku.com/new?template=https://github.com/amritraj78/STRING-SESSION"> <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-black?style=for-the-badge&logo=heroku" width="220" height="38.45"/></a></p>

---

## 🗒️ Necessary Environment Variables

| Variable | Description | Required |
| :--- | :--- | :--- |
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org/apps) | **Yes** |
| `API_HASH` | Telegram API HASH from [my.telegram.org](https://my.telegram.org/apps) | **Yes** |
| `BOT_TOKEN` | Bot Token from [@BotFather](https://t.me/BotFather) | **Yes** |
| `OWNER_ID` | Telegram User ID of the owner | **Yes** |
| `MONGO_DB_URI` | MongoDB Connection URL (from [MongoDB Atlas](https://cloud.mongodb.com)) | No |
| `MUST_JOIN` | Channel username/invite link for mandatory subscription | No |
| `PORT` | Web port for Koyeb health checks (default `8000`) | No |

---

### 🛠️ Self-Hosting / VPS

```bash
git clone https://github.com/amritraj78/STRING-SESSION
cd STRING-SESSION
pip3 install -r requirements.txt
cp sample.env .env
# Edit .env with your credentials
python3 main.py
```
