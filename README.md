<p align="center">
  <img src="https://files.catbox.moe/0kpdw9.jpg" alt="StringGen">
</p>

### 🤤 Features

- [»] Supports **Pyrogram v2** & **Pyrogram v1**
- [»] Supports **Telethon**
- [»] Supports String Session generation for **BotFather Bots**
- [»] Fully configured for **Koyeb** (built-in HTTP health check server on `$PORT`)
- [»] Dockerfile ready for Docker & Cloud deployments
- [»] Safe & secure session generation

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
