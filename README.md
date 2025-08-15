# Ansible Metrics Management Playbooks

This repository contains Ansible playbooks and roles for deploying and managing metrics exporters across different environments.

## Structure

```
ansible-playbooks/
├── main.yml                          # Main orchestration playbook
├── group_vars/
│   └── all.yml                       # Global variable defaults
├── inventory/
│   ├── production/                   # Production environment
│   │   ├── hosts.yml                 # Production inventory
│   │   └── group_vars/               # Production-specific variables
│   └── staging/                      # Staging environment
│       ├── hosts.yml                 # Staging inventory
│       └── group_vars/               # Staging-specific variables
├── host_vars/                        # Host-specific variables
└── roles/
    ├── common/                       # System preparation
    ├── fastapi-metrics-exporter/     # Main exporter installation
    ├── metrics-exporter-uninstall/   # Clean uninstall
    └── metrics-config/               # Configuration and display logic
```

## Roles

### common
System preparation and user/group management for metrics infrastructure.

### fastapi-metrics-exporter  
Installs and configures FastAPI-based metrics exporter with:
- OTLP (OpenTelemetry Protocol) support
- Configurable collectors (memory, CPU, filesystem, network, process)
- Proxmox v9 compatibility (filesystem permission handling)
- Systemd service management

### metrics-exporter-uninstall
Provides clean uninstall functionality with options for user/group removal.

### metrics-config
Handles configuration validation, debug output, and status reporting.

## Usage

### Prerequisites
- Ansible 2.9 or later
- Target hosts with Python 3 installed
- Sudo/root access on target hosts

### Basic Usage

1. **Configure inventory**: Edit `inventory/production/hosts.yml` or create your own inventory
2. **Set variables**: Override defaults in `group_vars/` or `host_vars/`
3. **Run playbook**: Execute with appropriate action and targets

### Semaphore Integration

This playbook is designed for use with Semaphore CI/CD. Required survey variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `action_type` | Choice | - | install/update/reinstall/uninstall |
| `component_selection` | Choice | metrics-exporter | Component to manage |
| `target_hosts` | String | all | Target host group |
| `otlp_endpoint` | String | localhost:4317 | OTLP collector endpoint |
| `force_removal` | Boolean | false | Remove users/groups on uninstall |

### Manual Execution

```bash
# Install on all hosts
ansible-playbook main.yml -e "action_type=install"

# Update Proxmox hosts only  
ansible-playbook main.yml -e "action_type=update target_hosts=proxmox"

# Uninstall with user/group removal
ansible-playbook main.yml -e "action_type=uninstall force_removal=true"

# Use specific environment
ansible-playbook -i inventory/production main.yml -e "action_type=install"
```

## Configuration

### Environment-Specific Settings

Configure different environments by editing files in:
- `inventory/production/group_vars/`
- `inventory/staging/group_vars/`

### Key Variables

```yaml
# OTLP Configuration
otlp_endpoint: "your-collector:4317"
otlp_insecure: "true/false"

# Collection Settings
collection_interval: 30
enabled_collectors: "memory,cpu,filesystem,network,process"
log_level: "INFO"

# Filesystem Exclusions (Proxmox)
filesystem_exclude_paths: "/sys/kernel/debug,/proc/sys/fs/binfmt_misc"
filesystem_exclude_types: "debugfs,binfmt_misc,tmpfs,devtmpfs,sysfs,proc"
```

### Proxmox Compatibility

The playbook includes special handling for Proxmox v9 filesystem permission restrictions:
- Excludes restricted kernel debug paths
- Provides graceful error handling for inaccessible filesystems
- Maintains compatibility with Proxmox v8 and earlier

## Security

- No hardcoded secrets (use Ansible Vault for sensitive data)
- Runs services with dedicated user account (`otelcol`)
- Configurable filesystem access restrictions
- Environment-specific security settings

## Troubleshooting

### Common Issues

1. **Permission errors on Proxmox v9**: Filesystem exclusions are automatically configured
2. **Service startup failures**: Check OTLP endpoint connectivity
3. **Port conflicts**: Default port 9100 can be changed via `metrics_exporter_port`

### Debug Mode

Enable verbose output:
```yaml
show_debug_output: true
show_survey_variables: true
log_level: "DEBUG"
```

## Contributing

1. Follow Ansible best practices
2. Update documentation for any new variables or features
3. Test changes in staging environment before production
4. Use conventional commit messages

## License

MIT License - see LICENSE file for details.