# Deployment Instructions for Render

## Common Problem: Environment Variables Not Loaded

If you see in the "Debug Info" sidebar values like:
- `DB_HOST: localhost`
- `DB_USER: root`  
- `DB_NAME: agri_data`

This means that environment variables **are NOT configured** on Render.

## Solution: Configure Environment Variables on Render

### Step 1: Access Render Console

1. Go to [render.com](https://render.com) and log in to your account
2. Select the **farm-analytics-dashboard** service
3. Go to the **Environment** section (in the left menu)

### Step 2: Add Environment Variables

Click on **"Add Environment Variable"** and add them one by one:

| Key | Value | Example |
|-----|-------|---------|
| `DB_HOST` | Your MySQL database host | `dpg-xxxxx-a.oregon-postgres.render.com` |
| `DB_PORT` | Database port | `3306` |
| `DB_USER` | Database username | `your_username` |
| `DB_PASSWORD` | Database password | `your_password` |
| `DB_NAME` | Database name | `agri_data` |

**⚠️ IMPORTANT:** 
- After adding each variable, make sure it appears in the list below
- Verify the values are correct (especially `DB_HOST` - it should NOT be `localhost`)
- Click **"Save Changes"** after adding all variables

### Step 3: Restart the Service

1. After adding all variables, go back to the service main page
2. Click **"Manual Deploy"** > **"Deploy latest commit"** to restart the service

### Step 4: Verify

1. Open the dashboard published on Render
2. Check the "Debug Info" sidebar
3. You should see the correct environment variable values (no longer `localhost`, `root`, etc.)

## Important Notes

⚠️ **Security**: Environment variables should NOT be added in the `render.yaml` file because:
- The file is committed to the repository
- Passwords would be exposed publicly

✅ **Best Practice**: Always use the Render Console to configure sensitive variables like passwords and database credentials.

## Troubleshooting

### If data still doesn't load:

1. **Verify database connection**:
   - Check Render logs for any connection errors
   - Verify that the database host is accessible from Render

2. **Verify database tables**:
   - Make sure the `production_data`, `consumption_data`, and `weather_data` tables exist
   - Verify that they contain data

3. **Check logs**:
   - Go to Render > farm-analytics-dashboard > **Logs**
   - Look for any database-related errors

### If you still see "Data not Available" errors:

- Verify that the MySQL database is accessible from Render (not all MySQL providers allow external connections)
- Consider using a Render-managed PostgreSQL database or a cloud MySQL database (e.g., PlanetScale, AWS RDS)

