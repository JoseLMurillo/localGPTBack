import time
import psutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def dynamic_wait_time(base_wait_time=90, max_wait_time=3600):
    """
    Calculate dynamic wait time based on system resource usage.
    
    Args:
    base_wait_time (int): Minimum wait time in seconds
    max_wait_time (int): Maximum wait time in seconds
    """
    try:
        # Get CPU usage percentage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Get memory usage percentage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Calculate scaling factor based on resource usage
        # Higher resource usage leads to longer wait times
        cpu_factor = 1 + (cpu_usage / 100)
        memory_factor = 1 + (memory_usage / 100)
        
        # Calculate wait time
        wait_time = base_wait_time * cpu_factor * memory_factor
        
        # Ensure wait time is within specified bounds
        wait_time = max(base_wait_time, min(wait_time, max_wait_time))
        
        # Log resource usage and calculated wait time
        logger.info(f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}% | Wait Time: {(wait_time/60):.2f} minuts")
        
        time.sleep(wait_time)
    
    except Exception as e:
        logger.error(f"Error calculating wait time: {e}")
        return base_wait_time