# === Stage 1: Build the Vite app ===
FROM node:22 AS builder

WORKDIR /app

COPY package.json package-lock.json* yarn.lock* ./
RUN npm install

COPY . .
RUN npm run build

# === Stage 2: Serve with nginx ===
FROM nginx:stable-alpine

# Remove default nginx config
RUN rm -rf /usr/share/nginx/html/*

# Copy built frontend
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
