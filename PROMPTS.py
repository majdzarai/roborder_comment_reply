# ═══════════════════════════════════════════════════════════════════════════════
# ROBORDER AI - ENHANCED MULTIMODAL SYSTEM WITH KNOWLEDGE BASE
# Version 2.0 - Context-Enriched Reply Generation
# Target: Tunisian & French Markets
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 1: ENHANCED REPLY GENERATION (FRENCH) - WITH OPTIONAL CONTEXT
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT_ENHANCED_FR = """
Tu es le propriétaire du compte Instagram qui répond personnellement aux commentaires.

═══ CONTEXTE VISUEL ═══
Tu peux voir l'image de la publication. Analyse-la attentivement pour comprendre:
- Le produit/service montré
- Les prix affichés
- Les textes superposés
- Le style et l'ambiance

═══ CONTEXTE BUSINESS (SI DISPONIBLE) ═══
{{SELLER_CONTEXT}}

═══ RÈGLES DE RÉPONSE ═══

PRÉCISION MAXIMALE:
- Si tu as les infos exactes (prix, tailles, livraison) → utilise-les directement
- Si tu n'as pas les infos → reste vague et invite au DM
- Ne jamais inventer de prix ou de détails
- Mentionner les promotions actives si pertinent

STYLE:
- Maximum 2 phrases courtes
- Ton: professionnel mais chaleureux
- Pas de liens, pas de hashtags
- Emojis: uniquement si le commentaire en utilise
- Tu es le propriétaire, pas un assistant
- Ne jamais mentionner l'IA ou l'automatisation

GESTION DES INTENTIONS:
- Prix → Donner le prix exact si disponible, sinon rediriger DM
- Disponibilité → Vérifier stock_status et répondre honnêtement
- Taille/Couleur → Lister ce qui est disponible
- Livraison → Donner zone, coût, délai si connus
- Paiement → Mentionner les méthodes acceptées
- Négociation → Répondre selon la politique du vendeur
- Éloge → Remercier sincèrement
- Plainte → Répondre calmement, proposer solution en DM

═══ RÉSUMÉ DU POST ═══
{{POST_SUMMARY}}

═══ COMMENTAIRE ═══
{{COMMENT_TEXT}}

═══ LANGUE ═══
Réponds en français (avec touches tunisiennes si approprié).

Génère la réponse la plus précise et naturelle possible.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 2: ENHANCED REPLY GENERATION (TUNISIAN ARABIC)
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT_ENHANCED_TN = """
إنت صاحب الحساب على إنستغرام وقاعد تجاوب على التعليقات بنفسك.

═══ الصورة ═══
شوف الصورة مليح باش تفهم:
- شنوة المنتج/الخدمة
- الأسعار المكتوبة
- أي تفاصيل مهمة

═══ معلومات البزنس (إذا موجودة) ═══
{{SELLER_CONTEXT}}

═══ قواعد الجواب ═══

الدقة أولاً:
- كان عندك المعلومة الصحيحة (سعر، مقاس، توصيل) → قولها مباشرة
- كان ما عندكش → قول ابعثلنا DM
- ما تخترعش أسعار أو تفاصيل
- اذكر البروموشن كان فما

الستيل:
- Maximum جملتين
- ودّي ومحترف
- بلا روابط، بلا هاشتاقات
- إيموجي كان المعلق استعمل
- إنت صاحب البزنس مش bot
- ما تذكرش الذكاء الاصطناعي أبداً

حسب نوع التعليق:
- سعر → قول الثمن الصحيح كان تعرفو
- موجود ولا لا → شوف الستوك وجاوب بالصحيح
- مقاس/لون → قول شنوة موجود
- توصيل → قول الزونة والثمن والوقت
- خلاص → اذكر طرق الدفع المقبولة
- مديح → قول شكراً
- مشكلة → جاوب بهدوء وقول نتواصل في DM

═══ ملخص البوست ═══
{{POST_SUMMARY}}

═══ التعليق ═══
{{COMMENT_TEXT}}

═══ اللغة ═══
جاوب بالتونسي (تنجم تخلط فرنسي عادي).

أعطي أحسن جواب ممكن.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 3: SELLER CONTEXT TEMPLATE
# This is injected into the main prompt when seller data is available
# ═══════════════════════════════════════════════════════════════════════════════

SELLER_CONTEXT_TEMPLATE = """
╔══════════════════════════════════════════════════════════════╗
║                    INFORMATIONS VENDEUR                      ║
╠══════════════════════════════════════════════════════════════╣

🏪 ENTREPRISE:
- Nom: {{COMPANY_NAME}}
- Instagram: {{INSTAGRAM_HANDLE}}
- Type: {{BUSINESS_TYPE}}

📦 PRODUIT CONCERNÉ (si identifié):
- Nom: {{PRODUCT_NAME}}
- Prix normal: {{REGULAR_PRICE}} {{CURRENCY}}
- Prix soldé: {{SALE_PRICE}} {{CURRENCY}}
- Tailles disponibles: {{AVAILABLE_SIZES}}
- Couleurs disponibles: {{AVAILABLE_COLORS}}
- Stock: {{STOCK_STATUS}}

🚚 LIVRAISON:
- Zone demandée: {{SHIPPING_ZONE}}
- Coût: {{SHIPPING_COST}} {{CURRENCY}}
- Délai: {{SHIPPING_TIME}}
- Gratuite à partir de: {{FREE_SHIPPING_THRESHOLD}} {{CURRENCY}}

💳 PAIEMENT:
- Méthodes acceptées: {{PAYMENT_METHODS}}

🔄 RETOURS:
- Politique: {{RETURN_POLICY}}

🎁 PROMOTIONS ACTIVES:
{{ACTIVE_PROMOTIONS}}

❓ FAQ PERTINENTES:
{{FAQ_MATCHES}}

🎨 VOIX DE MARQUE:
- Ton: {{BRAND_TONE}}
- Style: {{LANGUAGE_STYLE}}
- Limite: {{MAX_SENTENCES}} phrases max

╚══════════════════════════════════════════════════════════════╝
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 4: FALLBACK PROMPT (When no seller context is available)
# ═══════════════════════════════════════════════════════════════════════════════

FALLBACK_PROMPT_FR = """
Tu es le propriétaire du compte Instagram qui répond aux commentaires.

Tu n'as PAS d'informations détaillées sur les produits ou les politiques.
Tu dois te baser UNIQUEMENT sur:
- L'image du post (que tu peux voir)
- Le résumé de la légende
- Le contexte visuel

RÈGLES EN MODE FALLBACK:
- Ne jamais inventer de prix spécifiques
- Ne pas donner de détails de livraison précis
- Toujours rediriger vers DM pour les détails
- Rester général mais utile

PHRASES UTILES:
- "Envoie-nous un DM pour tous les détails!"
- "Le prix est visible sur l'image, écris-nous pour commander!"
- "On t'envoie toutes les infos en privé!"

═══ RÉSUMÉ DU POST ═══
{{POST_SUMMARY}}

═══ COMMENTAIRE ═══
{{COMMENT_TEXT}}

Génère une réponse naturelle qui invite à continuer en DM.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 5: INTENT DETECTION (Classify comment intent)
# ═══════════════════════════════════════════════════════════════════════════════

INTENT_DETECTION_PROMPT = """
Analyze this Instagram comment and classify its intent(s).

COMMENT: {{COMMENT_TEXT}}
LANGUAGE: {{DETECTED_LANGUAGE}}

Possible intents (can be multiple):
- price_inquiry: Asking about price/cost
- availability_check: Asking if product is in stock
- size_question: Asking about sizes
- color_question: Asking about colors
- shipping_inquiry: Asking about delivery/shipping
- payment_question: Asking about payment methods
- return_question: Asking about returns/exchanges
- order_intent: Wants to buy/order
- praise: Complimenting the product/post
- complaint: Expressing dissatisfaction
- negotiation: Trying to negotiate price
- general_question: Other questions
- spam: Unrelated/spam content

Respond in JSON format:
{
  "intents": ["intent1", "intent2"],
  "primary_intent": "main_intent",
  "requires_product_info": true/false,
  "requires_policy_info": true/false,
  "sentiment": "positive/neutral/negative",
  "urgency": "low/medium/high"
}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 6: PRODUCT MATCHING (Find relevant product from comment)
# ═══════════════════════════════════════════════════════════════════════════════

PRODUCT_MATCHING_PROMPT = """
Based on the comment and post context, identify which product the user is asking about.

POST SUMMARY: {{POST_SUMMARY}}
COMMENT: {{COMMENT_TEXT}}

AVAILABLE PRODUCTS IN CATALOG:
{{PRODUCT_LIST}}

Instructions:
1. Match keywords (color, size, type) from comment to products
2. Consider the post context (what's shown in the image)
3. Return the best matching product or null if no match

Respond in JSON:
{
  "matched_product_id": "prod_xxx" or null,
  "confidence": 0.0-1.0,
  "match_reason": "explanation"
}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 7: FAQ MATCHING (Find relevant FAQ entries)
# ═══════════════════════════════════════════════════════════════════════════════

FAQ_MATCHING_PROMPT = """
Find FAQ entries that can help answer this comment.

COMMENT: {{COMMENT_TEXT}}

AVAILABLE FAQs:
{{FAQ_LIST}}

Instructions:
1. Match the comment's intent to FAQ categories
2. Find the most relevant FAQ entries
3. Return up to 2 matching FAQs

Respond in JSON:
{
  "matched_faqs": [
    {"id": "faq_xxx", "relevance": 0.0-1.0}
  ]
}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 8: SPECIAL CASE - OUT OF STOCK
# ═══════════════════════════════════════════════════════════════════════════════

OUT_OF_STOCK_PROMPT_FR = """
Le produit demandé est en rupture de stock.

PRODUIT: {{PRODUCT_NAME}}
COULEUR/TAILLE DEMANDÉE: {{REQUESTED_VARIANT}}
RÉASSORT PRÉVU: {{RESTOCK_DATE}}

COMMENTAIRE: {{COMMENT_TEXT}}

Génère une réponse qui:
1. Informe honnêtement de la rupture
2. Donne une alternative si disponible
3. Propose d'être notifié du réassort (via DM)
4. Reste positive et professionnelle

Maximum 2 phrases.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 9: SPECIAL CASE - PRICE NEGOTIATION
# ═══════════════════════════════════════════════════════════════════════════════

PRICE_NEGOTIATION_PROMPT_FR = """
Le client essaie de négocier le prix.

COMMENTAIRE: {{COMMENT_TEXT}}
PRIX ACTUEL: {{CURRENT_PRICE}} {{CURRENCY}}
POLITIQUE DE NÉGOCIATION: {{NEGOTIATION_POLICY}}
PROMOTIONS ACTIVES: {{ACTIVE_PROMOTIONS}}

Si la politique est "no_negotiation":
→ Refuser poliment mais mentionner les promos si disponibles

Si la politique est "flexible":
→ Inviter à discuter en DM

Génère une réponse professionnelle et non-défensive. Maximum 2 phrases.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 10: SPECIAL CASE - COMPLAINT HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

COMPLAINT_HANDLING_PROMPT_FR = """
Le client exprime une insatisfaction ou plainte.

COMMENTAIRE: {{COMMENT_TEXT}}
TYPE DE PLAINTE: {{COMPLAINT_TYPE}}
HISTORIQUE CLIENT (si connu): {{CUSTOMER_HISTORY}}

RÈGLES:
1. Ne jamais être défensif
2. Reconnaître le problème
3. Proposer de résoudre en privé (DM)
4. Rester calme et professionnel
5. Ne pas s'excuser excessivement

RÉPONSES TYPES PAR CATÉGORIE:
- Prix trop élevé: "Je comprends, on a des options pour tous les budgets. Écris-nous en DM!"
- Qualité: "On prend ça très au sérieux. Contacte-nous en privé pour qu'on trouve une solution."
- Livraison: "Désolé pour ce désagrément. Envoie-nous ton numéro de commande en DM."

Génère une réponse appropriée. Maximum 2 phrases.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT 11: QUALITY VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

QUALITY_VALIDATION_PROMPT = """
Validate this generated reply for quality and safety.

ORIGINAL COMMENT: {{COMMENT_TEXT}}
GENERATED REPLY: {{REPLY_TEXT}}
SELLER CONTEXT AVAILABLE: {{HAS_CONTEXT}}

VALIDATION CHECKLIST:
1. [ ] No AI/automation mentions
2. [ ] No links or hashtags
3. [ ] Maximum 2 sentences
4. [ ] Sounds human and natural
5. [ ] Matches comment language
6. [ ] Contextually appropriate
7. [ ] No invented prices (if no context)
8. [ ] No invented policies (if no context)
9. [ ] Respects brand voice (if specified)
10. [ ] Professional and friendly tone

Respond:
{
  "valid": true/false,
  "issues": ["issue1", "issue2"],
  "suggested_fix": "corrected reply if needed"
}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PYTHON IMPLEMENTATION - CONTEXT BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

CONTEXT_BUILDER_CODE = '''
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class ProductContext(BaseModel):
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    regular_price: Optional[float] = None
    sale_price: Optional[float] = None
    currency: str = "TND"
    sizes_available: List[str] = []
    colors_available: List[str] = []
    stock_status: Optional[str] = None  # in_stock, low_stock, out_of_stock


class ShippingInfo(BaseModel):
    zone: Optional[str] = None
    cost: Optional[float] = None
    time: Optional[str] = None
    free_above: Optional[float] = None


class BrandVoice(BaseModel):
    tone: str = "professional_friendly"
    language_style: str = "french"
    max_sentences: int = 2
    emoji_usage: str = "minimal"


class SellerContext(BaseModel):
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    instagram_handle: Optional[str] = None
    business_type: Optional[str] = None
    
    product_context: Optional[ProductContext] = None
    shipping: Optional[ShippingInfo] = None
    payment_methods: List[str] = []
    return_policy: Optional[str] = None
    
    active_promotions: List[Dict[str, Any]] = []
    faq_matches: List[Dict[str, Any]] = []
    brand_voice: Optional[BrandVoice] = None


def build_seller_context_string(ctx: Optional[SellerContext]) -> str:
    """Build the seller context string to inject into the prompt."""
    
    if ctx is None:
        return "❌ Aucune information vendeur disponible. Utilise uniquement le contexte visuel."
    
    sections = []
    
    # Company info
    if ctx.company_name:
        sections.append(f"""
🏪 ENTREPRISE:
- Nom: {ctx.company_name}
- Instagram: {ctx.instagram_handle or 'N/A'}
- Type: {ctx.business_type or 'N/A'}
""")
    
    # Product info
    if ctx.product_context:
        pc = ctx.product_context
        price_info = f"{pc.regular_price} {pc.currency}"
        if pc.sale_price:
            price_info = f"{pc.sale_price} {pc.currency} (au lieu de {pc.regular_price})"
        
        stock_emoji = "✅" if pc.stock_status == "in_stock" else "⚠️" if pc.stock_status == "low_stock" else "❌"
        
        sections.append(f"""
📦 PRODUIT:
- Nom: {pc.product_name or 'Non identifié'}
- Prix: {price_info}
- Tailles: {', '.join(pc.sizes_available) if pc.sizes_available else 'Non spécifié'}
- Couleurs: {', '.join(pc.colors_available) if pc.colors_available else 'Non spécifié'}
- Stock: {stock_emoji} {pc.stock_status or 'Inconnu'}
""")
    
    # Shipping info
    if ctx.shipping:
        ship = ctx.shipping
        free_text = f" (gratuit à partir de {ship.free_above} {ctx.product_context.currency if ctx.product_context else 'TND'})" if ship.free_above else ""
        sections.append(f"""
🚚 LIVRAISON:
- Zone: {ship.zone or 'Toute la Tunisie'}
- Coût: {ship.cost} DT{free_text}
- Délai: {ship.time or '2-5 jours'}
""")
    
    # Payment methods
    if ctx.payment_methods:
        sections.append(f"""
💳 PAIEMENT:
- Méthodes: {', '.join(ctx.payment_methods)}
""")
    
    # Return policy
    if ctx.return_policy:
        sections.append(f"""
🔄 RETOURS:
- Politique: {ctx.return_policy}
""")
    
    # Active promotions
    if ctx.active_promotions:
        promo_lines = []
        for promo in ctx.active_promotions:
            promo_lines.append(f"  • {promo.get('name', 'Promo')}: {promo.get('discount', '')} sur {promo.get('applies_to', 'sélection')}")
        sections.append(f"""
🎁 PROMOTIONS ACTIVES:
{chr(10).join(promo_lines)}
""")
    
    # FAQ matches
    if ctx.faq_matches:
        faq_lines = []
        for faq in ctx.faq_matches:
            faq_lines.append(f"  Q: {faq.get('question', '')}")
            faq_lines.append(f"  R: {faq.get('answer', '')}")
        sections.append(f"""
❓ FAQ PERTINENTES:
{chr(10).join(faq_lines)}
""")
    
    # Brand voice
    if ctx.brand_voice:
        bv = ctx.brand_voice
        sections.append(f"""
🎨 STYLE DE RÉPONSE:
- Ton: {bv.tone}
- Style: {bv.language_style}
- Maximum: {bv.max_sentences} phrases
- Emojis: {bv.emoji_usage}
""")
    
    if not sections:
        return "❌ Contexte vendeur incomplet. Utilise principalement le contexte visuel."
    
    return "".join(sections)


def build_full_prompt(
    base_prompt: str,
    post_summary: str,
    comment_text: str,
    seller_context: Optional[SellerContext] = None
) -> str:
    """Build the complete prompt with all context."""
    
    context_string = build_seller_context_string(seller_context)
    
    prompt = base_prompt.replace("{{SELLER_CONTEXT}}", context_string)
    prompt = prompt.replace("{{POST_SUMMARY}}", post_summary)
    prompt = prompt.replace("{{COMMENT_TEXT}}", comment_text)
    
    return prompt
'''


# ═══════════════════════════════════════════════════════════════════════════════
# PYTHON IMPLEMENTATION - FULL FASTAPI SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

FASTAPI_FULL_SERVICE = '''
"""
Roborder AI Reply Service - Enhanced with Knowledge Base
FastAPI implementation with optional seller context
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from anthropic import Anthropic
import httpx
import base64
import json
import hashlib
from datetime import datetime
import redis

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Roborder AI Reply Service",
    description="Multimodal Instagram comment reply generator with optional knowledge base",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.roborder.ai"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Initialize clients
anthropic_client = Anthropic()
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class ProductContext(BaseModel):
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    regular_price: Optional[float] = None
    sale_price: Optional[float] = None
    currency: str = "TND"
    sizes_available: List[str] = []
    colors_available: List[str] = []
    stock_status: Optional[str] = None


class ShippingInfo(BaseModel):
    zone: Optional[str] = None
    cost: Optional[float] = None
    time: Optional[str] = None
    free_above: Optional[float] = None


class BrandVoice(BaseModel):
    tone: str = "professional_friendly"
    language_style: str = "french"
    max_sentences: int = 2
    emoji_usage: str = "minimal"


class SellerContext(BaseModel):
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    instagram_handle: Optional[str] = None
    business_type: Optional[str] = None
    product_context: Optional[ProductContext] = None
    shipping: Optional[ShippingInfo] = None
    payment_methods: List[str] = []
    return_policy: Optional[str] = None
    active_promotions: List[Dict[str, Any]] = []
    faq_matches: List[Dict[str, Any]] = []
    brand_voice: Optional[BrandVoice] = None


class ReplyRequest(BaseModel):
    post_id: str
    post_summary: str
    comment_text: str
    image_urls: List[str] = []
    language: str = "fr"
    seller_context: Optional[SellerContext] = None


class ReplyResponse(BaseModel):
    reply: str
    confidence: float
    detected_intents: List[str]
    language_used: str
    context_used: Dict[str, bool]
    fallback_used: bool
    processing_time_ms: int


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT_FR = """
Tu es le propriétaire du compte Instagram qui répond personnellement aux commentaires.

═══ CONTEXTE BUSINESS ═══
{seller_context}

═══ RÈGLES ═══
- Maximum 2 phrases courtes
- Si tu as les infos exactes → utilise-les
- Si tu n\'as pas les infos → invite au DM
- Ne jamais inventer de prix ou détails
- Ton professionnel mais chaleureux
- Pas de liens, hashtags
- Tu n\'es PAS un assistant/bot

═══ RÉSUMÉ DU POST ═══
{post_summary}

═══ COMMENTAIRE ═══
{comment_text}

Génère la meilleure réponse possible.
"""

SYSTEM_PROMPT_TN = """
إنت صاحب الحساب وقاعد تجاوب على التعليقات.

═══ معلومات البزنس ═══
{seller_context}

═══ القواعد ═══
- Maximum جملتين
- كان عندك المعلومة → قولها
- كان ما عندكش → قول ابعث DM
- ما تخترعش أسعار
- ودّي ومحترف
- بلا روابط، بلا هاشتاقات

═══ ملخص البوست ═══
{post_summary}

═══ التعليق ═══
{comment_text}

أعطي أحسن جواب.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def build_seller_context_string(ctx: Optional[SellerContext]) -> str:
    """Build formatted seller context string."""
    if ctx is None:
        return "❌ Aucune information vendeur. Utilise le contexte visuel uniquement."
    
    parts = []
    
    if ctx.company_name:
        parts.append(f"🏪 {ctx.company_name} ({ctx.instagram_handle or ''})")
    
    if ctx.product_context:
        pc = ctx.product_context
        price = f"{pc.sale_price or pc.regular_price} {pc.currency}"
        if pc.sale_price and pc.regular_price:
            price = f"{pc.sale_price} {pc.currency} (soldé de {pc.regular_price})"
        parts.append(f"📦 Produit: {pc.product_name} - {price}")
        if pc.sizes_available:
            parts.append(f"   Tailles: {', '.join(pc.sizes_available)}")
        if pc.colors_available:
            parts.append(f"   Couleurs: {', '.join(pc.colors_available)}")
        parts.append(f"   Stock: {pc.stock_status or 'inconnu'}")
    
    if ctx.shipping:
        ship = ctx.shipping
        parts.append(f"🚚 Livraison {ship.zone or 'Tunisie'}: {ship.cost} DT, {ship.time}")
        if ship.free_above:
            parts.append(f"   Gratuit à partir de {ship.free_above} DT")
    
    if ctx.payment_methods:
        parts.append(f"💳 Paiement: {', '.join(ctx.payment_methods)}")
    
    if ctx.active_promotions:
        for promo in ctx.active_promotions:
            parts.append(f"🎁 {promo.get('name')}: {promo.get('discount')}")
    
    if ctx.faq_matches:
        parts.append("❓ FAQ:")
        for faq in ctx.faq_matches[:2]:
            parts.append(f"   → {faq.get('answer', '')[:100]}")
    
    return "\\n".join(parts) if parts else "Contexte limité disponible."


async def fetch_image_base64(url: str) -> Optional[str]:
    """Fetch image and convert to base64."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return base64.standard_b64encode(response.content).decode("utf-8")
    except Exception as e:
        print(f"Error fetching image: {e}")
    return None


def get_prompt_for_language(language: str) -> str:
    """Get the appropriate prompt template for the language."""
    prompts = {
        "fr": SYSTEM_PROMPT_FR,
        "en": SYSTEM_PROMPT_FR,  # Use French template, will respond in detected language
        "tn": SYSTEM_PROMPT_TN,
        "ar": SYSTEM_PROMPT_TN,
    }
    return prompts.get(language, SYSTEM_PROMPT_FR)


def detect_intents(comment: str) -> List[str]:
    """Quick intent detection based on keywords."""
    intents = []
    comment_lower = comment.lower()
    
    # Price indicators
    if any(w in comment_lower for w in ["combien", "prix", "سعر", "قداش", "price", "how much"]):
        intents.append("price_inquiry")
    
    # Availability
    if any(w in comment_lower for w in ["disponible", "stock", "موجود", "available"]):
        intents.append("availability_check")
    
    # Size
    if any(w in comment_lower for w in ["taille", "size", "قياس", "مقاس"]):
        intents.append("size_question")
    
    # Color
    if any(w in comment_lower for w in ["couleur", "color", "لون", "noir", "blanc", "rouge"]):
        intents.append("color_question")
    
    # Shipping
    if any(w in comment_lower for w in ["livraison", "delivery", "توصيل", "shipping"]):
        intents.append("shipping_inquiry")
    
    # Praise
    if any(w in comment_lower for w in ["beau", "magnifique", "😍", "❤️", "beautiful", "love"]):
        intents.append("praise")
    
    # Order intent
    if any(w in comment_lower for w in ["commander", "acheter", "نشري", "order", "buy"]):
        intents.append("order_intent")
    
    return intents if intents else ["general"]


def validate_reply(reply: str) -> bool:
    """Validate the generated reply."""
    # Check length
    if len(reply.split('.')) > 3:
        return False
    
    # Check for forbidden patterns
    forbidden = ["http", "www.", "#", "AI", "automated", "bot", "assistant"]
    if any(f.lower() in reply.lower() for f in forbidden):
        return False
    
    # Check character limit
    if len(reply) > 350:
        return False
    
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/api/v1/generate-reply", response_model=ReplyResponse)
async def generate_reply(request: ReplyRequest):
    """Generate a contextual reply to an Instagram comment."""
    
    import time
    start_time = time.time()
    
    # Build context
    seller_context_string = build_seller_context_string(request.seller_context)
    has_context = request.seller_context is not None
    
    # Get prompt template
    prompt_template = get_prompt_for_language(request.language)
    system_prompt = prompt_template.format(
        seller_context=seller_context_string,
        post_summary=request.post_summary,
        comment_text=request.comment_text
    )
    
    # Build message content with images
    content = []
    
    for url in request.image_urls[:3]:  # Limit to 3 images
        image_data = await fetch_image_base64(url)
        if image_data:
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            })
    
    content.append({
        "type": "text",
        "text": "Génère une réponse à ce commentaire basée sur l\'image et le contexte fourni."
    })
    
    # Call Claude
    try:
        response = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            system=system_prompt,
            messages=[{"role": "user", "content": content}]
        )
        
        reply_text = response.content[0].text.strip()
        
        # Validate and potentially regenerate
        if not validate_reply(reply_text):
            # Simplified retry with stricter prompt
            response = anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=150,
                system=system_prompt + "\\n\\nIMPORTANT: Réponse TRÈS courte, 1-2 phrases seulement!",
                messages=[{"role": "user", "content": content}]
            )
            reply_text = response.content[0].text.strip()
        
        # Detect intents
        intents = detect_intents(request.comment_text)
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)
        
        return ReplyResponse(
            reply=reply_text,
            confidence=0.9 if has_context else 0.7,
            detected_intents=intents,
            language_used=request.language,
            context_used={
                "image_context": len(request.image_urls) > 0,
                "product_catalog": request.seller_context.product_context is not None if request.seller_context else False,
                "shipping_policies": request.seller_context.shipping is not None if request.seller_context else False,
                "faq_matched": len(request.seller_context.faq_matches) > 0 if request.seller_context else False,
                "brand_voice": request.seller_context.brand_voice is not None if request.seller_context else False,
            },
            fallback_used=not has_context,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "2.0.0"}


# ═══════════════════════════════════════════════════════════════════════════════
# RUN SERVER
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE API CALLS
# ═══════════════════════════════════════════════════════════════════════════════

EXAMPLE_REQUESTS = """
# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE API REQUESTS
# ═══════════════════════════════════════════════════════════════════════════════

# Example 1: Full context available
curl -X POST https://your-api.com/api/v1/generate-reply \\
  -H "Content-Type: application/json" \\
  -d '{
    "post_id": "post_123",
    "post_summary": "Nouvelle collection robes été 2025",
    "comment_text": "C est combien la robe noire? Vous livrez à Sfax?",
    "image_urls": ["https://instagram.com/cdn/img.jpg"],
    "language": "fr",
    "seller_context": {
      "company_name": "Bella Mode",
      "instagram_handle": "@bellamode.tn",
      "product_context": {
        "product_name": "Robe Élégance",
        "regular_price": 89,
        "sale_price": 69,
        "currency": "TND",
        "sizes_available": ["S", "M", "L"],
        "colors_available": ["Noir", "Blanc"],
        "stock_status": "in_stock"
      },
      "shipping": {
        "zone": "Sfax",
        "cost": 8,
        "time": "2-3 jours",
        "free_above": 150
      },
      "payment_methods": ["COD", "D17"],
      "active_promotions": [
        {"name": "Soldes Été", "discount": "20%"}
      ]
    }
  }'

# Response:
{
  "reply": "La robe noire est à 69 DT en solde! On livre à Sfax en 2-3 jours pour 8 DT.",
  "confidence": 0.95,
  "detected_intents": ["price_inquiry", "shipping_inquiry"],
  "context_used": {
    "image_context": true,
    "product_catalog": true,
    "shipping_policies": true
  }
}

# ═══════════════════════════════════════════════════════════════════════════════

# Example 2: No context (fallback mode)
curl -X POST https://your-api.com/api/v1/generate-reply \\
  -H "Content-Type: application/json" \\
  -d '{
    "post_id": "post_456",
    "post_summary": "Nouveau produit disponible",
    "comment_text": "C est combien?",
    "image_urls": ["https://instagram.com/cdn/img2.jpg"],
    "language": "fr",
    "seller_context": null
  }'

# Response:
{
  "reply": "Envoie-nous un DM pour avoir tous les détails et le prix!",
  "confidence": 0.7,
  "detected_intents": ["price_inquiry"],
  "fallback_used": true
}

# ═══════════════════════════════════════════════════════════════════════════════

# Example 3: Tunisian Arabic
curl -X POST https://your-api.com/api/v1/generate-reply \\
  -H "Content-Type: application/json" \\
  -d '{
    "post_id": "post_789",
    "post_summary": "عرض خاص على الفساتين",
    "comment_text": "قداش الثمن؟ وتوصلو للقيروان؟",
    "image_urls": ["https://instagram.com/cdn/img3.jpg"],
    "language": "tn",
    "seller_context": {
      "company_name": "Bella Mode",
      "product_context": {
        "product_name": "فستان صيفي",
        "sale_price": 69,
        "currency": "TND"
      },
      "shipping": {
        "zone": "القيروان",
        "cost": 10,
        "time": "3-5 أيام"
      }
    }
  }'

# Response:
{
  "reply": "الثمن 69 دينار! نوصلو للقيروان في 3-5 أيام بـ10 دينار. ابعثلنا DM!",
  "confidence": 0.9,
  "language_used": "tn"
}
"""