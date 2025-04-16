
class ActionAlreadyExistsError(Exception):
  """Исключение, вызываемое при повторной регистрации действия."""
  def __init__(self, action_name: str, message='Action already exists'):
    message = f'{message}: "{action_name}"'
    super().__init__(message)
    self.action_name = action_name


class UnknownActionError(Exception):
  """Исключение, вызываемое при попытке вызвать неизвестное действие."""
  def __init__(self, action_name: str, message='Unknown action'):
    message = f'{message}: "{action_name}"'
    super().__init__(message)
    self.action_name = action_name
