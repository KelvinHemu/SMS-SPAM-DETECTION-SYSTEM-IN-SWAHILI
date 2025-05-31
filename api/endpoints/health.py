"""
Health & Monitoring Endpoints
System status, health checks, and statistics
"""

from fastapi import APIRouter, Depends, status
from core.logging import get_logger
from api.models import HealthCheckResponse, SystemStatsResponse
from services import MessageAnalysisService

logger = get_logger()

# Create router
router = APIRouter()

# Global service instance
analysis_service = None


def get_analysis_service() -> MessageAnalysisService:
    """Dependency to get the analysis service instance"""
    global analysis_service
    if analysis_service is None:
        analysis_service = MessageAnalysisService()
        logger.info("Analysis service initialized for health endpoints")
    return analysis_service


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="System Health Check",
    description="""
    Get comprehensive system health status.
    
    **Checks**:
    - ML model loading status
    - Database connectivity
    - Component availability
    - Basic functionality
    
    **Use Cases**:
    - Load balancer health checks
    - Monitoring system integration
    - Deployment validation
    """
)
async def health_check(
    service: MessageAnalysisService = Depends(get_analysis_service)
) -> HealthCheckResponse:
    """
    Perform comprehensive health check
    
    Returns:
        HealthCheckResponse with system status
    """
    try:
        # Get health check from service
        health_data = service.health_check()
        
        # Create response
        response = HealthCheckResponse(
            version="1.0.0",
            models_loaded=health_data["models_loaded"],
            database_connected=health_data["database_connected"]
        )
        
        logger.debug(f"Health check: {response.status} - models:{response.models_loaded}, db:{response.database_connected}")
        return response
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        # Return unhealthy response
        return HealthCheckResponse(
            status="unhealthy",
            version="1.0.0",
            models_loaded=False,
            database_connected=False
        )


@router.get(
    "/health/simple",
    status_code=status.HTTP_200_OK,
    summary="Simple Health Check",
    description="""
    Simple health check endpoint for basic availability testing.
    
    Returns HTTP 200 OK if the service is running.
    
    **Use Cases**:
    - Basic uptime monitoring
    - Simple load balancer checks
    - Quick availability tests
    """
)
async def simple_health():
    """
    Simple health check - just returns OK if service is running
    
    Returns:
        Simple status message
    """
    return {"status": "ok", "service": "spam-detection-api"}


@router.get(
    "/health/detailed",
    status_code=status.HTTP_200_OK,
    summary="Detailed Health Check",
    description="""
    Detailed health check with component-level status.
    
    **Information Included**:
    - Individual component status
    - Request processing statistics
    - Performance metrics
    - Error rates
    """
)
async def detailed_health(
    service: MessageAnalysisService = Depends(get_analysis_service)
):
    """
    Detailed health check with component breakdown
    
    Returns:
        Detailed health information
    """
    try:
        health_data = service.health_check()
        
        return {
            "status": health_data["status"],
            "components": health_data.get("components", {}),
            "requests_processed": health_data.get("total_requests", 0),
            "version": "1.0.0",
            "timestamp": health_data.get("timestamp")
        }
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "components": {
                "text_classification": False,
                "phone_validation": False,
                "decision_engine": False
            },
            "version": "1.0.0"
        }


@router.get(
    "/stats",
    response_model=SystemStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="System Statistics",
    description="""
    Get comprehensive system statistics and metrics.
    
    **Statistics Include**:
    - Total requests processed
    - Decision outcome distribution
    - Phone database statistics
    - ML model information
    - System uptime
    - Performance metrics
    
    **Use Cases**:
    - Performance monitoring
    - Usage analytics
    - System optimization
    - Reporting dashboards
    """
)
async def get_system_stats(
    service: MessageAnalysisService = Depends(get_analysis_service)
) -> SystemStatsResponse:
    """
    Get comprehensive system statistics
    
    Returns:
        SystemStatsResponse with all system metrics
    """
    try:
        stats = service.get_system_stats()
        
        response = SystemStatsResponse(
            total_requests=stats["total_requests"],
            decisions_by_outcome=stats["decisions_by_outcome"],
            phone_database_stats=stats["phone_database_stats"],
            model_info=stats["model_info"],
            uptime_seconds=stats["uptime_seconds"]
        )
        
        logger.debug(f"Stats requested: {stats['total_requests']} total requests")
        return response
        
    except Exception as e:
        logger.error(f"Error getting system stats: {str(e)}")
        # Return empty stats on error
        return SystemStatsResponse(
            total_requests=0,
            decisions_by_outcome={},
            phone_database_stats={},
            model_info={"error": str(e)},
            uptime_seconds=0
        )


@router.get(
    "/metrics",
    status_code=status.HTTP_200_OK,
    summary="Prometheus-style Metrics",
    description="""
    Get metrics in Prometheus format for monitoring integration.
    
    **Metrics Exposed**:
    - spam_detection_requests_total
    - spam_detection_decisions_total{outcome}
    - spam_detection_processing_time_seconds
    - spam_detection_model_loaded
    - spam_detection_database_connected
    """
)
async def get_metrics(
    service: MessageAnalysisService = Depends(get_analysis_service)
):
    """
    Get metrics in Prometheus format
    
    Returns:
        Metrics in text format compatible with Prometheus
    """
    try:
        stats = service.get_system_stats()
        health = service.health_check()
        
        # Build Prometheus-style metrics
        metrics = []
        
        # Request metrics
        metrics.append(f"# HELP spam_detection_requests_total Total number of analysis requests")
        metrics.append(f"# TYPE spam_detection_requests_total counter") 
        metrics.append(f"spam_detection_requests_total {stats['total_requests']}")
        
        # Decision metrics
        metrics.append(f"# HELP spam_detection_decisions_total Total decisions by outcome")
        metrics.append(f"# TYPE spam_detection_decisions_total counter")
        for outcome, count in stats["decisions_by_outcome"].items():
            metrics.append(f'spam_detection_decisions_total{{outcome="{outcome.lower()}"}} {count}')
        
        # Model status
        metrics.append(f"# HELP spam_detection_model_loaded ML model loading status")
        metrics.append(f"# TYPE spam_detection_model_loaded gauge")
        metrics.append(f"spam_detection_model_loaded {1 if health['models_loaded'] else 0}")
        
        # Database status
        metrics.append(f"# HELP spam_detection_database_connected Database connection status")
        metrics.append(f"# TYPE spam_detection_database_connected gauge")
        metrics.append(f"spam_detection_database_connected {1 if health['database_connected'] else 0}")
        
        # Uptime
        metrics.append(f"# HELP spam_detection_uptime_seconds System uptime in seconds")
        metrics.append(f"# TYPE spam_detection_uptime_seconds gauge")
        metrics.append(f"spam_detection_uptime_seconds {stats['uptime_seconds']}")
        
        return "\n".join(metrics)
        
    except Exception as e:
        logger.error(f"Error generating metrics: {str(e)}")
        return f"# Error generating metrics: {str(e)}"


@router.get(
    "/version",
    status_code=status.HTTP_200_OK,
    summary="API Version Information",
    description="Get API version and build information"
)
async def get_version():
    """
    Get API version information
    
    Returns:
        Version and build information
    """
    return {
        "api_version": "1.0.0",
        "build_date": "2024-01-01",
        "features": [
            "text_classification",
            "phone_validation", 
            "decision_matrix",
            "batch_processing",
            "health_monitoring"
        ],
        "ml_model": "MultinomialNB",
        "supported_languages": ["en", "sw"]  # English, Swahili
    } 