import logging
import os
from pathlib import Path
from typing import Optional


def setup_logger(name: str, log_level: str = "INFO", log_to_file: bool = True) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_to_file:
        try:
            project_root = Path(__file__).parent.parent.parent
            log_dir = project_root / "logs"
            log_dir.mkdir(exist_ok=True)
            
            log_file = log_dir / "ue5_automation.log"
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
