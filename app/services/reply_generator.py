import re
import logging
from typing import Optional

from app.models import (
    ReplyRequest,
    ReplyResponse,
    CommentIntent,
    Language,
    ContextUsed,
)
from app.services.claude_service import ClaudeService
from app.services.cache_service import CacheService

logger = logging.getLogger(__name__)

# Patterns that indicate automated/AI-generated content
FORBIDDEN_PATTERNS = [
    r"(?i)as an ai",
    r"(?i)i'm an? (automated|ai)",
    r"(?i)automated (system|reply|response)",
    r"(?i)this (automated|ai)",
    r"(?i)artificial intelligence",
    r"(?i)je suis un(e)? (robot|bot|ia)",
    r"(?i)أنا (روبوت|بوت)",
]

# Enhanced intent detection keywords (matching CLAUDE.md intent categories)
INTENT_KEYWORDS = {
    CommentIntent.PRICE_INQUIRY: [
        "combien", "prix", "price", "how much", "كم", "بشحال", "قداش",
        "cout", "coute", "tarif", "سعر", "ثمن", "cost", "coûte"
    ],
    CommentIntent.AVAILABILITY: [
        "stock", "disponible", "available", "dispo", "موجود", "فما",
        "avez-vous", "reste", "en stock", "still have", "فيه", "عندكم"
    ],
    CommentIntent.SIZE_QUESTION: [
        "taille", "size", "قياس", "مقاس", "mesure", "s", "m", "l", "xl",
        "pointure", "tailles disponibles", "sizes available"
    ],
    CommentIntent.COLOR_QUESTION: [
        "couleur", "color", "لون", "noir", "blanc", "rouge", "bleu",
        "vert", "rose", "beige", "كحل", "ابيض", "احمر", "أزرق"
    ],
    CommentIntent.SHIPPING_INQUIRY: [
        "livraison", "delivery", "توصيل", "shipping", "délai", "يوصل",
        "expédition", "envoyer", "تبعثو", "توصلو", "deliver", "send"
    ],
    CommentIntent.PAYMENT_QUESTION: [
        "paiement", "payment", "خلاص", "cod", "payer", "carte", "virement",
        "d17", "نخلص", "كيفاش نخلص", "how to pay", "دفع"
    ],
    CommentIntent.RETURN_QUESTION: [
        "retour", "échange", "return", "ترجيع", "exchange", "rembours",
        "نرجع", "تبديل", "changer", "refund"
    ],
    CommentIntent.ORDER_INTENT: [
        "commander", "acheter", "order", "buy", "نشري", "نحب",
        "je veux", "i want", "intéressé", "نكومندي", "نوخذ", "take"
    ],
    CommentIntent.PRAISE: [
        "beau", "magnifique", "superbe", "love", "beautiful", "amazing",
        "جميل", "روعة", "parfait", "top", "bravo", "wow", "😍", "❤️",
        "💕", "🔥", "gorgeous", "stunning", "fantastic"
    ],
    CommentIntent.INTEREST: [
        "interested", "intéressé", "مهتم", "want to know", "tell me more",
        "curieux", "je veux savoir"
    ],
    CommentIntent.CONFUSION: [
        "comprends pas", "don't understand", "ما فهمت", "comment",
        "how", "كيفاش", "explain", "explique", "c'est quoi", "شنو هذا"
    ],
    CommentIntent.NEGATIVE: [
        "cher", "expensive", "غالي", "nul", "mauvais", "bad",
        "arnaque", "scam", "مشكل", "problème", "problem"
    ],
    CommentIntent.NEGOTIATION: [
        "moins cher", "نقص", "discount", "réduction", "promo",
        "meilleur prix", "better price", "نقص شوي", "بركة"
    ],
}


class ReplyGenerator:
    """Service for generating and validating Instagram replies."""

    def __init__(
        self,
        claude_service: ClaudeService,
        cache_service: CacheService,
    ):
        self.claude = claude_service
        self.cache = cache_service

    def detect_intents(self, comment_text: str) -> list[CommentIntent]:
        """Detect all matching intents from a comment."""
        comment_lower = comment_text.lower()
        detected = []
        for intent, keywords in INTENT_KEYWORDS.items():
            if any(keyword in comment_lower for keyword in keywords):
                detected.append(intent)
        return detected if detected else [CommentIntent.GENERAL]

    def detect_intent(self, comment_text: str) -> CommentIntent:
        """Detect the primary intent of a comment based on keywords."""
        intents = self.detect_intents(comment_text)
        return intents[0] if intents else CommentIntent.GENERAL

    def build_context_used(self, request: ReplyRequest) -> ContextUsed:
        """Build the context usage tracking object."""
        ctx = ContextUsed()
        ctx.image_context = len(request.image_urls) > 0

        if request.seller_context:
            sc = request.seller_context
            ctx.product_catalog = sc.product_context is not None
            ctx.shipping_policies = sc.shipping is not None
            ctx.faq_matched = len(sc.faq_matches) > 0
            ctx.brand_voice_applied = sc.brand_voice is not None
            ctx.promotion_mentioned = len(sc.active_promotions) > 0

        return ctx

    def validate_reply(self, reply: str) -> tuple[bool, Optional[str]]:
        """Validate a generated reply against quality rules."""
        # Check for forbidden patterns
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, reply):
                return False, "Contains AI/automation reference"

        # Check sentence count (max 2)
        sentences = [s.strip() for s in re.split(r'[.!?]', reply) if s.strip()]
        if len(sentences) > 2:
            return False, "Too many sentences"

        # Check for links
        if "http" in reply.lower() or "www." in reply.lower():
            return False, "Contains link"

        # Check for hashtags
        if "#" in reply:
            return False, "Contains hashtag"

        # Check character limit
        if len(reply) > 300:
            return False, "Exceeds character limit"

        return True, None

    async def generate(self, request: ReplyRequest) -> ReplyResponse:
        """Generate a reply for a comment."""
        # Detect all intents
        intents = self.detect_intents(request.comment_text)
        primary_intent = intents[0]
        logger.info(f"Detected intents: {intents} for comment: {request.comment_text[:50]}...")

        # Build context tracking
        context_used = self.build_context_used(request)
        has_seller_context = request.seller_context is not None

        # Generate reply using Claude with seller context
        reply = await self.claude.generate_reply(
            post_summary=request.post_summary,
            comment_text=request.comment_text,
            image_urls=request.image_urls,
            language=request.language,
            seller_context=request.seller_context,
        )

        # Validate the reply
        is_valid, error = self.validate_reply(reply)
        if not is_valid:
            logger.warning(f"Reply validation failed: {error}. Regenerating...")
            # Try once more with a regeneration hint
            reply = await self.claude.generate_reply(
                post_summary=request.post_summary,
                comment_text=request.comment_text,
                image_urls=request.image_urls,
                language=request.language,
                seller_context=request.seller_context,
            )
            # Re-validate
            is_valid, _ = self.validate_reply(reply)

        # Calculate confidence based on context availability and validation
        base_confidence = 0.95 if is_valid else 0.75
        if has_seller_context:
            # Higher confidence when we have seller context
            confidence = min(base_confidence + 0.03, 0.98)
        else:
            # Lower confidence in fallback mode
            confidence = base_confidence - 0.05

        return ReplyResponse(
            reply=reply,
            confidence=confidence,
            detected_intent=primary_intent,
            detected_intents=[i.value for i in intents],
            language_used=request.language,
            context_used=context_used,
            fallback_used=not has_seller_context,
        )
