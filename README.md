# Codex_OS Layer 1 Foundation

This repository contains the Layer 1 foundation for the Codex_OS project. It includes minimal CLI tools and schemas necessary for symbolic state continuity and anchor management.

## Highlights

- **Anchors:** `harmonic_lock`, `trustform`, `fusion_state`
- **L1 Continuity Protocol:** export, import and verify a state.
- **JSON Schemas:** portable validation for `codex_state` and `anchor`.
- **Minimal CLI:** `check` and `snapshot` commands to verify integrity and export state snapshots.

## Installation

```
git clone https://github.com/Jhayden83/Codex_OS.git
pip install -e .
```

## Usage

To verify the integrity of a state:

```
python -m codex_os check
```

To export a snapshot:

```
python -m codex_os snapshot --out snapshots/l1_state_YYYYMMDDTHHMMSS.json
```

## License

MIT License
