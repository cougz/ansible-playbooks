# LXC Ansible Playbooks

This directory contains Ansible roles and playbooks for managing OpenTelemetry Collector and Metrics Exporter on LXC containers.

## Directory Structure

```
lxc/
├── playbooks/               # Playbooks for different deployment scenarios
│   ├── main.yml             # Complete installation playbook
│   ├── install-otel.yml     # OpenTelemetry collector only
│   ├── install-metrics.yml  # Metrics exporter only
│   └── configure-only.yml   # Update configuration without reinstalling
│
├── roles/                   # Role definitions
    ├── common/              # Shared dependencies and setup
    ├── otel-collector/      # OpenTelemetry collector installation and config
    └── metrics-exporter/    # LXC metrics exporter installation and config
```

## Available Playbooks

- **main.yml**: Full installation of both components
- **install-otel.yml**: Install and configure OpenTelemetry collector only
- **install-metrics.yml**: Install and configure metrics exporter only
- **configure-only.yml**: Update configuration without reinstalling

## Usage

### Running from Semaphore

When running from Semaphore, use the playbooks directly with appropriate variables:

```bash
# Full installation
ansible-playbook lxc/playbooks/main.yml

# OpenTelemetry collector only
ansible-playbook lxc/playbooks/install-otel.yml

# Metrics exporter only
ansible-playbook lxc/playbooks/install-metrics.yml

# Update configuration only
ansible-playbook lxc/playbooks/configure-only.yml
```

### Required Variables

For OpenTelemetry collector:
```yaml
otel_endpoint: "your-otel-endpoint:4317"  # OTLP gRPC endpoint (no http:// prefix)
otel_version: "0.126.0"                   # Collector version to install
```

For metrics exporter:
```yaml
metrics_collection_interval: 30  # Seconds between metrics collection
```

## Technical Details

### Python Environment

All Python dependencies are installed in a virtual environment at `/opt/lxc-metrics/venv` to comply with externally managed environment restrictions on modern Debian/Ubuntu systems.

### Service Configuration

Both the OpenTelemetry collector and metrics exporter are configured as systemd services:

- OpenTelemetry collector: `otelcol-contrib.service`
- Metrics exporter: `lxc-metrics-exporter.service`

### Permissions

All services run as the `otelcol` user and group for better security.

### LXC-Specific Features

- Adapted metrics collection for LXC container environments
- Network interface monitoring optimized for LXC networking
- Cgroup-based resource monitoring suitable for containers
- Disk I/O monitoring adapted for container storage