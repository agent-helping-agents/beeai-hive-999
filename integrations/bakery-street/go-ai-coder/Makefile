# CloudyMcCodeFace - Makefile
# Professional build and deployment system

# Variables
APP_NAME := cloudy-mc-codeface
VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo "v1.0.0")
BUILD_TIME := $(shell date -u '+%Y-%m-%d_%H:%M:%S')
GO_VERSION := $(shell go version | awk '{print $$3}')
LDFLAGS := -ldflags "-X main.Version=$(VERSION) -X main.BuildTime=$(BUILD_TIME) -X main.GoVersion=$(GO_VERSION)"

# Build directories
BUILD_DIR := build
DIST_DIR := dist
BIN_DIR := bin

# Default target
.PHONY: all
all: clean build

# Clean build artifacts
.PHONY: clean
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR) $(DIST_DIR) $(BIN_DIR)
	@go clean -cache

# Install dependencies
.PHONY: deps
deps:
	@echo "📦 Installing dependencies..."
	@go mod download
	@go mod tidy

# Run tests
.PHONY: test
test:
	@echo "🧪 Running tests..."
	@go test -v ./...

# Run tests with coverage
.PHONY: test-coverage
test-coverage:
	@echo "📊 Running tests with coverage..."
	@go test -v -coverprofile=coverage.out ./...
	@go tool cover -html=coverage.out -o coverage.html

# Lint code
.PHONY: lint
lint:
	@echo "🔍 Linting code..."
	@golangci-lint run

# Format code
.PHONY: fmt
fmt:
	@echo "✨ Formatting code..."
	@go fmt ./...
	@goimports -w .

# Build the application
.PHONY: build
build: deps
	@echo "🔨 Building $(APP_NAME)..."
	@mkdir -p $(BIN_DIR)
	@go build $(LDFLAGS) -o $(BIN_DIR)/$(APP_NAME) cmd/main.go
	@echo "✅ Build complete: $(BIN_DIR)/$(APP_NAME)"

# Build for multiple platforms
.PHONY: build-all
build-all: deps
	@echo "🌍 Building for multiple platforms..."
	@mkdir -p $(DIST_DIR)
	
	# Linux AMD64
	@GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o $(DIST_DIR)/$(APP_NAME)-linux-amd64 cmd/main.go
	
	# Linux ARM64
	@GOOS=linux GOARCH=arm64 go build $(LDFLAGS) -o $(DIST_DIR)/$(APP_NAME)-linux-arm64 cmd/main.go
	
	# macOS AMD64
	@GOOS=darwin GOARCH=amd64 go build $(LDFLAGS) -o $(DIST_DIR)/$(APP_NAME)-darwin-amd64 cmd/main.go
	
	# macOS ARM64 (Apple Silicon)
	@GOOS=darwin GOARCH=arm64 go build $(LDFLAGS) -o $(DIST_DIR)/$(APP_NAME)-darwin-arm64 cmd/main.go
	
	# Windows AMD64
	@GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o $(DIST_DIR)/$(APP_NAME)-windows-amd64.exe cmd/main.go
	
	@echo "✅ Cross-platform builds complete"

# Install to system
.PHONY: install
install: build
	@echo "📦 Installing $(APP_NAME) to system..."
	@sudo cp $(BIN_DIR)/$(APP_NAME) /usr/local/bin/
	@sudo chmod +x /usr/local/bin/$(APP_NAME)
	@echo "✅ Installation complete"

# Uninstall from system
.PHONY: uninstall
uninstall:
	@echo "🗑️  Uninstalling $(APP_NAME)..."
	@sudo rm -f /usr/local/bin/$(APP_NAME)
	@echo "✅ Uninstallation complete"

# Create desktop entry
.PHONY: desktop-entry
desktop-entry:
	@echo "🖥️  Creating desktop entry..."
	@mkdir -p ~/.local/share/applications
	@echo "[Desktop Entry]" > ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "Version=1.0" >> ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "Type=Application" >> ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "Name=CloudyMcCodeFace" >> ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "Comment=AI-Powered Coding Assistant" >> ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "Exec=/usr/local/bin/cloudy-mc-codeface" >> ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "Icon=terminal" >> ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "Terminal=true" >> ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "Categories=Development;IDE;" >> ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "Keywords=AI;Coding;Go;Development;" >> ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "StartupNotify=true" >> ~/.local/share/applications/cloudy-mc-codeface.desktop
	@echo "✅ Desktop entry created"

# Create systemd service (for background operation)
.PHONY: service
service:
	@echo "⚙️  Creating systemd service..."
	@echo "[Unit]" | sudo tee /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "Description=CloudyMcCodeFace Service" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "After=network.target" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "[Service]" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "Type=simple" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "User=$(USER)" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "WorkingDirectory=$(HOME)/.cloudy-mc-codeface" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "ExecStart=/usr/local/bin/cloudy-mc-codeface --daemon" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "Restart=always" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "RestartSec=5" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "[Install]" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@echo "WantedBy=multi-user.target" | sudo tee -a /etc/systemd/system/cloudy-mc-codeface.service > /dev/null
	@sudo systemctl daemon-reload
	@echo "✅ Systemd service created"

# Run the application
.PHONY: run
run: build
	@echo "🚀 Running $(APP_NAME)..."
	@./$(BIN_DIR)/$(APP_NAME)

# Run with development settings
.PHONY: dev
dev: build
	@echo "🔧 Running in development mode..."
	@./$(BIN_DIR)/$(APP_NAME) --verbose --model llama3.2:3b

# Create release package
.PHONY: release
release: build-all
	@echo "📦 Creating release package..."
	@mkdir -p $(BUILD_DIR)
	@tar -czf $(BUILD_DIR)/$(APP_NAME)-$(VERSION).tar.gz -C $(DIST_DIR) .
	@echo "✅ Release package created: $(BUILD_DIR)/$(APP_NAME)-$(VERSION).tar.gz"

# Security scan
.PHONY: security
security:
	@echo "🔒 Running security scan..."
	@gosec ./...

# Docker security scan
.PHONY: docker-security
docker-security:
	@echo "🔒 Running Docker security scan..."
	@docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
		aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL \
		$(APP_NAME):$(VERSION)
	@docker run --rm -v $(PWD):/workspace \
		aquasec/trivy config --exit-code 1 --severity HIGH,CRITICAL \
		/workspace

# Build secure Docker image
.PHONY: docker-secure
docker-secure:
	@echo "🔒 Building secure Docker image..."
	@docker build \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD) \
		--build-arg VERSION=$(VERSION) \
		--no-cache \
		-t $(APP_NAME):$(VERSION) \
		-t $(APP_NAME):latest \
		.
	@echo "✅ Secure Docker image built"

# Deploy securely
.PHONY: deploy-secure
deploy-secure: docker-secure docker-security
	@echo "🚀 Deploying securely..."
	@docker-compose --profile security up -d
	@echo "✅ Secure deployment complete"

# Generate documentation
.PHONY: docs
docs:
	@echo "📚 Generating documentation..."
	@go doc -all ./... > docs/api.md
	@echo "✅ Documentation generated"

# Docker build
.PHONY: docker
docker:
	@echo "🐳 Building Docker image..."
	@docker build -t $(APP_NAME):$(VERSION) .
	@docker tag $(APP_NAME):$(VERSION) $(APP_NAME):latest
	@echo "✅ Docker image built"

# Show help
.PHONY: help
help:
	@echo "CloudyMcCodeFace - Available targets:"
	@echo ""
	@echo "  build        - Build the application"
	@echo "  build-all    - Build for multiple platforms"
	@echo "  install      - Install to system (/usr/local/bin)"
	@echo "  uninstall    - Remove from system"
	@echo "  desktop-entry- Create desktop application entry"
	@echo "  service      - Create systemd service"
	@echo "  run          - Build and run the application"
	@echo "  dev          - Run in development mode"
	@echo "  test         - Run tests"
	@echo "  test-coverage- Run tests with coverage"
	@echo "  lint         - Lint the code"
	@echo "  fmt          - Format the code"
	@echo "  security     - Run security scan"
	@echo "  docker-security - Run Docker security scan"
	@echo "  docker-secure - Build secure Docker image"
	@echo "  deploy-secure - Deploy securely with security scan"
	@echo "  docs         - Generate documentation"
	@echo "  docker       - Build Docker image"
	@echo "  release      - Create release package"
	@echo "  clean        - Clean build artifacts"
	@echo "  deps         - Install dependencies"
	@echo "  help         - Show this help"
	@echo ""
	@echo "Version: $(VERSION)"
	@echo "Go Version: $(GO_VERSION)"