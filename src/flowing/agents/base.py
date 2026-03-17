from abc import ABC, abstractmethod
import requests
import time
from typing import Dict, Any, List
from datetime import datetime
from flowing.observability.tracer import Tracer


class BaseAgent(ABC):
    """
    Enhanced base agent class with improved communication capabilities
    Includes retry logic, message history, and task delegation
    """
    
    def __init__(self, name: str, retry_policy: Dict[str, int] = None):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            retry_policy: Dict with 'max_retries' and 'timeout' keys
        """
        self.name = name
        self.retry_policy = retry_policy or {"max_retries": 3, "timeout": 5}
        self.message_history = []
        self.task_history = []
        self.outgoing_messages = []
        self.creation_time = datetime.now().isoformat()

          # 🔍 Observability
        self.tracer = Tracer()
        self.tracer.log(self.name, "agent_initialized", {
        "retry_policy": self.retry_policy
        })
        
    @abstractmethod
    def on_message(self, message: str):
        """
        Handle incoming message
        
        Args:
            message: Message content
        """
        pass
    
    @abstractmethod
    def on_task(self, description: str, price: float):
        """
        Handle incoming task
        
        Args:
            description: Task description
            price: Task compensation
        """
        pass
    
    def send_message_to_agent(
        self, 
        agent_url: str, 
        message: str
    ) -> Dict[str, Any]:
        """
        Send message to another agent with automatic retries
        
        Args:
            agent_url: URL of target agent
            message: Message to send
            
        Returns:
            Response dictionary with status
        """
        self.tracer.log(self.name, "send_message_attempt", {
        "target": agent_url,
        "message": message
        })
        
        for attempt in range(self.retry_policy["max_retries"]):
            try:
                response = requests.post(
                    f"{agent_url}/receive_message",
                    json={
                      "message": message,
                      "sender": self.name,
                      "trace_id": self.tracer.trace_id
                   },
                    timeout=self.retry_policy["timeout"]
                )
                response.raise_for_status()
                
                self.outgoing_messages.append({
                    "timestamp": datetime.now().isoformat(),
                    "to": agent_url,
                    "message": message,
                    "status": "sent"
                })
                
                print(f"✅ [{self.name}] Message sent to {agent_url}")
                return {"status": "ok", "response": response.json()}
                self.tracer.log(self.name, "message_sent_success", {
                "target": agent_url,
                "response_status": "ok"
                })
            
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout on attempt {attempt + 1}")
            except requests.exceptions.ConnectionError:
                print(f"🔌 Connection error on attempt {attempt + 1}")
            except Exception as e:
                print(f"❌ Error: {e}")
                self.tracer.log(self.name, "message_failed", {
                "target": agent_url,
                "reason": "max_retries_exceeded"
                })
            
            # Exponential backoff
            if attempt < self.retry_policy["max_retries"] - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        
        self.outgoing_messages.append({
            "timestamp": datetime.now().isoformat(),
            "to": agent_url,
            "message": message,
            "status": "failed"
        })
        
        return {"status": "failed", "error": "Max retries exceeded"}
    
    def delegate_task(
        self, 
        agent_url: str, 
        description: str, 
        price: float
    ) -> Dict[str, Any]:
        """
        Delegate task to another agent with automatic retries
        
        Args:
            agent_url: URL of target agent
            description: Task description
            price: Task compensation
            
        Returns:
            Response dictionary with task result
        """
        self.tracer.log(self.name, "task_delegation_attempt", {
        "target": agent_url,
        "description": description,
        "price": price
        })
        
        for attempt in range(self.retry_policy["max_retries"]):
            try:
                response = requests.post(
                    f"{agent_url}/run_task",
                    json={
                        "description": description,
                        "price": price,
                        "sender": self.name
                    },
                    timeout=self.retry_policy["timeout"]
                )
                response.raise_for_status()
                
                self.task_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "to": agent_url,
                    "description": description,
                    "price": price,
                    "status": "delegated",
                    "result": response.json()
                })
                
                print(f"✅ [{self.name}] Task delegated to {agent_url}")
                return response.json()

                self.tracer.log(self.name, "task_delegation_success", {
               "target": agent_url,
               "result": response.json()
               })
            
            except Exception as e:
                print(f"❌ Error on attempt {attempt + 1}: {e}")
                self.tracer.log(self.name, "task_delegation_failed", {
                "target": agent_url
                })
            
            if attempt < self.retry_policy["max_retries"] - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        
        self.task_history.append({
            "timestamp": datetime.now().isoformat(),
            "to": agent_url,
            "description": description,
            "price": price,
            "status": "failed"
        })
        
        return {"status": "failed", "error": "Max retries exceeded"}
    
    def get_message_history(self) -> List[Dict]:
        """Get history of incoming messages"""
        return self.message_history
    
    def get_task_history(self) -> List[Dict]:
        """Get history of delegated tasks"""
        return self.task_history
    
    def get_outgoing_messages(self) -> List[Dict]:
        """Get history of sent messages"""
        return self.outgoing_messages
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent metadata"""
        return {
            "name": self.name,
            "created_at": self.creation_time,
            "messages_sent": len(self.outgoing_messages),
            "tasks_delegated": len(self.task_history),
            "messages_received": len(self.message_history),
            "retry_policy": self.retry_policy
        }
