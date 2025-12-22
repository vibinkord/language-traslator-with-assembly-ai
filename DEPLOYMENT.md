# Deployment Guide

## Option 1: Deploy with Docker

### Prerequisites
- Docker
- Docker Compose

### Steps

1. **Build images:**
```bash
docker-compose build
```

2. **Start services:**
```bash
docker-compose up
```

Services will be available at:
- Frontend: http://localhost:3001
- Backend: http://localhost:5000

---

## Option 2: Deploy to Heroku

### Prerequisites
- Heroku CLI
- GitHub account

### Backend Deployment

1. **Create Heroku app:**
```bash
heroku create your-app-name-api
```

2. **Add buildpack:**
```bash
heroku buildpacks:add heroku/python
```

3. **Set environment variables:**
```bash
heroku config:set ASSEMBLYAI_API_KEY=your_key
```

4. **Deploy:**
```bash
cd Vibin_Translator_1/Code
git push heroku main
```

### Frontend Deployment

1. **Create Heroku app:**
```bash
heroku create your-app-name
```

2. **Add buildpack:**
```bash
heroku buildpacks:add heroku/nodejs
```

3. **Update API URL in frontend:**
```bash
heroku config:set VITE_API_URL=https://your-app-name-api.herokuapp.com
```

4. **Deploy:**
```bash
cd react-translator
git push heroku main
```

---

## Option 3: Deploy to AWS

### EC2 Instance

1. **Launch EC2 instance** (Ubuntu 20.04)

2. **SSH into instance:**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip nodejs npm git
```

4. **Clone repository:**
```bash
git clone https://github.com/vibinkord/language-traslator-with-assembly-ai.git
cd language-traslator-with-assembly-ai
```

5. **Setup backend:**
```bash
cd Vibin_Translator_1/Code
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
```

6. **Setup frontend:**
```bash
cd react-translator
npm install
npm run build
```

7. **Install Nginx:**
```bash
sudo apt install nginx
```

8. **Configure Nginx:**
Create `/etc/nginx/sites-available/translator`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/react-translator/dist;
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:5000/;
    }
}
```

9. **Start services:**
```bash
# Start backend
cd language-traslator-with-assembly-ai/Vibin_Translator_1/Code
nohup python3 main.py > backend.log 2>&1 &

# Restart Nginx
sudo systemctl restart nginx
```

---

## Option 4: Deploy to DigitalOcean

1. **Create Droplet** (Ubuntu 20.04)

2. **Follow AWS EC2 steps above** - process is similar

3. **Use DigitalOcean App Platform** (simpler):
   - Connect GitHub repo
   - Configure services
   - Deploy automatically

---

## Environment Variables for Production

### Backend
```
FLASK_ENV=production
DEBUG=False
ASSEMBLYAI_API_KEY=your_key_here
```

### Frontend
```
VITE_API_URL=https://your-api-domain.com
```

---

## Monitoring & Logging

### View logs
```bash
# Docker
docker-compose logs -f

# Heroku
heroku logs --tail

# AWS/DigitalOcean
tail -f backend.log
```

### Health check endpoint
```bash
curl http://your-domain.com/
```

---

## Performance Tips

1. **Enable GZIP compression** in Nginx
2. **Use CDN** for static assets
3. **Cache translations** in database
4. **Monitor API usage** from AssemblyAI
5. **Set rate limiting** on endpoints

---

## Troubleshooting

### CORS errors in production
- Ensure `FLASK_CORS` is properly configured
- Update allowed origins in `factory.py`

### API key not working
- Verify key in environment variables
- Check AssemblyAI account status

### Frontend not connecting to backend
- Verify `VITE_API_URL` environment variable
- Check CORS headers from backend
- Ensure backend is running

---

## Next Steps

1. Set up CI/CD with GitHub Actions
2. Add SSL certificate (Let's Encrypt)
3. Set up automated backups
4. Monitor performance metrics
5. Plan scaling strategy
