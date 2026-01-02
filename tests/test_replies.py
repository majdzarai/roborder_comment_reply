import pytest
from app.services.reply_generator import ReplyGenerator, FORBIDDEN_PATTERNS
from app.models import CommentIntent
import re


class TestReplyValidation:
    """Tests for reply validation logic."""

    def test_forbidden_patterns_detect_ai_mention(self):
        """Ensure AI mentions are detected."""
        test_cases = [
            "As an AI, I can help you",
            "I'm an automated system",
            "This automated reply is generated",
            "Using artificial intelligence",
        ]
        for text in test_cases:
            matches = any(re.search(pattern, text) for pattern in FORBIDDEN_PATTERNS)
            assert matches, f"Should detect forbidden pattern in: {text}"

    def test_allowed_replies_pass_validation(self):
        """Ensure normal replies pass validation."""
        test_cases = [
            "Merci beaucoup! Ecris-nous en DM.",
            "C'est 49 DT. N'hesite pas!",
            "Oui on l'a en noir!",
        ]
        # Create a minimal generator for testing
        class MockClaudeService:
            pass
        class MockCacheService:
            pass
        generator = ReplyGenerator(MockClaudeService(), MockCacheService())

        for reply in test_cases:
            is_valid, error = generator.validate_reply(reply)
            assert is_valid, f"Reply should pass validation: {reply}, error: {error}"

    def test_replies_with_links_fail(self):
        """Ensure replies with links fail validation."""
        class MockClaudeService:
            pass
        class MockCacheService:
            pass
        generator = ReplyGenerator(MockClaudeService(), MockCacheService())

        reply = "Check out https://example.com for more info"
        is_valid, error = generator.validate_reply(reply)
        assert not is_valid
        assert "link" in error.lower()

    def test_replies_with_hashtags_fail(self):
        """Ensure replies with hashtags fail validation."""
        class MockClaudeService:
            pass
        class MockCacheService:
            pass
        generator = ReplyGenerator(MockClaudeService(), MockCacheService())

        reply = "Great product! #sale #discount"
        is_valid, error = generator.validate_reply(reply)
        assert not is_valid
        assert "hashtag" in error.lower()


class TestIntentDetection:
    """Tests for comment intent detection."""

    def setup_method(self):
        """Set up test fixtures."""
        class MockClaudeService:
            pass
        class MockCacheService:
            pass
        self.generator = ReplyGenerator(MockClaudeService(), MockCacheService())

    def test_price_inquiry_french(self):
        """Detect French price inquiries."""
        comments = [
            "C'est combien?",
            "Quel est le prix?",
            "combien ca coute",
        ]
        for comment in comments:
            intent = self.generator.detect_intent(comment)
            assert intent == CommentIntent.PRICE_INQUIRY, f"Should detect price inquiry: {comment}"

    def test_price_inquiry_tunisian(self):
        """Detect Tunisian Arabic price inquiries."""
        comments = [
            "بشحال؟",
            "قداش الثمن؟",
        ]
        for comment in comments:
            intent = self.generator.detect_intent(comment)
            assert intent == CommentIntent.PRICE_INQUIRY, f"Should detect price inquiry: {comment}"

    def test_praise_detection(self):
        """Detect praise comments."""
        comments = [
            "Trop beau!",
            "Magnifique!",
            "I love it!",
        ]
        for comment in comments:
            intent = self.generator.detect_intent(comment)
            assert intent == CommentIntent.PRAISE, f"Should detect praise: {comment}"

    def test_availability_detection(self):
        """Detect availability questions."""
        comments = [
            "Vous avez en stock?",
            "C'est disponible?",
            "Dispo en noir?",
        ]
        for comment in comments:
            intent = self.generator.detect_intent(comment)
            assert intent == CommentIntent.AVAILABILITY, f"Should detect availability: {comment}"

    def test_negative_detection(self):
        """Detect negative comments."""
        comments = [
            "C'est trop cher",
            "Too expensive",
        ]
        for comment in comments:
            intent = self.generator.detect_intent(comment)
            assert intent == CommentIntent.NEGATIVE, f"Should detect negative: {comment}"

    def test_general_fallback(self):
        """Fall back to general for unmatched comments."""
        comment = "Random comment here"
        intent = self.generator.detect_intent(comment)
        assert intent == CommentIntent.GENERAL
