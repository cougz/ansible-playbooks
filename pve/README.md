# Proxmox VE OpenTelemetry and Metrics Collection

This directory contains a restructured version of the Proxmox OpenTelemetry and metrics collection playbooks.

## Directory Structure

```
pve/
├── playbooks/                    # Ansible playbooks with modular execution support
│   ├── main.yml                  # Main playbook with conditional execution
│   ├── install-otel.yml          # OpenTelemetry-specific playbook
│   ├── install-metrics.yml       # Metrics-specific playbook
│   └── configure-only.yml        # Configuration-only playbook
│
├── roles/                        # Role-based organization
│   ├── common/                   # Common tasks for all components
│   ├── otel-collector/           # OpenTelemetry collector role
│   │   ├── tasks/
│   │   ├── templates/
│   │   ├── defaults/
│   │   └── handlers/
│   └── metrics-exporter/         # Metrics exporter role
│       ├── tasks/
│       ├── templates/
│       ├── defaults/
│       └── handlers/
```

## Usage

### With Semaphore

When setting up a task in Semaphore:

1. Select the appropriate playbook based on your needs:
   - `main.yml` - For full control using extra variables
   - `install-otel.yml` - For OpenTelemetry collector operations
   - `install-metrics.yml` - For metrics exporter operations
   - `configure-only.yml` - For updating configurations only

2. Set extra variables to control execution:
   ```yaml
   # For main.yml
   component_selection: "all"  # Options: "all", "otel", "metrics"
   perform_install: true
   perform_configure: true
   perform_update: false
   
   # For component-specific playbooks
   action_type: "install"  # Options: "install", "configure", "update"
   
   # Required variables
   otel_endpoint: "http://your-otel-endpoint:4317"
   otel_version: "0.126.0"
   metrics_collection_interval: 30
   ```

### Playbook Selection Guide

- **Full Installation**: Use `main.yml` with default variables
- **Update Configuration Only**: Use `configure-only.yml` or `main.yml` with `perform_install: false, perform_configure: true`
- **Update OpenTelemetry**: Use `install-otel.yml` with `action_type: "update"`
- **Update Metrics Exporter**: Use `install-metrics.yml` with `action_type: "update"`

## Components

### OpenTelemetry Collector

The OpenTelemetry collector role installs and configures the OpenTelemetry collector for Proxmox hosts. It includes:

- OpenTelemetry Collector Contrib binary installation
- Systemd service configuration
- OTLP and Prometheus receivers configuration
- Secure system permissions and capabilities

### Metrics Exporter

The metrics exporter role provides:

- A shell script that collects Proxmox-specific metrics (host metrics, ZFS, NVMe temps, etc.)
- A Python Flask application that exposes metrics in Prometheus format
- Systemd service configuration
- Health and status endpoints

## Variables

See the default variables in each role's `defaults/main.yml` file for customization options.
