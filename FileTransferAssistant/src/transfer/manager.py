import os
import shutil
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Callable
from datetime import datetime
import threading
import queue

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_transfer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TransferItem:
    """Represents a file or directory to be transferred."""
    
    def __init__(self, source_path: str, destination_path: str, is_dir: bool = False):
        self.source_path = source_path
        self.destination_path = destination_path
        self.is_dir = is_dir
        self.status = 'pending'  # pending, transferring, completed, failed, skipped
        self.bytes_transferred = 0
        self.total_bytes = 0
        self.error = None
        self.start_time = None
        self.end_time = None
    
    def start_transfer(self):
        """Mark the transfer as started."""
        self.status = 'transferring'
        self.start_time = datetime.now()
    
    def complete(self, bytes_transferred: int = None):
        """Mark the transfer as completed."""
        self.status = 'completed'
        self.end_time = datetime.now()
        if bytes_transferred is not None:
            self.bytes_transferred = bytes_transferred
    
    def fail(self, error: str):
        """Mark the transfer as failed."""
        self.status = 'failed'
        self.error = error
        self.end_time = datetime.now()
    
    def skip(self, reason: str = None):
        """Mark the transfer as skipped."""
        self.status = 'skipped'
        if reason:
            self.error = reason
        self.end_time = datetime.now()
    
    @property
    def duration(self) -> float:
        """Get the duration of the transfer in seconds."""
        if not self.start_time or not self.end_time:
            return 0
        return (self.end_time - self.start_time).total_seconds()
    
    @property
    def speed(self) -> float:
        """Get the transfer speed in bytes per second."""
        if not self.duration or self.bytes_transferred == 0:
            return 0
        return self.bytes_transferred / self.duration


class TransferManager:
    """Manages file transfer operations with support for queuing and progress tracking."""
    
    def __init__(self, config=None):
        """Initialize the transfer manager.
        
        Args:
            config: Optional configuration dictionary.
        """
        self.config = config or {}
        self.queue = queue.Queue()
        self.active_transfers = {}
        self.completed_transfers = []
        self.failed_transfers = []
        self._stop_event = threading.Event()
        self._worker_thread = None
        self._callbacks = {
            'progress': [],
            'complete': [],
            'error': [],
            'start': [],
            'cancel': []
        }
    
    def add_callback(self, event_type: str, callback: Callable):
        """Add a callback function for transfer events.
        
        Args:
            event_type: One of 'progress', 'complete', 'error', 'start', 'cancel'.
            callback: Function to call when the event occurs.
        """
        if event_type in self._callbacks:
            self._callbacks[event_type].append(callback)
    
    def _notify(self, event_type: str, *args, **kwargs):
        """Notify all registered callbacks of an event."""
        for callback in self._callbacks.get(event_type, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {event_type} callback: {e}")
    
    def add_transfer(self, source_path: str, destination_path: str, is_dir: bool = False) -> str:
        """Add a file or directory to the transfer queue.
        
        Args:
            source_path: Path to the source file or directory.
            destination_path: Destination path.
            is_dir: Whether the source is a directory.
            
        Returns:
            A unique transfer ID.
        """
        transfer = TransferItem(source_path, destination_path, is_dir)
        transfer_id = str(id(transfer))
        self.queue.put((transfer_id, transfer))
        self.active_transfers[transfer_id] = transfer
        return transfer_id
    
    def start(self):
        """Start processing the transfer queue in a background thread."""
        if self._worker_thread and self._worker_thread.is_alive():
            return
            
        self._stop_event.clear()
        self._worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self._worker_thread.start()
    
    def stop(self):
        """Stop the transfer process."""
        self._stop_event.set()
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
    
    def _process_queue(self):
        """Process items in the transfer queue."""
        while not self._stop_event.is_set() and not self.queue.empty():
            try:
                transfer_id, transfer = self.queue.get_nowait()
                
                # Notify start
                self._notify('start', transfer_id, transfer)
                
                try:
                    if transfer.is_dir:
                        self._transfer_directory(transfer_id, transfer)
                    else:
                        self._transfer_file(transfer_id, transfer)
                    
                    if transfer.status == 'completed':
                        self.completed_transfers.append(transfer)
                    elif transfer.status == 'failed':
                        self.failed_transfers.append(transfer)
                    
                    # Notify completion
                    self._notify('complete', transfer_id, transfer)
                    
                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"Error during transfer: {error_msg}")
                    transfer.fail(error_msg)
                    self.failed_transfers.append(transfer)
                    self._notify('error', transfer_id, transfer, error_msg)
                
                # Remove from active transfers
                self.active_transfers.pop(transfer_id, None)
                
            except queue.Empty:
                break
    
    def _transfer_file(self, transfer_id: str, transfer: TransferItem):
        """Transfer a single file."""
        source = Path(transfer.source_path)
        dest = Path(transfer.destination_path)
        
        # Ensure destination directory exists
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if destination file exists
        if dest.exists():
            # TODO: Implement overwrite policy based on config
            transfer.skip("File already exists")
            return
        
        # Start transfer
        transfer.start_transfer()
        
        try:
            # Copy file with progress callback
            def copy_with_progress(src, dst, buffer_size=1024*1024):
                """Copy file with progress reporting."""
                with open(src, 'rb') as fsrc:
                    with open(dst, 'wb') as fdst:
                        while True:
                            if self._stop_event.is_set():
                                raise InterruptedError("Transfer cancelled")
                                
                            buf = fsrc.read(buffer_size)
                            if not buf:
                                break
                                
                            fdst.write(buf)
                            transfer.bytes_transferred += len(buf)
                            
                            # Notify progress
                            self._notify('progress', transfer_id, transfer)
                
                # Verify file size
                if os.path.getsize(src) != os.path.getsize(dst):
                    raise IOError("File size mismatch after copy")
                
                # Verify checksum if enabled
                if self.config.get('verify_checksum', False):
                    if self._calculate_checksum(src) != self._calculate_checksum(dst):
                        raise IOError("Checksum verification failed")
            
            # Perform the copy
            copy_with_progress(transfer.source_path, transfer.destination_path)
            
            # Update file permissions
            shutil.copymode(transfer.source_path, transfer.destination_path)
            
            # Mark as completed
            transfer.complete(os.path.getsize(transfer.source_path))
            
        except Exception as e:
            # Clean up partially transferred file
            if os.path.exists(transfer.destination_path):
                try:
                    os.remove(transfer.destination_path)
                except:
                    pass
            raise
    
    def _transfer_directory(self, transfer_id: str, transfer: TransferItem):
        """Transfer a directory recursively."""
        source = Path(transfer.source_path)
        dest = Path(transfer.destination_path)
        
        # Create destination directory
        try:
            dest.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise IOError(f"Failed to create directory {dest}: {e}")
        
        # Start transfer
        transfer.start_transfer()
        
        try:
            # Walk through source directory
            for root, dirs, files in os.walk(source):
                if self._stop_event.is_set():
                    raise InterruptedError("Transfer cancelled")
                
                # Create directories
                rel_path = os.path.relpath(root, source)
                dest_dir = dest / rel_path
                
                # Skip directories that already exist
                if not dest_dir.exists():
                    try:
                        dest_dir.mkdir(exist_ok=True)
                    except OSError as e:
                        logger.warning(f"Failed to create directory {dest_dir}: {e}")
                        continue
                
                # Copy files
                for file in files:
                    if self._stop_event.is_set():
                        raise InterruptedError("Transfer cancelled")
                    
                    src_file = Path(root) / file
                    dst_file = dest_dir / file
                    
                    # Skip existing files
                    if dst_file.exists():
                        continue
                    
                    try:
                        # Copy file
                        shutil.copy2(str(src_file), str(dst_file))
                        
                        # Update progress
                        file_size = src_file.stat().st_size
                        transfer.bytes_transferred += file_size
                        
                        # Notify progress
                        self._notify('progress', transfer_id, transfer)
                        
                    except Exception as e:
                        logger.warning(f"Failed to copy {src_file}: {e}")
                        continue
            
            # Mark as completed
            transfer.complete()
            
        except Exception as e:
            # Clean up partially transferred directory
            if dest.exists():
                try:
                    shutil.rmtree(dest)
                except:
                    pass
            raise
    
    @staticmethod
    def _calculate_checksum(file_path: str, block_size: int = 65536) -> str:
        """Calculate SHA-256 checksum of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()
    
    def get_transfer_status(self, transfer_id: str) -> Optional[Dict]:
        """Get the status of a transfer."""
        transfer = self.active_transfers.get(transfer_id)
        if not transfer:
            return None
        
        return {
            'id': transfer_id,
            'source': transfer.source_path,
            'destination': transfer.destination_path,
            'status': transfer.status,
            'bytes_transferred': transfer.bytes_transferred,
            'total_bytes': transfer.total_bytes or os.path.getsize(transfer.source_path) if not transfer.is_dir else 0,
            'progress': transfer.bytes_transferred / (transfer.total_bytes or 1) if transfer.total_bytes else 0,
            'speed': transfer.speed,
            'error': transfer.error
        }
    
    def get_overall_progress(self) -> Dict:
        """Get overall progress of all transfers."""
        total = self.queue.qsize() + len(self.active_transfers) + len(self.completed_transfers) + len(self.failed_transfers)
        completed = len(self.completed_transfers)
        failed = len(self.failed_transfers)
        active = len(self.active_transfers)
        
        return {
            'total': total,
            'completed': completed,
            'failed': failed,
            'active': active,
            'queued': self.queue.qsize(),
            'progress': (completed / total) * 100 if total > 0 else 0
        }
