from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Any


class Language(str, Enum):
    """Supported languages for reply generation."""
    FRENCH = "fr"
    ENGLISH = "en"
    ARABIC = "ar"
    TUNISIAN = "tn"


class BrandVoice(str, Enum):
    """Brand voice styles for replies."""
    PROFESSIONAL_FRIENDLY = "professional_friendly"
    CASUAL = "casual"
    FORMAL = "formal"


class CommentIntent(str, Enum):
    """Detected intent categories for comments."""
    PRICE_INQUIRY = "price_inquiry"
    AVAILABILITY = "availability"
    SIZE_QUESTION = "size_question"
    COLOR_QUESTION = "color_question"
    SHIPPING_INQUIRY = "shipping_inquiry"
    PAYMENT_QUESTION = "payment_question"
    RETURN_QUESTION = "return_question"
    ORDER_INTENT = "order_intent"
    PRODUCT_QUESTION = "product_question"
    PRAISE = "praise"
    INTEREST = "interest"
    CONFUSION = "confusion"
    NEGATIVE = "negative"
    NEGOTIATION = "negotiation"
    GENERAL = "general"


# ═══════════════════════════════════════════════════════════════════════════════
# SELLER KNOWLEDGE BASE MODELS (Optional - for enhanced context)
# ═══════════════════════════════════════════════════════════════════════════════

class ProductContext(BaseModel):
    """Product-specific context for accurate replies."""
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    product_name_ar: Optional[str] = None
    regular_price: Optional[float] = None
    sale_price: Optional[float] = None
    currency: str = "TND"
    sizes_available: list[str] = Field(default_factory=list)
    colors_available: list[dict[str, Any]] = Field(default_factory=list)
    stock_status: Optional[str] = None  # in_stock, low_stock, out_of_stock


class ShippingInfo(BaseModel):
    """Shipping information for the customer's zone."""
    zone: Optional[str] = None
    cost: Optional[float] = None
    time: Optional[str] = None
    free_above: Optional[float] = None


class BrandVoiceConfig(BaseModel):
    """Brand voice configuration for consistent replies."""
    tone: str = "professional_friendly"
    language_style: str = "french"
    max_sentences: int = 2
    emoji_usage: str = "minimal"  # none, minimal, moderate


class SellerContext(BaseModel):
    """
    Optional seller knowledge base context.
    When provided, enables highly accurate and personalized replies.
    """
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    instagram_handle: Optional[str] = None
    business_type: Optional[str] = None

    # Product context (if identified from post)
    product_context: Optional[ProductContext] = None

    # Policies
    shipping: Optional[ShippingInfo] = None
    payment_methods: list[str] = Field(default_factory=list)
    return_policy: Optional[str] = None

    # Dynamic content
    active_promotions: list[dict[str, Any]] = Field(default_factory=list)
    faq_matches: list[dict[str, Any]] = Field(default_factory=list)

    # Brand voice
    brand_voice: Optional[BrandVoiceConfig] = None


class ReplyRequest(BaseModel):
    """Request payload for generating a reply."""
    post_id: str = Field(..., description="Unique identifier for the Instagram post")
    post_summary: str = Field(..., description="Summary of the post content")
    comment_text: str = Field(..., description="The comment to reply to")
    image_urls: list[str] = Field(default_factory=list, description="URLs of post images")
    language: Language = Field(default=Language.FRENCH, description="Target language for reply")
    brand_voice: BrandVoice = Field(
        default=BrandVoice.PROFESSIONAL_FRIENDLY,
        description="Tone and style of the reply"
    )
    cta_allowed: bool = Field(default=False, description="Whether call-to-action is allowed")
    # Optional seller knowledge base context
    seller_context: Optional[SellerContext] = Field(
        default=None,
        description="Optional seller context for highly accurate replies"
    )


class ContextUsed(BaseModel):
    """Tracks which context sources were used in generating the reply."""
    image_context: bool = False
    product_catalog: bool = False
    shipping_policies: bool = False
    faq_matched: bool = False
    brand_voice_applied: bool = False
    promotion_mentioned: bool = False


class ReplyResponse(BaseModel):
    """Response payload containing the generated reply."""
    reply: str = Field(..., description="The generated reply text")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score of the reply")
    detected_intent: CommentIntent = Field(..., description="Detected intent of the comment")
    detected_intents: list[str] = Field(default_factory=list, description="All detected intents")
    language_used: Language = Field(..., description="Language used in the reply")
    context_used: ContextUsed = Field(default_factory=ContextUsed, description="Context sources used")
    fallback_used: bool = Field(default=False, description="Whether fallback mode was used")


class SummarizeRequest(BaseModel):
    """Request payload for summarizing a post."""
    post_id: str = Field(..., description="Unique identifier for the Instagram post")
    caption: str = Field(..., description="The post caption text")
    image_urls: list[str] = Field(..., description="URLs of post images")


class SummarizeResponse(BaseModel):
    """Response payload containing the post summary."""
    post_id: str = Field(..., description="Unique identifier for the Instagram post")
    summary: str = Field(..., description="Generated summary of the post")
    cached: bool = Field(default=False, description="Whether the result was from cache")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "2.0.0"
    services: dict = Field(default_factory=dict)
