# Multi-stage Docker build for CloudyMcCodeFace
# Security-first, privacy-focused containerization

# Stage 1: Build the application
FROM golang:1.21-alpine AS builder

# Security: Use specific version and verify checksums
ARG GO_VERSION=1.21
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

# Security: Add security labels for vulnerability scanning
LABEL maintainer="CloudyMcCodeFace Team" \
      org.opencontainers.image.title="CloudyMcCodeFace" \
      org.opencontainers.image.description="Secure AI-Powered Coding Assistant" \
      org.opencontainers.image.version="${VERSION:-dev}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="CloudyMcCodeFace" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/BoozeLee/go-ai-coder" \
      security.scan.enabled="true" \
      security.scan.type="vulnerability"

# Security: Install only essential build dependencies with no-cache
RUN apk add --no-cache --virtual .build-deps \
    git \
    ca-certificates \
    tzdata \
    && rm -rf /var/cache/apk/*

# Security: Create non-root user for build stage
RUN addgroup -g 1001 -S buildgroup && \
    adduser -u 1001 -S builduser -G buildgroup

# Security: Set secure working directory with proper permissions
WORKDIR /build
RUN chown -R builduser:buildgroup /build

# Security: Switch to non-root user for build
USER builduser

# Security: Copy go mod files first for better layer caching
COPY --chown=builduser:buildgroup go.mod go.sum ./

# Security: Download dependencies with checksum verification
RUN go mod download && go mod verify

# Security: Copy source code with proper ownership
COPY --chown=builduser:buildgroup . .

# Security: Build with security flags and optimizations
RUN CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64 \
    go build \
    -ldflags="-w -s -X main.Version=${VERSION:-dev} -X main.BuildTime=${BUILD_DATE} -X main.VCSRef=${VCS_REF}" \
    -trimpath \
    -buildmode=pie \
    -o cloudy-mc-codeface \
    cmd/main.go

# Security: Verify binary was created and is executable
RUN test -f cloudy-mc-codeface && chmod +x cloudy-mc-codeface

# Stage 2: Create minimal, secure runtime image
FROM scratch AS runtime

# Security: Copy only essential files from builder
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /build/cloudy-mc-codeface /app/cloudy-mc-codeface

# Security: Create minimal directory structure
WORKDIR /app

# Security: Create non-root user with specific UID/GID
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Security: Create secure data directory with proper permissions
RUN mkdir -p /app/data /app/config /app/logs && \
    chown -R appuser:appgroup /app && \
    chmod 755 /app && \
    chmod 700 /app/data /app/config /app/logs

# Security: Switch to non-root user
USER appuser

# Security: Set secure environment variables
ENV PATH="/app:${PATH}" \
    HOME="/app" \
    USER="appuser" \
    GOCACHE="/tmp/go-cache" \
    GOMODCACHE="/tmp/go-mod-cache" \
    CGO_ENABLED="0" \
    GOOS="linux" \
    GOARCH="amd64"

# Security: Create secure tmp directory
RUN mkdir -p /tmp/go-cache /tmp/go-mod-cache && \
    chmod 700 /tmp/go-cache /tmp/go-mod-cache

# Security: Set secure file permissions
RUN chmod 755 /app/cloudy-mc-codeface

# Security: Add health check without exposing sensitive information
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["./cloudy-mc-codeface", "--version"] || exit 1

# Security: Use exec form for proper signal handling
ENTRYPOINT ["./cloudy-mc-codeface"]

# Security: Default to help command (no sensitive data exposure)
CMD ["--help"]

# Security: Add security scanning metadata
LABEL security.scan.enabled="true" \
      security.scan.type="vulnerability" \
      security.scan.schedule="daily" \
      security.non-root="true" \
      security.read-only="false" \
      security.privileged="false"