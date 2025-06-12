"""bob_api.services.job_service

Job Service for BOB Google Maps API v0.6.0
Divine job management following Niṣkāma Karma Yoga principles.

Made with 🙏 for interconnected excellence
"""

import asyncio
import time
import uuid
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, asdict

from .interfaces import JobService, ScrapingService, CacheService, MetricsService


class JobStatus(Enum):
    """Job status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    """Job data structure."""
    id: str
    type: str
    status: JobStatus
    payload: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: float = 0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    progress: float = 0
    user_id: Optional[str] = None


class JobServiceImpl(JobService):
    """Divine job service implementation."""
    
    def __init__(
        self,
        scraping_service: Optional[ScrapingService] = None,
        cache_service: Optional[CacheService] = None,
        metrics_service: Optional[MetricsService] = None
    ):
        self.scraping_service = scraping_service
        self.cache_service = cache_service
        self.metrics_service = metrics_service
        self._initialized = False
        
        # In-memory job storage
        self._jobs: Dict[str, Job] = {}
        self._running_tasks: Dict[str, asyncio.Task] = {}
        
        # Job processing limits
        self._max_concurrent_jobs = 5
        self._job_timeout = 3600  # 1 hour
    
    async def initialize(self):
        """Initialize the job service."""
        if self._initialized:
            return
        
        self._initialized = True
    
    async def create_job(self, job_type: str, payload: Dict[str, Any]) -> str:
        """Create a new background job."""
        try:
            job_id = str(uuid.uuid4())
            
            job = Job(
                id=job_id,
                type=job_type,
                status=JobStatus.PENDING,
                payload=payload,
                created_at=time.time(),
                user_id=payload.get('user_id')
            )
            
            self._jobs[job_id] = job
            
            # Start job processing
            await self._start_job_processing(job_id)
            
            return job_id
            
        except Exception as e:
            raise RuntimeError(f"Failed to create job: {str(e)}")
    
    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status and progress."""
        try:
            job = self._jobs.get(job_id)
            if not job:
                return {
                    "success": False,
                    "error": "Job not found",
                    "job_id": job_id
                }
            
            return {
                "success": True,
                "job": asdict(job),
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "job_id": job_id,
                "timestamp": time.time()
            }
    
    async def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a running job."""
        try:
            job = self._jobs.get(job_id)
            if not job:
                return {
                    "success": False,
                    "error": "Job not found",
                    "job_id": job_id
                }
            
            if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                return {
                    "success": False,
                    "error": f"Job already {job.status.value}",
                    "job_id": job_id
                }
            
            # Cancel the running task
            task = self._running_tasks.get(job_id)
            if task:
                task.cancel()
                del self._running_tasks[job_id]
            
            # Update job status
            job.status = JobStatus.CANCELLED
            job.completed_at = time.time()
            
            return {
                "success": True,
                "message": "Job cancelled successfully",
                "job_id": job_id,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "job_id": job_id,
                "timestamp": time.time()
            }
    
    async def get_job_result(self, job_id: str) -> Dict[str, Any]:
        """Get completed job result."""
        try:
            job = self._jobs.get(job_id)
            if not job:
                return {
                    "success": False,
                    "error": "Job not found",
                    "job_id": job_id
                }
            
            if job.status != JobStatus.COMPLETED:
                return {
                    "success": False,
                    "error": f"Job not completed (status: {job.status.value})",
                    "job_id": job_id,
                    "status": job.status.value
                }
            
            return {
                "success": True,
                "job_id": job_id,
                "result": job.result,
                "completed_at": job.completed_at,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "job_id": job_id,
                "timestamp": time.time()
            }
    
    async def list_jobs(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List jobs for a user."""
        try:
            jobs = []
            
            for job in self._jobs.values():
                # Filter by user_id if provided
                if user_id and job.user_id != user_id:
                    continue
                
                jobs.append(asdict(job))
            
            # Sort by creation time (newest first)
            jobs.sort(key=lambda x: x['created_at'], reverse=True)
            
            return jobs
            
        except Exception as e:
            return []
    
    async def _start_job_processing(self, job_id: str):
        """Start processing a job."""
        try:
            # Check if we have too many concurrent jobs
            if len(self._running_tasks) >= self._max_concurrent_jobs:
                # Job will remain in PENDING status
                return
            
            job = self._jobs.get(job_id)
            if not job:
                return
            
            # Create and start the job task
            task = asyncio.create_task(self._process_job(job_id))
            self._running_tasks[job_id] = task
            
        except Exception as e:
            # Mark job as failed
            job = self._jobs.get(job_id)
            if job:
                job.status = JobStatus.FAILED
                job.error = str(e)
                job.completed_at = time.time()
    
    async def _process_job(self, job_id: str):
        """Process a job."""
        job = self._jobs.get(job_id)
        if not job:
            return
        
        try:
            # Update job status
            job.status = JobStatus.RUNNING
            job.started_at = time.time()
            job.progress = 0
            
            # Process based on job type
            if job.type == "batch_scrape":
                result = await self._process_batch_scrape_job(job)
            elif job.type == "single_scrape":
                result = await self._process_single_scrape_job(job)
            else:
                raise ValueError(f"Unknown job type: {job.type}")
            
            # Mark job as completed
            job.status = JobStatus.COMPLETED
            job.result = result
            job.completed_at = time.time()
            job.progress = 100
            
        except asyncio.CancelledError:
            job.status = JobStatus.CANCELLED
            job.completed_at = time.time()
            
        except Exception as e:
            job.status = JobStatus.FAILED
            job.error = str(e)
            job.completed_at = time.time()
            
        finally:
            # Remove from running tasks
            if job_id in self._running_tasks:
                del self._running_tasks[job_id]
            
            # Start next pending job if any
            await self._start_next_pending_job()
    
    async def _process_batch_scrape_job(self, job: Job) -> Dict[str, Any]:
        """Process a batch scrape job."""
        if not self.scraping_service:
            raise RuntimeError("Scraping service not available")
        
        payload = job.payload
        urls = payload.get('urls', [])
        
        if not urls:
            raise ValueError("No URLs provided for batch scrape")
        
        # Update progress
        job.progress = 10
        
        # Perform batch scraping
        results = await self.scraping_service.batch_scrape(
            urls=urls,
            extract_reviews=payload.get('extract_reviews', True),
            max_reviews=payload.get('max_reviews'),
            backend=payload.get('backend', 'auto'),
            max_workers=payload.get('max_workers', 4),
            timeout=payload.get('timeout', 60)
        )
        
        # Update progress
        job.progress = 90
        
        # Process results
        successful_results = [r for r in results if r.get('success')]
        failed_results = [r for r in results if not r.get('success')]
        
        return {
            "total_urls": len(urls),
            "successful": len(successful_results),
            "failed": len(failed_results),
            "success_rate": len(successful_results) / len(urls) if urls else 0,
            "results": results,
            "summary": {
                "total_businesses": len(successful_results),
                "total_reviews": sum(len(r.get('reviews', [])) for r in successful_results),
                "processing_time": time.time() - job.started_at
            }
        }
    
    async def _process_single_scrape_job(self, job: Job) -> Dict[str, Any]:
        """Process a single scrape job."""
        if not self.scraping_service:
            raise RuntimeError("Scraping service not available")
        
        payload = job.payload
        url = payload.get('url')
        
        if not url:
            raise ValueError("No URL provided for single scrape")
        
        # Update progress
        job.progress = 10
        
        # Perform scraping
        result = await self.scraping_service.scrape_url(
            url=url,
            extract_reviews=payload.get('extract_reviews', True),
            max_reviews=payload.get('max_reviews'),
            backend=payload.get('backend', 'auto'),
            timeout=payload.get('timeout', 60)
        )
        
        # Update progress
        job.progress = 90
        
        return {
            "url": url,
            "success": result.get('success', False),
            "result": result,
            "processing_time": time.time() - job.started_at
        }
    
    async def _start_next_pending_job(self):
        """Start the next pending job if capacity allows."""
        if len(self._running_tasks) >= self._max_concurrent_jobs:
            return
        
        # Find the oldest pending job
        pending_jobs = [
            job for job in self._jobs.values() 
            if job.status == JobStatus.PENDING
        ]
        
        if not pending_jobs:
            return
        
        # Sort by creation time and start the oldest
        pending_jobs.sort(key=lambda x: x.created_at)
        oldest_job = pending_jobs[0]
        
        await self._start_job_processing(oldest_job.id)
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy."""
        return self._initialized
    
    async def shutdown(self):
        """Shutdown the service gracefully."""
        # Cancel all running tasks
        for task in self._running_tasks.values():
            task.cancel()
        
        # Wait for tasks to complete
        if self._running_tasks:
            await asyncio.gather(*self._running_tasks.values(), return_exceptions=True)
        
        self._running_tasks.clear()
        self._jobs.clear()
        self._initialized = False 