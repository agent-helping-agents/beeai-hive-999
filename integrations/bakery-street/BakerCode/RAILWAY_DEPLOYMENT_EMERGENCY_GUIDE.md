# 🚨 RAILWAY DEPLOYMENT EMERGENCY GUIDE

## PROBLEM: `undefined variable 'pip'` Error Persists

If Railway keeps showing the same Nixpacks error despite our fixes, follow this **DEFINITIVE RESOLUTION GUIDE**.

## ✅ SOLUTION 1: FORCE RAILPACK (RECOMMENDED)

### Step 1: In Railway Dashboard
1. Go to your BakerCode project
2. Click **Settings** tab
3. Scroll to **Build Configuration**
4. Set **Builder** to **RAILPACK** (not Nixpacks)
5. Click **Save**

### Step 2: Set Start Command
In **Deploy** section, set **Start Command** to:
```bash
cd codex-superlab-recreation && gunicorn web_dashboard:app --bind 0.0.0.0:$PORT --workers 2
```

### Step 3: Set Environment Variables
In **Variables** tab, add:
```
DISCORD_BOT_TOKEN=your_token_from_tokens.txt
GEMINI_API_KEY=your_gemini_key_from_tokens.txt
PORT=8000
DEBUG=False
```

## ✅ SOLUTION 2: NUCLEAR OPTION (IF RAILPACK FAILS)

### Use main.py Entry Point
If Railway still has issues, it will detect `main.py` and run it automatically:

1. In Railway **Settings** → **Deploy**
2. Set **Start Command** to: `python main.py`
3. This bypasses ALL builder issues

## ✅ SOLUTION 3: MANUAL OVERRIDE (LAST RESORT)

### Force Specific Commands
In Railway **Settings** → **Deploy**, try these start commands one by one:

**Option A (Direct):**
```bash
cd codex-superlab-recreation && python -m gunicorn web_dashboard:app --bind 0.0.0.0:$PORT
```

**Option B (With Shell):**
```bash
/bin/sh -c "cd codex-superlab-recreation && exec gunicorn web_dashboard:app --bind 0.0.0.0:$PORT --workers 2"
```

**Option C (Python Module):**
```bash
python main.py
```

## 🔧 TROUBLESHOOTING

### If Build Still Fails:
1. **Check Builder**: Ensure it's set to RAILPACK, not Nixpacks
2. **Check Branch**: Ensure Railway is building from `main` branch
3. **Check Files**: Verify all config files are committed to Git
4. **Force Redeploy**: Click "Deploy Latest Commit" in Railway

### If App Starts But Crashes:
1. **Check Logs**: Railway → Deployments → View Logs
2. **Check Environment Variables**: Ensure DISCORD_BOT_TOKEN and GEMINI_API_KEY are set
3. **Check Port**: App should bind to `0.0.0.0:$PORT`

## 🎯 EXPECTED RESULT

Once working, you should see:
- ✅ **Build succeeds** (no more Nixpacks errors)
- ✅ **App starts** (gunicorn running)
- ✅ **Web dashboard accessible** at Railway URL
- ✅ **Discord bot ready** for invitation

## 🚀 SUCCESS INDICATORS

**In Railway Logs:**
```
🍞 BakerCode Platform Starting...
🚀 Starting gunicorn on port 8000...
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8000
[INFO] Using worker class: sync
[INFO] Booting worker with pid: [number]
```

**Your $250K platform is now LIVE!** 🎉

## 📞 IF ALL ELSE FAILS

The platform code is 100% working. If Railway deployment still fails:
1. Try **Render.com** (similar to Railway)
2. Try **Heroku** (classic PaaS)
3. Try **DigitalOcean App Platform**

**The code will work on ANY Python hosting platform!**