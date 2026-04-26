# StatFlight — PHI Critical Care Transport PWA

Two single-file pediatric and obstetric critical-care reference apps wrapped as an installable Progressive Web App. Works offline once installed on iPhone or Android.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Launcher — picks OB or Peds |
| `ob.html`    | StatFlight OB — maternal & neonatal |
| `peds.html`  | StatFlight Peds — pediatric critical care |
| `manifest.json` | PWA manifest (app name, icons, start URL) |
| `sw.js`      | Service worker — offline cache |
| `icon.svg` / `icon-180.png` / `icon-192.png` / `icon-512.png` | App icons |

---

## Try it locally

Open `index.html` in any modern browser. To test the service worker / install behavior, you need a local HTTP server (browsers won't register a service worker from `file://`):

```bash
cd statflight
python3 -m http.server 8000
# then open http://localhost:8000 in Chrome
```

---

## Deploy to GitHub Pages (free)

This is the fastest way to get it on your phone.

### 1. Initialize git locally

```bash
cd /path/to/statflight
git init
git add .
git commit -m "Initial commit — StatFlight PWA"
git branch -M main
```

### 2. Create a new GitHub repository

Go to https://github.com/new and create a repo (public or private). Name it something like `statflight`. **Do not** add a README or .gitignore on the GitHub side — your local repo already has them.

### 3. Push your code

Replace `YOUR_USERNAME` and `YOUR_REPO` with your actual values:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 4. Enable GitHub Pages

1. Open your repo on GitHub
2. Settings → Pages
3. Under "Build and deployment", set Source to **"Deploy from a branch"**
4. Branch: `main`, Folder: `/ (root)`
5. Click Save
6. Wait ~1-2 minutes for the first deploy
7. GitHub will give you a URL like `https://YOUR_USERNAME.github.io/YOUR_REPO/`

That URL is your live app.

### 5. Install on iPhone

1. Open the URL in **Safari** (must be Safari, not Chrome, for install)
2. Tap the Share button
3. Tap **Add to Home Screen**
4. Confirm. The StatFlight icon will appear on your home screen as a regular app
5. Launch from the home screen — runs full-screen, works offline

### 6. Install on Android

1. Open the URL in **Chrome**
2. Chrome will show an "Install app" banner, OR tap the ⋮ menu → **Install app**
3. The StatFlight icon will appear in your app drawer

---

## Updates

Whenever you change a file:

```bash
git add .
git commit -m "Description of change"
git push
```

GitHub Pages re-deploys automatically. The service worker on each device will pick up the new version on next launch (may need to close and reopen the app once to refresh the cache).

To force a cache rebuild after updates, bump the `CACHE_NAME` constant in `sw.js` (e.g. `'statflight-v2'`).

---

## Custom domain (optional)

If you have a domain, add a `CNAME` file with your domain inside, then point a DNS CNAME record at `YOUR_USERNAME.github.io`. GitHub Pages will serve over HTTPS automatically.

---

## Disclaimer

This is a clinical reference tool, not a medical device. All dosing should be verified against current PHI Health Clinical Care Guidelines and confirmed with medical control. Use at your own clinical discretion.
