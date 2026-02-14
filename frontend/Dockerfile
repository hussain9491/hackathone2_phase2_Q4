# FROM node:18-alpine AS builder

# WORKDIR /app

# # Copy package files
# COPY package.json package-lock.json ./

# # Install dependencies
# RUN npm ci --only=production

# # Copy source code
# COPY . .

# # Build the application
# RUN npm run build

# # Production stage
# FROM node:20-alpine AS builder

# WORKDIR /app

# # Copy package files and installed dependencies from builder
# COPY --from=builder /app/package.json ./
# COPY --from=builder /app/node_modules ./node_modules

# # Copy built application
# COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/public ./public

# # Copy necessary source files for runtime
# COPY --from=builder /app/src ./src

# # Expose port
# EXPOSE 3000

# # Health check
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#     CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1

# # Start the application
# CMD ["npm", "start"]


# ---------- BUILD STAGE ----------
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install ALL dependencies (build needs dev deps)
RUN npm ci

# Copy source
COPY . .

# Build Next.js app
RUN npm run build


# ---------- PRODUCTION STAGE ----------
FROM node:20-alpine AS production

WORKDIR /app

# Copy only required files from build stage
COPY --from=build /app/package.json ./
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public

EXPOSE 3000

# Start Next.js
CMD ["npm", "start"]
