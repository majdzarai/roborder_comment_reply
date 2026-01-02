# CLAUDE.md — Roborder AI Comment Reply System (Enhanced Edition)

## Version: 2.0 — Knowledge-Enriched Architecture

**Client:** Roborder (Tunisian SaaS Company)  
**Website:** https://app.roborder.ai  
**Target Markets:** Tunisia & France  
**Languages:** French, Arabic (Tunisian Dialect), English  
**Project Type:** Freelance Integration — Multimodal AI Reply Service with Seller Knowledge Base

---

## 🎯 What's New in This Version

This enhanced system introduces an **optional Seller Knowledge Base** that provides deep context about each business. When available, the AI uses this data to:

- Answer product questions with exact prices and specs
- Reference real store policies (shipping, returns, payment methods)
- Mention actual product names and collections
- Provide accurate availability information
- Maintain brand voice consistency
- Handle edge cases with business-specific logic

**Key Principle:** The knowledge base is **OPTIONAL**. If data exists, use it. If not, fall back to standard context-based replies.

---

## 🏗️ System Architecture (Enhanced)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ROBORDER ENHANCED ECOSYSTEM                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    SELLER KNOWLEDGE BASE (Optional)                 │   │
│   │                                                                     │   │
│   │   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │   │
│   │   │   Company   │ │  Products   │ │   Policies  │ │    FAQ      │   │   │
│   │   │   Profile   │ │  Catalog    │ │   & Rules   │ │  Database   │   │   │
│   │   └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │   │
│   │                                                                     │   │
│   │   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │   │
│   │   │   Brand     │ │  Pricing    │ │  Shipping   │ │   Custom    │   │   │
│   │   │   Voice     │ │  Rules      │ │   Zones     │ │   Replies   │   │   │
│   │   └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      AI REPLY SERVICE (Python/FastAPI)              │   │
│   │                                                                     │   │
│   │   INPUTS:                          PROCESSING:                      │   │
│   │   ├─ Post Image(s)                 ├─ Visual Analysis               │   │
│   │   ├─ Post Summary                  ├─ Intent Classification         │   │
│   │   ├─ Comment Text                  ├─ Knowledge Base Query          │   │
│   │   ├─ Language                      ├─ Context Enrichment            │   │
│   │   └─ Seller Context (optional)     └─ Reply Generation              │   │
│   │                                                                     │   │
│   │   OUTPUT:                                                           │   │
│   │   └─ Highly Accurate, Personalized Reply                            │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Seller Knowledge Base Schema

### 1. Company Profile (`company_profile`)

```json
{
  "company_id": "seller_123",
  "company_name": "Bella Mode Tunisia",
  "instagram_handle": "@bellamode.tn",
  "business_type": "fashion_retail",
  "description": "Boutique de mode féminine tendance, spécialisée dans les robes et ensembles pour femmes modernes.",
  "founded_year": 2020,
  "location": {
    "city": "Tunis",
    "governorate": "Tunis",
    "country": "Tunisia"
  },
  "contact": {
    "phone": "+216 XX XXX XXX",
    "whatsapp": "+216 XX XXX XXX",
    "email": "contact@bellamode.tn"
  },
  "social_links": {
    "instagram": "https://instagram.com/bellamode.tn",
    "facebook": "https://facebook.com/bellamode.tn",
    "tiktok": null
  },
  "brand_voice": {
    "tone": "friendly_professional",
    "formality": "semi_formal",
    "emoji_usage": "minimal",
    "language_preference": "french_with_tunisian_mix"
  },
  "working_hours": {
    "weekdays": "09:00-19:00",
    "saturday": "09:00-14:00",
    "sunday": "closed"
  }
}
```

### 2. Product Catalog (`products`)

```json
{
  "products": [
    {
      "product_id": "prod_001",
      "name": "Robe Élégance Été",
      "name_ar": "فستان أناقة الصيف",
      "category": "robes",
      "subcategory": "robes_été",
      "description": "Robe longue fluide parfaite pour l'été tunisien",
      "prices": {
        "regular": 89,
        "sale": 69,
        "currency": "TND"
      },
      "sizes": ["S", "M", "L", "XL"],
      "colors": [
        {"name": "Noir", "hex": "#000000", "available": true},
        {"name": "Blanc", "hex": "#FFFFFF", "available": true},
        {"name": "Rouge", "hex": "#FF0000", "available": false}
      ],
      "stock_status": "in_stock",
      "images": [
        "https://cdn.bellamode.tn/prod_001_1.jpg",
        "https://cdn.bellamode.tn/prod_001_2.jpg"
      ],
      "tags": ["été", "élégant", "mariage", "soirée"],
      "featured": true,
      "best_seller": true
    },
    {
      "product_id": "prod_002",
      "name": "Ensemble Casual Chic",
      "category": "ensembles",
      "prices": {
        "regular": 120,
        "sale": null,
        "currency": "TND"
      },
      "sizes": ["M", "L"],
      "colors": [
        {"name": "Beige", "available": true}
      ],
      "stock_status": "low_stock",
      "low_stock_threshold": 3
    }
  ]
}
```

### 3. Policies & Rules (`policies`)

```json
{
  "shipping": {
    "methods": [
      {
        "name": "Livraison Standard",
        "carrier": "Aramex",
        "delivery_time": "2-4 jours",
        "cost": 7,
        "currency": "TND",
        "free_above": 150
      },
      {
        "name": "Livraison Express",
        "carrier": "Fedex",
        "delivery_time": "24h",
        "cost": 15,
        "currency": "TND"
      }
    ],
    "zones": {
      "tunis": {"cost": 7, "time": "1-2 jours"},
      "sfax": {"cost": 8, "time": "2-3 jours"},
      "sousse": {"cost": 8, "time": "2-3 jours"},
      "other": {"cost": 10, "time": "3-5 jours"}
    },
    "international": {
      "available": false,
      "countries": []
    }
  },
  "payment": {
    "methods": [
      {"type": "cod", "name": "Paiement à la livraison", "available": true},
      {"type": "bank_transfer", "name": "Virement bancaire", "available": true},
      {"type": "card", "name": "Carte bancaire", "available": false},
      {"type": "d17", "name": "D17", "available": true}
    ],
    "cod_extra_fee": 0,
    "installments": {
      "available": false
    }
  },
  "returns": {
    "accepted": true,
    "window_days": 7,
    "conditions": "Produit non porté, étiquettes intactes",
    "exchange_only": true,
    "refund_available": false,
    "return_shipping_paid_by": "customer"
  },
  "sizing": {
    "guide_url": "https://bellamode.tn/guide-tailles",
    "custom_sizing": false,
    "size_exchange_free": true
  }
}
```

### 4. FAQ Database (`faq`)

```json
{
  "faqs": [
    {
      "id": "faq_001",
      "question_patterns": ["comment commander", "how to order", "كيفاش نكوموندي"],
      "category": "ordering",
      "answer_fr": "Pour commander, envoyez-nous un DM avec le produit souhaité et votre taille. On vous contactera pour confirmer!",
      "answer_tn": "ابعثلنا DM بالمنتج والتاي متاعك ونتواصلو معاك!",
      "priority": "high"
    },
    {
      "id": "faq_002",
      "question_patterns": ["livraison", "delivery", "توصيل", "délai"],
      "category": "shipping",
      "answer_fr": "Livraison partout en Tunisie en 2-4 jours. Gratuite à partir de 150 DT!",
      "answer_tn": "نوصلو لكل تونس في 2-4 أيام. التوصيل مجاني من 150 دينار!",
      "priority": "high"
    },
    {
      "id": "faq_003",
      "question_patterns": ["paiement", "payment", "خلاص", "cod"],
      "category": "payment",
      "answer_fr": "Paiement à la livraison (COD), virement bancaire ou D17.",
      "answer_tn": "تخلص عند التوصيل، virement ولا D17.",
      "priority": "medium"
    },
    {
      "id": "faq_004",
      "question_patterns": ["retour", "échange", "return", "ترجيع"],
      "category": "returns",
      "answer_fr": "Échange possible dans les 7 jours si le produit est intact avec ses étiquettes.",
      "answer_tn": "تنجم تبدل في 7 أيام كان المنتج مزال جديد.",
      "priority": "medium"
    },
    {
      "id": "faq_005",
      "question_patterns": ["taille", "size", "قياس", "mesure"],
      "category": "sizing",
      "answer_fr": "Consultez notre guide des tailles en DM. Si la taille ne convient pas, échange gratuit!",
      "answer_tn": "ابعثلنا DM نعطيوك القياسات. وكان ما جاتكش التاي نبدلوها مجانا!",
      "priority": "high"
    }
  ]
}
```

### 5. Pricing Rules (`pricing_rules`)

```json
{
  "currency": "TND",
  "display_format": "{price} DT",
  "promotions": {
    "active": [
      {
        "id": "promo_001",
        "name": "Soldes Été 2025",
        "type": "percentage",
        "value": 20,
        "applies_to": "category:robes_été",
        "start_date": "2025-06-01",
        "end_date": "2025-08-31",
        "code": null
      },
      {
        "id": "promo_002",
        "name": "Nouveau Client",
        "type": "fixed",
        "value": 10,
        "applies_to": "first_order",
        "code": "BIENVENUE10"
      }
    ]
  },
  "bundle_deals": [
    {
      "name": "Pack Été Complet",
      "products": ["prod_001", "prod_005"],
      "bundle_price": 140,
      "regular_total": 169,
      "savings": 29
    }
  ],
  "loyalty": {
    "enabled": false
  }
}
```

### 6. Custom Reply Templates (`custom_replies`)

```json
{
  "templates": [
    {
      "id": "tmpl_001",
      "trigger": "out_of_stock",
      "template_fr": "Ce modèle est épuisé pour le moment, mais on attend un réassort bientôt! Laisse ton DM et on te prévient.",
      "template_tn": "هذا الموديل خلى، أما باش يرجع قريب! ابعثلنا DM ونعلموك.",
      "use_when": "product.stock_status == 'out_of_stock'"
    },
    {
      "id": "tmpl_002",
      "trigger": "price_negotiation",
      "template_fr": "Nos prix sont fixes, mais on a souvent des promos! Suivez-nous pour ne rien rater.",
      "template_tn": "السوم ثابت، أما تابعونا على الصولد!",
      "use_when": "intent == 'negotiate_price'"
    },
    {
      "id": "tmpl_003",
      "trigger": "closing_hours",
      "template_fr": "On est actuellement fermés, mais on répond à vos DMs dès demain matin!",
      "template_tn": "مسكرين توا، أما غدوة الصباح نجاوبوك!",
      "use_when": "current_time.is_outside_working_hours"
    }
  ],
  "signature": {
    "enabled": false,
    "text": "— L'équipe Bella Mode 💕"
  }
}
```

### 7. Brand Voice Configuration (`brand_voice`)

```json
{
  "personality": {
    "traits": ["friendly", "professional", "helpful", "modern"],
    "avoid": ["aggressive", "pushy", "overly_casual", "slang"]
  },
  "language_rules": {
    "primary_language": "fr",
    "allow_code_switching": true,
    "code_switch_style": "natural_tunisian_french_mix",
    "formality_level": 0.6,
    "emoji_frequency": "rare",
    "allowed_emojis": ["😊", "💕", "✨", "🙏"],
    "banned_words": ["arnaque", "cheap", "pas cher"],
    "preferred_phrases": [
      "Avec plaisir",
      "N'hésitez pas",
      "On est là pour vous"
    ]
  },
  "response_style": {
    "max_sentences": 2,
    "max_characters": 300,
    "include_cta": "when_appropriate",
    "cta_types": ["dm_invite", "follow_invite"],
    "never_include": ["links", "hashtags", "price_without_context"]
  },
  "owner_persona": {
    "name": "Sonia",
    "gender": "female",
    "speaks_as": "owner",
    "first_person": true
  }
}
```

---

## 🔄 Context Resolution Logic

The system follows this priority when generating replies:

```
┌─────────────────────────────────────────────────────────────────┐
│                   CONTEXT RESOLUTION FLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ALWAYS AVAILABLE (Required)                                │
│      ├─ Post Image(s)                                           │
│      ├─ Post Caption/Summary                                    │
│      └─ Comment Text                                            │
│                                                                 │
│   2. IF KNOWLEDGE BASE EXISTS (Optional - Use if available)     │
│      │                                                          │
│      ├─ Is this a product question?                             │
│      │   └─ YES → Query products catalog for exact info         │
│      │                                                          │
│      ├─ Is this a policy question (shipping/payment/returns)?   │
│      │   └─ YES → Use policies data                             │
│      │                                                          │
│      ├─ Is this a common FAQ?                                   │
│      │   └─ YES → Use FAQ answer as base                        │
│      │                                                          │
│      ├─ Is there an active promotion?                           │
│      │   └─ YES → Mention if relevant                           │
│      │                                                          │
│      └─ Apply brand voice rules                                 │
│                                                                 │
│   3. IF NO KNOWLEDGE BASE                                       │
│      └─ Fall back to image + caption context only               │
│          (Standard reply generation)                            │
│                                                                 │
│   4. GENERATE REPLY                                             │
│      └─ Combine all available context                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📥 Enhanced API Specification

### Request Payload (Full)

```json
{
  "post_id": "post_789",
  "post_summary": "Nouvelle collection robes été 2025 - Modèles disponibles de S à XL",
  "comment_text": "C'est combien la robe noire? Vous livrez à Sfax?",
  "image_urls": [
    "https://instagram.com/cdn/image1.jpg"
  ],
  "language": "fr",
  
  "seller_context": {
    "company_id": "seller_123",
    "company_name": "Bella Mode Tunisia",
    "instagram_handle": "@bellamode.tn",
    
    "product_context": {
      "product_id": "prod_001",
      "product_name": "Robe Élégance Été",
      "price": 89,
      "sale_price": 69,
      "currency": "TND",
      "sizes_available": ["S", "M", "L", "XL"],
      "colors_available": ["Noir", "Blanc"],
      "stock_status": "in_stock"
    },
    
    "policies": {
      "shipping_to_sfax": {
        "available": true,
        "cost": 8,
        "time": "2-3 jours"
      },
      "payment_methods": ["COD", "Virement", "D17"],
      "free_shipping_above": 150
    },
    
    "brand_voice": {
      "tone": "friendly_professional",
      "language_mix": "french_tunisian",
      "max_sentences": 2,
      "emoji_usage": "minimal"
    },
    
    "active_promotions": [
      {
        "name": "Soldes Été",
        "discount": "20%",
        "applies_to": "robes_été"
      }
    ],
    
    "faq_matches": [
      {
        "question": "livraison sfax",
        "answer": "Oui on livre à Sfax en 2-3 jours pour 8 DT!"
      }
    ]
  }
}
```

### Request Payload (Minimal - No Knowledge Base)

```json
{
  "post_id": "post_789",
  "post_summary": "Nouvelle collection robes été",
  "comment_text": "C'est combien?",
  "image_urls": ["https://instagram.com/cdn/image1.jpg"],
  "language": "fr",
  
  "seller_context": null
}
```

### Response Payload

```json
{
  "reply": "La robe noire est à 69 DT (en solde!). Oui on livre à Sfax en 2-3 jours pour 8 DT. Envoie-nous un DM pour commander!",
  "confidence": 0.95,
  "detected_intent": ["price_inquiry", "shipping_inquiry"],
  "language_used": "fr",
  "context_used": {
    "image_context": true,
    "product_catalog": true,
    "shipping_policies": true,
    "faq_matched": true,
    "promotion_mentioned": true
  },
  "fallback_used": false
}
```

---

## 🧠 Intent Detection Categories

| Intent | Trigger Patterns | Knowledge Base Query |
|--------|------------------|---------------------|
| `price_inquiry` | "combien", "prix", "سعر", "قداش" | `products.prices` |
| `availability_check` | "disponible", "en stock", "موجود" | `products.stock_status` |
| `size_question` | "taille", "قياس", "size" | `products.sizes` |
| `color_question` | "couleur", "لون", "noir", "blanc" | `products.colors` |
| `shipping_inquiry` | "livraison", "توصيل", "délai" | `policies.shipping` |
| `payment_question` | "paiement", "خلاص", "COD" | `policies.payment` |
| `return_question` | "retour", "échange", "ترجيع" | `policies.returns` |
| `order_intent` | "commander", "acheter", "نشري" | → Redirect to DM |
| `praise` | "beau", "magnifique", "😍" | → Thank warmly |
| `complaint` | "problème", "مشكل", "arnaque" | → Handle carefully |
| `negotiation` | "moins cher", "نقص", "discount" | `custom_replies.price_negotiation` |

---

## 🔧 Implementation Details

### Knowledge Base Storage Options

**Option 1: JSON Files (Simple)**
```
/data/sellers/
  ├── seller_123/
  │   ├── profile.json
  │   ├── products.json
  │   ├── policies.json
  │   ├── faq.json
  │   └── brand_voice.json
  └── seller_456/
      └── ...
```

**Option 2: Database (Scalable)**
```sql
-- PostgreSQL / Supabase Schema
CREATE TABLE sellers (
  id UUID PRIMARY KEY,
  company_name TEXT,
  instagram_handle TEXT,
  profile JSONB,
  brand_voice JSONB
);

CREATE TABLE products (
  id UUID PRIMARY KEY,
  seller_id UUID REFERENCES sellers(id),
  name TEXT,
  prices JSONB,
  sizes TEXT[],
  colors JSONB,
  stock_status TEXT
);

CREATE TABLE policies (
  seller_id UUID REFERENCES sellers(id),
  shipping JSONB,
  payment JSONB,
  returns JSONB
);
```

**Option 3: Vector Database (Advanced - Semantic Search)**
```python
# Using Pinecone/Weaviate for semantic FAQ matching
from pinecone import Pinecone

# Store FAQ embeddings
faq_embedding = embed("comment commander")
index.upsert([(faq_id, faq_embedding, {"answer": "..."})])

# Query similar questions
results = index.query(embed(user_comment), top_k=3)
```

### Context Injection Strategy

```python
def build_context_prompt(request: ReplyRequest) -> str:
    """Build the full context prompt with optional knowledge base."""
    
    # Base context (always available)
    context = f"""
POST SUMMARY:
{request.post_summary}

COMMENT:
{request.comment_text}
"""
    
    # Optional: Seller context enrichment
    if request.seller_context:
        sc = request.seller_context
        
        context += f"""

SELLER INFORMATION:
- Company: {sc.company_name} ({sc.instagram_handle})
"""
        
        # Product context
        if sc.product_context:
            pc = sc.product_context
            context += f"""
PRODUCT DETAILS:
- Name: {pc.product_name}
- Price: {pc.price} {pc.currency}
- Sale Price: {pc.sale_price} {pc.currency if pc.sale_price else 'N/A'}
- Sizes Available: {', '.join(pc.sizes_available)}
- Colors: {', '.join(pc.colors_available)}
- Stock: {pc.stock_status}
"""
        
        # Shipping context
        if sc.policies and sc.policies.get('shipping_to_sfax'):
            ship = sc.policies['shipping_to_sfax']
            context += f"""
SHIPPING INFO:
- Delivers to customer location: Yes
- Cost: {ship['cost']} DT
- Time: {ship['time']}
- Free shipping above: {sc.policies.get('free_shipping_above', 'N/A')} DT
"""
        
        # Active promotions
        if sc.active_promotions:
            context += "\nACTIVE PROMOTIONS:\n"
            for promo in sc.active_promotions:
                context += f"- {promo['name']}: {promo['discount']} off {promo['applies_to']}\n"
        
        # FAQ matches
        if sc.faq_matches:
            context += "\nRELEVANT FAQ ANSWERS:\n"
            for faq in sc.faq_matches:
                context += f"- Q: {faq['question']} → A: {faq['answer']}\n"
        
        # Brand voice
        if sc.brand_voice:
            bv = sc.brand_voice
            context += f"""
BRAND VOICE RULES:
- Tone: {bv['tone']}
- Language style: {bv['language_mix']}
- Max sentences: {bv['max_sentences']}
- Emoji usage: {bv['emoji_usage']}
"""
    
    return context
```

---

## 📋 Example Scenarios

### Scenario 1: Full Context Available

**Input:**
```json
{
  "comment_text": "C'est combien la robe noire? Vous livrez à Sfax?",
  "seller_context": {
    "product_context": {"price": 89, "sale_price": 69},
    "policies": {"shipping_to_sfax": {"cost": 8, "time": "2-3 jours"}}
  }
}
```

**Output:**
```
"La robe noire est à 69 DT en ce moment. On livre à Sfax en 2-3 jours pour 8 DT!"
```

### Scenario 2: Partial Context (No Product Match)

**Input:**
```json
{
  "comment_text": "C'est combien la robe noire?",
  "seller_context": {
    "company_name": "Bella Mode",
    "product_context": null
  }
}
```

**Output:**
```
"Envoie-nous un DM avec une capture de la robe qui t'intéresse et on te donne tous les détails!"
```

### Scenario 3: No Context (Fallback Mode)

**Input:**
```json
{
  "comment_text": "C'est combien?",
  "seller_context": null
}
```

**Output:**
```
"Le prix est affiché dans la description. N'hésite pas à nous écrire en DM pour plus d'infos!"
```

### Scenario 4: Out of Stock Product

**Input:**
```json
{
  "comment_text": "Vous avez en rouge?",
  "seller_context": {
    "product_context": {
      "colors": [{"name": "Rouge", "available": false}]
    }
  }
}
```

**Output:**
```
"Le rouge est épuisé pour le moment, mais on attend un réassort bientôt! Laisse-nous ton DM et on te prévient."
```

### Scenario 5: Tunisian Arabic with Context

**Input:**
```json
{
  "comment_text": "قداش الثمن؟ وتوصلو للقيروان؟",
  "language": "tn",
  "seller_context": {
    "product_context": {"price": 89, "sale_price": 69},
    "policies": {"shipping": {"other": {"cost": 10, "time": "3-5 jours"}}}
  }
}
```

**Output:**
```
"الثمن 69 دينار (صولد!). نوصلو للقيروان في 3-5 أيام بـ10 دينار. ابعثلنا DM!"
```

---

## 🛠️ Roborder Integration Guide

### For Roborder's Backend Team

**Minimal Integration (No Changes Needed):**
```javascript
// Roborder's existing code
const reply = await fetch('https://your-ai-service.com/api/v1/generate-reply', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    post_id: postId,
    post_summary: postSummary,
    comment_text: comment.text,
    image_urls: post.images,
    language: detectedLanguage,
    seller_context: null  // Works without context!
  })
});
```

**Enhanced Integration (With Context):**
```javascript
// Roborder fetches seller data and passes it
const sellerData = await db.getSeller(sellerId);
const productMatch = await db.findProductByImage(postImageUrl);

const reply = await fetch('https://your-ai-service.com/api/v1/generate-reply', {
  method: 'POST',
  body: JSON.stringify({
    post_id: postId,
    post_summary: postSummary,
    comment_text: comment.text,
    image_urls: post.images,
    language: detectedLanguage,
    seller_context: {
      company_id: sellerData.id,
      company_name: sellerData.name,
      product_context: productMatch,
      policies: sellerData.policies,
      brand_voice: sellerData.brandVoice,
      faq_matches: await matchFAQ(comment.text, sellerData.faqs)
    }
  })
});
```

---

## 📈 Success Metrics

| Metric | Without Context | With Full Context |
|--------|-----------------|-------------------|
| Reply Accuracy | 70% | 95%+ |
| Price Accuracy | N/A | 100% |
| Policy Accuracy | Generic | Exact |
| Customer Satisfaction | Good | Excellent |
| Conversion to DM | 15% | 35%+ |
| Human Escalation | 20% | 5% |

---

## 🚀 Deployment Checklist

- [ ] Core API endpoint working
- [ ] Image processing functional
- [ ] French replies generating correctly
- [ ] Tunisian Arabic replies working
- [ ] Optional context injection working
- [ ] Fallback mode tested
- [ ] Response validation active
- [ ] Rate limiting configured
- [ ] Logging implemented
- [ ] Documentation complete
- [ ] Demo ready for Roborder

---

## 📞 Support & Maintenance

**Freelancer:** [Your Name]  
**Email:** [your@email.com]  
**Response Time:** 24-48h  
**Support Period:** 30 days post-delivery

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-02 | Initial documentation |
| 2.0.0 | 2026-01-02 | Added Knowledge Base system, enhanced context handling |