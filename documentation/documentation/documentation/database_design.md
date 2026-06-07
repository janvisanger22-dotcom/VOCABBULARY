
# Database Design — VOGUEABULARY
 Summary
The database system manages user data, clothing items, and outfit recommendations. It supports backend processing and AI-based suggestions.

## 1. Overview
The database system stores all user data, clothing items, outfit recommendations, and history. It supports backend processing and AI-based recommendations.

---

## 2. Tables

### User Table
user_id (Primary Key)
name
email
password
style_preference

---

### Clothing Table
item_id (Primary Key)
user_id (Foreign Key)
type (Shirt, Jeans)
color
category (Top, Bottom, Shoes)
season
image

---

### Outfit Table
outfit_id (Primary Key)
user_id (Foreign Key)
items_selected
occasion
date_created

---

### History Table
history_id (Primary Key)
user_id
outfit_id
date

---

## 3. Relationships

- One user → many clothing items
- One user → many outfits
- One outfit → many clothing items
- History stores previous recommendations

---

## 4. Storage Concept

- Data stored in MongoDB / Firebase (conceptual)
- Images stored in cloud storage (Cloudinary)
- Backend (Harman) retrieves and stores data

---

## 5. Integration with Backend

- Backend fetches wardrobe data from database
- Backend sends data to AI system
- AI returns outfit recommendation
- Backend saves result in database
- Result is shown to user

---

## 6. System Flow

User → Frontend → Backend → Database → AI → Output
