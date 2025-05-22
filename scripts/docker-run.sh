#!/bin/bash
# MCP Builder - Docker Helper Scripts
# Convenient commands for running MCP server in different modes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_usage() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  build       Build Docker images"
    echo "  dev         Run development server with hot reloading"
    echo "  prod        Run production server"
    echo "  sse         Run SSE transport server (port 8000)"
    echo "  test        Run tests in container"
    echo "  shell       Get shell access to container"
    echo "  clean       Clean up Docker resources"
    echo "  logs        Show container logs"
    echo ""
    echo "Options:"
    echo "  --rebuild   Force rebuild images"
    echo "  --no-cache  Build without cache"
    echo "  --detach    Run in background"
    echo ""
    echo "Examples:"
    echo "  $0 build                    # Build all images"
    echo "  $0 dev                      # Start development server"
    echo "  $0 prod --detach           # Start production server in background"
    echo "  $0 sse                      # Start SSE server on port 8000"
    echo "  $0 test                     # Run tests"
    echo "  $0 shell dev                # Get shell in dev container"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Build Docker images
build_images() {
    local rebuild_flag=""
    local no_cache_flag=""
    
    if [[ "$*" == *"--rebuild"* ]]; then
        rebuild_flag="--no-cache"
        print_info "Rebuilding images from scratch..."
    fi
    
    if [[ "$*" == *"--no-cache"* ]]; then
        no_cache_flag="--no-cache"
        print_info "Building without cache..."
    fi
    
    print_info "Building MCP Builder Docker images..."
    
    # Build production image
    docker build $rebuild_flag $no_cache_flag --target production -t mcp-builder:latest .
    
    # Build development image
    docker build $rebuild_flag $no_cache_flag --target development -t mcp-builder:dev .
    
    print_success "Docker images built successfully!"
}

# Run development server
run_dev() {
    local detach_flag=""
    
    if [[ "$*" == *"--detach"* ]]; then
        detach_flag="-d"
    fi
    
    print_info "Starting MCP Builder development server..."
    print_info "Source code is mounted for hot reloading"
    
    docker-compose --profile development up $detach_flag mcp-server-dev
}

# Run production server
run_prod() {
    local detach_flag=""
    
    if [[ "$*" == *"--detach"* ]]; then
        detach_flag="-d"
    fi
    
    print_info "Starting MCP Builder production server..."
    docker-compose up $detach_flag mcp-server
}

# Run SSE server
run_sse() {
    local detach_flag=""
    
    if [[ "$*" == *"--detach"* ]]; then
        detach_flag="-d"
    fi
    
    print_info "Starting MCP Builder SSE server on port 8000..."
    print_info "Access server at: http://localhost:8000"
    docker-compose up $detach_flag mcp-server-sse
}

# Run tests
run_tests() {
    print_info "Running MCP Builder tests in container..."
    docker-compose --profile testing run --rm mcp-server-test
}

# Get shell access
run_shell() {
    local service="mcp-server"
    
    if [[ "$2" == "dev" ]]; then
        service="mcp-server-dev"
        print_info "Opening shell in development container..."
    else
        print_info "Opening shell in production container..."
    fi
    
    docker-compose exec $service /bin/bash || \
    docker run --rm -it --entrypoint /bin/bash mcp-builder:latest
}

# Show logs
show_logs() {
    local service="mcp-server"
    
    if [[ "$2" == "dev" ]]; then
        service="mcp-server-dev"
    elif [[ "$2" == "sse" ]]; then
        service="mcp-server-sse"
    fi
    
    print_info "Showing logs for $service..."
    docker-compose logs -f $service
}

# Clean up Docker resources
clean_docker() {
    print_warning "Cleaning up MCP Builder Docker resources..."
    
    # Stop and remove containers
    docker-compose down --remove-orphans
    
    # Remove images
    docker rmi mcp-builder:latest mcp-builder:dev 2>/dev/null || true
    
    # Clean up volumes (optional)
    read -p "Remove persistent volumes? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v
        print_info "Volumes removed"
    fi
    
    # Clean up build cache
    docker builder prune -f
    
    print_success "Docker cleanup completed!"
}

# Validate MCP server
validate_server() {
    print_info "Validating MCP server setup..."
    
    # Check if we can build successfully
    if build_images --no-cache; then
        print_success "Docker build validation passed!"
    else
        print_error "Docker build validation failed!"
        exit 1
    fi
    
    # Test container startup
    print_info "Testing container startup..."
    if docker run --rm mcp-builder:latest python -c "import src.server; print('MCP server imports successfully')"; then
        print_success "Container startup validation passed!"
    else
        print_error "Container startup validation failed!"
        exit 1
    fi
    
    print_success "MCP server Docker setup validated successfully!"
}

# Main script logic
main() {
    check_docker
    
    case $1 in
        build)
            build_images "$@"
            ;;
        dev)
            run_dev "$@"
            ;;
        prod)
            run_prod "$@"
            ;;
        sse)
            run_sse "$@"
            ;;
        test)
            run_tests
            ;;
        shell)
            run_shell "$@"
            ;;
        logs)
            show_logs "$@"
            ;;
        clean)
            clean_docker
            ;;
        validate)
            validate_server
            ;;
        help|--help|-h)
            print_usage
            ;;
        *)
            if [[ -z "$1" ]]; then
                print_error "No command specified."
            else
                print_error "Unknown command: $1"
            fi
            echo ""
            print_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"