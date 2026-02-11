import json
from typing import Dict, Any, List
from datetime import datetime

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class AsyncMessaging:
    """
    Asynchronous messaging system using Redis
    Enables non-blocking communication between agents
    Messages are queued and processed asynchronously
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """
        Initialize async messaging system
        
        Args:
            redis_url: Redis connection URL
        """
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.from_url(redis_url)
                self.redis_client.ping()  # Test connection
                print("✅ Connected to Redis")
            except Exception as e:
                print(f"❌ Redis connection failed: {e}")
                self.redis_client = None
        else:
            self.redis_client = None
            print("⚠️ Redis not installed. Install with: pip install redis")
    
    def is_available(self) -> bool:
        """Check if Redis is available"""
        return self.redis_client is not None
    
    def send_message_async(
        self, 
        target_agent: str, 
        message: str,
        sender: str = "Agent",
        metadata: Dict[str, Any] = None
    ) -> bool:
        """
        Send message to agent queue (non-blocking)
        
        Args:
            target_agent: Name of target agent
            message: Message content
            sender: Name of sending agent
            metadata: Additional metadata
            
        Returns:
            True if message was queued, False otherwise
        """
        
        if not self.redis_client:
            print("❌ Redis not available")
            return False
        
        message_data = {
            "type": "message",
            "sender": sender,
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        try:
            queue_name = f"agent:{target_agent}:messages"
            self.redis_client.rpush(queue_name, json.dumps(message_data))
            print(f"✅ Message queued for {target_agent}")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def get_messages(self, agent_name: str, max_count: int = None) -> List[Dict]:
        """
        Retrieve all messages queued for agent
        
        Args:
            agent_name: Name of agent
            max_count: Maximum number of messages to retrieve
            
        Returns:
            List of messages
        """
        
        if not self.redis_client:
            return []
        
        messages = []
        queue_name = f"agent:{agent_name}:messages"
        
        try:
            while True:
                if max_count and len(messages) >= max_count:
                    break
                msg = self.redis_client.lpop(queue_name)
                if msg is None:
                    break
                messages.append(json.loads(msg))
            return messages
        except Exception as e:
            print(f"❌ Error retrieving messages: {e}")
            return []
    
    def send_task_async(
        self, 
        target_agent: str, 
        description: str, 
        price: float,
        sender: str = "Agent",
        priority: int = 5
    ) -> bool:
        """
        Queue task for agent (non-blocking)
        
        Args:
            target_agent: Name of target agent
            description: Task description
            price: Task compensation
            sender: Name of sending agent
            priority: Task priority (1-10, higher is more important)
            
        Returns:
            True if task was queued, False otherwise
        """
        
        if not self.redis_client:
            return False
        
        task_data = {
            "type": "task",
            "sender": sender,
            "description": description,
            "price": price,
            "priority": priority,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            queue_name = f"agent:{target_agent}:tasks"
            self.redis_client.rpush(queue_name, json.dumps(task_data))
            print(f"✅ Task queued for {target_agent} (priority: {priority})")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def get_tasks(self, agent_name: str, max_count: int = None) -> List[Dict]:
        """
        Retrieve all tasks queued for agent
        
        Args:
            agent_name: Name of agent
            max_count: Maximum number of tasks to retrieve
            
        Returns:
            List of tasks
        """
        
        if not self.redis_client:
            return []
        
        tasks = []
        queue_name = f"agent:{agent_name}:tasks"
        
        try:
            while True:
                if max_count and len(tasks) >= max_count:
                    break
                task = self.redis_client.lpop(queue_name)
                if task is None:
                    break
                tasks.append(json.loads(task))
            return tasks
        except Exception as e:
            print(f"❌ Error retrieving tasks: {e}")
            return []
    
    def get_queue_length(self, agent_name: str, queue_type: str = "messages") -> int:
        """
        Get number of items in queue
        
        Args:
            agent_name: Name of agent
            queue_type: Either 'messages' or 'tasks'
            
        Returns:
            Number of items in queue
        """
        
        if not self.redis_client:
            return 0
        
        try:
            queue_name = f"agent:{agent_name}:{queue_type}"
            return self.redis_client.llen(queue_name)
        except:
            return 0
    
    def clear_queue(self, agent_name: str, queue_type: str = "messages") -> bool:
        """
        Clear all items from queue
        
        Args:
            agent_name: Name of agent
            queue_type: Either 'messages' or 'tasks'
            
        Returns:
            True if queue was cleared
        """
        
        if not self.redis_client:
            return False
        
        try:
            queue_name = f"agent:{agent_name}:{queue_type}"
            self.redis_client.delete(queue_name)
            print(f"✅ Queue cleared: {queue_name}")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
