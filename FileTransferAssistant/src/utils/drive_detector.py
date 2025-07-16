import os
import psutil
import win32api
import win32file
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class DriveDetector:
    """Detects and manages external drives on Windows systems."""
    
    def __init__(self):
        """Initialize the drive detector."""
        self._system_drives = self._get_system_drives()
    
    def _get_system_drives(self) -> List[str]:
        """Get a list of system drive letters that should be ignored."""
        system_drives = []
        
        # Get the system drive (usually C:)
        system_drive = os.environ.get('SystemDrive', 'C:')
        system_drives.append(system_drive.upper())
        
        # Get Windows directory drive
        windows_drive = os.environ.get('SystemRoot', 'C:\\Windows')
        if ':' in windows_drive:
            system_drives.append(windows_drive[:2].upper())
        
        # Get program files directories
        for env_var in ['ProgramFiles', 'ProgramFiles(x86)', 'ProgramW6432']:
            if env_var in os.environ:
                path = os.environ[env_var]
                if ':' in path:
                    drive = path[:2].upper()
                    if drive not in system_drives:
                        system_drives.append(drive)
        
        return system_drives
    
    def get_all_drives(self) -> List[Dict]:
        """Get all available drives with their details."""
        drives = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                
                drive_info = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'opts': partition.opts,
                    'total_size': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent_used': usage.percent,
                    'is_system': partition.device[:2].upper() in self._system_drives,
                    'label': self._get_volume_label(partition.device)
                }
                
                drives.append(drive_info)
            except Exception as e:
                print(f"Error getting info for {partition.device}: {e}")
        
        return drives
    
    def get_external_drives(self) -> List[Dict]:
        """Get only external/removable drives."""
        all_drives = self.get_all_drives()
        return [d for d in all_drives if not d['is_system']]
    
    def _get_volume_label(self, drive_letter: str) -> str:
        """Get the volume label of a drive."""
        try:
            if not drive_letter.endswith('\\'):
                drive_letter += '\\'
            volume_name = win32api.GetVolumeInformation(drive_letter)[0]
            return volume_name or 'Local Disk'
        except Exception:
            return 'Removable Disk'
    
    def get_drive_from_path(self, path: str) -> Optional[Dict]:
        """Get drive information for a given path."""
        try:
            path = os.path.abspath(path)
            drive_letter = path[:2].upper()
            
            for drive in self.get_all_drives():
                if drive['device'].upper().startswith(drive_letter):
                    return drive
        except Exception as e:
            print(f"Error getting drive for path {path}: {e}")
        
        return None
    
    def get_available_space(self, path: str) -> Optional[int]:
        """Get available space in bytes for the drive containing the given path."""
        try:
            usage = psutil.disk_usage(os.path.abspath(path))
            return usage.free
        except Exception as e:
            print(f"Error getting available space for {path}: {e}")
            return None
    
    def is_removable(self, drive_letter: str) -> bool:
        """Check if a drive is removable."""
        try:
            if not drive_letter.endswith('\\'):
                drive_letter += '\\'
            return win32file.GetDriveType(drive_letter) == win32file.DRIVE_REMOVABLE
        except Exception:
            return False
    
    def get_best_destination_drive(self) -> Optional[Dict]:
        """Get the best external drive to use as a destination."""
        external_drives = self.get_external_drives()
        
        if not external_drives:
            return None
        
        # Sort by free space (descending)
        external_drives.sort(key=lambda x: x['free'], reverse=True)
        return external_drives[0]
