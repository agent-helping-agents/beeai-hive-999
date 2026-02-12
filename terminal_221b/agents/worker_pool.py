"""
Worker Pool - Concurrent Agent Execution for Terminal 221b

Implements asyncio-based concurrent agent operations enabling:
- Parallel transaction processing across multiple contexts
- Concurrent analytical objectives
- Resource allocation and rate limiting
- Graceful shutdown handling

"Many hands make light work, Watson."
"""

import asyncio
import uuid
from typing import Optional, Dict, List, Any, AsyncGenerator, Callable
from dataclasses import dataclass, field
from enum import Enum
import time

from terminal_221b.agents.detective_agent import DetectiveAgent
from terminal_221b.agents.advisor_deps import AdvisorDeps


class WorkerStatus(Enum):
    """Worker status states."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    SHUTDOWN = "shutdown"


@dataclass
class Task:
    """Represents a task to be executed by a worker."""
    id: str
    description: str
    handler: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    priority: int = 5  # 1-10, lower = higher priority
    deadline: Optional[float] = None
    created_at: float = field(default_factory=time.time)
    result: Any = None
    error: Optional[str] = None
    status: str = "pending"  # pending, running, completed, failed


@dataclass
class Worker:
    """Represents a worker agent instance."""
    id: str
    agent: DetectiveAgent
    status: WorkerStatus = WorkerStatus.IDLE
    current_task: Optional[Task] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_compute_time: float = 0.0
    created_at: float = field(default_factory=time.time)


class WorkerPool:
    """
    Manages a pool of detective agents for concurrent operations.
    
    Usage:
        pool = WorkerPool(max_workers=5)
        await pool.start()
        
        # Submit tasks
        task_id = await pool.submit(
            "Analyze address ABC",
            agent.analyze_address,
            "ABC123..."
        )
        
        # Get results
        result = await pool.get_result(task_id)
        
        # Shutdown
        await pool.stop()
    """
    
    def __init__(
        self,
        deps: AdvisorDeps,
        max_workers: int = 5,
        max_queue_size: int = 100,
        personality: str = "holmes",
    ):
        self.deps = deps
        self.max_workers = max_workers
        self.max_queue_size = max_queue_size
        self.personality = personality
        
        self.workers: Dict[str, Worker] = {}
        self.task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue(
            maxsize=max_queue_size
        )
        self.tasks: Dict[str, Task] = {}
        self.results: Dict[str, Any] = {}
        
        self._shutdown_event = asyncio.Event()
        self._worker_tasks: List[asyncio.Task] = []
        self._is_running = False
        
    async def start(self):
        """Start the worker pool."""
        if self._is_running:
            return
            
        self._is_running = True
        self._shutdown_event.clear()
        
        # Create initial workers
        for i in range(self.max_workers):
            await self._spawn_worker()
            
        print(f"🚀 Worker pool started with {self.max_workers} detectives")
        
    async def stop(self, timeout: float = 30.0):
        """
        Stop the worker pool gracefully.
        
        Args:
            timeout: Maximum time to wait for in-flight tasks
        """
        print(f"🛑 Shutting down worker pool (timeout: {timeout}s)...")
        
        self._shutdown_event.set()
        
        # Cancel all worker tasks
        for task in self._worker_tasks:
            task.cancel()
            
        # Wait for completion
        try:
            await asyncio.wait_for(
                asyncio.gather(*self._worker_tasks, return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            print("⚠️  Some workers did not shut down gracefully")
            
        # Clean up agents
        for worker in self.workers.values():
            if worker.agent.sim_server:
                await worker.agent.sim_server.stop()
                
        self._is_running = False
        print("✅ Worker pool stopped")
        
    async def _spawn_worker(self):
        """Create a new worker."""
        worker_id = f"worker_{uuid.uuid4().hex[:8]}"
        
        # Create agent for this worker
        agent = await self._create_agent()
        
        worker = Worker(
            id=worker_id,
            agent=agent,
            status=WorkerStatus.IDLE,
        )
        
        self.workers[worker_id] = worker
        
        # Start worker task
        task = asyncio.create_task(
            self._worker_loop(worker),
            name=f"worker_loop_{worker_id}"
        )
        self._worker_tasks.append(task)
        
        return worker
    
    async def _create_agent(self) -> DetectiveAgent:
        """Create a new detective agent."""
        from terminal_221b.agents.detective_agent import create_detective
        return await create_detective(
            deps=self.deps,
            personality=self.personality,
            enable_simulation=self.deps.simulation_mode,
        )
    
    async def _worker_loop(self, worker: Worker):
        """Main loop for a worker."""
        try:
            while not self._shutdown_event.is_set():
                try:
                    # Get task from queue (with timeout to check shutdown)
                    priority, task = await asyncio.wait_for(
                        self.task_queue.get(),
                        timeout=1.0
                    )
                    
                    await self._execute_task(worker, task)
                    
                except asyncio.TimeoutError:
                    continue
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"❌ Worker {worker.id} error: {e}")
            worker.status = WorkerStatus.ERROR
            
    async def _execute_task(self, worker: Worker, task: Task):
        """Execute a task on a worker."""
        start_time = time.time()
        worker.status = WorkerStatus.BUSY
        worker.current_task = task
        task.status = "running"
        
        try:
            # Execute the handler
            result = await task.handler(*task.args, **task.kwargs)
            
            task.result = result
            task.status = "completed"
            self.results[task.id] = result
            worker.tasks_completed += 1
            
        except Exception as e:
            task.error = str(e)
            task.status = "failed"
            self.results[task.id] = {"error": str(e)}
            worker.tasks_failed += 1
            print(f"❌ Task {task.id} failed: {e}")
            
        finally:
            elapsed = time.time() - start_time
            worker.total_compute_time += elapsed
            worker.status = WorkerStatus.IDLE
            worker.current_task = None
            
    async def submit(
        self,
        description: str,
        handler: Callable,
        *args,
        priority: int = 5,
        deadline: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Submit a task to the worker pool.
        
        Args:
            description: Human-readable task description
            handler: Async function to execute
            *args: Positional arguments for handler
            priority: Task priority (1-10, lower = higher)
            deadline: Unix timestamp deadline (optional)
            **kwargs: Keyword arguments for handler
            
        Returns:
            Task ID for tracking
        """
        task_id = f"task_{uuid.uuid4().hex[:12]}"
        
        task = Task(
            id=task_id,
            description=description,
            handler=handler,
            args=args,
            kwargs=kwargs,
            priority=priority,
            deadline=deadline,
        )
        
        self.tasks[task_id] = task
        
        # Add to queue (priority queue uses tuple: (priority, task))
        await self.task_queue.put((priority, task))
        
        return task_id
    
    async def get_result(self, task_id: str, timeout: Optional[float] = None) -> Any:
        """
        Wait for and retrieve a task result.
        
        Args:
            task_id: Task ID from submit()
            timeout: Maximum time to wait
            
        Returns:
            Task result
        """
        start_time = time.time()
        
        while True:
            if task_id in self.results:
                return self.results[task_id]
            
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")
            
            await asyncio.sleep(0.1)
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current pool status."""
        return {
            "workers": {
                "total": len(self.workers),
                "idle": sum(1 for w in self.workers.values() if w.status == WorkerStatus.IDLE),
                "busy": sum(1 for w in self.workers.values() if w.status == WorkerStatus.BUSY),
                "error": sum(1 for w in self.workers.values() if w.status == WorkerStatus.ERROR),
            },
            "tasks": {
                "pending": self.task_queue.qsize(),
                "total_submitted": len(self.tasks),
                "completed": sum(1 for t in self.tasks.values() if t.status == "completed"),
                "failed": sum(1 for t in self.tasks.values() if t.status == "failed"),
            },
            "compute_time": sum(w.total_compute_time for w in self.workers.values()),
        }


# ============================================================================
# GENERATOR PATTERN
# ============================================================================

async def worker_generator(
    deps: AdvisorDeps,
    count: int = 3,
    personality: str = "holmes"
) -> AsyncGenerator[DetectiveAgent, None]:
    """
    Generate workers on-demand for parallel processing.
    
    Usage:
        async for agent in worker_generator(deps, count=5):
            result = await agent.investigate("...")
            yield result
    """
    for i in range(count):
        agent = await create_detective(deps, personality, enable_simulation=False)
        yield agent


async def start_worker(
    deps: AdvisorDeps,
    task_queue: asyncio.Queue,
    result_queue: asyncio.Queue,
    personality: str = "holmes",
    worker_id: Optional[str] = None,
):
    """
    Start a single worker process.
    
    Usage:
        task_queue = asyncio.Queue()
        result_queue = asyncio.Queue()
        
        worker_task = asyncio.create_task(
            start_worker(deps, task_queue, result_queue)
        )
        
        await task_queue.put(("investigate", "address_123"))
        result = await result_queue.get()
    """
    agent = await create_detective(deps, personality)
    worker_id = worker_id or f"worker_{uuid.uuid4().hex[:8]}"
    
    print(f"🔍 Detective {worker_id} reporting for duty")
    
    try:
        while True:
            task_type, *args = await task_queue.get()
            
            if task_type == "shutdown":
                break
                
            try:
                if task_type == "investigate":
                    result = await agent.investigate(args[0])
                elif task_type == "transfer":
                    result = await agent.execute_transfer(*args)
                elif task_type == "analyze":
                    result = await agent.analyze_address(*args)
                else:
                    result = {"error": f"Unknown task: {task_type}"}
                    
                await result_queue.put({"success": True, "result": result})
                
            except Exception as e:
                await result_queue.put({"success": False, "error": str(e)})
                
    finally:
        if agent.sim_server:
            await agent.sim_server.stop()
        print(f"🛑 Detective {worker_id} signing off")


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

async def parallel_investigations(
    queries: List[str],
    deps: Optional[AdvisorDeps] = None,
    max_workers: int = 3,
    personality: str = "holmes"
) -> List[Dict[str, Any]]:
    """
    Run multiple investigations in parallel.
    
    Args:
        queries: List of investigation queries
        deps: Configuration (created from env if None)
        max_workers: Maximum concurrent workers
        personality: Detective personality to use
        
    Returns:
        List of results corresponding to queries
    """
    deps = deps or AdvisorDeps.from_env()
    
    async with WorkerPool(deps, max_workers, personality=personality) as pool:
        # Submit all tasks
        task_ids = []
        for query in queries:
            agent = await create_detective(deps, personality)
            task_id = await pool.submit(
                f"Investigate: {query[:50]}...",
                agent.investigate,
                query
            )
            task_ids.append(task_id)
        
        # Collect results
        results = []
        for task_id in task_ids:
            result = await pool.get_result(task_id)
            results.append(result)
            
    return results


# Context manager for WorkerPool
class WorkerPool:
    """Extended WorkerPool with async context manager support."""
    
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
        return False
