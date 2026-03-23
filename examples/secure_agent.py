from stti.core.provenance import ProvenanceLedger
from stti.core.gate import PurityGate, SecurityError

# --- SETUP ---
ledger = ProvenanceLedger()
ledger.ingest("User_12345", "database_lookup")
ledger.ingest(123, "id_generator")

# --- 1. CLEAN TRANSFORMER (PASS) ---
def clean_transform(x):
    return x.strip()

try:
    PurityGate.verify(clean_transform)
    print("CASE 1: Clean Transformer - PASS")
except SecurityError:
    print("CASE 1: Clean Transformer - BLOCK")

# --- 2. CLOSURE (BLOCK) ---
secret_prefix = "ADMIN_"
def closure_attempt(x):
    return secret_prefix + x

try:
    PurityGate.verify(closure_attempt)
    print("CASE 2: Closure Attempt - PASS")
except SecurityError:
    print("CASE 2: Closure Attempt - BLOCK")

# --- 3. CORRECT VALUE / CORRECT SOURCE (PASS) ---
val_3 = "User_12345"
source_3 = "database_lookup"
if ledger.is_grounded(val_3, source_3):
    print(f"CASE 3: Correct Value/Source ({val_3}) - PASS")
else:
    print(f"CASE 3: Correct Value/Source ({val_3}) - BLOCK")

# --- 4. OFF-BY-ONE HALLUCINATION (BLOCK) ---
val_4 = "User_1234"
source_4 = "database_lookup"
if ledger.is_grounded(val_4, source_4):
    print(f"CASE 4: Off-by-one Hallucination ({val_4}) - PASS")
else:
    print(f"CASE 4: Off-by-one Hallucination ({val_4}) - BLOCK")

# --- 5. CORRECT VALUE / WRONG SOURCE (BLOCK) ---
val_5 = "User_12345"
source_5 = "untrusted_llm_inference"
if ledger.is_grounded(val_5, source_5):
    print(f"CASE 5: Correct Value/Wrong Source ({source_5}) - PASS")
else:
    print(f"CASE 5: Correct Value/Wrong Source ({source_5}) - BLOCK")

# --- 6. TYPE COERCION ATTEMPT (BLOCK) ---
# Ledger has int(123) from 'id_generator'
val_6 = 123.0 
source_6 = "id_generator"
if ledger.is_grounded(val_6, source_6):
    print(f"CASE 6: Type Coercion Attempt ({type(val_6)}) - PASS")
else:
    print(f"CASE 6: Type Coercion Attempt ({type(val_6)}) - BLOCK")
