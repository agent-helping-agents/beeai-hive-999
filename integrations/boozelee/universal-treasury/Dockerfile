# Universal Treasury CLI Docker Image
FROM alpine:latest

# Install dependencies
RUN apk add --no-cache ca-certificates

# Set working directory
WORKDIR /app

# Copy binary
COPY treasury /usr/local/bin/treasury

# Make binary executable
RUN chmod +x /usr/local/bin/treasury

# Set entrypoint
ENTRYPOINT ["treasury"]

# Default command
CMD ["--help"]

# Metadata
LABEL maintainer="Universal Treasury <support@universal-treasury.com>"
LABEL version="1.0.0"
LABEL description="Universal Financial Operations CLI"
