from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from learn_english_bot.db.models import User, UserFlow
from learn_english_bot.features.onboarding.keyboards import build_language_keyboard
from learn_english_bot.features.onboarding.languages import is_supported_language
from learn_english_bot.messengers.contracts import (
    AnswerCallback,
    EditMessage,
    MessengerAction,
    MessengerContext,
    MessengerKeyboard,
    SendMessage,
)
from learn_english_bot.repositories.flows import FlowRepository
from learn_english_bot.repositories.users import UserRepository

ONBOARDING_FLOW = "onboarding"
STEP_WELCOME = "welcome"
STEP_CHOOSE_LANGUAGE = "choose_language"

WELCOME_MESSAGE = "Привет"
CHOOSE_LANGUAGE_MESSAGE = "Выберите ваш язык:"
LANGUAGE_SELECTED_MESSAGE = "Готово, язык сохранен."
UNSUPPORTED_LANGUAGE_MESSAGE = "Этот язык пока недоступен."


class OnboardingFlow:
    name = ONBOARDING_FLOW
    initial_step = STEP_WELCOME

    def __init__(self, session: AsyncSession) -> None:
        self._users = UserRepository(session)
        self._flows = FlowRepository(session)

    async def start_or_continue(
        self,
        context: MessengerContext,
        user: User,
    ) -> list[MessengerAction]:
        flow = await self._flows.get_active(user_id=user.id, flow_name=self.name)
        if flow is None:
            flow = await self._flows.create_active(
                user_id=user.id,
                flow_name=self.name,
                current_step=self.initial_step,
            )

        return await self.render_current_step(context, flow)

    async def render_current_step(
        self,
        context: MessengerContext,
        flow: UserFlow,
    ) -> list[MessengerAction]:
        if flow.current_step == STEP_WELCOME:
            await self._flows.set_step(flow, current_step=STEP_CHOOSE_LANGUAGE, data={"page": 0})
            return [
                SendMessage(chat_id=context.chat_id, text=WELCOME_MESSAGE),
                SendMessage(
                    chat_id=context.chat_id,
                    text=CHOOSE_LANGUAGE_MESSAGE,
                    keyboard=build_language_keyboard(0),
                ),
            ]

        if flow.current_step == STEP_CHOOSE_LANGUAGE:
            page = _get_page(flow.data)
            return [
                SendMessage(
                    chat_id=context.chat_id,
                    text=CHOOSE_LANGUAGE_MESSAGE,
                    keyboard=build_language_keyboard(page),
                )
            ]

        await self._flows.set_step(flow, current_step=STEP_WELCOME, data={})
        return await self.render_current_step(context, flow)

    async def show_language_page(
        self,
        context: MessengerContext,
        flow: UserFlow,
        page: int,
    ) -> list[MessengerAction]:
        data = dict(flow.data or {})
        data["page"] = page
        await self._flows.set_step(flow, current_step=STEP_CHOOSE_LANGUAGE, data=data)

        actions = _replace_current_message_or_send(
            context,
            text=CHOOSE_LANGUAGE_MESSAGE,
            keyboard=build_language_keyboard(page),
        )
        actions.extend(_answer_callback(context))
        return actions

    async def select_language(
        self,
        context: MessengerContext,
        user: User,
        flow: UserFlow,
        language_code: str,
    ) -> list[MessengerAction]:
        if not is_supported_language(language_code):
            return _answer_callback(
                context,
                text=UNSUPPORTED_LANGUAGE_MESSAGE,
                show_alert=True,
            )

        data = dict(flow.data or {})
        data["base_language"] = language_code

        await self._users.set_base_language(user, language_code)
        await self._users.mark_onboarding_completed(user)
        await self._flows.complete(flow, data=data)

        actions = _replace_current_message_or_send(
            context,
            text=LANGUAGE_SELECTED_MESSAGE,
            keyboard=None,
        )
        actions.extend(_answer_callback(context))
        return actions


def _replace_current_message_or_send(
    context: MessengerContext,
    *,
    text: str,
    keyboard: MessengerKeyboard | None,
) -> list[MessengerAction]:
    if context.message_id is not None:
        return [
            EditMessage(
                chat_id=context.chat_id,
                message_id=context.message_id,
                text=text,
                keyboard=keyboard,
            )
        ]

    return [SendMessage(chat_id=context.chat_id, text=text, keyboard=keyboard)]


def _answer_callback(
    context: MessengerContext,
    *,
    text: str | None = None,
    show_alert: bool = False,
) -> list[MessengerAction]:
    if context.callback_id is None:
        return []

    return [
        AnswerCallback(
            callback_id=context.callback_id,
            text=text,
            show_alert=show_alert,
        )
    ]


def _get_page(data: dict[str, Any] | None) -> int:
    if not data:
        return 0

    page = data.get("page", 0)
    if isinstance(page, int):
        return page
    return 0
