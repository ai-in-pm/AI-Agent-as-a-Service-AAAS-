import pyautogui
import keyboard
from typing import Tuple, Optional
import logging

class KeyboardController:
    def __init__(self):
        # Configure PyAutoGUI settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        self.logger = logging.getLogger(__name__)

    def type_text(self, text: str) -> bool:
        """
        Type text using PyAutoGUI
        """
        try:
            pyautogui.write(text)
            return True
        except Exception as e:
            self.logger.error(f"Error typing text: {str(e)}")
            return False

    def press_key(self, key: str) -> bool:
        """
        Press a single key
        """
        try:
            keyboard.press_and_release(key)
            return True
        except Exception as e:
            self.logger.error(f"Error pressing key: {str(e)}")
            return False

    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Get current mouse position
        """
        return pyautogui.position()

    def move_mouse(self, x: int, y: int, duration: float = 0.2) -> bool:
        """
        Move mouse to specific coordinates
        """
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            self.logger.error(f"Error moving mouse: {str(e)}")
            return False

    def click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """
        Click at current position or specified coordinates
        """
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y)
            else:
                pyautogui.click()
            return True
        except Exception as e:
            self.logger.error(f"Error clicking: {str(e)}")
            return False
