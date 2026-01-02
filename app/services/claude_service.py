import httpx
import base64
import logging
from typing import Optional
from pathlib import Path

from app.config import get_settings
from app.models import Language, SellerContext

logger = logging.getLogger(__name__)

# Load prompts from files
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

# OpenRouter API configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_prompt(filename: str) -> str:
    """Load a prompt template from file."""
    filepath = PROMPTS_DIR / filename
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt file not found: {filepath}")


def build_seller_context_string(ctx: Optional[SellerContext], language: Language = Language.FRENCH) -> str:
    """Build formatted seller context string for injection into prompts."""
    if ctx is None:
        if language in (Language.ARABIC, Language.TUNISIAN):
            return "❌ ما فماش معلومات على البزنس. استعمل الكونتكست البصري فقط."
        return "❌ Aucune information vendeur disponible. Utilise uniquement le contexte visuel."

    parts = []
    is_arabic = language in (Language.ARABIC, Language.TUNISIAN)

    # Company info
    if ctx.company_name:
        if is_arabic:
            parts.append(f"🏪 الشركة: {ctx.company_name} ({ctx.instagram_handle or ''})")
        else:
            parts.append(f"🏪 Entreprise: {ctx.company_name} ({ctx.instagram_handle or ''})")

    # Product info
    if ctx.product_context:
        pc = ctx.product_context
        currency = pc.currency

        # Format price
        if pc.sale_price and pc.regular_price:
            price_str = f"{pc.sale_price} {currency} (au lieu de {pc.regular_price})" if not is_arabic else f"{pc.sale_price} {currency} (بدل {pc.regular_price})"
        else:
            price_str = f"{pc.sale_price or pc.regular_price} {currency}"

        # Stock status emoji
        stock_map = {"in_stock": "✅", "low_stock": "⚠️", "out_of_stock": "❌"}
        stock_emoji = stock_map.get(pc.stock_status, "❓")

        if is_arabic:
            parts.append(f"📦 المنتج: {pc.product_name_ar or pc.product_name or 'غير محدد'}")
            parts.append(f"   💰 السعر: {price_str}")
            if pc.sizes_available:
                parts.append(f"   📐 المقاسات: {', '.join(pc.sizes_available)}")
            if pc.colors_available:
                colors = [c.get('name', c) if isinstance(c, dict) else c for c in pc.colors_available]
                available_colors = [c.get('name') for c in pc.colors_available if isinstance(c, dict) and c.get('available', True)]
                if available_colors:
                    parts.append(f"   🎨 الألوان المتوفرة: {', '.join(available_colors)}")
            parts.append(f"   {stock_emoji} الستوك: {pc.stock_status or 'غير معروف'}")
        else:
            parts.append(f"📦 Produit: {pc.product_name or 'Non identifié'}")
            parts.append(f"   💰 Prix: {price_str}")
            if pc.sizes_available:
                parts.append(f"   📐 Tailles: {', '.join(pc.sizes_available)}")
            if pc.colors_available:
                available_colors = [c.get('name') for c in pc.colors_available if isinstance(c, dict) and c.get('available', True)]
                if available_colors:
                    parts.append(f"   🎨 Couleurs dispo: {', '.join(available_colors)}")
            parts.append(f"   {stock_emoji} Stock: {pc.stock_status or 'Inconnu'}")

    # Shipping info
    if ctx.shipping:
        ship = ctx.shipping
        if is_arabic:
            parts.append(f"🚚 التوصيل: {ship.zone or 'كل تونس'} - {ship.cost} دينار في {ship.time or '2-5 أيام'}")
            if ship.free_above:
                parts.append(f"   🆓 توصيل مجاني من {ship.free_above} دينار")
        else:
            parts.append(f"🚚 Livraison: {ship.zone or 'Toute Tunisie'} - {ship.cost} DT en {ship.time or '2-5 jours'}")
            if ship.free_above:
                parts.append(f"   🆓 Gratuit à partir de {ship.free_above} DT")

    # Payment methods
    if ctx.payment_methods:
        if is_arabic:
            parts.append(f"💳 طرق الخلاص: {', '.join(ctx.payment_methods)}")
        else:
            parts.append(f"💳 Paiement: {', '.join(ctx.payment_methods)}")

    # Return policy
    if ctx.return_policy:
        if is_arabic:
            parts.append(f"🔄 سياسة الترجيع: {ctx.return_policy}")
        else:
            parts.append(f"🔄 Retours: {ctx.return_policy}")

    # Active promotions
    if ctx.active_promotions:
        if is_arabic:
            parts.append("🎁 العروض النشطة:")
        else:
            parts.append("🎁 Promotions actives:")
        for promo in ctx.active_promotions:
            name = promo.get('name', 'Promo')
            discount = promo.get('discount', '')
            parts.append(f"   • {name}: {discount}")

    # FAQ matches
    if ctx.faq_matches:
        if is_arabic:
            parts.append("❓ أجوبة FAQ:")
        else:
            parts.append("❓ FAQ pertinentes:")
        for faq in ctx.faq_matches[:2]:
            answer = faq.get('answer', '')[:100]
            parts.append(f"   → {answer}")

    # Brand voice
    if ctx.brand_voice:
        bv = ctx.brand_voice
        if is_arabic:
            parts.append(f"🎨 ستايل الجواب: {bv.tone}, max {bv.max_sentences} جمل")
        else:
            parts.append(f"🎨 Style: {bv.tone}, max {bv.max_sentences} phrases")

    if not parts:
        if is_arabic:
            return "⚠️ معلومات محدودة. استعمل الكونتكست البصري."
        return "⚠️ Contexte limité. Utilise principalement le contexte visuel."

    return "\n".join(parts)


class ClaudeService:
    """Service for interacting with Claude via OpenRouter API."""

    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.anthropic_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://app.roborder.ai",
            "X-Title": "Roborder AI Reply Service"
        }

    def _get_system_prompt(self, language: Language) -> str:
        """Get the appropriate system prompt for the language."""
        prompt_files = {
            Language.FRENCH: "system_prompt_fr.txt",
            Language.ENGLISH: "system_prompt_en.txt",
            Language.TUNISIAN: "system_prompt_tn.txt",
            Language.ARABIC: "system_prompt_tn.txt",  # Use Tunisian for Arabic
        }
        filename = prompt_files.get(language, "system_prompt_fr.txt")
        return load_prompt(filename)

    async def fetch_image_as_base64(self, url: str) -> tuple[str, str]:
        """Fetch image from URL and convert to base64."""
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(url, follow_redirects=True)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "image/jpeg")
            if "png" in content_type:
                media_type = "image/png"
            elif "gif" in content_type:
                media_type = "image/gif"
            elif "webp" in content_type:
                media_type = "image/webp"
            else:
                media_type = "image/jpeg"

            image_data = base64.standard_b64encode(response.content).decode("utf-8")
            return image_data, media_type

    async def _call_openrouter(
        self,
        model: str,
        messages: list[dict],
        max_tokens: int = 150
    ) -> str:
        """Make a request to OpenRouter API."""
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OPENROUTER_BASE_URL,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    async def generate_reply(
        self,
        post_summary: str,
        comment_text: str,
        image_urls: list[str],
        language: Language = Language.FRENCH,
        seller_context: Optional[SellerContext] = None,
    ) -> str:
        """Generate a reply to a comment using Claude Vision via OpenRouter."""
        # Build seller context string
        seller_context_str = build_seller_context_string(seller_context, language)

        # Build system prompt with placeholders replaced
        system_prompt = self._get_system_prompt(language)
        system_prompt = system_prompt.replace("{{SELLER_CONTEXT}}", seller_context_str)
        system_prompt = system_prompt.replace("{{POST_SUMMARY}}", post_summary)
        system_prompt = system_prompt.replace("{{COMMENT_TEXT}}", comment_text)

        # Prepare content with images (OpenAI format for vision)
        content = []
        for url in image_urls:
            try:
                image_data, media_type = await self.fetch_image_as_base64(url)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{media_type};base64,{image_data}"
                    }
                })
            except Exception as e:
                logger.warning(f"Failed to fetch image {url}: {e}")

        # Use language-appropriate user message
        if language in (Language.ARABIC, Language.TUNISIAN):
            user_text = "ولّد جواب على التعليق بناءً على الصورة والكونتكست."
        else:
            user_text = "Génère une réponse à ce commentaire basée sur l'image et le contexte fourni."

        content.append({
            "type": "text",
            "text": user_text
        })

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ]

        # Use Claude 3.5 Sonnet via OpenRouter for better quality
        return await self._call_openrouter(
            model="openai/gpt-4.1-nano",
            messages=messages,
            max_tokens=self.settings.max_tokens_per_reply
        )

    async def summarize_post(
        self,
        caption: str,
        image_urls: list[str],
    ) -> str:
        """Generate a summary of a post for caching."""
        summary_prompt = load_prompt("summary_prompt.txt")
        summary_prompt = summary_prompt.replace("{{CAPTION}}", caption)

        # Prepare content with images
        content = []
        for url in image_urls:
            try:
                image_data, media_type = await self.fetch_image_as_base64(url)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{media_type};base64,{image_data}"
                    }
                })
            except Exception as e:
                logger.warning(f"Failed to fetch image {url}: {e}")

        content.append({
            "type": "text",
            "text": summary_prompt
        })

        messages = [
            {"role": "user", "content": content}
        ]

        return await self._call_openrouter(
            model="openai/gpt-4.1-nano",
            messages=messages,
            max_tokens=200
        )

    async def detect_language(self, comment_text: str) -> Language:
        """Detect the language of a comment."""
        detection_prompt = load_prompt("language_detection_prompt.txt")
        detection_prompt = detection_prompt.replace("{{COMMENT_TEXT}}", comment_text)

        messages = [
            {"role": "user", "content": detection_prompt}
        ]

        # Use Haiku for fast, cheap language detection
        code = await self._call_openrouter(
            model="openai/gpt-4.1-nano",
            messages=messages,
            max_tokens=10
        )

        code = code.lower().strip()
        language_map = {
            "fr": Language.FRENCH,
            "en": Language.ENGLISH,
            "ar": Language.ARABIC,
            "tn": Language.TUNISIAN,
        }
        return language_map.get(code, Language.FRENCH)
