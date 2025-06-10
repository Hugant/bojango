from abc import ABC, abstractmethod
from typing import Type, Callable

from telegram import Update
from telegram.ext import ContextTypes

from bojango.action.screen import ScreenType, ActionScreen
from bojango.action.strategies.base import BaseContentStrategy


class BaseScreenBehavior(ABC):
  BEHAVIORS: dict[ScreenType, Type['BaseScreenBehavior']] = {}

  @staticmethod
  def resolve_behavior(screen_type: ScreenType) -> 'BaseScreenBehavior':
    behavior_cls = BaseScreenBehavior.BEHAVIORS.get(screen_type)

    if behavior_cls is None:
      raise ValueError(f'Behavior type {screen_type} not supported')

    return behavior_cls()

  @abstractmethod
  async def render(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    strategy: BaseContentStrategy
  ) -> None:
    raise NotImplementedError


def register_behavior(screen_type: ScreenType) -> Callable[[Type[BaseScreenBehavior]], Type[BaseScreenBehavior]]:
  """
  Декоратор для регистрации поведения экрана.

  :param screen_type: Тип экрана (ScreenType), для которого регистрируется поведение.
  """
  def decorator(cls: Type[BaseScreenBehavior]) -> Type[BaseScreenBehavior]:
    BaseScreenBehavior.BEHAVIORS[screen_type] = cls
    return cls

  return decorator