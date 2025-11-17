# Troubleshooting Guide

Common issues and their solutions for Friend Finder Lite.

## Installation Issues

### npm install fails

**Symptoms**: Errors when running `npm install` in server or client directory

**Solutions**:
1. Check Node.js version: `node -v` (should be v16+)
2. Clear npm cache: `npm cache clean --force`
3. Delete `node_modules` and `package-lock.json`, then retry
4. Try using `npm ci` instead of `npm install`

### Cannot find module errors

**Symptoms**: `Error: Cannot find module 'express'` or similar

**Solution**:
```bash
cd server
npm install express cors dotenv @supabase/supabase-js
cd ../client
npm install react react-dom react-router-dom react-scripts
```

## Connection Issues

### Cannot connect to backend

**Symptoms**: Frontend shows errors, API calls fail

**Checklist**:
1. ✓ Is the backend server running? (`cd server && npm start`)
2. ✓ Is it running on port 5000? (Check terminal output)
3. ✓ Can you access `http://localhost:5000/api/health`?
4. ✓ Check browser console for CORS errors

**Solutions**:
- Ensure backend is running before starting frontend
- Check for port conflicts: `lsof -i :5000` (Mac/Linux) or `netstat -ano | findstr :5000` (Windows)
- Restart both servers

### CORS errors

**Symptoms**: `Access-Control-Allow-Origin` errors in browser console

**Solution**:
Make sure CORS is configured in `server/server.js`:
```javascript
const cors = require('cors');
app.use(cors());
```

If still failing:
```javascript
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));
```

## Database Issues

### Cannot connect to Supabase

**Symptoms**: `Invalid Supabase URL` or connection timeout errors

**Checklist**:
1. ✓ Is `.env` file in the `server` directory?
2. ✓ Are credentials correct? (Check Supabase dashboard)
3. ✓ Is Supabase project active?
4. ✓ Is URL format correct? `https://xxx.supabase.co`

**Solutions**:
1. Verify `.env` file exists: `ls -la server/.env`
2. Check `.env` format:
   ```
   SUPABASE_URL=https://abcdefgh.supabase.co
   SUPABASE_ANON_KEY=eyJ...
   ```
3. Restart server after changing `.env`
4. Test connection with a simple script:
   ```javascript
   const { createClient } = require('@supabase/supabase-js');
   const supabase = createClient('YOUR_URL', 'YOUR_KEY');
   supabase.from('profiles').select('count').then(console.log);
   ```

### Database tables not found

**Symptoms**: `relation "profiles" does not exist`

**Solution**:
Tables should have been created via migration. Verify in Supabase:
1. Go to Supabase Dashboard → SQL Editor
2. Run: `SELECT * FROM information_schema.tables WHERE table_schema = 'public';`
3. Should see: profiles, interests, activities, connections

If tables are missing, check that the migration was applied.

### Foreign key constraint violations

**Symptoms**: `violates foreign key constraint` errors

**Common Causes**:
1. Trying to create interest/activity for non-existent profile
2. Trying to create connection with invalid profile IDs

**Solution**:
Always ensure profile exists before creating related records:
```javascript
// Check profile exists first
const { data: profile } = await supabase
  .from('profiles')
  .select('id')
  .eq('id', profileId)
  .single();

if (!profile) {
  throw new Error('Profile not found');
}
```

## Frontend Issues

### Blank page after starting frontend

**Symptoms**: Page loads but shows nothing

**Checklist**:
1. ✓ Check browser console for errors
2. ✓ Is React app running on correct port? (3000)
3. ✓ Any compile errors in terminal?

**Solutions**:
1. Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. Check for JavaScript errors in console
4. Restart React dev server: `npm start`

### Changes not reflecting

**Symptoms**: Made code changes but nothing updates

**Solutions**:
1. React should auto-reload. Check if server crashed
2. Hard refresh browser
3. Restart dev server
4. Clear browser cache: `Ctrl+Shift+Delete`

### "Proxy error" messages

**Symptoms**: `Could not proxy request /api/profiles`

**Solutions**:
1. Ensure backend is running on port 5000
2. Check `proxy` in `client/package.json` points to `http://localhost:5000`
3. Restart frontend server after backend starts

### React Router not working

**Symptoms**: Clicking links shows blank page or 404

**Solutions**:
1. Check if `BrowserRouter` is wrapping your app
2. Verify routes are defined in `App.js`
3. Check for console errors
4. Make sure React Router is installed: `npm list react-router-dom`

## Runtime Issues

### "Profile not found" errors

**Symptoms**: Trying to view profile shows error

**Causes**:
1. Profile was deleted
2. Invalid profile ID in URL
3. LocalStorage has stale ID

**Solutions**:
1. Clear localStorage: `localStorage.clear()` in browser console
2. Create new profile
3. Check database: `SELECT * FROM profiles WHERE id = 'xxx';`

### Cannot send connection requests

**Symptoms**: Button doesn't work or shows error

**Checklist**:
1. ✓ Do you have a profile created? (Need currentProfileId)
2. ✓ Are you trying to connect with yourself? (Not allowed)
3. ✓ Does connection already exist?

**Solutions**:
1. Create profile first if you don't have one
2. Check browser console for specific error
3. Verify target profile exists
4. Check database for existing connections:
   ```sql
   SELECT * FROM connections
   WHERE sender_id = 'your-id'
   OR receiver_id = 'your-id';
   ```

### Matches page shows no results

**Symptoms**: Matches page is empty

**Causes**:
1. No other profiles in database
2. No shared interests/activities
3. Profile has no interests/activities set

**Solutions**:
1. Create more test profiles with shared interests
2. Run seed script: `node server/seed.js`
3. Add interests to your profile
4. Check database: `SELECT COUNT(*) FROM profiles;`

### Filters not working

**Symptoms**: Filter doesn't return expected results

**Debugging**:
1. Check network tab for API request
2. Verify filter values are being sent
3. Test with single filter first
4. Check backend logs for query

**Solutions**:
1. Ensure backend filter endpoint is working
2. Case sensitivity: filters are case-insensitive
3. Partial matches: "san" should match "San Francisco"
4. Clear filters and try again

## Performance Issues

### Slow page loads

**Symptoms**: Pages take >3 seconds to load

**Solutions**:
1. Check network tab for slow API calls
2. Verify database queries are indexed
3. Check if Supabase project is in same region
4. Reduce number of profiles for testing
5. Enable React production build: `npm run build`

### API timeouts

**Symptoms**: Requests take forever or timeout

**Solutions**:
1. Check Supabase dashboard for database issues
2. Verify network connection
3. Check if too many concurrent requests
4. Add request timeouts in frontend
5. Monitor Supabase performance metrics

## Development Issues

### Hot reload not working

**Symptoms**: Have to manually refresh after code changes

**Solutions**:
1. Check if `npm start` shows "webpack compiled successfully"
2. Disable browser extensions
3. Try different port: `PORT=3001 npm start`
4. Delete `.cache` folder in client directory

### ESLint errors preventing build

**Symptoms**: Build fails due to linting errors

**Solutions**:
1. Fix the errors (recommended)
2. Disable specific rules in `.eslintrc`
3. Temporary: `DISABLE_ESLINT_PLUGIN=true npm start`

### Git issues

**Symptoms**: Cannot commit or push

**Solutions**:
1. Make sure `.gitignore` includes:
   ```
   node_modules/
   .env
   build/
   ```
2. Remove tracked files: `git rm -r --cached node_modules`
3. Force add if needed: `git add -f filename`

## Testing Issues

### Cannot seed database

**Symptoms**: `node server/seed.js` fails

**Solutions**:
1. Check `.env` configuration
2. Verify Supabase connection
3. Check for existing data (might cause conflicts)
4. Clear tables first if needed:
   ```sql
   DELETE FROM connections;
   DELETE FROM activities;
   DELETE FROM interests;
   DELETE FROM profiles;
   ```

### Test profiles not showing

**Symptoms**: Seeded profiles don't appear in UI

**Solutions**:
1. Hard refresh browser
2. Check if seed script completed successfully
3. Verify in Supabase dashboard: `SELECT * FROM profiles;`
4. Check browser console for API errors

## Production Issues

### Build fails

**Symptoms**: `npm run build` shows errors

**Solutions**:
1. Fix all TypeScript/ESLint errors
2. Check for missing dependencies
3. Remove unused imports
4. Verify all environment variables are set

### Deployed app not working

**Symptoms**: Works locally but fails in production

**Checklist**:
1. ✓ Environment variables set in hosting platform?
2. ✓ API URL configured correctly in frontend?
3. ✓ CORS configured for production domain?
4. ✓ HTTPS certificate installed?

**Solutions**:
1. Check hosting platform logs
2. Verify Supabase allows connections from production IP
3. Test API endpoints directly
4. Check browser console on production site

## Getting Help

If you're still stuck:

1. **Check Logs**
   - Backend: Terminal where `npm start` is running
   - Frontend: Browser console (F12)
   - Supabase: Dashboard → Logs

2. **Verify Basics**
   - Node.js version: `node -v`
   - npm version: `npm -v`
   - Dependencies installed: `ls node_modules`

3. **Test Isolation**
   - Test backend alone: `curl http://localhost:5000/api/health`
   - Test database alone: Check Supabase dashboard
   - Test frontend alone: Disable API calls temporarily

4. **Search for Errors**
   - Copy exact error message
   - Search in project issues
   - Google error message
   - Check Stack Overflow

5. **Create Minimal Reproduction**
   - Isolate the problem
   - Create minimal test case
   - Document steps to reproduce

## Useful Commands

### Check what's running on ports
```bash
# Mac/Linux
lsof -i :5000
lsof -i :3000

# Windows
netstat -ano | findstr :5000
netstat -ano | findstr :3000
```

### Kill process on port
```bash
# Mac/Linux
kill -9 $(lsof -t -i:5000)

# Windows
taskkill /PID <PID> /F
```

### Clear all caches
```bash
# npm cache
npm cache clean --force

# Browser cache
# Chrome: Ctrl+Shift+Delete → Clear browsing data

# React cache
rm -rf node_modules/.cache
```

### Reset everything
```bash
# Stop all servers
# Ctrl+C in all terminal windows

# Clean client
cd client
rm -rf node_modules package-lock.json
npm install

# Clean server
cd ../server
rm -rf node_modules package-lock.json
npm install

# Restart
cd ../server && npm start
# In another terminal:
cd client && npm start
```

## Still Having Issues?

1. Check the main README.md
2. Review the QUICKSTART.md
3. Verify all prerequisites are installed
4. Try on a clean system/VM
5. Compare your code with working example
