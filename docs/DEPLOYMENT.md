# 🚀 IDentix Deployment Guide

This guide describes how to deploy the IDentix Attendance Management System to a production-like environment.

## 📋 Prerequisites

- **Server**: A Linux server (Ubuntu 22.04 LTS recommended)
- **Domain**: A domain name pointing to your server
- **Dependencies**: Python 3.8+, Node.js 16+, Nginx, Gunicorn

---

## 🔧 Backend Deployment

1. **Clone Repository**:
   ```bash
   git clone https://github.com/A7med580/IDentix.git
   cd IDentix
   ```

2. **Setup Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

3. **Database & Features**:
   Ensure `data/database.json` and `data/features/` are present.
   *Note: In production, you might want to switch `database_manager.py` to use PostgreSQL instead of JSON.*

4. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5001 server:app
   ```

---

## 🎨 Frontend Deployment

1. **Build React App**:
   ```bash
   cd frontend
   npm install
   npm run build
   ```
   This generates static files in `frontend/dist`.

2. **Serve with Nginx**:
   Configure Nginx to serve `frontend/dist` and proxy API requests to Gunicorn.

   Example `/etc/nginx/sites-available/identix`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       root /path/to/IDentix/frontend/dist;
       index index.html;

       location / {
           try_files $uri $uri/ /index.html;
       }

       location /api {
           proxy_pass http://localhost:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

---

## 🔒 Security Best Practices

1. **HTTPS**: Use Let's Encrypt (Certbot) to enable SSL.
2. **Environment Variables**: Store sensitive keys in `.env`.
3. **Firewall**: Enable UFW, allow ports 80, 443, and SSH (22).
4. **CORS**: Update `flask_cors` origin to your specific domain.

---

## 🐋 Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN cd frontend && npm install && npm run build

EXPOSE 5001
CMD ["gunicorn", "-b", "0.0.0.0:5001", "server:app"]
```
