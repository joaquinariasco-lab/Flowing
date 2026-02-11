class AutonomousController:
    def run_cycle(self):
        tasks = self.generate_tasks()
        assignments = self.assign(tasks)
        results = self.execute(assignments)
        self.evaluate(results)
        self.update_economy(results)

import json
import time
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime
import requests


class Task:
    """Represents a task to be assigned and executed"""
    
    def __init__(self, task_id: str, description: str, complexity: float, reward: float):
        self.task_id = task_id
        self.description = description
        self.complexity = complexity  # 0.0-1.0
        self.reward = reward
        self.created_at = datetime.now()
        self.status = "pending"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "complexity": self.complexity,
            "reward": self.reward,
            "status": self.status
        }


class AgentAssignment:
    """Represents assignment of a task to an agent"""
    
    def __init__(self, agent_id: str, agent_url: str, task: Task):
        self.agent_id = agent_id
        self.agent_url = agent_url
        self.task = task
        self.assigned_at = datetime.now()
        self.completed_at = None
        self.result = None
        self.success = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "task_id": self.task.task_id,
            "assigned_at": self.assigned_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "success": self.success
        }


class Economy:
    """Manages agent balances and reward distribution"""
    
    def __init__(self):
        self.agent_balances = {}
        self.transaction_history = []
    
    def initialize_agent(self, agent_id: str, initial_balance: float = 100.0):
        """Initialize agent with starting balance"""
        self.agent_balances[agent_id] = initial_balance
        self.transaction_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "initialization",
            "agent_id": agent_id,
            "amount": initial_balance
        })
    
    def add_reward(self, agent_id: str, amount: float, reason: str = "task_completion"):
        """Add reward to agent balance"""
        if agent_id not in self.agent_balances:
            self.initialize_agent(agent_id, 0.0)
        
        self.agent_balances[agent_id] += amount
        self.transaction_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "reward",
            "agent_id": agent_id,
            "amount": amount,
            "reason": reason
        })
    
    def deduct_penalty(self, agent_id: str, amount: float, reason: str = "failed_task"):
        """Deduct penalty from agent balance"""
        if agent_id not in self.agent_balances:
            self.initialize_agent(agent_id, 0.0)
        
        self.agent_balances[agent_id] -= amount
        self.transaction_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "penalty",
            "agent_id": agent_id,
            "amount": amount,
            "reason": reason
        })
    
    def get_balance(self, agent_id: str) -> float:
        """Get agent balance"""
        return self.agent_balances.get(agent_id, 0.0)
    
    def get_all_balances(self) -> Dict[str, float]:
        """Get all agent balances"""
        return self.agent_balances.copy()


class AutonomousController:
    """
    Autonomous controller for multi-agent task management
    Generates tasks, assigns them to agents, executes, evaluates, and updates economy
    """
    
    def __init__(self, agents: Dict[str, str], initial_balance: float = 100.0):
        """Initialize autonomous controller"""
        
        Args:
            agents: Dictionary mapping agent_id to agent_url
            initial_balance: Starting balance for each agent
        """
        self.agents = agents  # {agent_id: agent_url}
        self.economy = Economy()
        self.task_history = []
        self.assignment_history = []
        self.cycle_count = 0
        
        # Initialize economy for all agents
        for agent_id in agents.keys():
            self.economy.initialize_agent(agent_id, initial_balance)
    
    def generate_tasks(self, num_tasks: int = 5) -> List[Task]:
        """Generate random tasks for agents"""
        
        Args:
            num_tasks: Number of tasks to generate
            
        Returns:
            List of Task objects
        """
        tasks = []
        task_descriptions = [
            "Analyze data patterns",
            "Optimize algorithm efficiency",
            "Validate system integrity",
            "Process large dataset",
            "Coordinate with other agents",
            "Generate report summary",
            "Execute benchmark tests",
            "Update system configuration",
            "Monitor performance metrics",
            "Resolve conflicts between agents"
        ]
        
        for i in range(num_tasks):
            task_id = f"task_{self.cycle_count}_{i}"
            description = random.choice(task_descriptions)
            complexity = round(random.uniform(0.1, 1.0), 2)
            reward = round(complexity * 50, 2)  # Reward based on complexity
            
            task = Task(task_id, description, complexity, reward)
            tasks.append(task)
            self.task_history.append(task)
        
        print(f"\n🎯 Generated {num_tasks} tasks")
        return tasks
    
    def assign(self, tasks: List[Task]) -> List[AgentAssignment]:
        """Assign tasks to agents (load balancing strategy)"""
        
        Args:
            tasks: List of tasks to assign
            
        Returns:
            List of AgentAssignment objects
        """
        assignments = []
        agent_ids = list(self.agents.keys())
        
        if not agent_ids:
            print("❌ No agents available for assignment")
            return assignments
        
        for idx, task in enumerate(tasks):
            # Round-robin assignment with consideration for agent load
            agent_id = agent_ids[idx % len(agent_ids)]
            agent_url = self.agents[agent_id]
            
            assignment = AgentAssignment(agent_id, agent_url, task)
            assignments.append(assignment)
            self.assignment_history.append(assignment)
            
            print(f"📋 Assigned task {task.task_id} to {agent_id}")
        
        print(f"✅ Assigned {len(assignments)} tasks")
        return assignments
    
    def execute(self, assignments: List[AgentAssignment]) -> List[AgentAssignment]:
        """Execute tasks by sending them to agents"""
        
        Args:
            assignments: List of AgentAssignment objects
            
        Returns:
            List of completed assignments with results
        """
        results = []
        
        for assignment in assignments:
            try:
                response = requests.post(
                    f"{assignment.agent_url}/run_task",
                    json={
                        "description": assignment.task.description,
                        "price": assignment.task.reward,
                        "sender": "AutonomousController"
                    },
                    timeout=5
                )
                response.raise_for_status()
                
                assignment.result = response.json()
                assignment.success = True
                assignment.completed_at = datetime.now()
                
                print(f"✅ Task {assignment.task.task_id} executed successfully on {assignment.agent_id}")
            
            except requests.exceptions.Timeout:
                print(f"⏱️ Task {assignment.task.task_id} timed out on {assignment.agent_id}")
                assignment.success = False
                assignment.result = {"error": "timeout"}
            
            except requests.exceptions.ConnectionError:
                print(f"🔌 Cannot connect to {assignment.agent_id} at {assignment.agent_url}")
                assignment.success = False
                assignment.result = {"error": "connection_error"}
            
            except Exception as e:
                print(f"❌ Task {assignment.task.task_id} failed: {str(e)}")
                assignment.success = False
                assignment.result = {"error": str(e)}
            
            results.append(assignment)
        
        print(f"\n📊 Execution complete: {sum(1 for r in results if r.success)}/{len(results)} successful")
        return results
    
    def evaluate(self, assignments: List[AgentAssignment]) -> Dict[str, Any]:
        """Evaluate task execution results"""
        
        Args:
            assignments: List of completed assignments
            
        Returns:
            Evaluation summary
        """
        total_tasks = len(assignments)
        successful_tasks = sum(1 for a in assignments if a.success)
        failed_tasks = total_tasks - successful_tasks
        success_rate = (successful_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        evaluation = {
            "total_tasks": total_tasks,
            "successful": successful_tasks,
            "failed": failed_tasks,
            "success_rate": round(success_rate, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n📈 Evaluation Results:")
        print(f"   Total Tasks: {total_tasks}")
        print(f"   Successful: {successful_tasks}")
        print(f"   Failed: {failed_tasks}")
        print(f"   Success Rate: {success_rate:.2f}%")
        
        return evaluation
    
    def update_economy(self, assignments: List[AgentAssignment]):
        """Update agent balances based on task execution results"""
        
        Args:
            assignments: List of completed assignments
        """
        print(f"\n💰 Updating Economy:")
        
        for assignment in assignments:
            agent_id = assignment.agent_id
            task_reward = assignment.task.reward
            
            if assignment.success:
                # Reward for successful task completion
                self.economy.add_reward(
                    agent_id,
                    task_reward,
                    f"completed_task_{assignment.task.task_id}"
                )
                print(f"   ✅ {agent_id} earned ${task_reward}")
            else:
                # Small penalty for failed task
                penalty = round(task_reward * 0.1, 2)
                self.economy.deduct_penalty(
                    agent_id,
                    penalty,
                    f"failed_task_{assignment.task.task_id}"
                )
                print(f"   ❌ {agent_id} penalized ${penalty}")
        
        # Print current balances
        print(f"\n💵 Agent Balances:")
        for agent_id, balance in self.economy.get_all_balances().items():
            print(f"   {agent_id}: ${balance:.2f}")
    
    def run_cycle(self, num_tasks: int = 5) -> Dict[str, Any]:
        """Run a complete autonomous cycle"""
        
        Args:
            num_tasks: Number of tasks to generate and execute
            
        Returns:
            Cycle summary with all results
        """
        self.cycle_count += 1
        print(f"\n{'='*60}")
        print(f"🔄 CYCLE {self.cycle_count} STARTED")
        print(f"{'='*60}")
        
        # Step 1: Generate tasks
        tasks = self.generate_tasks(num_tasks)
        
        # Step 2: Assign tasks to agents
        assignments = self.assign(tasks)
        
        # Step 3: Execute tasks
        results = self.execute(assignments)
        
        # Step 4: Evaluate results
        evaluation = self.evaluate(results)
        
        # Step 5: Update economy
        self.update_economy(results)
        
        cycle_summary = {
            "cycle": self.cycle_count,
            "evaluation": evaluation,
            "balances": self.economy.get_all_balances(),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n{'='*60}")
        print(f"✅ CYCLE {self.cycle_count} COMPLETED")
        print(f"{'='*60}\n")
        
        return cycle_summary
    
    def run_multiple_cycles(self, num_cycles: int = 3, num_tasks: int = 5, interval: float = 2.0):
        """Run multiple autonomous cycles with interval between cycles"""
        
        Args:
            num_cycles: Number of cycles to run
            num_tasks: Number of tasks per cycle
            interval: Seconds to wait between cycles
        """
        print(f"\n🚀 Starting {num_cycles} autonomous cycles...\n")
        
        cycle_results = []
        
        for cycle in range(num_cycles):
            result = self.run_cycle(num_tasks)
            cycle_results.append(result)
            
            if cycle < num_cycles - 1:
                print(f"⏳ Waiting {interval}s before next cycle...\n")
                time.sleep(interval)
        
        return cycle_results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall controller statistics""" 
        total_tasks = len(self.task_history)
        total_assignments = len(self.assignment_history)
        successful_assignments = sum(1 for a in self.assignment_history if a.success)
        
        return {
            "cycles_completed": self.cycle_count,
            "total_tasks_generated": total_tasks,
            "total_assignments": total_assignments,
            "successful_assignments": successful_assignments,
            "success_rate": (successful_assignments / total_assignments * 100) if total_assignments > 0 else 0,
            "agent_balances": self.economy.get_all_balances(),
            "timestamp": datetime.now().isoformat()
        }
    
    def save_report(self, filename: str = "controller_report.json"):
        """Save controller report to JSON file""" 
        report = {
            "controller_statistics": self.get_statistics(),
            "agents": self.agents,
            "transaction_history": self.economy.transaction_history
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📝 Report saved to {filename}")


# Example usage
if __name__ == "__main__":
    # Define agents
    agents = {
        "AgentA": "http://localhost:5000",
        "AgentB": "http://localhost:5001",
        "AgentC": "http://localhost:5002"
    }
    
    # Initialize controller
    controller = AutonomousController(agents, initial_balance=100.0)
    
    # Run multiple cycles
    try:
        controller.run_multiple_cycles(num_cycles=3, num_tasks=5, interval=2.0)
        
        # Print statistics
        print("\n📊 FINAL STATISTICS:")
        stats = controller.get_statistics()
        print(json.dumps(stats, indent=2))
        
        # Save report
        controller.save_report()
    
    except KeyboardInterrupt:
        print("\n⛔ Controller stopped by user")
    except Exception as e:
        print(f"\n❌ Controller error: {e}")
