# Deployment Guide for InJoy Beauty

This guide will help you deploy your InJoy Beauty website to Render (free tier).

## Prerequisites

1. A GitHub account with your repository pushed
2. A Render account (sign up at https://render.com - it's free)

## Step-by-Step Deployment

### 1. Push Your Code to GitHub

Make sure all your changes are committed and pushed to your GitHub repository:
- `beckyannm/injoybeauty`

### 2. Sign Up / Log In to Render

1. Go to https://render.com
2. Sign up or log in (you can use your GitHub account)

### 3. Create a New Web Service

1. Click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository: `beckyannm/injoybeauty`

### 4. Configure the Service

Use these settings:

- **Name**: `injoybeauty` (or any name you prefer)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn backend.app:app --bind 0.0.0.0:$PORT`
- **Plan**: Select **Free** (for now)

### 5. Set Environment Variables

In the "Environment Variables" section, click "Add Environment Variable" for each one:

**Important:** Enter the KEY in the left field, and the VALUE in the right field.

1. **Key:** `FLASK_ENV`  
   **Value:** `production`

2. **Key:** `DEBUG`  
   **Value:** `False`

3. **Key:** `SECRET_KEY`  
   **Value:** (Click "Generate" button to create one automatically)

4. **Key:** `RESEND_API_KEY`  
   **Value:** `re_epGa96hn_8nvbJjH9qx5hftfypBsmzRdd`

5. **Key:** `NOTIFICATION_EMAIL`  
   **Value:** `rebeccamayne27@gmail.com`

6. **Key:** `CORS_ORIGINS`  
   **Value:** `https://injoybeauty.ca,https://www.injoybeauty.ca,http://localhost:5000`

### 6. Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying your app
3. This takes about 5-10 minutes the first time
4. You'll get a URL like: `https://injoybeauty.onrender.com`

### 7. Test Your Render URL First

**IMPORTANT:** Before connecting your custom domain, test that your app works on Render's URL:

1. After deployment completes, you'll get a URL like: `https://injoybeauty.onrender.com`
2. **Test this URL first** - make sure the site loads correctly
3. If the Render URL works, then proceed to connect your custom domain

### 8. Connect Your Custom Domain (injoybeauty.ca)

Once your Render URL is working:

1. Go to your service settings in Render
2. Click **"Custom Domains"** in the left sidebar
3. Click **"Add Custom Domain"**
4. Enter: `injoybeauty.ca` (without www)
5. Click **"Add"**
6. Render will show you DNS records to add:
   - **CNAME Record**: 
     - Name: `@` or `injoybeauty.ca`
     - Value: `your-app-name.onrender.com` (your Render URL)
   - **OR A Record** (if CNAME not supported):
     - Render will provide an IP address
7. **Also add www subdomain:**
   - Click **"Add Custom Domain"** again
   - Enter: `www.injoybeauty.ca`
   - Use the same CNAME or A record

### 9. Update DNS Settings

1. Go to where you registered `injoybeauty.ca` (GoDaddy, Namecheap, etc.)
2. Find DNS Management / DNS Settings
3. Add the CNAME or A records that Render provided
4. **Save** the DNS changes

### 10. Wait for SSL Certificate

**Important:** After adding the domain in Render:
- Render automatically provisions an SSL certificate (free)
- This can take **5-30 minutes** after DNS propagates
- You'll see "SSL Certificate" status in Render dashboard
- Wait until it shows "Active" or "Valid"

**Do NOT try to access the site until:**
1. DNS has propagated (check with: https://dnschecker.org)
2. SSL certificate shows as "Active" in Render dashboard

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Make sure `requirements.txt` has all dependencies
- Verify Python version (3.11.0)

### App Crashes
- Check the logs in Render dashboard
- Verify all environment variables are set
- Make sure database initialization works

### SSL Error (ERR_SSL_VERSION_OR_CIPHER_MISMATCH)

This usually means:
1. **SSL certificate not ready yet** - Wait 5-30 minutes after adding domain
2. **DNS not propagated** - Check at https://dnschecker.org
3. **Wrong DNS records** - Verify CNAME/A records match Render's instructions
4. **Domain not added in Render** - Make sure you added it in Custom Domains section

**Steps to fix:**
1. Check Render dashboard → Custom Domains → SSL Certificate status
2. Wait until SSL shows "Active" or "Valid"
3. Try accessing via Render URL first: `https://your-app.onrender.com`
4. If Render URL works but custom domain doesn't, it's a DNS/SSL issue
5. Clear browser cache and try again

### Custom Domain Not Working
- Verify DNS records are correct
- Wait for DNS propagation (check at dnschecker.org)
- Check Render's custom domain status
- Make sure SSL certificate is "Active" in Render dashboard
- Try the Render URL first to confirm app is working

## Free Tier Limitations

- Service may spin down after 15 minutes of inactivity
- First request after spin-down may be slow (cold start)
- 750 hours/month free (enough for always-on if needed)

## Need Help?

Check Render's documentation: https://render.com/docs
