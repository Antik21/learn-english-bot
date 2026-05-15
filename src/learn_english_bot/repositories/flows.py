from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from learn_english_bot.db.models import UserFlow

ACTIVE = "active"
COMPLETED = "completed"


class FlowRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_active(self, *, user_id: int, flow_name: str) -> UserFlow | None:
        result = await self._session.execute(
            select(UserFlow).where(
                UserFlow.user_id == user_id,
                UserFlow.flow_name == flow_name,
                UserFlow.status == ACTIVE,
            )
        )
        return result.scalar_one_or_none()

    async def create_active(
        self,
        *,
        user_id: int,
        flow_name: str,
        current_step: str,
        data: dict[str, Any] | None = None,
    ) -> UserFlow:
        flow = UserFlow(
            user_id=user_id,
            flow_name=flow_name,
            status=ACTIVE,
            current_step=current_step,
            data=data or {},
        )
        self._session.add(flow)
        await self._session.flush()
        return flow

    async def set_step(
        self,
        flow: UserFlow,
        *,
        current_step: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        flow.current_step = current_step
        if data is not None:
            flow.data = data
        await self._session.flush()

    async def complete(self, flow: UserFlow, data: dict[str, Any] | None = None) -> None:
        flow.status = COMPLETED
        flow.completed_at = datetime.utcnow()
        if data is not None:
            flow.data = data
        await self._session.flush()
