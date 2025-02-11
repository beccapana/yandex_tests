ENDPOINT = "https://petstore.swagger.io/v2"

import os
current_dir = os.path.dirname(__file__)
DATA_DIR = os.path.join(current_dir, "test_cases")

NEW_PET_POS_FILE = os.path.join(DATA_DIR, "NewPetPos.xlsx") #pairwise.teremokgames.com/5jl9g/
NEW_PET_NEG_FILE = os.path.join(DATA_DIR, "NewPetNeg.xlsx") #pairwise.teremokgames.com/5jl6o/
