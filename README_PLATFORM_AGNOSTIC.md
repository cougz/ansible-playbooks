# Platform-Agnostic Ansible Playbooks

This repository has been restructured to be platform-agnostic, allowing you to deploy to any host regardless of whether it's a PVE host, LXC container, VM, or bare metal server.

## Structure

```
ansible-playbooks/
├── main.yml                 # Main playbook with host selection
├── inventory/              # Inventory files (if needed)
├── roles/                  # Platform-agnostic roles
│   ├── common/            # Common setup tasks
│   └── fastapi-metrics-exporter/  # Metrics exporter role
└── legacy/                # Previous platform-specific playbooks
    ├── lxc/
    └── pve/
```

## Usage with Semaphore UI

### Survey Variables

1. **target_hosts** (required)
   - Type: Text
   - Default: `all`
   - Description: Specify which hosts to target
   - Examples:
     - `all` - All hosts in inventory
     - `lxc` - All LXC containers (if grouped)
     - `pve` - All PVE hosts (if grouped)
     - `t-*.home.seiffert.me` - Pattern matching
     - `host1.example.com,host2.example.com` - Specific hosts

2. **action_type** (required)
   - Type: Choice
   - Options:
     - `install` - Install the component
     - `update` - Update configuration
     - `uninstall` - Remove the component

3. **component_selection** (required)
   - Type: Choice
   - Options:
     - `metrics-exporter` - FastAPI Metrics Exporter

4. **force_removal** (optional)
   - Type: Boolean
   - Default: `false`
   - Description: Remove otelcol user/group during uninstall

### Example Scenarios

#### Install metrics-exporter on all LXC containers:
- `target_hosts`: `lxc`
- `action_type`: `install`
- `component_selection`: `metrics-exporter`

#### Install on specific hosts:
- `target_hosts`: `host1.example.com,host2.example.com`
- `action_type`: `install`
- `component_selection`: `metrics-exporter`

#### Install on hosts matching pattern:
- `target_hosts`: `t-*.home.seiffert.me`
- `action_type`: `install`
- `component_selection`: `metrics-exporter`

#### Uninstall from all hosts:
- `target_hosts`: `all`
- `action_type`: `uninstall`
- `component_selection`: `metrics-exporter`
- `force_removal`: `true`

## Platform Support

The playbooks automatically detect the platform and adjust accordingly:
- Debian/Ubuntu
- RedHat/CentOS/Fedora
- Alpine Linux
- Any systemd-based Linux distribution