# 渔业管理系统部署说明

## 开发环境部署

### 系统要求

- Python 3.8+
- pip 20+

### 步骤

1. **克隆项目**

   ```bash
   git clone https://github.com/backqwe/fishery-system.git
   cd fishery-system
   ```

2. **创建并激活虚拟环境**

   ```bash
   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**（可选）

   创建 `.env` 文件：
   ```
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DEV_DATABASE_URL=sqlite:///fishery_dev.db
   ```

5. **初始化数据库**

   ```bash
   python database/init_db.py
   ```

6. **启动应用**

   ```bash
   python app.py
   ```

   应用将在 `http://localhost:5000` 启动。

---

## 生产环境部署

### 使用 Gunicorn + Nginx

1. **安装 Gunicorn**

   ```bash
   pip install gunicorn
   ```

2. **配置环境变量**

   创建 `/etc/fishery-system/.env` 文件：
   ```
   FLASK_ENV=production
   SECRET_KEY=your-strong-secret-key
   DATABASE_URL=postgresql://user:password@localhost/fishery_prod
   CORS_ORIGINS=https://your-domain.com
   ```

3. **启动 Gunicorn**

   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"
   ```

4. **配置 Nginx**

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

5. **设置 Systemd 服务**（自动启动）

   创建 `/etc/systemd/system/fishery-system.service`：
   ```ini
   [Unit]
   Description=Fishery Management System
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/fishery-system
   ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 "app:create_app('production')"
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   sudo systemctl enable fishery-system
   sudo systemctl start fishery-system
   ```

---

## 使用 Docker 部署

1. **创建 Dockerfile**

   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt gunicorn
   COPY . .
   EXPOSE 8000
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app('production')"]
   ```

2. **构建并运行**

   ```bash
   docker build -t fishery-system .
   docker run -d -p 8000:8000 \
     -e FLASK_ENV=production \
     -e SECRET_KEY=your-secret-key \
     -e DATABASE_URL=sqlite:///fishery.db \
     fishery-system
   ```

---

## 数据库迁移

使用 Flask-Migrate 管理数据库迁移：

```bash
# 初始化迁移目录（首次执行）
flask db init

# 生成迁移脚本
flask db migrate -m "描述本次变更"

# 执行迁移
flask db upgrade

# 回滚迁移
flask db downgrade
```

---

## 常见问题

**Q: 启动时提示模块找不到？**

A: 确保已激活虚拟环境并安装了所有依赖：
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Q: 数据库连接失败？**

A: 检查环境变量中的 `DATABASE_URL` 配置是否正确，确保数据库服务已启动。

**Q: 跨域请求被拒绝？**

A: 在 `.env` 文件中设置 `CORS_ORIGINS` 为允许的前端域名。
