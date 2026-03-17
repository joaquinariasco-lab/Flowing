import requests
import time
from typing import Dict, Any

class CommunicationClient:
    """
    Enhanced communication client for agent-to-agent communication
    with automatic retries, exponential backoff, and configurable timeouts
    """
    
    def __init__(self, max_retries=3, timeout=5, backoff_factor=2):
        """
        Initialize communication client
        
        Args:
            max_retries: Maximum number of retry attempts
            timeout: Request timeout in seconds
            backoff_factor: Multiplier for exponential backoff
        """
        self.max_retries = max_retries
        self.timeout = timeout
        self.backoff_factor = backoff_factor
    
    def send_message(
        self, 
        target_url: str, 
        message: str,
        sender_name: str = "Agent"
    ) -> Dict[str, Any]:
        """
        Send a message with automatic retries
        
        Args:
            target_url: URL of the target agent
            message: Message content to send
            sender_name: Name of the sending agent
            
        Returns:
            Dictionary with status and response
        """
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{target_url}/receive_message",
                    json={"message": message, "sender": sender_name},
                    timeout=self.timeout
                )
                response.raise_for_status()
                print(f"✅ [{sender_name}] Message sent to {target_url}")
                return {"status": "ok", "response": response.json()}
            
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout on attempt {attempt + 1}/{self.max_retries}")
            except requests.exceptions.ConnectionError:
                print(f"🔌 Connection error on attempt {attempt + 1}/{self.max_retries}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Wait before retrying (exponential backoff)
            if attempt < self.max_retries - 1:
                wait_time = self.backoff_factor ** attempt
                print(f"⏳ Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
        
        return {"status": "failed", "error": "Max retries exceeded"}
    
    def send_task(
        self, 
        target_url: str, 
        description: str, 
        price: float,
        sender_name: str = "Agent"
    ) -> Dict[str, Any]:
        """
        Send a task with automatic retries
        
        Args:
            target_url: URL of the target agent
            description: Task description
            price: Task compensation
            sender_name: Name of the sending agent
            
        Returns:
            Dictionary with status and response
        """
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{target_url}/run_task",
                    json={
                        "description": description,
                        "price": price,
                        "sender": sender_name
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                print(f"✅ [{sender_name}] Task sent to {target_url}")
                return {"status": "ok", "response": response.json()}
            
            except Exception as e:
                print(f"❌ Error on attempt {attempt + 1}/{self.max_retries}: {e}")
            
            if attempt < self.max_retries - 1:
                wait_time = self.backoff_factor ** attempt
                time.sleep(wait_time)
        
        return {"status": "failed", "error": "Max retries exceeded"}
    
    def health_check(self, target_url: str, timeout: int = 2) -> bool:
        """
        Check if an agent is reachable
        
        Args:
            target_url: URL of the target agent
            timeout: Timeout for health check
            
        Returns:
            True if agent is reachable, False otherwise
        """
        try:
            response = requests.get(
                f"{target_url}/identity",
                timeout=timeout
            )
            return response.status_code == 200
        except:
            return False
