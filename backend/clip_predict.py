import torch
import clip
from PIL import Image
import os

# ── STEP 1: LOAD CLIP MODEL ──
# CLIP comes in different sizes. ViT-B/32 means:
# ViT = Vision Transformer (type of neural network)
# B = Base size (not too big, not too small)
# /32 = patch size of 32 pixels
# device = where to run it (cpu since we have no GPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading CLIP on {device}...")
model, preprocess = clip.load("ViT-B/32", device=device)
print("CLIP loaded!")

# ── STEP 2: DEFINE LANDMARKS WITH RICH DESCRIPTIONS ──
# This is the KEY to CLIP's accuracy
# Better descriptions = better recognition
# We give multiple angles of description
landmark_prompts = {
    "taj_mahal": [
        "a photo of Taj Mahal in Agra India",
        "white marble mausoleum Taj Mahal with reflecting pool",
        "Taj Mahal UNESCO world heritage site India"
    ],
    "red_fort": [
        "a photo of Red Fort in Delhi India",
        "Lal Qila red sandstone fort Delhi",
        "Red Fort historical monument India"
    ],
    "qutub_minar": [
        "a photo of Qutub Minar tower in Delhi India",
        "tall minaret Qutub Minar Delhi",
        "Qutub Minar UNESCO heritage site Delhi India"
    ],
    "india_gate": [
        "a photo of India Gate war memorial New Delhi",
        "India Gate arch monument Delhi India",
        "India Gate triumphal arch New Delhi"
    ],
    "charminar": [
        "a photo of Charminar mosque Hyderabad India",
        "four minarets Charminar monument Hyderabad",
        "Charminar historical landmark Hyderabad India"
    ],
    "hampi": [
        "a photo of Hampi ruins Karnataka India",
        "Vijayanagara empire ruins Hampi India",
        "ancient temple ruins Hampi Karnataka"
    ],
    "lotus_temple": [
        "a photo of Lotus Temple Delhi India",
        "Bahai Lotus Temple white petals New Delhi",
        "Lotus shaped temple Delhi India"
    ],
    "ajanta_caves": [
        "a photo of Ajanta Caves Maharashtra India",
        "Buddhist rock cut caves Ajanta India",
        "Ajanta cave paintings ancient India"
    ],
    "gateway_of_india": [
        "a photo of Gateway of India Mumbai",
        "Gateway of India arch monument Mumbai harbour",
        "Gateway of India historical monument Maharashtra"
    ],
    "virupaksha_temple": [
        "a photo of Virupaksha Temple Hampi Karnataka India",
        "ancient Virupaksha temple tower Hampi ruins",
        "Virupaksha temple UNESCO heritage Hampi India"
    ],
    "mysore_palace": [
        "a photo of Mysore Palace Karnataka India",
        "Amba Vilas Palace Mysore illuminated palace India",
        "Mysore Palace royal heritage building Karnataka"
    ],
    "gol_gumbaz": [
        "a photo of Gol Gumbaz Bijapur Karnataka India",
        "large dome mausoleum Gol Gumbaz Bijapur",
        "Gol Gumbaz whispering gallery monument Karnataka"
    ],
    "badami_caves": [
        "a photo of Badami Cave Temples Karnataka India",
        "rock cut cave temples Badami Chalukya Karnataka",
        "Badami caves ancient Hindu temple Karnataka India"
    ],
    "belur_temple": [
        "a photo of Chennakeshava Temple Belur Karnataka India",
        "Hoysala temple intricate carvings Belur Karnataka",
        "Belur temple star shaped Hoysala architecture India"
    ],
    "halebidu_temple": [
        "a photo of Hoysaleswara Temple Halebidu Karnataka India",
        "Halebidu twin temples Hoysala carvings Karnataka",
        "Halebidu temple detailed stone carvings India"
    ],
    "chitradurga_fort": [
        "a photo of Chitradurga Fort Karnataka India",
        "rocky hill fort Chitradurga Karnataka India",
        "Chitradurga fort stone walls Karnataka India"
    ],
    "gomateshwara": [
        "a photo of Gomateshwara statue Shravanabelagola Karnataka",
        "giant Bahubali monolithic statue Shravanabelagola India",
        "Gommateshwara Jain statue Karnataka India"
    ],
    "pattadakal": [
        "a photo of Pattadakal temples Karnataka India",
        "Chalukya temples UNESCO Pattadakal Karnataka",
        "ancient stone temples Pattadakal Karnataka India"
    ],
    "aihole_temples": [
        "a photo of Aihole temples Karnataka India",
        "ancient Chalukya rock temples Aihole Karnataka",
        "Aihole Durga temple Karnataka India"
    ],
    "bidar_fort": [
        "a photo of Bidar Fort Karnataka India",
        "medieval fort Bidar Bahmani sultanate Karnataka",
        "Bidar Fort ancient walls Karnataka India"
    ],
}

# ── STEP 3: LANDMARK INFO DATABASE ──
landmark_info = {
    "taj_mahal": {
        "name": "Taj Mahal",
        "location": "Agra, Uttar Pradesh, India",
        "history": "The Taj Mahal was built by Mughal emperor Shah Jahan between 1632 and 1653 in memory of his beloved wife Mumtaz Mahal. It took over 20,000 artisans to complete.",
        "facts": [
            "The Taj Mahal took 22 years to build.",
            "Over 1000 elephants carried the building materials.",
            "The marble changes color at different times of day.",
            "The four minarets are slightly tilted outward for safety.",
            "It became a UNESCO World Heritage Site in 1983."
        ],
        "culture": "The Taj Mahal is a symbol of eternal love and one of India's most treasured cultural icons."
    },
    "red_fort": {
        "name": "Red Fort",
        "location": "Delhi, India",
        "history": "Red Fort was built by Mughal Emperor Shah Jahan in 1639. It served as the main residence of Mughal emperors for nearly 200 years.",
        "facts": [
            "Red Fort took 10 years to build from 1639 to 1648.",
            "It is made of red sandstone which gives it its name.",
            "The fort has a perimeter of 2.5 km.",
            "India's Prime Minister hoists the flag here every Independence Day.",
            "It became a UNESCO World Heritage Site in 2007."
        ],
        "culture": "Red Fort is a symbol of India's rich Mughal heritage and national pride."
    },
    "qutub_minar": {
        "name": "Qutub Minar",
        "location": "Delhi, India",
        "history": "Qutub Minar was built in 1193 by Qutub-ud-din Aibak. It is the world's tallest brick minaret at 72.5 metres.",
        "facts": [
            "Qutub Minar is 72.5 metres tall.",
            "It has 379 steps inside.",
            "It was built in stages by different rulers.",
            "The Iron Pillar nearby has not rusted in 1600 years.",
            "It became a UNESCO World Heritage Site in 1993."
        ],
        "culture": "Qutub Minar represents the beginning of Islamic architecture in India."
    },
    "india_gate": {
        "name": "India Gate",
        "location": "New Delhi, India",
        "history": "India Gate was built in 1931 as a war memorial to honor 70,000 Indian soldiers who died in World War I.",
        "facts": [
            "India Gate is 42 metres tall.",
            "It was designed by Sir Edwin Lutyens.",
            "Names of 13,300 soldiers are inscribed on it.",
            "The Amar Jawan Jyoti flame burns continuously since 1972.",
            "It is one of the largest war memorials in India."
        ],
        "culture": "India Gate is a symbol of national pride and sacrifice."
    },
    "charminar": {
        "name": "Charminar",
        "location": "Hyderabad, Telangana, India",
        "history": "Charminar was built in 1591 by Muhammad Quli Qutb Shah to celebrate the end of a deadly plague.",
        "facts": [
            "Charminar means Four Minarets in Urdu.",
            "Each minaret is 56 metres tall.",
            "It was built to mark the end of a plague epidemic.",
            "There is a mosque on the top floor.",
            "It is surrounded by one of the largest bazaars in India."
        ],
        "culture": "Charminar is the icon of Hyderabad and represents its rich Islamic architectural heritage."
    },
    "hampi": {
        "name": "Hampi",
        "location": "Hampi, Karnataka, India",
        "history": "Hampi was the capital of the Vijayanagara Empire in the 14th to 16th centuries. It was one of the largest cities in the world at its peak.",
        "facts": [
            "Hampi was once the second largest city in the world after Beijing.",
            "The ruins spread over 4,100 hectares of land.",
            "Hampi has over 1,600 surviving remains.",
            "It became a UNESCO World Heritage Site in 1986.",
            "The Tungabhadra river flows alongside the ruins."
        ],
        "culture": "Hampi represents the golden age of South Indian culture, art and architecture."
    },
    "lotus_temple": {
        "name": "Lotus Temple",
        "location": "New Delhi, India",
        "history": "The Lotus Temple was built in 1986 and serves as the Bahai House of Worship. It was designed by Iranian architect Fariborz Sahba.",
        "facts": [
            "The Lotus Temple has 27 free-standing marble petals.",
            "It can accommodate up to 2,500 people at a time.",
            "People of all religions are welcome inside.",
            "It has won numerous architectural awards.",
            "It receives over 4 million visitors every year."
        ],
        "culture": "The Lotus Temple is a symbol of unity and peace welcoming people of all faiths."
    },
    "ajanta_caves": {
        "name": "Ajanta Caves",
        "location": "Aurangabad, Maharashtra, India",
        "history": "The Ajanta Caves are 30 rock-cut Buddhist cave monuments dating from the 2nd century BCE.",
        "facts": [
            "Ajanta Caves were carved out of solid rock over 2000 years ago.",
            "There are 30 caves in total.",
            "The paintings inside are masterpieces of Buddhist art.",
            "They were rediscovered by a British officer in 1819.",
            "They became a UNESCO World Heritage Site in 1983."
        ],
        "culture": "The Ajanta Caves represent the height of ancient Indian artistic achievement."
    },
    "gateway_of_india": {
        "name": "Gateway of India",
        "location": "Mumbai, Maharashtra, India",
        "history": "The Gateway of India was built in 1924 to commemorate the visit of King George V and Queen Mary to Mumbai in 1911.",
        "facts": [
            "The Gateway of India is 26 metres tall.",
            "It was built in Indo-Saracenic architectural style.",
            "The last British troops left India through this gate in 1948.",
            "It overlooks the Arabian Sea.",
            "It is one of the most visited monuments in India."
        ],
        "culture": "The Gateway of India is the iconic symbol of Mumbai."
    },
    "virupaksha_temple": {
        "name": "Virupaksha Temple",
        "location": "Hampi, Karnataka, India",
        "history": "The Virupaksha Temple is one of the oldest functioning temples in India, dedicated to Lord Shiva. It dates back to the 7th century and was the royal temple of the Vijayanagara Empire.",
        "facts": [
            "The main tower is 50 metres tall.",
            "The temple has been in continuous worship for over 1300 years.",
            "It is part of the UNESCO World Heritage Site of Hampi.",
            "The temple has a unique feature — an inverted image of the tower appears on the inner wall.",
            "Virupaksha means the lord with odd eyes referring to Lord Shiva."
        ],
        "culture": "Virupaksha Temple is the spiritual heart of Hampi and remains one of the most sacred pilgrimage sites in Karnataka."
    },
    "mysore_palace": {
        "name": "Mysore Palace",
        "location": "Mysore, Karnataka, India",
        "history": "Mysore Palace, also known as Amba Vilas Palace, was built between 1897 and 1912. It was the official residence of the Wadiyar dynasty who ruled the Kingdom of Mysore.",
        "facts": [
            "Mysore Palace is the second most visited monument in India after Taj Mahal.",
            "It is illuminated by nearly 100,000 bulbs every Sunday and on holidays.",
            "The palace took 15 years to build.",
            "It has 12 Hindu temples within its premises.",
            "The palace is a blend of Hindu, Muslim, Rajput and Gothic styles."
        ],
        "culture": "Mysore Palace is the symbol of Karnataka's royal heritage. The Dasara festival celebrated here every year is one of the most grand festivals in India."
    },
    "gol_gumbaz": {
        "name": "Gol Gumbaz",
        "location": "Bijapur, Karnataka, India",
        "history": "Gol Gumbaz is the mausoleum of Mohammed Adil Shah built in 1656. It has the second largest dome in the world after St. Peter's Basilica in Rome.",
        "facts": [
            "The dome diameter is 37.9 metres.",
            "It has a famous whispering gallery where sounds echo 7 times.",
            "Gol Gumbaz means round dome in Persian.",
            "The mausoleum took 30 years to build.",
            "It can accommodate 10,000 people inside."
        ],
        "culture": "Gol Gumbaz represents the architectural brilliance of the Adil Shahi dynasty and is the pride of north Karnataka."
    },
    "badami_caves": {
        "name": "Badami Cave Temples",
        "location": "Badami, Karnataka, India",
        "history": "The Badami Cave Temples were built by the Chalukya dynasty in the 6th and 7th centuries. They are rock-cut temples carved directly into sandstone cliffs.",
        "facts": [
            "There are four main cave temples at Badami.",
            "Cave 1 is dedicated to Shiva, Cave 2 and 3 to Vishnu, Cave 4 to Jain saints.",
            "The caves were built between 543 and 598 CE.",
            "Badami was the capital of the early Chalukya kingdom.",
            "The sculptures inside are considered masterpieces of Indian art."
        ],
        "culture": "Badami Caves are a remarkable example of early Hindu and Jain rock cut architecture in South India."
    },
    "belur_temple": {
        "name": "Chennakeshava Temple Belur",
        "location": "Belur, Karnataka, India",
        "history": "The Chennakeshava Temple was built by King Vishnuvardhana of the Hoysala Empire in 1117 CE to celebrate his victory over the Cholas. It took 103 years to complete.",
        "facts": [
            "The temple has over 600 sculptures on its outer walls.",
            "It took 103 years to complete.",
            "No two sculptures on the temple are identical.",
            "The temple sits on a star-shaped platform called jagati.",
            "It is one of the finest examples of Hoysala architecture."
        ],
        "culture": "Belur temple represents the golden age of Hoysala art and is considered one of the greatest architectural achievements of Karnataka."
    },
    "halebidu_temple": {
        "name": "Hoysaleswara Temple Halebidu",
        "location": "Halebidu, Karnataka, India",
        "history": "The Hoysaleswara Temple was built in the 12th century by the Hoysala king Vishnuvardhana. It is a twin temple dedicated to Lord Shiva and his consort.",
        "facts": [
            "The temple has over 240 elephants carved on its base.",
            "It was never fully completed despite decades of construction.",
            "The temple has no tower unlike most Hindu temples.",
            "It has some of the most intricate stone carvings in the world.",
            "The frieze has continuous bands of sculptures running around the entire temple."
        ],
        "culture": "Halebidu temple is a UNESCO tentative World Heritage Site and the finest example of Hoysala craftsmanship in India."
    },
    "chitradurga_fort": {
        "name": "Chitradurga Fort",
        "location": "Chitradurga, Karnataka, India",
        "history": "Chitradurga Fort was built by Nayaka chieftains and later expanded by Hyder Ali and Tipu Sultan in the 18th century. It is built on a rocky hill and is known as the Stone Fortress.",
        "facts": [
            "The fort has 19 secret entrances.",
            "It has 4 main gates and 19 smaller gates.",
            "The fort encloses an area of 1500 acres.",
            "It has 38 bastions protecting its walls.",
            "Chitradurga means rocky city in Kannada."
        ],
        "culture": "Chitradurga Fort represents the military genius of Karnataka's rulers and is an important historical landmark of the region."
    },
    "gomateshwara": {
        "name": "Gomateshwara Statue",
        "location": "Shravanabelagola, Karnataka, India",
        "history": "The Gomateshwara statue was built in 981 CE by the Ganga dynasty minister Chamundaraya. It is a monolithic statue of Bahubali carved from a single granite rock.",
        "facts": [
            "The statue is 57 feet tall making it one of the tallest monolithic statues in the world.",
            "It was carved from a single piece of granite rock.",
            "The Mahamastakabhisheka ceremony is held every 12 years.",
            "The statue has been standing for over 1000 years.",
            "It is visible from 30 km away on a clear day."
        ],
        "culture": "The Gomateshwara statue is the most sacred pilgrimage site for Jains worldwide and represents Karnataka's rich Jain heritage."
    },
    "pattadakal": {
        "name": "Pattadakal Temples",
        "location": "Pattadakal, Karnataka, India",
        "history": "Pattadakal is a group of 10 temples built by the Chalukya dynasty between the 6th and 8th centuries. It was the coronation site of Chalukya kings.",
        "facts": [
            "Pattadakal has 10 temples of which 9 are Hindu and 1 is Jain.",
            "It became a UNESCO World Heritage Site in 1987.",
            "The temples show both North Indian and South Indian styles of architecture.",
            "It was used as the royal coronation ground of Chalukya kings.",
            "The Virupaksha temple here was built to celebrate victory over the Pallavas."
        ],
        "culture": "Pattadakal represents the culmination of early Chalukya architecture and is a treasure trove of Indian temple building traditions."
    },
    "aihole_temples": {
        "name": "Aihole Temples",
        "location": "Aihole, Karnataka, India",
        "history": "Aihole has over 120 temples built by the Chalukya dynasty between the 4th and 12th centuries. It is considered the cradle of Indian temple architecture.",
        "facts": [
            "Aihole has over 120 ancient temples.",
            "It is called the cradle of Indian temple architecture.",
            "The Durga temple here has a unique apsidal plan similar to Buddhist chaityas.",
            "Some temples date back to the 4th century CE.",
            "Aihole was the first capital of the Chalukya dynasty."
        ],
        "culture": "Aihole is where Indian temple architecture was born and perfected. It is one of the most historically significant sites in Karnataka."
    },
    "bidar_fort": {
        "name": "Bidar Fort",
        "location": "Bidar, Karnataka, India",
        "history": "Bidar Fort was built by Ahmad Shah Wali of the Bahmani Sultanate in 1432. It is one of the most impressive medieval forts in the Deccan region and served as the capital of the Bahmani kingdom.",
        "facts": [
            "Bidar Fort has a perimeter of 10 km.",
            "It has 37 bastions protecting its walls.",
            "The fort was built using red laterite stone.",
            "It contains 30 monuments inside its walls.",
            "Bidar is famous for Bidriware — a unique metal craft that originated here."
        ],
        "culture": "Bidar Fort represents the golden age of the Bahmani Sultanate and is a symbol of Karnataka's rich medieval Islamic heritage."
    },
    
    
}

# ── STEP 4: PRECOMPUTE TEXT EMBEDDINGS ──
# We convert all our text descriptions to embeddings ONCE
# This saves time — no need to recompute every prediction
print("Computing text embeddings...")
landmark_text_embeddings = {}

for landmark_key, prompts in landmark_prompts.items():
    # Tokenize the text prompts
    # Tokenizing = converting words to numbers CLIP understands
    text_tokens = clip.tokenize(prompts).to(device)

    # Get embeddings from CLIP
    with torch.no_grad():
        text_features = model.encode_text(text_tokens)

        # Normalize — this makes cosine similarity work correctly
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

        # Average the embeddings for all prompts of this landmark
        # Multiple prompts = more robust recognition
        avg_features = text_features.mean(dim=0)
        avg_features = avg_features / avg_features.norm()

        landmark_text_embeddings[landmark_key] = avg_features

print(f"Text embeddings ready for {len(landmark_text_embeddings)} landmarks!")

# ── STEP 5: PREDICTION FUNCTION ──
def predict_landmark(image_path):

    # Open and preprocess image
    # preprocess = resize, crop, normalize (CLIP's specific requirements)
    image = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)

    # Get image embedding from CLIP
    with torch.no_grad():
        image_features = model.encode_image(image)

        # Normalize image embedding
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    # ── COSINE SIMILARITY ──
    # Compare image embedding against each landmark's text embedding
    # Higher similarity = more likely match
    similarities = {}
    for landmark_key, text_features in landmark_text_embeddings.items():
        # Dot product of normalized vectors = cosine similarity
        similarity = (image_features @ text_features.unsqueeze(-1)).item()
        similarities[landmark_key] = similarity

    # Find landmark with highest similarity
    best_match = max(similarities, key=similarities.get)

    # Convert similarity to confidence percentage
    # Softmax converts raw scores to probabilities that add up to 100%
    scores = torch.tensor(list(similarities.values()))
    probabilities = torch.nn.functional.softmax(scores * 10, dim=0)
    confidence = round(probabilities[list(similarities.keys()).index(best_match)].item() * 100, 1)

    # Get landmark info
    info = landmark_info.get(best_match, {})

    return {
        "landmark": info.get("name", best_match),
        "confidence": confidence,
        "location": info.get("location", "Unknown"),
        "history": info.get("history", ""),
        "facts": info.get("facts", []),
        "culture": info.get("culture", "")
    }