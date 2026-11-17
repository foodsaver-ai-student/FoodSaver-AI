
FOOD_TIPS = {

    "tomato": {
        "storage": [
            "Keep unripe tomatoes at room temperature.",
            "Refrigerate ripe tomatoes if not using soon.",
            "Wash tomatoes just before using."
        ],
        "waste": [
            "Use sound, overripe tomatoes in soups or sauces.",
            "Freeze tomato puree for later use.",
            "Discard rotten or moldy tomatoes safely."
        ]
    },

    "apple": {
        "storage": [
            "Store apples in the refrigerator.",
            "Keep damaged apples separate.",
            "Check apples regularly for spoilage."
        ],
        "waste": [
            "Use sound, aging apples in pies or smoothies.",
            "Prepare homemade applesauce.",
            "Discard rotten apples safely."
        ]
    },

    "banana": {
        "storage": [
            "Keep unripe bananas at room temperature.",
            "Refrigerate ripe bananas to slow ripening.",
            "Freeze peeled bananas for later use."
        ],
        "waste": [
            "Use sound, overripe bananas in banana bread.",
            "Prepare banana smoothies.",
            "Discard rotten or moldy bananas."
        ]
    },

    "potato": {
        "storage": [
            "Store potatoes in a cool, dark, dry place.",
            "Use a ventilated storage container.",
            "Keep potatoes away from direct sunlight."
        ],
        "waste": [
            "Plan meals before buying potatoes.",
            "Use suitable leftover cooked potatoes safely.",
            "Discard rotten or spoiled potatoes."
        ]
    },

    "orange": {
        "storage": [
            "Refrigerate oranges for longer storage.",
            "Keep oranges dry before storing.",
            "Remove damaged oranges from the batch."
        ],
        "waste": [
            "Use sound extra oranges in smoothies.",
            "Freeze fresh orange juice.",
            "Discard moldy or rotten oranges."
        ]
    },

    "bellpepper": {
        "storage": [
            "Store bell peppers in the refrigerator.",
            "Keep them dry before storage.",
            "Use cut peppers in an airtight container."
        ],
        "waste": [
            "Use sound peppers in salads and stir-fries.",
            "Freeze chopped peppers for cooking.",
            "Discard rotten or moldy peppers."
        ]
    },

    "carrot": {
        "storage": [
            "Store carrots in the refrigerator.",
            "Remove leafy tops before storage.",
            "Keep carrots in a suitable airtight container."
        ],
        "waste": [
            "Use sound carrots in soups and salads.",
            "Add suitable carrot leftovers to meals.",
            "Discard rotten or moldy carrots."
        ]
    },

    "cucumber": {
        "storage": [
            "Keep cucumbers refrigerated.",
            "Store them dry.",
            "Use cut cucumber in an airtight container."
        ],
        "waste": [
            "Use fresh cucumber in salads.",
            "Add suitable leftovers to sandwiches.",
            "Discard rotten or moldy cucumbers."
        ]
    },

    "mango": {
        "storage": [
            "Ripen unripe mangoes at room temperature.",
            "Refrigerate ripe mangoes.",
            "Store cut mango in an airtight container."
        ],
        "waste": [
            "Use sound ripe mangoes in smoothies.",
            "Freeze mango pieces for later use.",
            "Discard rotten or moldy mangoes."
        ]
    },

    "strawberry": {
        "storage": [
            "Refrigerate strawberries promptly.",
            "Keep strawberries dry until washing.",
            "Remove damaged berries from the batch."
        ],
        "waste": [
            "Use sound ripe strawberries in smoothies.",
            "Freeze clean strawberries for later use.",
            "Discard moldy or rotten strawberries."
        ]
    }
}


def get_food_tips(label):

    label = label.lower().strip()

    # Remove freshness prefix if present
    for prefix in ["fresh", "rotten"]:
        if label.startswith(prefix):
            label = label[len(prefix):]
            break

    label = label.strip()

    tips = FOOD_TIPS.get(label)

    if tips:

        return {
            "food": label.title(),
            "storage": tips["storage"],
            "waste": tips["waste"]
        }

    return {
        "food": "Other Food",
        "storage": [
            "Follow food-specific storage instructions.",
            "Keep perishable food at safe temperatures."
        ],
        "waste": [
            "Plan meals to avoid excess purchases.",
            "Discard spoiled food safely."
        ]
    }
