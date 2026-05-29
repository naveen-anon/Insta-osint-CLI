
import os
import instaloader

class InstaLiveScanner:
    def __init__(self):
        self.loader = instaloader.Instaloader(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            download_pictures=False,
            download_videos=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False
        )
        self.authenticated = False

    def setup_session(self, session_user=None):
        """Bypass parameters ke liye local profile session inject karta hai"""
        if session_user:
            try:
                self.loader.load_session_from_profile(session_user)
                self.authenticated = True
                return {"status": "success", "msg": f"Session active for: {session_user}"}
            except Exception as e:
                return {"status": "fallback", "msg": f"Session alert: {str(e)}"}
        return {"status": "anonymous", "msg": "Running in public scanner mode."}

    def execute_live_intel(self, username):
        """Instagram architecture se live meta dump nikalta hai"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            return {
                "status": "success",
                "profile": {
                    "username": profile.username,
                    "profile_url": f"https://www.instagram.com/{profile.username}/",
                    "full_name": profile.full_name,
                    "biography": profile.biography,
                },
                "account_analysis": {
                    "private": profile.is_private,
                    "verified": profile.is_verified,
                    "business_account": profile.is_business_account,
                },
                "profile_stats": {
                    "followers": str(profile.followers),
                    "following": str(profile.followees),
                    "posts": str(profile.mediacount)
                }
            }
        except instaloader.exceptions.ProfileNotExistsException:
            return {"status": "error", "msg": "Profile non-existent on Instagram."}
        except instaloader.exceptions.ConnectionException as ce:
            return {"status": "error", "msg": f"Rate-limit or Security block: {str(ce)}"}
        except Exception as e:
            return {"status": "error", "msg": f"Pipeline failed: {str(e)}"}
      
