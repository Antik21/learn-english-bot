from typing import Any

from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from learn_english_bot.db.models import User, UserFlow
from learn_english_bot.features.onboarding.keyboards import build_language_keyboard
from learn_english_bot.features.onboarding.languages import is_supported_language
from learn_english_bot.repositories.flows import FlowRepository
from learn_english_bot.repositories.users import UserRepository


ONBOARDING_FLOW = "onboarding"
STEP_WELCOME = "welcome"
STEP_CHOOSE_LANGUAGE = "choose_language"

WELCOME_MESSAGE = "Привет"
CHOOSE_LANGUAGE_MESSAGE = "Выберите ваш язык:"
LANGUAGE_SELECTED_MESSAGE = "Готово, язык сохранен."


class OnboardingFlow:
    name = ONBOARDING_FLOW
    initial_step = STEP_WELCOME

    def __init__(self, session: AsyncSession) -> None:
        self._users = UserRepository(session)
        self._flows = FlowRepository(session)

    async def start_or_continue(self, message: Message, user: User) -> None:
        flow = await self._flows.get_active(user_id=user.id, flow_name=self.name)
        if flow is None:
            flow = await self._flows.create_active(
                user_id=user.id,
                flow_name=self.name,
                current_step=self.initial_step,
            )

        await self.render_current_step(message, flow)

    async def render_current_step(self, message: Message, flow: UserFlow) -> None:
        if flow.current_step == STEP_WELCOME:
            await message.answer(WELCOME_MESSAGE)
            await self._flows.set_step(flow, current_step=STEP_CHOOSE_LANGUAGE, data={"page": 0})
            await message.answer(CHOOSE_LANGUAGE_MESSAGE, reply_markup=build_language_keyboard(0))
            return

        if flow.current_step == STEP_CHOOSE_LANGUAGE:
            page = _get_page(flow.data)
            await message.answer(CHOOSE_LANGUAGE_MESSAGE, reply_markup=build_language_keyboard(page))
            return

        await self._flows.set_step(flow, current_step=STEP_WELCOME, data={})
        await self.render_current_step(message, flow)

    async def show_language_page(
        self,
        callback: CallbackQuery,
        flow: UserFlow,
        page: int,
    ) -> None:
        data = dict(flow.data or {})
        data["page"] = page
        await self._flows.set_step(flow, current_step=STEP_CHOOSE_LANGUAGE, data=data)

        if isinstance(callback.message, Message):
            await callback.message.edit_text(
                CHOOSE_LANGUAGE_MESSAGE,
                reply_markup=build_language_keyboard(page),
            )
        await callback.answer()

    async def select_language(
        self,
        callback: CallbackQuery,
        user: User,
        flow: UserFlow,
        language_code: str,
    ) -> None:
        if not is_supported_language(language_code):
            await callback.answer("Этот язык пока недоступен.", show_alert=True)
            return

        data = dict(flow.data or {})
        data["base_language"] = language_code

        await self._users.set_base_language(user, language_code)
        await self._users.mark_onboarding_completed(user)
        await self._flows.complete(flow, data=data)

        if isinstance(callback.message, Message):
            await callback.message.edit_text(LANGUAGE_SELECTED_MESSAGE)
        await callback.answer()


def _get_page(data: dict[str, Any] | None) -> int:
    if not data:
        return 0

    page = data.get("page", 0)
    if isinstance(page, int):
        return page
    return 0
