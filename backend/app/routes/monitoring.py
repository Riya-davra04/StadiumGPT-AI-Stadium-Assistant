from fastapi import APIRouter, Depends, WebSocket
from typing import Dict, Any
from app.services.monitoring import MonitoringService
from app.routes.auth import get_current_user

router = APIRouter()
service = MonitoringService()


@router.get("/metrics")
async def get_metrics(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    return await service.get_live_metrics()


@router.get("/sections")
async def get_sections(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    return await service.get_section_status()


@router.post("/alert/{section}")
async def create_alert(
    section: str,
    message: str,
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    return await service.generate_alert(section, message)


@router.get("/alerts")
async def get_alerts(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    return {"alerts": await service.get_active_alerts()}