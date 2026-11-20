# 🔥 Firebase Hosting Setup Guide
## Deploy to pmsg.edmhs.us

---

## 📋 Prerequisites

1. **Node.js installed** (check: `node --version`)
2. **npm installed** (check: `npm --version`)
3. **Firebase project created** at https://console.firebase.google.com
4. **Access to edmhs.us DNS settings**

---

## 🚀 Step-by-Step Setup

### Step 1: Install Firebase CLI

```bash
# Install Firebase Tools
npm install -g firebase-tools

# Verify installation
firebase --version
```

### Step 2: Login to Firebase

```bash
# This will open a browser for authentication
firebase login
```

### Step 3: Initialize Firebase in Your Project

```bash
# Navigate to the project
cd ~/chatbots/pain-management-support-group

# Initialize Firebase Hosting
firebase init hosting
```

**When prompted:**
- ✅ Select your Firebase project (or create a new one)
- ✅ What do you want to use as your public directory? → **presentation_export**
- ✅ Configure as a single-page app? → **No**
- ✅ Set up automatic builds? → **No**
- ✅ File already exists. Overwrite? → **No**

### Step 4: Deploy to Firebase

```bash
# Make the deploy script executable
chmod +x deploy_to_firebase.sh

# Deploy!
./deploy_to_firebase.sh
```

**OR deploy manually:**
```bash
firebase deploy --only hosting
```

---

## 🌐 Custom Domain Setup (pmsg.edmhs.us)

### Step 1: Open Firebase Console

1. Go to: https://console.firebase.google.com
2. Select your project
3. Click "Hosting" in the left menu
4. Click "Add custom domain"

### Step 2: Enter Your Domain

Enter: **pmsg.edmhs.us**

### Step 3: Get DNS Records

Firebase will show you DNS records to add. Example:

```
Type: A
Name: pmsg
Value: 151.101.1.195 (Firebase's IP)

Type: A  
Name: pmsg
Value: 151.101.65.195 (Firebase's IP)
```

### Step 4: Update DNS at edmhs.us

Go to your DNS provider (wherever edmhs.us is hosted) and add:

**A Records:**
```
Host: pmsg
Points to: 151.101.1.195
TTL: 3600

Host: pmsg
Points to: 151.101.65.195
TTL: 3600
```

**TXT Record (for verification):**
```
Host: pmsg
Value: (copy from Firebase Console)
TTL: 3600
```

### Step 5: Wait for DNS Propagation

- DNS changes take 5-30 minutes
- Check status: https://dnschecker.org/#A/pmsg.edmhs.us
- Firebase will auto-verify and provision SSL

### Step 6: SSL Certificate (Automatic)

Firebase automatically provisions a free SSL certificate from Let's Encrypt.
Wait 24 hours max for HTTPS to be available.

---

## 📂 What Gets Deployed

```
presentation_export/
├── index.html              ← Homepage
├── documentation/          ← 11 HTML docs
├── visualizations/         ← 6 PNG charts
└── data/                   ← 5 JSON files

Total Size: ~2 MB
```

---

## 🔄 Redeploying Updates

Whenever you update the content:

```bash
# 1. Regenerate export (if needed)
python3 export_for_presentation.py

# 2. Deploy
./deploy_to_firebase.sh
```

**Or manually:**
```bash
firebase deploy --only hosting
```

---

## 🎯 Your URLs

After deployment:

**Firebase Default:**
- https://your-project-id.web.app
- https://your-project-id.firebaseapp.com

**Custom Domain (after DNS setup):**
- https://pmsg.edmhs.us
- https://pmsg.edmhs.us/documentation/simulation_results_report.html
- https://pmsg.edmhs.us/visualizations/01_pain_trajectories.png

---

## 🔒 Security & Performance

The `firebase.json` includes:

✅ **Caching Headers**
- Images: 2 hours
- JS/CSS: 1 hour
- JSON: 5 minutes

✅ **Clean URLs**
- `/about` instead of `/about.html`

✅ **SSL/HTTPS**
- Auto-provisioned
- Free Let's Encrypt certificate

✅ **CDN**
- Global edge network
- Fast loading worldwide

---

## 🛠️ Troubleshooting

### "Firebase command not found"
```bash
npm install -g firebase-tools
```

### "Not logged in"
```bash
firebase login
```

### "Project not initialized"
```bash
firebase init hosting
```

### "DNS not propagating"
- Wait 30 minutes
- Check: https://dnschecker.org
- Clear your browser cache
- Try incognito mode

### "SSL certificate pending"
- Takes up to 24 hours
- Verify DNS records are correct
- Check Firebase Console status

---

## 📊 Firebase Console

**Useful Links:**

- **Hosting Dashboard:** https://console.firebase.google.com/project/YOUR_PROJECT/hosting
- **Custom Domains:** Add/manage domains
- **Usage Stats:** See bandwidth and requests
- **Deployment History:** Rollback if needed

---

## 💡 Advanced: CI/CD Deployment

For automatic deployments from GitHub:

```yaml
# .github/workflows/firebase-deploy.yml
name: Deploy to Firebase

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: w9jds/firebase-action@master
        with:
          args: deploy --only hosting
        env:
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_TOKEN }}
```

Get token:
```bash
firebase login:ci
```

---

## 🎉 After Deployment

Your platform will be accessible at:

**Main Site:**
https://pmsg.edmhs.us

**Share These Links:**

- Student Manual: https://pmsg.edmhs.us/documentation/student_manual___patient_guide.html
- Simulation Results: https://pmsg.edmhs.us/documentation/simulation_results_report.html
- Quick Start: https://pmsg.edmhs.us/documentation/quick_start_guide.html

**For Knowledge Bases:**

Base URL: https://pmsg.edmhs.us/

---

## 📞 Support

**Firebase Documentation:**
https://firebase.google.com/docs/hosting

**Custom Domain Setup:**
https://firebase.google.com/docs/hosting/custom-domain

**DNS Help:**
https://support.google.com/firebase/answer/9021429

---

**🎯 Summary:**

1. Install Firebase CLI: `npm install -g firebase-tools`
2. Login: `firebase login`
3. Initialize: `firebase init hosting`
4. Deploy: `./deploy_to_firebase.sh`
5. Add DNS records for pmsg.edmhs.us
6. Wait for SSL certificate
7. Share: https://pmsg.edmhs.us 🎉

---

*Last Updated: November 2026*
