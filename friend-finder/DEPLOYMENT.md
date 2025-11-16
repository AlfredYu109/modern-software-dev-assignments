# Deployment Guide

This guide covers deploying Friend Finder Lite to production.

## Prerequisites

- Supabase project (production instance)
- Git repository
- Domain name (optional but recommended)

## Option 1: Deploy to Render (Recommended)

Render offers free tier hosting for both frontend and backend.

### Backend Deployment

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**
   - Connect your GitHub repository
   - Root directory: `server`
   - Build command: `npm install`
   - Start command: `npm start`

3. **Add Environment Variables**
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_ANON_KEY`: Your Supabase anon key

4. **Deploy**
   - Render will automatically build and deploy
   - Note your backend URL (e.g., `https://friend-finder-api.onrender.com`)

### Frontend Deployment

1. **Update API URL**
   - In `client/package.json`, update or remove the proxy
   - Create `client/.env.production`:
     ```
     REACT_APP_API_URL=https://your-backend-url.onrender.com
     ```

2. **Update API calls in components**
   - Replace `/api/` with `${process.env.REACT_APP_API_URL}/api/`
   - Or use a baseURL configuration

3. **Create a Static Site on Render**
   - Root directory: `client`
   - Build command: `npm install && npm run build`
   - Publish directory: `build`

4. **Deploy**
   - Render will build and host your static site

## Option 2: Deploy to Vercel

### Backend (API Routes)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Create `vercel.json` in server directory**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "server.js",
         "use": "@vercel/node"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "server.js"
       }
     ]
   }
   ```

3. **Deploy**
   ```bash
   cd server
   vercel --prod
   ```

4. **Add Environment Variables**
   - In Vercel dashboard, add SUPABASE_URL and SUPABASE_ANON_KEY

### Frontend

1. **Update API URL in client code**

2. **Deploy**
   ```bash
   cd client
   vercel --prod
   ```

## Option 3: Deploy to Railway

1. **Create Railway account** at [railway.app](https://railway.app)

2. **Deploy Backend**
   - New Project → Deploy from GitHub
   - Select your repository
   - Root directory: `server`
   - Add environment variables

3. **Deploy Frontend**
   - Add new service
   - Root directory: `client`
   - Build command: `npm run build`
   - Start command: `npx serve -s build`

## Option 4: Traditional VPS (DigitalOcean, AWS, etc.)

### Setup Server

1. **Install Node.js**
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. **Install PM2**
   ```bash
   sudo npm install -g pm2
   ```

3. **Clone Repository**
   ```bash
   git clone your-repo
   cd friend-finder
   ```

4. **Install Dependencies**
   ```bash
   cd server && npm install
   cd ../client && npm install && npm run build
   ```

5. **Configure Environment**
   ```bash
   cd ../server
   nano .env
   # Add your Supabase credentials
   ```

6. **Start Backend with PM2**
   ```bash
   pm2 start server.js --name friend-finder-api
   pm2 save
   pm2 startup
   ```

7. **Serve Frontend with Nginx**
   ```bash
   sudo apt install nginx
   ```

   Create `/etc/nginx/sites-available/friend-finder`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           root /path/to/friend-finder/client/build;
           try_files $uri /index.html;
       }

       location /api {
           proxy_pass http://localhost:5000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

   Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/friend-finder /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

8. **Setup SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

## Production Checklist

### Security
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS (SSL certificate)
- [ ] Update CORS settings to allow only your frontend domain
- [ ] Consider adding rate limiting
- [ ] Review Supabase RLS policies
- [ ] Add authentication (recommended for production)

### Performance
- [ ] Enable gzip compression
- [ ] Add caching headers
- [ ] Optimize images (if added later)
- [ ] Consider CDN for static assets
- [ ] Monitor API response times

### Monitoring
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Monitor server uptime
- [ ] Track API usage and performance
- [ ] Set up backup strategy for database

### Backend CORS Configuration

Update `server/server.js` for production:

```javascript
const allowedOrigins = [
  'http://localhost:3000',
  'https://yourdomain.com',
  'https://www.yourdomain.com'
];

app.use(cors({
  origin: function(origin, callback) {
    if (!origin || allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));
```

## Environment Variables

### Backend (.env)
```
PORT=5000
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
NODE_ENV=production
```

### Frontend (.env.production)
```
REACT_APP_API_URL=https://your-api-domain.com
```

## Post-Deployment

1. **Test all features**
   - Create profile
   - Browse profiles
   - Send connection request
   - Filter functionality
   - Matching algorithm

2. **Monitor logs**
   - Check for errors
   - Verify database connections
   - Monitor response times

3. **Setup monitoring**
   - Uptime monitoring (e.g., UptimeRobot)
   - Error tracking (e.g., Sentry)
   - Analytics (optional)

## Rollback Strategy

If deployment fails:

1. **Revert to previous version**
   ```bash
   git revert HEAD
   git push
   ```

2. **Check logs**
   - Server logs
   - Database logs
   - Browser console

3. **Common issues**
   - Environment variables not set
   - CORS misconfiguration
   - Database connection timeout
   - Build errors

## Scaling Considerations

As your app grows:

1. **Database**
   - Upgrade Supabase plan if needed
   - Add database indexes for performance
   - Consider read replicas

2. **Backend**
   - Use load balancer for multiple instances
   - Implement caching (Redis)
   - Optimize database queries

3. **Frontend**
   - Use CDN for static assets
   - Implement code splitting
   - Add service workers for offline support

## Cost Estimates

### Free Tier (Getting Started)
- Supabase: Free up to 500MB database
- Render: Free tier (sleeps after inactivity)
- Vercel: Free tier (100GB bandwidth)
- **Total: $0/month**

### Small Scale (100-1000 users)
- Supabase: $25/month (Pro plan)
- Render: $7-14/month (Starter tier)
- Domain: $12/year
- **Total: ~$35-40/month**

### Medium Scale (1000+ users)
- Supabase: $25-100/month
- Render/Railway: $20-50/month
- CDN: $5-20/month
- **Total: ~$50-170/month**

## Support

For deployment issues:
- Check the main README.md
- Review server logs
- Verify environment variables
- Test locally first
- Check Supabase dashboard for database issues

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [PM2 Documentation](https://pm2.keymetrics.io/docs/usage/quick-start/)
- [Nginx Documentation](https://nginx.org/en/docs/)
