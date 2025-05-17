# Frontend-Nginx Integration Guide

## Overview
This document explains how Nginx serves as the web server and reverse proxy for the Document Manager UI, handling both static file serving and API request proxying.

## Nginx Configuration

### Basic Structure
```nginx
# Main configuration file: /etc/nginx/nginx.conf
events {
    worker_connections 1024;  # Maximum concurrent connections
}

http {
    # MIME type support
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging configuration
    log_format detailed_log '$remote_addr - $remote_user [$time_local] '
                          '"$request" $status $body_bytes_sent '
                          '"$http_referer" "$http_user_agent" '
                          'Request_time=$request_time '
                          'Upstream_addr=$upstream_addr '
                          'Upstream_response_time=$upstream_response_time';

    error_log /var/log/nginx/error.log debug;
    access_log /var/log/nginx/access.log detailed_log;
}
```

### Server Configuration
```nginx
server {
    listen 80 default_server;
    server_name _;  # Accepts any hostname

    # React App Serving
    location / {
        root /usr/share/nginx/html;  # React build files location
        index index.html;
        try_files $uri $uri/ /index.html;  # SPA support
        
        # Cache control for React app
        add_header Cache-Control "no-cache, no-store, must-revalidate" always;
        expires 0;
    }

    # API Proxy Configuration
    location /api/ {
        proxy_pass http://backend:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # Timeout settings for long-running requests
        proxy_connect_timeout 660s;
        proxy_send_timeout 660s;
        proxy_read_timeout 660s;
        
        # File upload settings
        client_max_body_size 100M;
        proxy_buffering off;
        proxy_request_buffering off;
    }
}
```

## Key Features

### 1. Static File Serving
- Serves React build files from `/usr/share/nginx/html`
- Handles SPA routing through `try_files` directive
- Configures proper caching headers for static assets
- Supports gzip compression for better performance

### 2. API Request Proxying
- Routes `/api/*` requests to Flask backend
- Maintains proper headers for backend communication
- Handles CORS configuration
- Manages file uploads and large requests

### 3. Performance Optimizations
```nginx
# Enable gzip compression
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# Static file caching
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    root /usr/share/nginx/html;
    expires max;
    add_header Cache-Control public;
}
```

### 4. Security Headers
```nginx
# CORS configuration
add_header 'Access-Control-Allow-Origin' 'http://localhost:5002' always;
add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, DELETE, PUT, PATCH';
add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, Cache-Control';
add_header 'Access-Control-Allow-Credentials' 'true';
```

## Deployment Flow

1. **Build Process**
   ```bash
   # Build React application
   cd frontend/doc-manager-ui
   npm run build
   ```

2. **Nginx Setup**
   ```bash
   # Copy build files to nginx serving directory
   cp -r build/* /usr/share/nginx/html/
   
   # Copy nginx configuration
   cp nginx.conf /etc/nginx/nginx.conf
   ```

3. **Start Services**
   ```bash
   # Restart nginx to apply changes
   nginx -s reload
   ```

## Common Issues and Solutions

### 1. CORS Issues
- Ensure proper CORS headers in nginx configuration
- Verify allowed origins match your frontend URL
- Check for preflight request handling

### 2. File Upload Problems
- Verify `client_max_body_size` setting
- Check `proxy_buffering` settings
- Ensure proper timeout configurations

### 3. Static File Caching
- Clear browser cache if files aren't updating
- Verify cache control headers
- Check file permissions in nginx directory

## Monitoring and Logging

### Access Logs
```nginx
# Detailed access logging
access_log /var/log/nginx/access.log detailed_log;
```

### Error Logs
```nginx
# Debug level error logging
error_log /var/log/nginx/error.log debug;
```

## Best Practices

1. **Security**
   - Keep nginx updated
   - Use HTTPS in production
   - Implement rate limiting
   - Configure proper CORS policies

2. **Performance**
   - Enable gzip compression
   - Configure proper caching
   - Optimize worker connections
   - Use appropriate buffer sizes

3. **Maintenance**
   - Regular log rotation
   - Monitor error logs
   - Keep SSL certificates updated
   - Regular configuration review

## Production Considerations

1. **SSL/TLS Configuration**
   - Obtain SSL certificates
   - Configure HTTPS
   - Enable HTTP/2
   - Implement HSTS

2. **Load Balancing**
   - Configure upstream servers
   - Implement health checks
   - Set up failover

3. **Monitoring**
   - Set up log monitoring
   - Configure error alerts
   - Monitor performance metrics
