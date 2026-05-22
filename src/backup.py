import os
import shutil
import logging
import json
from datetime import datetime
from src.config import AppPaths

logger = logging.getLogger("migration")

class BackupManager:
    """Manages automated backups and rollbacks of migration targets."""
    
    def __init__(self, paths: AppPaths):
        self.paths = paths
        self.backup_dir = os.path.join(paths.new_roaming, "migration_backups")
        
    def create_backup(self) -> str:
        """
        Creates a timestamped backup of every destination path this migration may alter.
        Returns the path to the backup folder.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        current_backup_path = os.path.join(self.backup_dir, timestamp)
        
        # Create backup directory
        os.makedirs(current_backup_path, exist_ok=True)
        logger.info(f"Creating backup at: {current_backup_path}")
        
        manifest = []
        backed_up_count = 0

        for label, src_path in self._backup_targets():
            backup_path = os.path.join(current_backup_path, "snapshot", label)
            entry = {
                "label": label,
                "destination": src_path,
                "existed": os.path.exists(src_path),
                "type": None,
            }

            if os.path.isdir(src_path):
                entry["type"] = "directory"
                try:
                    shutil.copytree(src_path, backup_path)
                    logger.info(f"Backed up directory {src_path} to {backup_path}")
                    backed_up_count += 1
                except Exception as e:
                    logger.error(f"Failed to backup directory {src_path}: {e}")
                    raise e
            elif os.path.isfile(src_path):
                entry["type"] = "file"
                try:
                    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                    shutil.copy2(src_path, backup_path)
                    logger.info(f"Backed up file {src_path} to {backup_path}")
                    backed_up_count += 1
                except Exception as e:
                    logger.error(f"Failed to backup file {src_path}: {e}")
                    raise e
            else:
                logger.debug(f"Path not found for backup: {src_path}")

            manifest.append(entry)

        manifest_path = os.path.join(current_backup_path, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        if backed_up_count == 0:
            logger.info("No active files found to backup. Proceeding with clean migration.")

        return current_backup_path

    def restore_backup(self, backup_folder: str) -> None:
        """Restores files from a specific backup folder."""
        logger.info(f"Restoring backup from: {backup_folder}")

        manifest_path = os.path.join(backup_folder, "manifest.json")
        if not os.path.exists(manifest_path):
            self._restore_legacy_backup(backup_folder)
            return

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        for entry in manifest:
            label = entry["label"]
            dest_path = entry["destination"]
            src_path = os.path.join(backup_folder, "snapshot", label)

            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)
            elif os.path.isfile(dest_path):
                os.remove(dest_path)

            if not entry["existed"]:
                logger.info(f"Removed migration-created path: {dest_path}")
                continue

            try:
                if entry["type"] == "directory":
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copytree(src_path, dest_path)
                    logger.info(f"Restored directory {dest_path}")
                elif entry["type"] == "file":
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(src_path, dest_path)
                    logger.info(f"Restored file {dest_path}")
            except Exception as e:
                logger.error(f"Failed to restore {dest_path}: {e}")
                raise e

    def clean_backups(self) -> None:
        """Deletes the entire migration backups directory to free up space."""
        if os.path.exists(self.backup_dir):
            logger.info(f"Deleting all backups at: {self.backup_dir}")
            shutil.rmtree(self.backup_dir)
            logger.info("Backup directory deleted successfully.")
        else:
            logger.info("No backups found to clean up.")

    def _backup_targets(self):
        """Returns all destination paths that migration code can mutate."""
        return [
            ("settings.json", os.path.join(self.paths.new_roaming, "User", "settings.json")),
            ("state.vscdb", os.path.join(self.paths.new_roaming, "User", "globalStorage", "state.vscdb")),
            ("globalStorage.storage.json", os.path.join(self.paths.new_roaming, "User", "globalStorage", "storage.json")),
            ("Local State", os.path.join(self.paths.new_roaming, "Local State")),
            ("app_storage.json", os.path.join(self.paths.new_roaming, "app_storage.json")),
            ("CachedProfilesData", os.path.join(self.paths.new_roaming, "CachedProfilesData")),
            ("shared_proto_db", os.path.join(self.paths.new_roaming, "shared_proto_db")),
            ("Backups", os.path.join(self.paths.new_roaming, "Backups")),
            ("User.History", os.path.join(self.paths.new_roaming, "User", "History")),
            ("User.workspaceStorage", os.path.join(self.paths.new_roaming, "User", "workspaceStorage")),
            ("User.profiles", os.path.join(self.paths.new_roaming, "User", "profiles")),
            ("extensions", os.path.join(self.paths.new_dot, "extensions")),
            ("gemini", self.paths.new_gemini),
        ]

    def _restore_legacy_backup(self, backup_folder: str) -> None:
        """Restores backups made by earlier versions of the tool."""
        restore_map = [
            ("settings.json", os.path.join(self.paths.new_roaming, "User", "settings.json")),
            ("state.vscdb", os.path.join(self.paths.new_roaming, "User", "globalStorage", "state.vscdb")),
            ("extensions.json", os.path.join(self.paths.new_dot, "extensions", "extensions.json")),
            ("Local State", os.path.join(self.paths.new_roaming, "Local State")),
        ]

        logger.warning("Legacy backup format detected. Restoring critical files only.")
        for name, dest_file in restore_map:
            src_file = os.path.join(backup_folder, name)
            if os.path.exists(src_file):
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                try:
                    shutil.copy2(src_file, dest_file)
                    logger.info(f"Restored {name} to {dest_file}")
                except Exception as e:
                    logger.error(f"Failed to restore {name} to {dest_file}: {e}")
                    raise e
