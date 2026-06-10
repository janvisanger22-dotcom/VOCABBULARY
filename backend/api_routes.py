"""
Backend API Routes — vougeabulary
Lead: Harman (Backend — Core API)

Defines all REST API endpoints.
Each route receives a JSON request, calls the appropriate
service layer, and returns a JSON response.

Endpoints:
  GET  /api/wardrobe           → list all wardrobe items
  POST /api/wardrobe           → add a new item
  DELETE /api/wardrobe/<id>   → remove an item
  POST /api/recommend          → get outfit recommendations
  POST /api/chat               → AI stylist message
  GET  /api/shop/<style>       → shopping info by style
"""

# ── System Flow Diagram ───────────────────────────────────────────────────────
#
#  [Browser] --POST /api/recommend--> [api_routes.py]
#                                          |
#                                 load wardrobe (database.py)
#                                          |
#                             build Wardrobe object (clothing_item.py)
#                                          |
#                         RecommendationEngine.recommend() (recommendation_engine.py)
#                                          |
#                                  serialize to JSON
#                                          |
#  [Browser] <---JSON response-----------[api_routes.py]
#
# ─────────────────────────────────────────────────────────────────────────────

# ── Request / Response Contracts ──────────────────────────────────────────────

"""
POST /api/recommend
  Request:
    {
      "temp":     int   — temperature in Celsius (e.g. 22)
      "occasion": str   — one of: casual, work, formal, party, sport
      "rain":     bool  — true if raining
    }
  Response:
    {
      "outfits": [
        {
          "score": float,
          "items": [
            { "role": str, "name": str, "color": str, "hex": str }
          ]
        }
      ],
      "empty": bool  — true if wardrobe has no items
    }

POST /api/chat
  Request:
    {
      "message":  str   — user's message
      "style":    str   — current style profile key
      "history":  list  — [{role, content}] last N messages
    }
  Response:
    {
      "response":   str — AI reply text (supports markdown bold + links)
      "powered_by": str — "Claude AI" or "Vouge AI"
    }

POST /api/wardrobe
  Request:
    {
      "name":      str
      "category":  str
      "color":     str
      "occasions": [str]
      "weather":   [str]
    }
  Response:
    { "success": true, "item": { ...saved item... } }

DELETE /api/wardrobe/<item_id>
  Response:
    { "success": true }

GET /api/shop/<style>
  Response:
    {
      "name": str, "emoji": str, "tagline": str,
      "description": str, "colors": [str],
      "brands": [str],
      "links": [
        {
          "term": str,
          "google": url, "asos": url,
          "pinterest": url, "depop": url
        }
      ]
    }
"""

# ── Error Response Format ─────────────────────────────────────────────────────
"""
All errors return:
  { "error": "human-readable message", "code": "ERROR_CODE" }

Error codes:
  EMPTY_WARDROBE      — no items in wardrobe
  VALIDATION_ERROR    — invalid field in request body
  NOT_FOUND           — item ID does not exist
  NO_RESULTS          — no outfits matched the criteria
  INTERNAL_ERROR      — unexpected server error
"""

# ── HTTP Status Codes Used ────────────────────────────────────────────────────
"""
200 OK           — successful GET or DELETE
201 Created      — successful POST (item added)
400 Bad Request  — validation error in request body
404 Not Found    — item ID not found
500 Server Error — unexpected exception
"""
