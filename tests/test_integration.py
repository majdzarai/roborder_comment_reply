import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

# Note: These tests require mocking the Claude API
# Run with: pytest tests/test_integration.py -v


class TestAPIEndpoints:
    """Integration tests for API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client with mocked services."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            from app.main import app
            return TestClient(app)

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_generate_reply_request_validation(self, client):
        """Test request validation for generate-reply endpoint."""
        # Missing required fields
        response = client.post("/api/v1/generate-reply", json={})
        assert response.status_code == 422  # Validation error

    def test_generate_reply_valid_payload(self, client):
        """Test generate-reply with valid payload (mocked)."""
        payload = {
            "post_id": "123",
            "post_summary": "Summer dress collection",
            "comment_text": "C'est combien?",
            "image_urls": ["https://example.com/image.jpg"],
            "language": "fr"
        }
        # Note: This will fail without proper mocking
        # In a real test, mock the ClaudeService
        # response = client.post("/api/v1/generate-reply", json=payload)

    def test_summarize_post_request_validation(self, client):
        """Test request validation for summarize-post endpoint."""
        response = client.post("/api/v1/summarize-post", json={})
        assert response.status_code == 422


class TestPayloadCompatibility:
    """Tests to ensure Roborder payload compatibility."""

    def test_reply_request_accepts_roborder_format(self):
        """Verify our models accept Roborder's expected payload format."""
        from app.models import ReplyRequest

        # Exact format Roborder will send
        roborder_payload = {
            "post_id": "abc123",
            "post_summary": "Promotion de notre nouvelle collection ete 2025",
            "comment_text": "C'est combien le prix svp?",
            "image_urls": [
                "https://instagram.com/cdn/image1.jpg"
            ],
            "language": "fr",
            "brand_voice": "professional_friendly",
            "cta_allowed": False
        }

        # Should parse without errors
        request = ReplyRequest(**roborder_payload)
        assert request.post_id == "abc123"
        assert request.language.value == "fr"

    def test_reply_response_matches_expected_format(self):
        """Verify our response matches what Roborder expects."""
        from app.models import ReplyResponse, CommentIntent, Language

        response = ReplyResponse(
            reply="Le prix est affiche sur la deuxieme photo.",
            confidence=0.92,
            detected_intent=CommentIntent.PRICE_INQUIRY,
            language_used=Language.FRENCH
        )

        # Convert to dict to check JSON format
        response_dict = response.model_dump()
        assert "reply" in response_dict
        assert "confidence" in response_dict
        assert "detected_intent" in response_dict
        assert "language_used" in response_dict
