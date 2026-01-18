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

In the "Environment Variables" section, add:

- `FLASK_ENV` = `production`
- `DEBUG` = `False`
- `SECRET_KEY` = (Click "Generate" to create one)
- `RESEND_API_KEY` = `re_epGa96hn_8nvbJjH9qx5hftfypBsmzRdd` (your existing key)
- `NOTIFICATION_EMAIL` = `rebeccamayne27@gmail.com`
- `CORS_ORIGINS` = `https://injoybeauty.ca,https://www.injoybeauty.ca,http://localhost:5000`

### 6. Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying your app
3. This takes about 5-10 minutes the first time
4. You'll get a URL like: `https://injoybeauty.onrender.com`

### 7. Connect Your Custom Domain (injoybeauty.ca)

Once deployed:

1. Go to your service settings in Render
2. Click **"Custom Domains"**
3. Add your domain: `injoybeauty.ca`
4. Render will provide DNS records to add:
   - **CNAME**: `injoybeauty.ca` → `your-app.onrender.com`
   - Or **A Record**: Point to Render's IP (if provided)
5. Update your domain's DNS settings (wherever you registered injoybeauty.ca)
6. Wait for DNS propagation (can take up to 48 hours, usually much faster)

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Make sure `requirements.txt` has all dependencies
- Verify Python version (3.11.0)

### App Crashes
- Check the logs in Render dashboard
- Verify all environment variables are set
- Make sure database initialization works

### Custom Domain Not Working
- Verify DNS records are correct
- Wait for DNS propagation
- Check Render's custom domain status

## Free Tier Limitations

- Service may spin down after 15 minutes of inactivity
- First request after spin-down may be slow (cold start)
- 750 hours/month free (enough for always-on if needed)

## Need Help?

Check Render's documentation: https://render.com/docs
