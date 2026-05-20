from src.social.base_client import BaseSocialClient

class MockClient(BaseSocialClient):
    def post_content(self, content_text, media_path=None):
        print(f"[MOCK] Posting: {content_text}")
        if media_path:
            print(f"[MOCK] Attaching media: {media_path}")
        return True

    def close(self):
        print("[MOCK] Mock client closed.")
