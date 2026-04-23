# Build stage
FROM node:22-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm audit fix --only=production || true

# Run stage
FROM node:22-alpine

WORKDIR /app

# Install curl for healthcheck
# hadolint ignore=DL3018
RUN apk add --no-cache curl

COPY --from=builder /app/node_modules ./node_modules
COPY . .

RUN chown -R node:node /app
USER node

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

CMD ["node", "app.js"]
