# Free demo deployment with Render and Neon

This guide deploys the FastAPI API, Store Manager dashboard, Dispatcher dashboard,
and Waypoint Express web client. Render hosts the application; Neon provides the
PostgreSQL database. This route does not require an Oracle VM.

Free services can sleep when idle and have usage limits. The API may take about
a minute to start after inactivity. Render's free web-service hours are shared
by the workspace; running both the API and Flutter web service continuously can
use them more quickly. This setup is for a demo, not production.

## 1. Push the project to GitHub

Render deploys from a Git repository. Push this project to a GitHub repository
that your Render account can access. Do not push database passwords or local
`.env` files.

## 2. Create the free Neon database

1. Create a project on [Neon](https://neon.tech/).
2. In the project dashboard, open **Connect** and copy the PostgreSQL connection
   string. Prefer the pooled connection string if Neon offers both.
3. Keep the connection string private. In the next steps, change only its
   initial scheme from `postgresql://` (or `postgres://`) to
   `postgresql+psycopg://`. Preserve the rest of the URL, including its
   `sslmode=require` query parameter.

## 3. Deploy the API on Render

1. In [Render](https://dashboard.render.com/), select **New > Web Service** and
   connect the GitHub repository. Name the service `waypoint-api`.
2. Select **Docker** as the runtime, leave the repository root as the root
   directory, and set the Dockerfile path to
   `Backend/apps/api/Dockerfile.render`.
3. Select the **Free** instance plan.
4. Add these environment variables:

   | Key | Value |
   | --- | --- |
   | `DATABASE_URL` | The Neon connection string with the `postgresql+psycopg://` scheme |
   | `SECRET_KEY` | A long, unique random secret; do not reuse the database password |
   | `ENV` | `production` |
   | `DEMO_MODE` | `true` |

5. Set the health check path to `/health` and deploy.
6. When the deployment succeeds, copy the API's public URL from its Render
   dashboard, for example `https://waypoint-api-example.onrender.com`.
   Render assigns the real hostname; use that exact URL below.

The Dockerfile runs database migrations and idempotent demo seeding before
starting the API. The seed credentials are demo credentials; do not use them
for real accounts or real customer data.

## 4. Deploy the Store Manager static site

Create a Render **Static Site** for the same repository and name it
`waypoint-store`:

| Setting | Value |
| --- | --- |
| Root Directory | `apps/web` |
| Build Command | `npm ci && VITE_API_BASE_URL=https://YOUR-API-HOST.onrender.com/api/v1 npm run build` |
| Publish Directory | `dist` |

Replace `YOUR-API-HOST.onrender.com` with the API URL from step 3, without
`https://`. After deployment, copy this site's public URL.

## 5. Deploy the Dispatcher static site

Create another **Static Site** for the same repository and name it
`waypoint-dispatcher`:

| Setting | Value |
| --- | --- |
| Root Directory | `Frontend/dispatcher` |
| Build Command | `npm ci && VITE_API_BASE_URL=https://YOUR-API-HOST.onrender.com/api/v1 npm run build` |
| Publish Directory | `dist` |

Use the API hostname from step 3. After deployment, copy this site's public URL.

## 6. Deploy Waypoint Express for the web

Create a Render **Web Service** using the same repository:

1. Select **Docker** runtime and the **Free** plan.
   Name the service `waypoint-express`.
2. Set the root directory to `Frontend/waypoint_express/waypoint_express`.
3. Use the `Dockerfile` in that directory.
4. Add the build environment variable `API_BASE_URL` with the value
   `https://YOUR-API-HOST.onrender.com/api/v1`, substituting the API hostname
   from step 3.
5. Deploy and copy this service's public URL.

## 7. Allow the deployed client origins

Go to the API service's **Environment** settings. Set `CORS_ORIGINS` to the
three exact HTTPS origins from the deployed sites, separated by commas and
without trailing slashes. For example:

```text
https://your-store-site.onrender.com,https://your-dispatch-site.onrender.com,https://your-express-service.onrender.com
```

Save and redeploy the API. Use the actual URLs shown by Render, which may differ
from the example if a service name is already taken.

## 8. Open the app

Use the public URLs shown on the three client services in the Render dashboard:

- Store Manager: the `waypoint-store` Static Site URL
- Dispatcher: the `waypoint-dispatcher` Static Site URL
- Waypoint Express: the `waypoint-express` Web Service URL

The API health check is available at `https://YOUR-API-HOST.onrender.com/health`.
Free Render services can be slow on their first request after sitting idle.

## Troubleshooting

- **Browser reports a CORS error:** confirm `CORS_ORIGINS` exactly matches all
  deployed client origins and redeploy the API.
- **Client cannot reach the API:** confirm the build command or
  `API_BASE_URL` contains the actual API hostname and `/api/v1`.
- **API fails during startup:** inspect the Render logs for migration, Neon
  connection, or seeding errors. Check that the database URL uses
  `postgresql+psycopg://` and retains `sslmode=require`.
- **Service wakes slowly:** this is expected on Render's free plan after idle
  time.
- **Data safety:** Neon free is suitable for a demo. Back up any data you need
  to keep; do not treat this setup as production storage.
