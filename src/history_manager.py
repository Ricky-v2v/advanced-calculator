from collections import deque
import json
from pathlib import Path

class HistoryManager:
    """历史记录管理器类
    
    功能：
    1. 内存中保存最近的计算记录
    2. 将历史记录持久化到文件
    3. 从文件加载历史记录
    4. 支持获取最近的记录
    """
    
    def __init__(self, max_memory_size=100):
        """初始化历史记录管理器
        
        Args:
            max_memory_size (int): 内存中保存的最大记录数
        """
        self.memory_history = deque(maxlen=max_memory_size)
        self.history_file = Path.home() / '.calculator_history.json'
        self._load_history()
    
    def add_record(self, record):
        """添加新的记录
        
        Args:
            record (str): 要添加的记录
        """
        self.memory_history.append(record)
        self._save_history()
    
    def get_recent_history(self, count=None):
        """获取最近的历史记录
        
        Args:
            count (int, optional): 要获取的记录数量。默认为None，表示获取所有记录。
        
        Returns:
            list: 历史记录列表
        """
        if count is None:
            return list(self.memory_history)
        return list(self.memory_history)[-count:]
    
    def _save_history(self):
        """将历史记录保存到文件"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.memory_history), f, ensure_ascii=False, indent=2)
        except Exception:
            # 保存失败时不抛出异常，只是静默失败
            pass
    
    def _load_history(self):
        """从文件加载历史记录"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    records = json.load(f)
                    self.memory_history.extend(records)
        except Exception:
            # 加载失败时不抛出异常，使用空的历史记录
            pass