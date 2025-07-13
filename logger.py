import logging
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    Настраивает и возвращает логгер с указанным именем
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Форматтер для логов
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Хендлер для файла
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Хендлер для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Добавляем хендлеры к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 