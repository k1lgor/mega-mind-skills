#!/usr/bin/env bash
# task.md Backup & Staleness Checker
# Usage: ./scripts/backup-task-state.sh [check|backup]
#
# Prevents the single-point-of-failure documented in Janus analysis Item 1.
# - backup: saves a timestamped snapshot of docs/plans/task.md
# - check: compares current task.md against backup for staleness

set -euo pipefail

TASK_FILE="docs/plans/task.md"
BACKUP_DIR="docs/plans/backups"

mkdir -p "$BACKUP_DIR"

case "${1:-check}" in
  backup)
    if [ ! -f "$TASK_FILE" ]; then
      echo "WARNING: $TASK_FILE does not exist — nothing to back up"
      exit 0
    fi
    TS=$(date +%Y%m%d-%H%M%S)
    cp "$TASK_FILE" "$BACKUP_DIR/task-$TS.md"
    echo "Backed up $TASK_FILE → $BACKUP_DIR/task-$TS.md"
    # Keep only last 20 backups
    ls -t "$BACKUP_DIR"/task-*.md 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null || true
    ;;
  check)
    if [ ! -f "$TASK_FILE" ]; then
      echo "MISSING: $TASK_FILE does not exist — create a stub"
      exit 1
    fi
    LATEST=$(ls -t "$BACKUP_DIR"/task-*.md 2>/dev/null | head -1)
    if [ -z "$LATEST" ]; then
      echo "INFO: No backups yet — create one with '$0 backup'"
      exit 0
    fi
    if ! diff -q "$TASK_FILE" "$LATEST" >/dev/null 2>&1; then
      echo "CHANGED: $TASK_FILE has been modified since last backup ($LATEST)"
    else
      echo "OK: $TASK_FILE matches last backup"
    fi
    ;;
  *)
    echo "Usage: $0 {check|backup}"
    exit 1
    ;;
esac
