from abc import ABC, abstractmethod

class BaseSocialClient(ABC):
    @abstractmethod
    def post_content(self, content_text, media_path=None):
        pass

    @abstractmethod
    def close(self):
        pass
