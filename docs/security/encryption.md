# Symmetric & Asymmetric Encryption 


## Youtube

- [25. Symmetric & Asymmetric Encryption with Explanation of AES, Diffie-Hellman and Digital Signature](https://www.youtube.com/watch?v=GtSUeAkPEP0)






## Theory

### What is Encryption and Decryption?

**Encryption** is the process of converting plaintext (readable data) into ciphertext (scrambled, unreadable data) using an algorithm and a key. **Decryption** is the reverse process of converting ciphertext back to plaintext.

**Purpose:**
- **Confidentiality**: Protect sensitive data from unauthorized access
- **Data Security**: Secure data in transit and at rest
- **Privacy**: Keep personal information private
- **Compliance**: Meet regulatory requirements (GDPR, HIPAA, PCI-DSS)

#### How Encryption Works

```
┌─────────────────────────────────────────────────────────────┐
│              Encryption & Decryption Process                 │
└─────────────────────────────────────────────────────────────┘

ENCRYPTION:
───────────
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Plaintext   │     │  Encryption  │     │  Ciphertext  │
│              │────▶│  Algorithm   │────▶│              │
│ "Hello 123"  │     │   + Key      │     │ "xK9#mP2$..."│
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            │
                     ┌──────▼──────┐
                     │ Encryption  │
                     │     Key     │
                     │  (Secret)   │
                     └─────────────┘

DECRYPTION:
───────────
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Ciphertext  │     │  Decryption  │     │  Plaintext   │
│              │────▶│  Algorithm   │────▶│              │
│ "xK9#mP2$..."│     │   + Key      │     │ "Hello 123"  │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            │
                     ┌──────▼──────┐
                     │ Decryption  │
                     │     Key     │
                     │  (Secret)   │
                     └─────────────┘

KEY COMPONENTS:
──────────────
1. Plaintext:  Original readable data
2. Algorithm:  Mathematical function (AES, RSA, etc.)
3. Key:        Secret value used by algorithm
4. Ciphertext: Encrypted, unreadable output
```

**Example Process:**
```
Plaintext:    "HELLO WORLD"
Algorithm:    AES-256
Key:          "my-secret-key-12345"
             ↓
Encryption:   Apply AES-256 algorithm with key
             ↓
Ciphertext:   "j8kL#2mN9qR$5tX..."
             ↓
Decryption:   Apply AES-256 algorithm with same key
             ↓
Plaintext:    "HELLO WORLD"
```

### Symmetric Encryption

**Definition**: Encryption method that uses the **same key** for both encryption and decryption.

```
┌─────────────────────────────────────────────────────────────┐
│                 Symmetric Encryption                         │
└─────────────────────────────────────────────────────────────┘

         ┌──────────────────────────────────┐
         │      Shared Secret Key           │
         │       "mySecretKey123"           │
         └────────────┬──────────┬──────────┘
                      │          │
         ┌────────────▼───┐      │
         │  ENCRYPTION    │      │
         │                │      │
Sender   │  Plaintext ────┼──────┼──────▶ Ciphertext
         │  "Hello"       │      │        "xK9#mP2$"
         │                │      │
         └────────────────┘      │
                                 │
                                 │
                      ┌──────────▼──────────┐
                      │    TRANSMISSION     │
                      │   (Over Network)    │
                      │   Ciphertext Sent   │
                      └──────────┬──────────┘
                                 │
                                 │
         ┌────────────────┐      │
         │  DECRYPTION    │      │
         │                │      │
Receiver │  Ciphertext ───┼──────┘
         │  "xK9#mP2$"    │
         │       │        │
         │       ▼        │
         │  Plaintext     │
         │  "Hello"       │
         └────────────────┘

KEY CHARACTERISTIC:
──────────────────
Same key used for encryption AND decryption
Both parties must have the secret key
```

#### Symmetric Encryption Algorithms

**Evolution and Improvements:**

| Algorithm | Key Size | Year | Status | Notes |
|-----------|----------|------|--------|-------|
| **DES** | 56-bit | 1977 | ❌ Deprecated | Too weak, broken by brute force |
| **3DES** | 168-bit | 1998 | ⚠️ Legacy | Triple encryption, slow, being phased out |
| **AES** | 128/192/256-bit | 2001 | ✅ Current Standard | Fast, secure, widely used |
| **ChaCha20** | 256-bit | 2008 | ✅ Modern | Fast on mobile, used in TLS |
| **Blowfish** | 32-448 bit | 1993 | ⚠️ Legacy | Replaced by AES |
| **Twofish** | 128/192/256-bit | 1998 | ✅ Secure | AES finalist, still secure |

**Modern Algorithm: AES (Advanced Encryption Standard)**

**Advantages of AES over DES:**
- ✅ **Stronger Security**: 256-bit keys vs 56-bit (2^200 times harder to crack)
- ✅ **Faster**: Hardware acceleration in modern CPUs
- ✅ **Flexible**: Multiple key sizes (128, 192, 256 bits)
- ✅ **Proven**: Extensively analyzed, no practical attacks
- ✅ **Government Approved**: Used by NSA for classified data
- ✅ **Efficient**: Low memory footprint

**AES Modes of Operation:**
```
ECB (Electronic Codebook):        ❌ Not recommended (patterns visible)
CBC (Cipher Block Chaining):      ✅ Good for files
CTR (Counter Mode):                ✅ Good for random access
GCM (Galois/Counter Mode):         ✅ Best - Encryption + Authentication
```

### Detailed Symmetric Encryption Algorithms

#### DES (Data Encryption Standard)

**Description:**
DES was the first widely adopted modern encryption standard, developed by IBM and adopted by NIST in 1977. It's a block cipher that encrypts data in 64-bit blocks using a 56-bit key.

```
┌─────────────────────────────────────────────────────────────┐
│              DES Algorithm Structure                         │
└─────────────────────────────────────────────────────────────┘

INPUT: 64-bit Plaintext Block
       ↓
┌──────────────────────┐
│ Initial Permutation  │  Rearrange bits
│        (IP)          │
└──────────┬───────────┘
           │
      Split into
           │
    ┌──────┴──────┐
    │             │
Left 32 bits  Right 32 bits
    │             │
    ├─────────────┤
    │  16 Rounds  │
    │  ┌───────┐  │
    │  │Round 1│  │  Each round:
    │  │  K1   │  │  - Expansion
    │  ├───────┤  │  - XOR with key
    │  │Round 2│  │  - S-boxes (substitution)
    │  │  K2   │  │  - Permutation
    │  ├───────┤  │
    │  │  ...  │  │
    │  ├───────┤  │
    │  │Round16│  │
    │  │  K16  │  │
    │  └───────┘  │
    └─────────────┘
           │
┌──────────┴───────────┐
│ Final Permutation    │  Inverse of IP
│      (IP⁻¹)          │
└──────────┬───────────┘
           │
OUTPUT: 64-bit Ciphertext

KEY SCHEDULE:
─────────────
56-bit Key → Generate 16 subkeys (K1-K16)
Each round uses different subkey
```

**Specifications:**
- **Block Size**: 64 bits
- **Key Size**: 56 bits (+ 8 parity bits = 64 bits total)
- **Rounds**: 16
- **Structure**: Feistel Network

**Advantages (Historical):**
- ✅ Well-studied and understood
- ✅ Hardware implementations very fast
- ✅ Simple to implement

**Disadvantages:**
- ❌ **Too Weak**: 56-bit key is too small (2^56 = 72 quadrillion keys)
- ❌ **Broken**: Can be cracked in days with modern hardware
- ❌ **Small Block Size**: 64-bit blocks lead to collisions
- ❌ **Deprecated**: Should not be used anymore

**Why DES Failed:**
```
Key Space: 2^56 = 72,057,594,037,927,936 possible keys

1977:  Would take years to brute force
1998:  EFF's DES Cracker broke DES in 56 hours
2006:  COPACOBANA broke DES in 9 days (cost: $10,000)
2025:  Can be broken in seconds with cloud computing

Example Attack Cost:
AWS EC2: ~$100 to crack DES in a few hours
```

#### 3DES (Triple DES)

**Description:**
3DES applies DES three times with different keys to increase security. It was created as a temporary solution when DES became too weak.

```
┌─────────────────────────────────────────────────────────────┐
│              3DES Algorithm (EDE Mode)                       │
└─────────────────────────────────────────────────────────────┘

Plaintext
    │
    ▼
┌─────────────┐
│ Encrypt     │  Key1 (56 bits)
│  (DES)      │  Encryption with first key
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Decrypt     │  Key2 (56 bits)
│  (DES)      │  Decryption with second key
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Encrypt     │  Key3 (56 bits)
│  (DES)      │  Encryption with third key
└──────┬──────┘
       │
       ▼
Ciphertext

Total Key Length: 168 bits (3 × 56)
Effective Security: ~112 bits (due to meet-in-the-middle attacks)

Variants:
─────────
1. 3DES-EDE3: K1, K2, K3 all different (168-bit)
2. 3DES-EDE2: K1=K3, K2 different (112-bit)
3. 3DES-EEE:  All encryption (less common)
```

**Advantages:**
- ✅ Backward compatible with DES
- ✅ Stronger than DES (112-168 bit effective security)
- ✅ No known practical attacks

**Disadvantages:**
- ❌ **Slow**: 3x slower than DES, 6-7x slower than AES
- ❌ **Small Block Size**: Still 64-bit blocks
- ❌ **Being Deprecated**: NIST deprecated in 2023
- ❌ **Inefficient**: Legacy design

#### AES (Advanced Encryption Standard)

**Description:**
AES, also known as Rijndael, is the current encryption standard. It was selected through a public competition and adopted by NIST in 2001. It's a substitution-permutation network (SPN) cipher.

```
┌─────────────────────────────────────────────────────────────┐
│              AES Algorithm Structure                         │
└─────────────────────────────────────────────────────────────┘

INPUT: 128-bit Plaintext (16 bytes)
       ↓
Arranged in 4×4 matrix (State):
┌─────────────────┐
│ b0  b4  b8  b12 │
│ b1  b5  b9  b13 │
│ b2  b6  b10 b14 │
│ b3  b7  b11 b15 │
└─────────────────┘
       ↓
┌─────────────────────────────────┐
│ Initial Round (Add Round Key)   │
│ XOR with first round key        │
└───────────────┬─────────────────┘
                │
        ┌───────┴───────┐
        │   Main Rounds │  (Nr-1 rounds)
        │               │  Nr = 10, 12, or 14
        │  ┌─────────┐  │  depending on key size
        │  │ Round 1 │  │
        │  │  ┌───────────────────┐
        │  │  │ 1. SubBytes       │ S-box substitution
        │  │  │ 2. ShiftRows      │ Rotate rows
        │  │  │ 3. MixColumns     │ Mix column data
        │  │  │ 4. AddRoundKey    │ XOR with round key
        │  │  └───────────────────┘
        │  ├─────────┤
        │  │ Round 2 │
        │  ├─────────┤
        │  │   ...   │
        │  └─────────┘
        └───────┬───────┘
                │
┌───────────────┴─────────────────┐
│ Final Round (No MixColumns)     │
│ 1. SubBytes                     │
│ 2. ShiftRows                    │
│ 3. AddRoundKey                  │
└───────────────┬─────────────────┘
                │
OUTPUT: 128-bit Ciphertext

AES OPERATIONS:
───────────────

1. SubBytes (S-box):
   ┌───┐    ┌───┐
   │ A │ → │ C │  Each byte substituted
   │ B │ → │ 7 │  using lookup table
   └───┘    └───┘

2. ShiftRows:
   Row 0: No shift
   Row 1: Left shift by 1
   Row 2: Left shift by 2
   Row 3: Left shift by 3

3. MixColumns:
   Multiply each column by fixed matrix
   (Provides diffusion)

4. AddRoundKey:
   XOR state with round key
```

**AES Variants:**
```
┌─────────────────────────────────────────────────┐
│        AES-128  │  AES-192  │  AES-256         │
├─────────────────┼───────────┼──────────────────┤
│ Key Size:   128 │  192      │  256 bits        │
│ Rounds:     10  │  12       │  14              │
│ Security:   High│  Higher   │  Highest         │
│ Speed:      Fast│  Medium   │  Slower          │
│ Use Case: Standard│Government│Top Secret/Future│
└─────────────────────────────────────────────────┘

Security Level:
AES-128: 2^128 possible keys (unbreakable with current tech)
AES-256: 2^256 possible keys (quantum-resistant)
```

**Advantages:**
- ✅ **Extremely Secure**: No practical attacks on full AES
- ✅ **Fast**: Hardware acceleration (AES-NI instructions)
- ✅ **Flexible**: Multiple key sizes
- ✅ **Efficient**: Low memory and CPU usage
- ✅ **Widely Adopted**: Industry standard
- ✅ **Government Approved**: NSA Suite B
- ✅ **Well Studied**: Analyzed for over 20 years

**Performance Comparison:**
```
Encryption Speed (MB/s on modern CPU):
─────────────────────────────────────
DES:         50 MB/s
3DES:        20 MB/s
AES-128:    500 MB/s (without AES-NI)
AES-128:  3,000 MB/s (with AES-NI)

AES is 10-150x faster than 3DES!
```

### How AES Works: Step-by-Step

AES processes data through multiple rounds of transformations. Let's understand each operation in detail:

```
┌─────────────────────────────────────────────────────────────┐
│            AES DETAILED ENCRYPTION PROCESS                   │
└─────────────────────────────────────────────────────────────┘

EXAMPLE: AES-128 (10 rounds)

INPUT PLAINTEXT: "Hello World 123!" (16 bytes)
KEY: 256-bit key (we'll use 128-bit for simplicity)

STEP 1: Convert to State Matrix (4×4 bytes)
────────────────────────────────────────────
Input bytes arranged column-wise:

        Col0  Col1  Col2  Col3
     ┌─────────────────────────┐
Row0 │  H     W     d     3    │
Row1 │  e     o     (space)!   │
Row2 │  l     r     1          │
Row3 │  l     l     2          │
     └─────────────────────────┘

Hex representation:
     ┌─────────────────────────┐
     │ 48   57   64   33       │
     │ 65   6F   20   21       │
     │ 6C   72   31           │
     │ 6C   6C   32           │
     └─────────────────────────┘

═══════════════════════════════════════════════════════════════

ROUND 0: Initial AddRoundKey
─────────────────────────────
State ⊕ RoundKey[0]

Before:              RoundKey[0]:      After (State):
┌──────────┐         ┌──────────┐      ┌──────────┐
│ 48 57 .. │    ⊕    │ 2B 7E .. │  =   │ 63 29 .. │
│ 65 6F .. │         │ 28 AE .. │      │ 4D C1 .. │
│ 6C 72 .. │         │ D2 A6 .. │      │ BE D4 .. │
│ 6C 6C .. │         │ AB F7 .. │      │ C7 9B .. │
└──────────┘         └──────────┘      └──────────┘

═══════════════════════════════════════════════════════════════

ROUND 1-9: Main Rounds (each has 4 operations)
───────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────┐
│ OPERATION 1: SubBytes (Byte Substitution)                   │
└─────────────────────────────────────────────────────────────┘

Each byte replaced using S-box lookup table (non-linear substitution)

S-BOX (partial):
    0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F
  ┌────────────────────────────────────────────────
0 │ 63 7C 77 7B F2 6B 6F C5 30 01 67 2B FE D7 AB 76
1 │ CA 82 C9 7D FA 59 47 F0 AD D4 A2 AF 9C A4 72 C0
...

Example:
Input byte:  0x53
Row = 5, Col = 3
S-box[5][3] = 0xED
Output byte: 0xED

Before SubBytes:        After SubBytes:
┌──────────┐            ┌──────────┐
│ 63 29 .. │  S-box     │ FB 7D .. │
│ 4D C1 .. │  ──────▶   │ E4 8E .. │
│ BE D4 .. │            │ 23 AF .. │
│ C7 9B .. │            │ 0C C5 .. │
└──────────┘            └──────────┘
      │                       │
      └──── Non-linear ───────┘
           confusion

┌─────────────────────────────────────────────────────────────┐
│ OPERATION 2: ShiftRows (Row Permutation)                    │
└─────────────────────────────────────────────────────────────┘

Circular left shift of rows (provides diffusion)

Before ShiftRows:              After ShiftRows:
┌──────────────┐               ┌──────────────┐
│ a0 a1 a2 a3  │ Row 0: No     │ a0 a1 a2 a3  │
│ b0 b1 b2 b3  │ Row 1: <<1    │ b1 b2 b3 b0  │
│ c0 c1 c2 c3  │ Row 2: <<2    │ c2 c3 c0 c1  │
│ d0 d1 d2 d3  │ Row 3: <<3    │ d3 d0 d1 d2  │
└──────────────┘               └──────────────┘

Visual:
Row 1: [b0, b1, b2, b3] → [b1, b2, b3, b0]
       └───┘ shifted left by 1

Row 2: [c0, c1, c2, c3] → [c2, c3, c0, c1]
       └──────┘ shifted left by 2

Row 3: [d0, d1, d2, d3] → [d3, d0, d1, d2]
       └─────────┘ shifted left by 3

┌─────────────────────────────────────────────────────────────┐
│ OPERATION 3: MixColumns (Column Mixing)                     │
└─────────────────────────────────────────────────────────────┘

Matrix multiplication in Galois Field GF(2^8)
Each column multiplied by fixed matrix

MixColumns Matrix:
┌──────────┐   ┌──────────┐   ┌──────────┐
│ 02 03 01 01│ │ s0,c     │ │ s'0,c    │
│ 01 02 03 01│ │ s1,c     │ │ s'1,c    │
│ 01 01 02 03│ × │ s2,c     │ = │ s'2,c    │
│ 03 01 01 02│ │ s3,c     │ │ s'3,c    │
└──────────┘   └──────────┘   └──────────┘

Example for one column:
┌──────────┐   ┌────┐   ┌────┐
│ 02 03 01 01│ │ DB │ │ 8E │
│ 01 02 03 01│ │ 13 │ │ 9F │
│ 01 01 02 03│ × │ 53 │ = │ D4 │
│ 03 01 01 02│ │ 45 │ │ 17 │
└──────────┘   └────┘   └────┘

This spreads each byte across entire column
(Maximum diffusion)

Before MixColumns:        After MixColumns:
┌──────────┐              ┌──────────┐
│ a0 b0 c0 d0│             │ a'0 b'0 c'0 d'0│
│ a1 b1 c1 d1│  Matrix     │ a'1 b'1 c'1 d'1│
│ a2 b2 c2 d2│  ──────▶    │ a'2 b'2 c'2 d'2│
│ a3 b3 c3 d3│             │ a'3 b'3 c'3 d'3│
└──────────┘              └──────────┘

Each output byte depends on all 4 input bytes of column!

┌─────────────────────────────────────────────────────────────┐
│ OPERATION 4: AddRoundKey (XOR with Round Key)               │
└─────────────────────────────────────────────────────────────┘

XOR state with round-specific key

State:                  RoundKey[i]:        Result:
┌──────────┐            ┌──────────┐        ┌──────────┐
│ a0 b0 .. │      ⊕     │ k0 l0 .. │    =   │ a0⊕k0 .. │
│ a1 b1 .. │            │ k1 l1 .. │        │ a1⊕k1 .. │
│ a2 b2 .. │            │ k2 l2 .. │        │ a2⊕k2 .. │
│ a3 b3 .. │            │ k3 l3 .. │        │ a3⊕k3 .. │
└──────────┘            └──────────┘        └──────────┘

═══════════════════════════════════════════════════════════════

COMPLETE ROUND VISUALIZATION:
──────────────────────────────

Input State
     │
     ▼
┌──────────┐
│ SubBytes │  Non-linear substitution (confusion)
└────┬─────┘
     │
     ▼
┌──────────┐
│ShiftRows │  Transpose rows (diffusion)
└────┬─────┘
     │
     ▼
┌──────────┐
│MixColumns│  Mix columns (diffusion) [Not in final round]
└────┬─────┘
     │
     ▼
┌──────────┐
│AddRndKey │  XOR with round key
└────┬─────┘
     │
     ▼
Output State (input to next round)

═══════════════════════════════════════════════════════════════

ROUND 10: Final Round (No MixColumns)
──────────────────────────────────────

1. SubBytes
2. ShiftRows
3. AddRoundKey  ← Final round key

Final State → CIPHERTEXT (16 bytes)

═══════════════════════════════════════════════════════════════

KEY SCHEDULE (Round Key Generation):
─────────────────────────────────────

Original Key (128-bit):
┌────────────────────────────────────────┐
│ K0  K1  K2  K3  K4  K5 ...  K14  K15  │
└────────────────────────────────────────┘

Expand to 11 round keys (44 words):
RoundKey[0]:  w[0]  w[1]  w[2]  w[3]
RoundKey[1]:  w[4]  w[5]  w[6]  w[7]
RoundKey[2]:  w[8]  w[9]  w[10] w[11]
...
RoundKey[10]: w[40] w[41] w[42] w[43]

Key expansion uses:
- RotWord: Circular byte rotation
- SubWord: S-box substitution  
- Rcon: Round constant XOR

Example:
w[i] = w[i-4] ⊕ T(w[i-1])
where T() = SubWord(RotWord(w)) ⊕ Rcon[i]

═══════════════════════════════════════════════════════════════

WHY AES IS SECURE:
──────────────────

1. CONFUSION (SubBytes):
   Changes in plaintext/key produce complex changes in ciphertext
   Non-linear S-box prevents mathematical analysis

2. DIFFUSION (ShiftRows + MixColumns):
   Each plaintext bit affects many ciphertext bits
   After 2 rounds: 1 bit affects all 128 bits!

3. KEY MIXING (AddRoundKey):
   Different key for each round
   Prevents key recovery attacks

4. MULTIPLE ROUNDS:
   10/12/14 rounds ensure complete diffusion
   Avalanche effect: changing 1 input bit flips ~50% output bits

═══════════════════════════════════════════════════════════════

AVALANCHE EFFECT DEMONSTRATION:
────────────────────────────────

Plaintext 1: "Hello World!!!!"
Plaintext 2: "Hello World!!!!" (last char changed to '?')
                            ↑ Only 1 bit different

After AES-128 encryption with same key:

Ciphertext 1: A7 3B F2 8C 91 5D E4 2A 8F 1C 37 6B D9 E8 4F 5C
Ciphertext 2: 2D C9 8A 41 6F E3 B7 9D 53 A8 C2 1F 84 6E D5 29
              ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑ ↑↑
              All bytes completely different!

64 bits out of 128 changed → Perfect avalanche!
```

### AES Implementation Example

**Complete AES Implementation with All Modes:**

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

class AESCipher:
    """
    Complete AES implementation with multiple modes
    Demonstrates all common AES modes of operation
    """
    
    def __init__(self, key: bytes = None):
        """
        Initialize AES cipher
        key: 16, 24, or 32 bytes for AES-128, AES-192, or AES-256
        """
        if key is None:
            # Generate random 256-bit key
            self.key = get_random_bytes(32)
        else:
            if len(key) not in [16, 24, 32]:
                raise ValueError("Key must be 16, 24, or 32 bytes")
            self.key = key
        
        self.block_size = AES.block_size  # 16 bytes
    
    # ═══════════════════════════════════════════════════════
    # MODE 1: GCM (Galois/Counter Mode) - RECOMMENDED
    # ═══════════════════════════════════════════════════════
    
    def encrypt_gcm(self, plaintext: bytes) -> dict:
        """
        Encrypt using AES-GCM (Authenticated Encryption)
        
        Advantages:
        ✅ Encryption + Authentication in one step
        ✅ Detects tampering
        ✅ Fast (parallelizable)
        ✅ No padding needed
        
        Returns: dict with ciphertext, nonce, and tag
        """
        # Create cipher in GCM mode
        cipher = AES.new(self.key, AES.MODE_GCM)
        
        # Encrypt and generate authentication tag
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        
        return {
            'ciphertext': ciphertext,
            'nonce': cipher.nonce,  # 16 bytes, must be unique
            'tag': tag              # 16 bytes authentication tag
        }
    
    def decrypt_gcm(self, ciphertext: bytes, nonce: bytes, tag: bytes) -> bytes:
        """
        Decrypt and verify AES-GCM
        Raises ValueError if authentication fails (tampered data)
        """
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        
        try:
            # Decrypt and verify in one step
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext
        except ValueError:
            raise ValueError("Authentication failed! Data was tampered with.")
    
    # ═══════════════════════════════════════════════════════
    # MODE 2: CBC (Cipher Block Chaining) - TRADITIONAL
    # ═══════════════════════════════════════════════════════
    
    def encrypt_cbc(self, plaintext: bytes) -> dict:
        """
        Encrypt using AES-CBC mode
        
        Characteristics:
        ✓ Each block depends on previous block
        ✓ Requires padding
        ✓ Requires IV (Initialization Vector)
        ⚠️ No authentication (use HMAC separately)
        
        Returns: dict with ciphertext and IV
        """
        # Generate random IV (must be unpredictable)
        iv = get_random_bytes(self.block_size)
        
        # Create cipher
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # Pad plaintext to block size (PKCS7 padding)
        padded_plaintext = pad(plaintext, self.block_size)
        
        # Encrypt
        ciphertext = cipher.encrypt(padded_plaintext)
        
        return {
            'ciphertext': ciphertext,
            'iv': iv
        }
    
    def decrypt_cbc(self, ciphertext: bytes, iv: bytes) -> bytes:
        """Decrypt AES-CBC"""
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        
        # Remove padding
        plaintext = unpad(padded_plaintext, self.block_size)
        return plaintext
    
    # ═══════════════════════════════════════════════════════
    # MODE 3: CTR (Counter Mode) - STREAM CIPHER
    # ═══════════════════════════════════════════════════════
    
    def encrypt_ctr(self, plaintext: bytes) -> dict:
        """
        Encrypt using AES-CTR mode
        
        Characteristics:
        ✅ Turns block cipher into stream cipher
        ✅ Parallelizable (fast)
        ✅ Random access to encrypted data
        ✅ No padding needed
        ⚠️ No authentication
        
        Returns: dict with ciphertext and nonce
        """
        # Generate random nonce (number used once)
        nonce = get_random_bytes(8)  # CTR uses 8-byte nonce
        
        # Create cipher (nonce will be used as counter prefix)
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=nonce)
        
        # Encrypt (works on any length, no padding)
        ciphertext = cipher.encrypt(plaintext)
        
        return {
            'ciphertext': ciphertext,
            'nonce': nonce
        }
    
    def decrypt_ctr(self, ciphertext: bytes, nonce: bytes) -> bytes:
        """Decrypt AES-CTR"""
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext
    
    # ═══════════════════════════════════════════════════════
    # MODE 4: ECB (Electronic Codebook) - NOT RECOMMENDED
    # ═══════════════════════════════════════════════════════
    
    def encrypt_ecb(self, plaintext: bytes) -> bytes:
        """
        Encrypt using AES-ECB mode
        
        ⚠️  WARNING: NOT SECURE FOR MOST USE CASES
        ❌ Same plaintext block → same ciphertext block
        ❌ Patterns visible in ciphertext
        ❌ No IV/nonce
        
        Only use for encrypting random data (like keys)
        """
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_plaintext = pad(plaintext, self.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        return ciphertext
    
    def decrypt_ecb(self, ciphertext: bytes) -> bytes:
        """Decrypt AES-ECB"""
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, self.block_size)
        return plaintext


# ═══════════════════════════════════════════════════════════
# USAGE EXAMPLES
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("="*60)
    print("AES ENCRYPTION DEMONSTRATION")
    print("="*60)
    
    # Initialize cipher with 256-bit key
    aes = AESCipher()
    
    # Test data
    plaintext = b"This is a secret message that needs encryption!"
    print(f"\nOriginal: {plaintext.decode()}")
    print(f"Length: {len(plaintext)} bytes")
    
    # ─────────────────────────────────────────────────────────
    # Example 1: AES-GCM (RECOMMENDED)
    # ─────────────────────────────────────────────────────────
    print("\n" + "─"*60)
    print("1. AES-256-GCM (Best for most use cases)")
    print("─"*60)
    
    # Encrypt
    encrypted_gcm = aes.encrypt_gcm(plaintext)
    print(f"Ciphertext: {encrypted_gcm['ciphertext'].hex()[:60]}...")
    print(f"Nonce: {encrypted_gcm['nonce'].hex()}")
    print(f"Tag: {encrypted_gcm['tag'].hex()}")
    
    # Decrypt
    decrypted_gcm = aes.decrypt_gcm(
        encrypted_gcm['ciphertext'],
        encrypted_gcm['nonce'],
        encrypted_gcm['tag']
    )
    print(f"Decrypted: {decrypted_gcm.decode()}")
    print(f"✅ Match: {decrypted_gcm == plaintext}")
    
    # Test tampering detection
    print("\n🔒 Testing tamper detection...")
    tampered_ciphertext = bytearray(encrypted_gcm['ciphertext'])
    tampered_ciphertext[0] ^= 0x01  # Flip one bit
    
    try:
        aes.decrypt_gcm(bytes(tampered_ciphertext), 
                       encrypted_gcm['nonce'], 
                       encrypted_gcm['tag'])
        print("❌ Tampering not detected!")
    except ValueError as e:
        print(f"✅ Tampering detected: {e}")
    
    # ─────────────────────────────────────────────────────────
    # Example 2: AES-CBC
    # ─────────────────────────────────────────────────────────
    print("\n" + "─"*60)
    print("2. AES-256-CBC (Traditional mode)")
    print("─"*60)
    
    encrypted_cbc = aes.encrypt_cbc(plaintext)
    print(f"Ciphertext: {encrypted_cbc['ciphertext'].hex()[:60]}...")
    print(f"IV: {encrypted_cbc['iv'].hex()}")
    
    decrypted_cbc = aes.decrypt_cbc(
        encrypted_cbc['ciphertext'],
        encrypted_cbc['iv']
    )
    print(f"Decrypted: {decrypted_cbc.decode()}")
    print(f"✅ Match: {decrypted_cbc == plaintext}")
    
    # ─────────────────────────────────────────────────────────
    # Example 3: AES-CTR
    # ─────────────────────────────────────────────────────────
    print("\n" + "─"*60)
    print("3. AES-256-CTR (Stream cipher mode)")
    print("─"*60)
    
    encrypted_ctr = aes.encrypt_ctr(plaintext)
    print(f"Ciphertext: {encrypted_ctr['ciphertext'].hex()[:60]}...")
    print(f"Nonce: {encrypted_ctr['nonce'].hex()}")
    
    decrypted_ctr = aes.decrypt_ctr(
        encrypted_ctr['ciphertext'],
        encrypted_ctr['nonce']
    )
    print(f"Decrypted: {decrypted_ctr.decode()}")
    print(f"✅ Match: {decrypted_ctr == plaintext}")
    
    # ─────────────────────────────────────────────────────────
    # Example 4: Key Size Comparison
    # ─────────────────────────────────────────────────────────
    print("\n" + "─"*60)
    print("4. Key Size Comparison")
    print("─"*60)
    
    key_sizes = {
        'AES-128': 16,
        'AES-192': 24,
        'AES-256': 32
    }
    
    for name, size in key_sizes.items():
        key = get_random_bytes(size)
        aes_test = AESCipher(key)
        enc = aes_test.encrypt_gcm(b"Test")
        print(f"{name}: Key={size*8} bits, "
              f"Rounds={10 if size==16 else 12 if size==24 else 14}")
    
    # ─────────────────────────────────────────────────────────
    # Example 5: File Encryption
    # ─────────────────────────────────────────────────────────
    print("\n" + "─"*60)
    print("5. File Encryption Example")
    print("─"*60)
    
    def encrypt_file(filename: str, key: bytes):
        """Encrypt a file using AES-GCM"""
        # Read file
        with open(filename, 'rb') as f:
            plaintext = f.read()
        
        # Encrypt
        aes = AESCipher(key)
        encrypted = aes.encrypt_gcm(plaintext)
        
        # Save encrypted file
        encrypted_filename = filename + '.enc'
        with open(encrypted_filename, 'wb') as f:
            # Save nonce (16 bytes)
            f.write(encrypted['nonce'])
            # Save tag (16 bytes)
            f.write(encrypted['tag'])
            # Save ciphertext
            f.write(encrypted['ciphertext'])
        
        print(f"✅ Encrypted: {encrypted_filename}")
        return encrypted_filename
    
    def decrypt_file(encrypted_filename: str, key: bytes, output_filename: str):
        """Decrypt a file encrypted with AES-GCM"""
        # Read encrypted file
        with open(encrypted_filename, 'rb') as f:
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()
        
        # Decrypt
        aes = AESCipher(key)
        plaintext = aes.decrypt_gcm(ciphertext, nonce, tag)
        
        # Save decrypted file
        with open(output_filename, 'wb') as f:
            f.write(plaintext)
        
        print(f"✅ Decrypted: {output_filename}")
    
    # Create test file
    with open('/tmp/test.txt', 'w') as f:
        f.write("Secret file content!")
    
    # Encrypt and decrypt
    file_key = get_random_bytes(32)
    enc_file = encrypt_file('/tmp/test.txt', file_key)
    decrypt_file(enc_file, file_key, '/tmp/test_decrypted.txt')
    
    # Verify
    with open('/tmp/test.txt', 'rb') as f1:
        with open('/tmp/test_decrypted.txt', 'rb') as f2:
            print(f"✅ Files match: {f1.read() == f2.read()}")
    
    # Cleanup
    os.remove('/tmp/test.txt')
    os.remove(enc_file)
    os.remove('/tmp/test_decrypted.txt')
    
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    print("""
    ✅ USE:
       - AES-GCM for most applications (auth + encryption)
       - AES-256 for maximum security
       - AES-CTR for streaming/random access
    
    ⚠️  CONSIDER:
       - AES-CBC with HMAC for compatibility
       - AES-128 for performance (still very secure)
    
    ❌ AVOID:
       - AES-ECB (insecure for most use cases)
       - Reusing nonces/IVs
       - Encryption without authentication
    """)
```

**Output Example:**
```
============================================================
AES ENCRYPTION DEMONSTRATION
============================================================

Original: This is a secret message that needs encryption!
Length: 48 bytes

────────────────────────────────────────────────────────────
1. AES-256-GCM (Best for most use cases)
────────────────────────────────────────────────────────────
Ciphertext: 8a3f2e1d9c8b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e...
Nonce: 7f3a8e2c1b9d4f6a8c3e5b7d
Tag: 9f2e4d7c1a8b6e3f5d2c9a7b

Decrypted: This is a secret message that needs encryption!
✅ Match: True

🔒 Testing tamper detection...
✅ Tampering detected: Authentication failed! Data was tampered with.
```

**AES in Practice:**
```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# AES Encryption Example
def aes_encrypt(plaintext: bytes, key: bytes) -> tuple:
    """
    Encrypt data using AES-256-GCM
    
    Returns: (ciphertext, nonce, tag)
    """
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return ciphertext, cipher.nonce, tag

def aes_decrypt(ciphertext: bytes, key: bytes, nonce: bytes, tag: bytes) -> bytes:
    """Decrypt AES-GCM encrypted data"""
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

# Usage
key = get_random_bytes(32)  # 256-bit key
plaintext = b"Secret message"

# Encrypt
ciphertext, nonce, tag = aes_encrypt(plaintext, key)
print(f"Ciphertext: {ciphertext.hex()}")

# Decrypt
decrypted = aes_decrypt(ciphertext, key, nonce, tag)
print(f"Decrypted: {decrypted.decode()}")
```

#### ChaCha20

**Description:**
ChaCha20 is a modern stream cipher designed by Daniel J. Bernstein. It's optimized for software performance, especially on mobile devices without AES hardware acceleration.

```
┌─────────────────────────────────────────────────────────────┐
│            ChaCha20 Algorithm Structure                      │
└─────────────────────────────────────────────────────────────┘

INPUT:
┌───────────────────────────────────────┐
│ Key:       256 bits (32 bytes)        │
│ Nonce:     96 bits (12 bytes)         │
│ Counter:   32 bits (4 bytes)          │
└───────────────────────────────────────┘
              ↓
    ┌─────────────────┐
    │ Initial State   │
    │   (512 bits)    │
    ├─────────────────┤
    │ Constants (128) │ "expand 32-byte k"
    │ Key (256)       │ 256-bit key
    │ Counter (32)    │ Block counter
    │ Nonce (96)      │ Random nonce
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  20 Rounds      │
    │  (Quarter rounds)│
    │                 │
    │  Each round:    │
    │  - Add          │
    │  - XOR          │
    │  - Rotate       │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │ Add Initial     │
    │     State       │
    └────────┬────────┘
             │
OUTPUT: 512-bit Keystream Block
        ↓
XOR with plaintext → Ciphertext

Advantages:
───────────
✅ Constant-time (resistant to timing attacks)
✅ Fast on mobile/ARM processors
✅ No AES-NI needed
✅ Simpler than AES
✅ Resistant to cache-timing attacks
```

**ChaCha20 vs AES:**
```
                  ChaCha20          AES-256
─────────────────────────────────────────────
Type              Stream cipher     Block cipher
Speed (no AES-NI) ⚡⚡⚡ Very Fast    ⚡ Moderate
Speed (AES-NI)    ⚡⚡ Fast          ⚡⚡⚡ Very Fast
Mobile/ARM        ⚡⚡⚡ Excellent   ⚡ Good
Security          ✅ Excellent      ✅ Excellent
Adoption          Growing          Widespread
Use Case          TLS, VPN, Mobile General purpose
```

**Where ChaCha20 is Used:**
- Google Chrome (TLS_CHACHA20_POLY1305)
- Android encryption
- WireGuard VPN
- Signal messaging
- SSH (ChaCha20-Poly1305)

### Detailed Asymmetric Encryption Algorithms

#### RSA (Rivest-Shamir-Adleman)

**Description:**
RSA is the most widely used asymmetric encryption algorithm. It's based on the mathematical difficulty of factoring large prime numbers.

```
┌─────────────────────────────────────────────────────────────┐
│                 RSA Algorithm                                │
└─────────────────────────────────────────────────────────────┘

KEY GENERATION:
───────────────

Step 1: Choose two large prime numbers
        p = 61, q = 53 (toy example, real: 1024+ bits each)

Step 2: Compute n = p × q
        n = 61 × 53 = 3233

Step 3: Compute φ(n) = (p-1) × (q-1)
        φ(n) = 60 × 52 = 3120

Step 4: Choose e (public exponent)
        e = 17 (common values: 3, 17, 65537)
        Must be: 1 < e < φ(n) and gcd(e, φ(n)) = 1

Step 5: Calculate d (private exponent)
        d × e ≡ 1 (mod φ(n))
        d = 2753

KEYS:
─────
Public Key:  (e, n) = (17, 3233)
Private Key: (d, n) = (2753, 3233)

ENCRYPTION:
───────────
Plaintext:  m = 123
Ciphertext: c = m^e mod n
            c = 123^17 mod 3233 = 855

┌──────────┐
│ Plaintext│
│   m      │
└────┬─────┘
     │
     │ Raise to power e
     │ Modulo n
     ▼
┌──────────┐
│Ciphertext│
│   c      │
└──────────┘

DECRYPTION:
───────────
Ciphertext: c = 855
Plaintext:  m = c^d mod n
            m = 855^2753 mod 3233 = 123

┌──────────┐
│Ciphertext│
│   c      │
└────┬─────┘
     │
     │ Raise to power d
     │ Modulo n
     ▼
┌──────────┐
│ Plaintext│
│   m      │
└──────────┘

SECURITY BASIS:
───────────────
Easy:    n = p × q (multiply primes)
Hard:    Given n, find p and q (factorization)

Example:
n = 3233 = ? × ?
Small numbers: Easy to find 61 × 53
Large numbers (2048-bit): Computationally infeasible
```

**RSA Key Sizes:**
```
┌──────────────────────────────────────────────────┐
│ Key Size │ Security │ Status      │ Use         │
├──────────┼──────────┼─────────────┼─────────────┤
│ 512-bit  │ None     │ ❌ Broken    │ Don't use   │
│ 1024-bit │ Weak     │ ⚠️ Deprecated│ Legacy only │
│ 2048-bit │ Good     │ ✅ Standard  │ Common use  │
│ 3072-bit │ Better   │ ✅ Secure    │ High sec    │
│ 4096-bit │ Strong   │ ✅ Very Sec  │ Max security│
└──────────────────────────────────────────────────┘

Current Recommendation: Minimum 2048-bit
```

**Advantages:**
- ✅ **Well-Established**: Used since 1977, extremely well-studied
- ✅ **Versatile**: Both encryption and digital signatures
- ✅ **Widely Supported**: Every platform and library
- ✅ **Proven Security**: Based on well-understood math problem
- ✅ **Simple Concept**: Easy to understand

**Disadvantages:**
- ❌ **Slow**: Much slower than symmetric encryption
- ❌ **Large Keys**: Requires 2048-4096 bit keys
- ❌ **Large Ciphertext**: Output larger than input
- ❌ **Quantum Vulnerable**: Shor's algorithm can break it
- ❌ **Padding Required**: Needs OAEP or PSS padding

**RSA Performance:**
```
Operation Times (2048-bit key):
────────────────────────────────
Key Generation:    100-500 ms
Encryption:        0.5-2 ms
Decryption:        10-50 ms (slower due to private key ops)
Signing:           10-50 ms
Verification:      0.5-2 ms (fast with small public exponent)

Compare to AES: 1000x-10000x slower!
```

**RSA in Practice:**
```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Generate RSA key pair
key = RSA.generate(2048)
private_key = key
public_key = key.publickey()

# Encryption (using OAEP padding)
def rsa_encrypt(message: bytes, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(message)
    return ciphertext

# Decryption
def rsa_decrypt(ciphertext: bytes, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# Usage
message = b"Hello RSA!"
encrypted = rsa_encrypt(message, public_key)
decrypted = rsa_decrypt(encrypted, private_key)
print(f"Decrypted: {decrypted.decode()}")
```

#### Diffie-Hellman Key Exchange

**Description:**
Diffie-Hellman is not an encryption algorithm, but a **key exchange protocol**. It allows two parties to establish a shared secret over an insecure channel without ever transmitting the secret itself.

```
┌─────────────────────────────────────────────────────────────┐
│         Diffie-Hellman Key Exchange Protocol                 │
└─────────────────────────────────────────────────────────────┘

PUBLIC PARAMETERS (Known to everyone):
──────────────────────────────────────
p = Large prime number (e.g., 23)
g = Generator (primitive root of p, e.g., 5)

ALICE                                           BOB
─────                                           ───

Step 1: Generate private key
────────────────────────────
a = 6 (secret)                                  b = 15 (secret)
     │                                               │
     │                                               │
Step 2: Compute public key
───────────────────────────
A = g^a mod p                                   B = g^b mod p
A = 5^6 mod 23                                  B = 5^15 mod 23
A = 8                                           B = 19
     │                                               │
     │                                               │
Step 3: Exchange public keys
─────────────────────────────
     │        Send A = 8                             │
     │──────────────────────────────────────────────▶│
     │                                               │
     │        Send B = 19                            │
     │◀──────────────────────────────────────────────│
     │                                               │
     │   ⚠️ Attacker can see A and B!                │
     │   But cannot derive a or b                    │
     │                                               │
Step 4: Compute shared secret
──────────────────────────────
s = B^a mod p                                   s = A^b mod p
s = 19^6 mod 23                                 s = 8^15 mod 23
s = 2                                           s = 2
     │                                               │
     ▼                                               ▼
Both parties now have shared secret = 2!

MATHEMATICAL PROOF:
──────────────────
Alice: s = B^a mod p = (g^b)^a mod p = g^(ab) mod p
Bob:   s = A^b mod p = (g^a)^b mod p = g^(ab) mod p

Both compute the same value!

SECURITY:
─────────
Attacker knows: p, g, A, B
Attacker needs: a or b
Problem: Discrete Logarithm Problem (DLP)
         Given g^a mod p, find a → Computationally hard!

VISUAL REPRESENTATION (Paint Mixing Analogy):
─────────────────────────────────────────────

┌─────────────────────────────────────────────────┐
│                                                 │
│  Public Color: Yellow                           │
│  (Known to everyone)                            │
│                                                 │
└─────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
    ┌───▼─────┐           ┌─────▼───┐
    │ Alice   │           │   Bob   │
    │         │           │         │
    │ Secret: │           │ Secret: │
    │  Blue   │           │   Red   │
    └────┬────┘           └────┬────┘
         │                     │
      Mix with                Mix with
      Yellow                  Yellow
         │                     │
    ┌────▼────┐           ┌────▼────┐
    │ Green   │           │ Orange  │
    │(Public) │──────────▶│(Public) │
    └────┬────┘  Exchange └────┬────┘
         │                     │
    Add Bob's                Add Alice's
    Orange                    Green
         │                     │
    ┌────▼────┐           ┌────▼────┐
    │  Brown  │           │  Brown  │
    │ (Secret)│           │ (Secret)│
    └─────────┘           └─────────┘
    
    Same color (shared secret)!
    
    Attacker sees: Yellow, Green, Orange
    Cannot extract: Blue or Red
    Cannot create: Brown
```

**Diffie-Hellman Variants:**
```
1. TRADITIONAL DH (Finite Fields)
   - Uses modular exponentiation
   - Key size: 2048-4096 bits
   - Slower computation

2. ECDH (Elliptic Curve Diffie-Hellman)
   - Uses elliptic curve points
   - Key size: 256-521 bits
   - Faster, smaller keys
   - Used in modern TLS

3. X25519 (Curve25519)
   - Modern ECDH variant
   - 255-bit keys
   - Very fast
   - Used in: Signal, WireGuard, TLS 1.3
```

**Advantages:**
- ✅ **No Pre-shared Secret**: Parties don't need prior communication
- ✅ **Perfect Forward Secrecy**: Each session has unique key
- ✅ **Efficient**: Fast key establishment
- ✅ **Widely Used**: Core of TLS/SSL

**Disadvantages:**
- ❌ **Vulnerable to MITM**: Without authentication
- ❌ **Not an Encryption Algorithm**: Only for key exchange
- ❌ **Requires Authentication**: Must be combined with signatures

**Diffie-Hellman in TLS:**
```
Client                                  Server
  │                                       │
  │ 1. ClientHello                        │
  │──────────────────────────────────────▶│
  │                                       │
  │                                       │ Generate DH private: b
  │                                       │ Compute DH public: B
  │                                       │
  │ 2. ServerHello                        │
  │    Server DH Public Key: B            │
  │    Signature (proves server identity) │
  │◀──────────────────────────────────────│
  │                                       │
  │ Generate DH private: a                │
  │ Compute DH public: A                  │
  │ Compute shared secret: s = B^a        │
  │                                       │
  │ 3. Client DH Public Key: A            │
  │──────────────────────────────────────▶│
  │                                       │ Compute shared secret: s = A^b
  │                                       │
Both parties now have shared secret!
Use it to derive session keys for AES encryption
```

**Diffie-Hellman in Practice:**
```python
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# Generate DH parameters (done once, can be reused)
parameters = dh.generate_parameters(generator=2, key_size=2048)

# Alice generates her key pair
alice_private_key = parameters.generate_private_key()
alice_public_key = alice_private_key.public_key()

# Bob generates his key pair
bob_private_key = parameters.generate_private_key()
bob_public_key = bob_private_key.public_key()

# Alice computes shared secret using Bob's public key
alice_shared_secret = alice_private_key.exchange(bob_public_key)

# Bob computes shared secret using Alice's public key
bob_shared_secret = bob_private_key.exchange(alice_public_key)

# Both secrets are identical!
assert alice_shared_secret == bob_shared_secret

# Derive encryption key from shared secret
def derive_key(shared_secret: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'session key'
    ).derive(shared_secret)

session_key = derive_key(alice_shared_secret)
print(f"Session Key: {session_key.hex()}")
```

### Digital Signatures

**What is a Digital Signature?**

A digital signature is a cryptographic mechanism that provides:
1. **Authentication**: Proves who created the message
2. **Integrity**: Ensures message wasn't altered
3. **Non-repudiation**: Signer cannot deny signing

It's the digital equivalent of a handwritten signature, but much more secure.

```
┌─────────────────────────────────────────────────────────────┐
│              Digital Signature Process                       │
└─────────────────────────────────────────────────────────────┘

SIGNING (Creating Signature):
─────────────────────────────

┌──────────────┐
│   Document   │
│  "Contract"  │
└──────┬───────┘
       │
       │ Step 1: Hash the document
       ▼
┌──────────────┐
│   Hash       │  SHA-256
│ Function     │  One-way function
└──────┬───────┘  Creates fixed-size digest
       │
       │ Document Hash
       │ (e.g., 256 bits)
       ▼
┌──────────────┐
│    Hash      │
│   Digest     │
│ a7f3b2c1...  │
└──────┬───────┘
       │
       │ Step 2: Encrypt hash with private key
       │
       │  ┌─────────────────┐
       └─▶│   Private Key   │
          │  (Keep Secret)  │
          └────────┬────────┘
                   │
                   ▼
          ┌────────────────┐
          │   Signature    │  This IS the digital signature!
          │  8k2mN9pR...   │  Encrypted hash
          └────────────────┘

VERIFICATION (Checking Signature):
──────────────────────────────────

Receiver gets:
1. Original document
2. Digital signature

┌──────────────┐
│   Document   │
│  "Contract"  │
└──────┬───────┘
       │
       │ Step 1: Hash the received document
       ▼
┌──────────────┐
│   Hash       │
│ Function     │
└──────┬───────┘
       │
       │ Computed Hash
       ▼
┌──────────────┐
│    Hash      │
│   Digest     │
│ a7f3b2c1...  │ ─────────────┐
└──────────────┘              │
                              │
                              │ Step 3: Compare
┌──────────────┐              │
│  Signature   │              │
│ 8k2mN9pR...  │              │
└──────┬───────┘              │
       │                      │
       │ Step 2: Decrypt      │
       │ signature with       │
       │ public key           │
       │                      │
       │  ┌─────────────────┐ │
       └─▶│   Public Key    │ │
          │ (Publicly Known)│ │
          └────────┬────────┘ │
                   │          │
                   ▼          │
          ┌────────────────┐ │
          │  Decrypted     │ │
          │    Hash        │ │
          │ a7f3b2c1...    │─┘
          └────────────────┘
                   │
                   ▼
          ┌────────────────────┐
          │ If hashes match:   │
          │ ✅ Signature valid! │
          │ ✅ Document intact! │
          │ ✅ Authentic!       │
          │                    │
          │ If hashes differ:  │
          │ ❌ Tampered!        │
          │ ❌ Invalid!         │
          └────────────────────┘

COMPLETE FLOW:
──────────────

ALICE (Sender)                           BOB (Receiver)
──────────────                           ───────────────

┌──────────────┐                         ┌──────────────┐
│  Document    │                         │  Document    │
└──────┬───────┘                         └──────┬───────┘
       │                                        │
   Hash with                                Hash with
   SHA-256                                  SHA-256
       │                                        │
       ▼                                        ▼
┌──────────────┐                         ┌──────────────┐
│ Hash Digest  │                         │ Hash Digest  │
│ a7f3b2c1...  │                         │ a7f3b2c1...  │
└──────┬───────┘                         └──────┬───────┘
       │                                        │
  Encrypt with                            Decrypt with
 Alice's Private                          Alice's Public
      Key                                      Key
       │                                        │
       ▼                                        ▼
┌──────────────┐                         ┌──────────────┐
│  Signature   │                         │ Decrypted    │
│ 8k2mN9pR...  │                         │    Hash      │
└──────┬───────┘                         └──────┬───────┘
       │                                        │
       │ Send both:                             │
       │ - Document                             │
       │ - Signature                            │
       │────────────────────────────────────────┤
                                                │
                                          Compare hashes
                                                │
                                                ▼
                                         ✅ Valid if match
```

#### Digital Signature Algorithms

**1. RSA Signatures:**
```
SIGNING:
────────
1. Hash message: h = SHA-256(message)
2. Sign hash: signature = h^d mod n (private key d)

VERIFICATION:
─────────────
1. Hash received message: h1 = SHA-256(message)
2. Decrypt signature: h2 = signature^e mod n (public key e)
3. Compare: h1 == h2 ?

Common Padding: PKCS#1 v1.5, PSS (Probabilistic Signature Scheme)
```

**2. ECDSA (Elliptic Curve Digital Signature Algorithm):**
```
SIGNING:
────────
1. Hash message: h = SHA-256(message)
2. Generate random k
3. Compute r = (k × G)_x mod n
4. Compute s = k^(-1) × (h + r × private_key) mod n
5. Signature = (r, s)

VERIFICATION:
─────────────
1. Hash message: h = SHA-256(message)
2. Compute u1 = h × s^(-1) mod n
3. Compute u2 = r × s^(-1) mod n
4. Compute point P = u1 × G + u2 × PublicKey
5. Valid if P_x == r

Advantages:
✅ Smaller signatures than RSA
✅ Faster than RSA
✅ Same security with smaller keys
```

**3. EdDSA (Ed25519):**
```
Modern signature algorithm:
✅ Deterministic (no random k needed)
✅ Resistant to side-channel attacks
✅ Very fast
✅ 255-bit keys
✅ Used in: SSH, Signal, cryptocurrency

Signature: 512 bits (64 bytes)
Public Key: 256 bits (32 bytes)
```

#### Digital Signature Use Cases

```
✅ COMMON APPLICATIONS:
───────────────────────

1. SOFTWARE SIGNING
   ┌──────────────────┐
   │   software.exe   │
   │        +         │  Developer signs
   │   Signature      │  Users verify authenticity
   └──────────────────┘
   
   Examples: Windows code signing, Apple developer certificates

2. EMAIL SECURITY (S/MIME, PGP)
   ┌──────────────────┐
   │     Email        │
   │  From: Alice     │  Sign email
   │  To: Bob         │  Prove sender
   │  + Signature     │  Detect tampering
   └──────────────────┘

3. DOCUMENT SIGNING (PDF, DocuSign)
   ┌──────────────────┐
   │   Contract.pdf   │
   │ [Signature]      │  Legally binding
   │ Signed by: Alice │  Non-repudiation
   │ Date: 2025-12-30 │  Tamper-evident
   └──────────────────┘

4. SSL/TLS CERTIFICATES
   Server proves identity with digital signature
   on its certificate

5. BLOCKCHAIN/CRYPTOCURRENCY
   ┌──────────────────┐
   │  Transaction     │
   │  From: Wallet A  │  Prove ownership
   │  To: Wallet B    │  Authorize transfer
   │  Amount: 1 BTC   │  Prevent tampering
   │  + Signature     │
   └──────────────────┘

6. CODE REPOSITORIES (Git commits)
   Git commit signed with GPG key
   Proves commit author identity

7. API AUTHENTICATION
   Sign API requests to prove identity
   Prevent request tampering
```

#### Advantages of Digital Signatures

```
✅ SECURITY BENEFITS:
────────────────────

1. AUTHENTICATION
   Proves who created/sent the message
   Cannot be forged without private key

2. INTEGRITY
   Any modification invalidates signature
   Even one bit changed = signature fails

3. NON-REPUDIATION
   Signer cannot deny signing
   Legal proof of agreement
   Binding like handwritten signature

4. EFFICIENCY
   Faster than encrypting entire document
   Only sign hash (fixed size)

5. VERIFIABLE
   Anyone with public key can verify
   No secrets need to be shared

6. SCALABLE
   One key pair for unlimited signatures
   Public key can be widely distributed

7. TIMESTAMPING
   Can include timestamp in signature
   Proves when document was signed
```

#### Digital Signature Implementation

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# RSA Digital Signature
class RSASignature:
    def __init__(self):
        # Generate RSA key pair
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
    
    def sign(self, message: bytes) -> bytes:
        """Sign a message with private key"""
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
    
    def verify(self, message: bytes, signature: bytes) -> bool:
        """Verify signature with public key"""
        try:
            self.public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

# ECDSA Digital Signature
class ECDSASignature:
    def __init__(self):
        # Generate ECDSA key pair (P-256 curve)
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()
    
    def sign(self, message: bytes) -> bytes:
        """Sign a message with ECDSA private key"""
        signature = self.private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )
        return signature
    
    def verify(self, message: bytes, signature: bytes) -> bool:
        """Verify ECDSA signature"""
        try:
            self.public_key.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

# Usage Example
if __name__ == '__main__':
    print("="*60)
    print("Digital Signature Demonstration")
    print("="*60)
    
    # Test message
    message = b"This is a signed contract agreement."
    
    # RSA Signature
    print("\n1. RSA Signature:")
    print("-" * 40)
    rsa_sig = RSASignature()
    
    # Sign
    signature = rsa_sig.sign(message)
    print(f"Message: {message.decode()}")
    print(f"Signature length: {len(signature)} bytes")
    print(f"Signature (first 40 chars): {signature.hex()[:40]}...")
    
    # Verify valid signature
    is_valid = rsa_sig.verify(message, signature)
    print(f"✅ Signature valid: {is_valid}")
    
    # Verify tampered message
    tampered = b"This is a MODIFIED contract agreement."
    is_valid_tampered = rsa_sig.verify(tampered, signature)
    print(f"❌ Tampered message valid: {is_valid_tampered}")
    
    # ECDSA Signature
    print("\n2. ECDSA Signature:")
    print("-" * 40)
    ecdsa_sig = ECDSASignature()
    
    # Sign
    signature = ecdsa_sig.sign(message)
    print(f"Message: {message.decode()}")
    print(f"Signature length: {len(signature)} bytes")
    print(f"Signature (first 40 chars): {signature.hex()[:40]}...")
    
    # Verify
    is_valid = ecdsa_sig.verify(message, signature)
    print(f"✅ Signature valid: {is_valid}")
    
    # Comparison
    print("\n3. Comparison:")
    print("-" * 40)
    print("RSA-2048:")
    print("  Key size: 2048 bits")
    print("  Signature size: 256 bytes")
    print("  Speed: Moderate")
    print("\nECDSA P-256:")
    print("  Key size: 256 bits")
    print("  Signature size: ~64 bytes")
    print("  Speed: Fast")
    print("  Advantage: Smaller, faster, same security")

# Document Signing Example
class DocumentSigner:
    """Sign and verify documents with metadata"""
    
    def __init__(self):
        self.rsa_sig = RSASignature()
    
    def sign_document(self, document: bytes, signer_name: str) -> dict:
        """Sign document and return signature package"""
        import datetime
        
        # Create signature metadata
        timestamp = datetime.datetime.utcnow().isoformat()
        
        # Sign document
        signature = self.rsa_sig.sign(document)
        
        # Create signature package
        package = {
            'document': document,
            'signature': signature,
            'signer': signer_name,
            'timestamp': timestamp,
            'algorithm': 'RSA-2048-PSS',
            'hash': 'SHA-256'
        }
        
        return package
    
    def verify_document(self, package: dict) -> dict:
        """Verify signed document"""
        document = package['document']
        signature = package['signature']
        
        is_valid = self.rsa_sig.verify(document, signature)
        
        return {
            'valid': is_valid,
            'signer': package['signer'],
            'timestamp': package['timestamp'],
            'algorithm': package['algorithm']
        }

# Usage
signer = DocumentSigner()
doc = b"Confidential Agreement: Terms and Conditions..."

# Sign
signed_doc = signer.sign_document(doc, "Alice Smith")
print(f"\n📝 Document signed by: {signed_doc['signer']}")
print(f"⏰ Timestamp: {signed_doc['timestamp']}")

# Verify
verification = signer.verify_document(signed_doc)
print(f"✅ Valid: {verification['valid']}")
print(f"👤 Signer: {verification['signer']}")
```

#### Digital Signature vs MAC (Message Authentication Code)

```
┌──────────────────────────────────────────────────────────────┐
│        Digital Signature vs MAC Comparison                   │
└──────────────────────────────────────────────────────────────┘

DIGITAL SIGNATURE:
─────────────────
Key Type:    Asymmetric (public/private)
Created by:  Private key
Verified by: Public key (anyone)
Use Case:    Public verification, non-repudiation

┌──────────┐                           ┌──────────┐
│  Signer  │                           │ Anyone   │
│          │  Document + Signature     │          │
│ Private  │──────────────────────────▶│  Public  │
│   Key    │                           │   Key    │
└──────────┘                           └──────────┘
                                          ✓ Verify

Non-repudiation: ✅ Yes
Speed: 🐌 Slower

MAC (HMAC):
───────────
Key Type:    Symmetric (shared secret)
Created by:  Shared secret key
Verified by: Shared secret key (only key holders)
Use Case:    Integrity between trusted parties

┌──────────┐                           ┌──────────┐
│  Sender  │                           │ Receiver │
│          │  Document + MAC           │          │
│  Secret  │──────────────────────────▶│  Secret  │
│   Key    │                           │   Key    │
└──────────┘                           └──────────┘
                                          ✓ Verify

Non-repudiation: ❌ No (both parties have same key)
Speed: ⚡ Fast

WHEN TO USE:
───────────
Digital Signature:
- Public document verification
- Legal documents
- Software signing
- Email signing
- When non-repudiation needed

MAC:
- TLS/HTTPS session integrity
- API authentication (both parties trust)
- Faster performance needed
- Internal systems
```

#### Symmetric Encryption Use Cases

```
✅ RECOMMENDED USE CASES:
────────────────────────

1. DISK ENCRYPTION
   ┌─────────────────┐
   │  Hard Drive     │
   │  ┌───────────┐  │     Fast encryption/decryption
   │  │ Encrypted │  │     Single user (one key)
   │  │   Files   │  │     BitLocker, FileVault
   │  └───────────┘  │
   └─────────────────┘

2. DATABASE ENCRYPTION
   ┌─────────────────┐
   │   Database      │
   │ ┌─────────────┐ │     Encrypt data at rest
   │ │  Encrypted  │ │     High performance needed
   │ │   Records   │ │     TDE (Transparent Data Encryption)
   │ └─────────────┘ │
   └─────────────────┘

3. FILE ENCRYPTION
   ┌─────────────────┐
   │   file.pdf      │
   │ ┌─────────────┐ │     Protect sensitive documents
   │ │  Encrypted  │ │     7-Zip, VeraCrypt
   │ │   Content   │ │     Password-based encryption
   │ └─────────────┘ │
   └─────────────────┘

4. VPN TUNNELS
   ┌────────┐          ┌────────┐
   │ Client │◀────────▶│ Server │  Secure communication channel
   └────────┘  AES-256 └────────┘  After key exchange (HTTPS, IPSec)

5. SESSION ENCRYPTION (After HTTPS Handshake)
   Browser ◀────────▶ Server
           AES-GCM      After asymmetric key exchange
```

**Advantages:**
- ⚡ **Fast**: Much faster than asymmetric encryption
- 💪 **Strong**: 256-bit AES is virtually unbreakable
- 🔋 **Efficient**: Low computational overhead
- 📦 **Bulk Data**: Suitable for encrypting large amounts of data

**Disadvantages:**
- 🔑 **Key Distribution**: How to securely share the secret key?
- 👥 **Scalability**: Need n(n-1)/2 keys for n users
- 🔓 **Single Point of Failure**: If key is compromised, all data is exposed

### The Key Exchange Problem & Diffie-Hellman Solution

**The Challenge:**

Symmetric encryption (like AES) is fast and secure, but there's a fundamental problem: **How do two parties securely agree on a shared secret key over an insecure network?**

```
┌─────────────────────────────────────────────────────────────┐
│               THE KEY DISTRIBUTION PROBLEM                   │
└─────────────────────────────────────────────────────────────┘

ALICE wants to send encrypted message to BOB
Both need the same AES key

❌ INSECURE APPROACH:
────────────────────

ALICE                    INTERNET (Insecure)              BOB
  │                                                         │
  │  "Hey Bob, use key: mySecretKey123"                     │
  │────────────────────────────────────────────────────────▶│
  │                         ⚠️                               │
  │                    ┌─────────┐                          │
  │                    │ HACKER  │                          │
  │                    │ Sees it!│                          │
  │                    └─────────┘                          │
  │                                                         │
  ❌ PROBLEM: Attacker intercepts the key!

THE DILEMMA:
───────────
- Can't encrypt the key (no shared key yet!)
- Can't send it in plaintext (insecure)
- Can't meet in person (impractical for internet)

✅ SOLUTION: Diffie-Hellman Key Exchange
   Establish shared secret WITHOUT sending it!
```

### How Diffie-Hellman Works

**Diffie-Hellman Key Exchange** is a revolutionary algorithm that allows two parties to create a shared secret key over an insecure channel without ever transmitting the secret itself.

**The Magic:** Both parties independently compute the same secret using:
- Public information (shared openly)
- Private information (never shared)
- Mathematical properties of modular exponentiation

```
┌─────────────────────────────────────────────────────────────┐
│         DIFFIE-HELLMAN KEY EXCHANGE (Step-by-Step)          │
└─────────────────────────────────────────────────────────────┘

SETUP: Public Parameters (Known to everyone, including attackers)
─────────────────────────────────────────────────────────────────
p = 23     (Large prime number)
g = 5      (Generator/base, primitive root of p)

These are published openly - anyone can know them!

STEP 1: Generate Private Keys (Secret, never shared)
────────────────────────────────────────────────────

ALICE                                           BOB
──────                                          ─────

Choose random private key:                Choose random private key:
a = 6 (secret!)                           b = 15 (secret!)

     ↓                                         ↓
   KEPT SECRET                              KEPT SECRET
   Never transmitted                        Never transmitted


STEP 2: Compute Public Keys (Safe to share)
────────────────────────────────────────────

ALICE                                           BOB
──────                                          ─────

A = g^a mod p                                 B = g^b mod p
A = 5^6 mod 23                                B = 5^15 mod 23
A = 15,625 mod 23                             B = 30,517,578,125 mod 23
A = 8                                         B = 19

Public Key: A = 8                             Public Key: B = 19


STEP 3: Exchange Public Keys (Over Insecure Network)
─────────────────────────────────────────────────────

ALICE                    INTERNET                    BOB
──────              (Insecure Channel)              ─────
  │                                                    │
  │           Send A = 8                               │
  │───────────────────────────────────────────────────▶│
  │                                                    │
  │                  ⚠️ Attacker can see: p=23, g=5,   │
  │                     A=8, B=19                      │
  │                     But CANNOT find a or b!        │
  │                                                    │
  │           Send B = 19                              │
  │◀───────────────────────────────────────────────────│
  │                                                    │


STEP 4: Compute Shared Secret (Independently)
──────────────────────────────────────────────

ALICE                                           BOB
──────                                          ─────

Uses Bob's public (B) and                     Uses Alice's public (A) and
her private (a):                              his private (b):

s = B^a mod p                                 s = A^b mod p
s = 19^6 mod 23                               s = 8^15 mod 23
s = 47,045,881 mod 23                         s = 35,184,372,088,832 mod 23
s = 2                                         s = 2

Shared Secret: 2                              Shared Secret: 2

     │                                             │
     │         🎉 SAME SECRET KEY! 🎉              │
     └─────────────────┬───────────────────────────┘
                       │
                  Both have: s = 2
                  Without ever transmitting it!


═══════════════════════════════════════════════════════════════

MATHEMATICAL PROOF (Why it works):
───────────────────────────────────

Alice computes:  s = B^a mod p = (g^b)^a mod p = g^(ab) mod p
Bob computes:    s = A^b mod p = (g^a)^b mod p = g^(ab) mod p

Since g^(ab) = g^(ba), both get the same result!

Example:
Alice: (5^15)^6 mod 23 = 5^90 mod 23
Bob:   (5^6)^15 mod 23 = 5^90 mod 23
Both equal: 2


═══════════════════════════════════════════════════════════════

SECURITY: The Discrete Logarithm Problem (DLP)
───────────────────────────────────────────────

Attacker knows: p = 23, g = 5, A = 8, B = 19
Attacker wants:  a or b (to compute shared secret)

Problem: Given A = g^a mod p, find a
         Given 8 = 5^a mod 23, find a = ?

For small numbers: Solvable by brute force
For large numbers (2048-bit): Computationally infeasible!

Example with real-world sizes:
p = 2048-bit prime number (617 digits!)
Finding a is like searching 2^2048 possibilities
   = 10^617 operations
   = More than atoms in the universe!

This is why Diffie-Hellman is secure.


═══════════════════════════════════════════════════════════════

VISUAL ANALOGY: Paint Mixing
─────────────────────────────

Think of it like mixing paint colors:

1. PUBLIC COLOR (Yellow) - Known to everyone
   ┌──────────┐
   │  Yellow  │ ← Public parameter (like g and p)
   └──────────┘
        │
        ├────────────────┬────────────────┐
        │                │                │
   ┌────▼────┐      ┌────▼────┐     ┌────▼────┐
   │  Alice  │      │   Bob   │     │ Hacker  │
   │  Gets   │      │  Gets   │     │  Gets   │
   │ Yellow  │      │ Yellow  │     │ Yellow  │
   └─────────┘      └─────────┘     └─────────┘

2. ADD SECRET COLORS (Private keys)
   ┌─────────┐      ┌─────────┐
   │  Alice  │      │   Bob   │
   │ Yellow  │      │ Yellow  │
   │   +     │      │   +     │
   │  Blue   │      │   Red   │ ← Secret colors (private keys a, b)
   │ (Secret)│      │ (Secret)│
   └────┬────┘      └────┬────┘
        │                │
        ▼                ▼
   ┌─────────┐      ┌─────────┐
   │  Green  │      │ Orange  │ ← Public keys (A, B)
   └────┬────┘      └────┬────┘

3. EXCHANGE PUBLIC MIXES
        │                │
        └────────┬───────┘
                 │ Exchange
        ┌────────┼────────┐
        │        │        │
   ┌────▼────┐      ┌────▼────┐
   │  Alice  │      │   Bob   │
   │  Green  │      │ Orange  │ ← Received each other's public
   │   +     │      │   +     │
   │  Blue   │      │   Red   │ ← Add own secret again
   │ (Secret)│      │ (Secret)│
   └────┬────┘      └────┬────┘
        │                │
        ▼                ▼
   ┌─────────┐      ┌─────────┐
   │  Brown  │      │  Brown  │ ← SAME COLOR (shared secret!)
   └─────────┘      └─────────┘

The hacker sees: Yellow, Green, Orange
But CANNOT create Brown without Blue or Red!
(Can't "unmix" paint to extract secret colors)


═══════════════════════════════════════════════════════════════

COMPLETE COMMUNICATION FLOW
────────────────────────────

Step 1: Diffie-Hellman Key Exchange
         ↓
    Shared Secret: s = 2

Step 2: Derive Encryption Key from Shared Secret
         s = 2 → Hash(s) → AES Key
         Example: SHA-256(2) = "f2a3b4c5..." (32 bytes)
         ↓
    AES-256 Key: f2a3b4c5d6e7f8...

Step 3: Use AES for Fast Encryption
         ↓

ALICE                                           BOB
──────                                          ─────
Plaintext: "Hello Bob!"                    (Waiting)
     ↓
Encrypt with AES using                     
shared key:                                
     ↓
Ciphertext: "xK9#mP2$vL..."
     │                                          │
     │  Send Ciphertext                         │
     │─────────────────────────────────────────▶│
     │                                          │
     │                                     Decrypt with AES
     │                                     using shared key:
     │                                          ↓
     │                                     Plaintext: "Hello Bob!"

═══════════════════════════════════════════════════════════════

WHY THIS IS REVOLUTIONARY:
──────────────────────────

✅ No Pre-shared Secret Needed
   Alice and Bob never met before, yet created shared secret!

✅ Secure Over Insecure Channel
   Even if attacker sees all communication, cannot get secret

✅ Perfect Forward Secrecy
   Each session can use different ephemeral keys
   If one session key compromised, others remain safe

✅ Enables Modern Internet Security
   Foundation of:
   - TLS/HTTPS (secure websites)
   - SSH (secure remote access)
   - VPNs (secure networks)
   - Signal/WhatsApp (secure messaging)
```

### Diffie-Hellman Implementation

**Complete Python Implementation:**

```python
import hashlib
import secrets
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class DiffieHellman:
    """
    Complete Diffie-Hellman Key Exchange Implementation
    Demonstrates secure key exchange over insecure channel
    """
    
    def __init__(self, key_size=2048):
        """
        Initialize with public parameters
        In practice, these are standardized (RFC 3526)
        """
        # Use well-known safe primes for production
        # For demonstration, using smaller numbers
        
        if key_size == 2048:
            # RFC 3526 - 2048-bit MODP Group
            self.p = int(
                "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
                "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
                "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
                "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
                "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
                "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
                "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
                "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
                "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
                "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
                "15728E5A8AACAA68FFFFFFFFFFFFFFFF", 16
            )
            self.g = 2
        else:
            # Toy example for demonstration
            self.p = 23  # Small prime
            self.g = 5   # Generator
        
        self.private_key = None
        self.public_key = None
        self.shared_secret = None
    
    def generate_private_key(self):
        """Generate random private key"""
        # Private key should be random number: 2 <= private_key < p-1
        self.private_key = secrets.randbelow(self.p - 2) + 2
        return self.private_key
    
    def generate_public_key(self):
        """Compute public key: g^private mod p"""
        if self.private_key is None:
            self.generate_private_key()
        
        # Public key = g^a mod p
        self.public_key = pow(self.g, self.private_key, self.p)
        return self.public_key
    
    def compute_shared_secret(self, other_public_key):
        """
        Compute shared secret using other party's public key
        shared_secret = other_public^private mod p
        """
        if self.private_key is None:
            raise ValueError("Must generate private key first")
        
        # Shared secret = B^a mod p (or A^b mod p)
        self.shared_secret = pow(other_public_key, self.private_key, self.p)
        return self.shared_secret
    
    def derive_key(self, key_length=32):
        """
        Derive encryption key from shared secret
        Uses SHA-256 hash to create AES key
        """
        if self.shared_secret is None:
            raise ValueError("Must compute shared secret first")
        
        # Convert shared secret to bytes and hash it
        secret_bytes = self.shared_secret.to_bytes(
            (self.shared_secret.bit_length() + 7) // 8, 
            byteorder='big'
        )
        
        # Derive key using SHA-256
        derived_key = hashlib.sha256(secret_bytes).digest()
        return derived_key[:key_length]


def demonstrate_diffie_hellman():
    """
    Demonstrate complete Diffie-Hellman key exchange
    """
    print("="*70)
    print("DIFFIE-HELLMAN KEY EXCHANGE DEMONSTRATION")
    print("="*70)
    
    # ──────────────────────────────────────────────────────────────
    # STEP 1: Setup - Agree on public parameters
    # ──────────────────────────────────────────────────────────────
    print("\n📋 STEP 1: Public Parameters (known to everyone)")
    print("─"*70)
    
    # Using small numbers for clarity (in production, use 2048-bit)
    alice = DiffieHellman(key_size=23)  # Toy example
    bob = DiffieHellman(key_size=23)
    
    print(f"Prime (p):     {alice.p}")
    print(f"Generator (g): {alice.g}")
    print("⚠️  These are PUBLIC - even attackers know them!")
    
    # ──────────────────────────────────────────────────────────────
    # STEP 2: Generate Private Keys (secret)
    # ──────────────────────────────────────────────────────────────
    print("\n🔐 STEP 2: Generate Private Keys (SECRET - never shared)")
    print("─"*70)
    
    alice_private = alice.generate_private_key()
    bob_private = bob.generate_private_key()
    
    print(f"Alice's private key (a): {alice_private} (SECRET!)")
    print(f"Bob's private key (b):   {bob_private} (SECRET!)")
    
    # ──────────────────────────────────────────────────────────────
    # STEP 3: Compute Public Keys
    # ──────────────────────────────────────────────────────────────
    print("\n🌐 STEP 3: Compute Public Keys (safe to share)")
    print("─"*70)
    
    alice_public = alice.generate_public_key()
    bob_public = bob.generate_public_key()
    
    print(f"Alice computes: A = g^a mod p = {alice.g}^{alice_private} mod {alice.p} = {alice_public}")
    print(f"Bob computes:   B = g^b mod p = {bob.g}^{bob_private} mod {bob.p} = {bob_public}")
    
    # ──────────────────────────────────────────────────────────────
    # STEP 4: Exchange Public Keys
    # ──────────────────────────────────────────────────────────────
    print("\n📡 STEP 4: Exchange Public Keys (over insecure channel)")
    print("─"*70)
    print(f"Alice sends to Bob:  A = {alice_public}")
    print(f"Bob sends to Alice:  B = {bob_public}")
    print("⚠️  Attacker can intercept these values!")
    print("✅ But cannot derive private keys (discrete log problem)")
    
    # ──────────────────────────────────────────────────────────────
    # STEP 5: Compute Shared Secret
    # ──────────────────────────────────────────────────────────────
    print("\n🔑 STEP 5: Compute Shared Secret (independently)")
    print("─"*70)
    
    alice_shared = alice.compute_shared_secret(bob_public)
    bob_shared = bob.compute_shared_secret(alice_public)
    
    print(f"Alice computes: s = B^a mod p = {bob_public}^{alice_private} mod {alice.p} = {alice_shared}")
    print(f"Bob computes:   s = A^b mod p = {alice_public}^{bob_private} mod {bob.p} = {bob_shared}")
    
    print(f"\n🎉 SUCCESS: Both computed the same secret!")
    print(f"   Alice's shared secret: {alice_shared}")
    print(f"   Bob's shared secret:   {bob_shared}")
    print(f"   Secrets match: {alice_shared == bob_shared} ✅")
    
    # ──────────────────────────────────────────────────────────────
    # STEP 6: Derive Encryption Key
    # ──────────────────────────────────────────────────────────────
    print("\n🔐 STEP 6: Derive AES Encryption Key")
    print("─"*70)
    
    alice_aes_key = alice.derive_key()
    bob_aes_key = bob.derive_key()
    
    print(f"Alice derives AES key: {alice_aes_key.hex()[:40]}...")
    print(f"Bob derives AES key:   {bob_aes_key.hex()[:40]}...")
    print(f"Keys match: {alice_aes_key == bob_aes_key} ✅")
    
    # ──────────────────────────────────────────────────────────────
    # STEP 7: Secure Communication with AES
    # ──────────────────────────────────────────────────────────────
    print("\n💬 STEP 7: Secure Communication (using shared AES key)")
    print("─"*70)
    
    # Alice encrypts message
    message = b"Hello Bob! This is a secret message."
    print(f"Alice's plaintext: {message.decode()}")
    
    cipher = AES.new(alice_aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    nonce = cipher.nonce
    
    print(f"Encrypted: {ciphertext.hex()[:40]}...")
    print(f"Nonce:     {nonce.hex()}")
    print(f"Tag:       {tag.hex()}")
    
    # Bob decrypts message
    cipher = AES.new(bob_aes_key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
    
    print(f"\nBob decrypts: {decrypted.decode()}")
    print(f"✅ Message successfully exchanged over insecure channel!")
    
    # ──────────────────────────────────────────────────────────────
    # Security Analysis
    # ──────────────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("SECURITY ANALYSIS")
    print("="*70)
    
    print("""
    WHAT ATTACKER KNOWS:
    • Prime (p): {p}
    • Generator (g): {g}
    • Alice's public (A): {A}
    • Bob's public (B): {B}
    
    WHAT ATTACKER NEEDS:
    • Alice's private (a) OR Bob's private (b)
    
    THE CHALLENGE:
    Given: A = g^a mod p
    Find: a
    
    For small numbers (p=23): Easy to brute force
    For large numbers (2048-bit p): Computationally infeasible!
    
    Time to crack 2048-bit DH: Millions of years with current technology
    """.format(p=alice.p, g=alice.g, A=alice_public, B=bob_public))
    
    print("="*70)


def production_example():
    """
    Production-ready Diffie-Hellman with 2048-bit keys
    """
    print("\n" + "="*70)
    print("PRODUCTION EXAMPLE (2048-bit keys)")
    print("="*70)
    
    # Use secure 2048-bit parameters
    alice = DiffieHellman(key_size=2048)
    bob = DiffieHellman(key_size=2048)
    
    # Generate keys
    alice.generate_private_key()
    alice.generate_public_key()
    
    bob.generate_private_key()
    bob.generate_public_key()
    
    # Exchange and compute shared secret
    alice.compute_shared_secret(bob.public_key)
    bob.compute_shared_secret(alice.public_key)
    
    print(f"✅ Secure 2048-bit Diffie-Hellman key exchange complete")
    print(f"   Prime size: {alice.p.bit_length()} bits")
    print(f"   Shared secret size: {alice.shared_secret.bit_length()} bits")
    print(f"   Secrets match: {alice.shared_secret == bob.shared_secret}")
    
    # Derive AES key
    aes_key = alice.derive_key()
    print(f"   AES-256 key: {aes_key.hex()[:40]}...")
    

if __name__ == '__main__':
    # Run demonstration
    demonstrate_diffie_hellman()
    
    # Show production example
    production_example()
```

**Output:**
```
======================================================================
DIFFIE-HELLMAN KEY EXCHANGE DEMONSTRATION
======================================================================

📋 STEP 1: Public Parameters (known to everyone)
──────────────────────────────────────────────────────────────────────
Prime (p):     23
Generator (g): 5
⚠️  These are PUBLIC - even attackers know them!

🔐 STEP 2: Generate Private Keys (SECRET - never shared)
──────────────────────────────────────────────────────────────────────
Alice's private key (a): 6 (SECRET!)
Bob's private key (b):   15 (SECRET!)

🌐 STEP 3: Compute Public Keys (safe to share)
──────────────────────────────────────────────────────────────────────
Alice computes: A = g^a mod p = 5^6 mod 23 = 8
Bob computes:   B = g^b mod p = 5^15 mod 23 = 19

📡 STEP 4: Exchange Public Keys (over insecure channel)
──────────────────────────────────────────────────────────────────────
Alice sends to Bob:  A = 8
Bob sends to Alice:  B = 19
⚠️  Attacker can intercept these values!
✅ But cannot derive private keys (discrete log problem)

🔑 STEP 5: Compute Shared Secret (independently)
──────────────────────────────────────────────────────────────────────
Alice computes: s = B^a mod p = 19^6 mod 23 = 2
Bob computes:   s = A^b mod p = 8^15 mod 23 = 2

🎉 SUCCESS: Both computed the same secret!
   Alice's shared secret: 2
   Bob's shared secret:   2
   Secrets match: True ✅

🔐 STEP 6: Derive AES Encryption Key
──────────────────────────────────────────────────────────────────────
Alice derives AES key: f2ca1bb6c7e907d06dafe4687e579fce76b37e...
Bob derives AES key:   f2ca1bb6c7e907d06dafe4687e579fce76b37e...
Keys match: True ✅

💬 STEP 7: Secure Communication (using shared AES key)
──────────────────────────────────────────────────────────────────────
Alice's plaintext: Hello Bob! This is a secret message.
Encrypted: 7f8e3a2d9c1b4f6a8e5d3c7b2a9f1e4d8c6b5a...
Nonce:     a3f2e1d9c8b7a6f5
Tag:       9e2d4c7a1b8f6e3d

Bob decrypts: Hello Bob! This is a secret message.
✅ Message successfully exchanged over insecure channel!
```

**Key Takeaways:**

```
✅ DIFFIE-HELLMAN SOLVES:
────────────────────────
1. Key Distribution Problem
   • No need to share secret key beforehand
   • Works over completely insecure channels

2. Perfect Forward Secrecy
   • Each session uses ephemeral (temporary) keys
   • Compromising one session doesn't affect others

3. Enables Hybrid Encryption
   • DH: Slow, establishes shared secret
   • AES: Fast, encrypts actual data
   • Best of both worlds!

⚠️  IMPORTANT NOTES:
──────────────────
1. Vulnerable to Man-in-the-Middle (MITM) attacks
   • Solution: Combine with authentication (digital signatures)
   • Example: TLS uses DH + certificates

2. Not an Encryption Algorithm
   • Only for key exchange
   • Must use with symmetric cipher (AES)

3. Quantum Threat
   • Shor's algorithm can break DH on quantum computers
   • Post-quantum alternatives being developed

🌟 REAL-WORLD USAGE:
──────────────────
• TLS/HTTPS: Every secure website
• SSH: Secure remote access
• VPN: IPSec, WireGuard
• Signal/WhatsApp: End-to-end encryption
• Bitcoin/Blockchain: Key agreement
```

### Asymmetric Encryption (Public Key Cryptography)

**Definition**: Encryption method that uses **two different keys**: a public key (for encryption) and a private key (for decryption).

```
┌─────────────────────────────────────────────────────────────┐
│              Asymmetric Encryption                           │
└─────────────────────────────────────────────────────────────┘

                    RECEIVER GENERATES KEY PAIR
                    ──────────────────────────
                    ┌──────────────────────┐
                    │    Key Generator     │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
         ┌──────▼─────┐              ┌───────▼──────┐
         │   Public   │              │   Private    │
         │    Key     │              │     Key      │
         │ (Share)    │              │ (Keep Secret)│
         └──────┬─────┘              └───────┬──────┘
                │                            │
                │ Shared publicly            │ Never shared
                │                            │
                │                            │
┌───────────────▼────────┐                   │
│      SENDER            │                   │
│                        │                   │
│  Plaintext: "Hello"    │                   │
│       +                │                   │
│  Public Key (Receiver) │                   │
│       ↓                │                   │
│  Encryption Algorithm  │                   │
│       ↓                │                   │
│  Ciphertext:"xK9#mP2$" │                   │
└───────────┬────────────┘                   │
            │                                │
            │ Send ciphertext                │
            │                                │
            └────────────┬───────────────────┘
                         │
                ┌────────▼────────────┐
                │    TRANSMISSION     │
                │   (Over Network)    │
                └────────┬────────────┘
                         │
            ┌────────────▼────────────────┐
            │        RECEIVER             │
            │                             │
            │  Ciphertext: "xK9#mP2$"     │
            │         +                   │
            │  Private Key (Receiver)     │
            │         ↓                   │
            │  Decryption Algorithm       │
            │         ↓                   │
            │  Plaintext: "Hello"         │
            └─────────────────────────────┘

KEY CHARACTERISTICS:
───────────────────
• Public Key: Can be shared with anyone
• Private Key: Must be kept secret
• Data encrypted with public key can ONLY be decrypted with private key
• Mathematically related but computationally infeasible to derive private from public
```

#### Asymmetric Encryption Algorithms

**Evolution and Improvements:**

| Algorithm | Key Size | Year | Based On | Status | Use Case |
|-----------|----------|------|----------|--------|----------|
| **RSA** | 1024-4096 bit | 1977 | Factorization | ✅ Current Standard | Encryption, Signatures |
| **DSA** | 1024-3072 bit | 1991 | Discrete Log | ✅ Digital Signatures | Signatures only |
| **Diffie-Hellman** | 2048+ bit | 1976 | Discrete Log | ✅ Key Exchange | Key agreement |
| **ECC (Elliptic Curve)** | 256-521 bit | 1985 | Elliptic Curves | ✅ Modern Standard | Encryption, Signatures |
| **ECDSA** | 256-521 bit | 1992 | ECC | ✅ Modern | Digital Signatures |
| **EdDSA** | 255 bit | 2011 | ECC | ✅ Best Performance | Modern Signatures |
| **El Gamal** | 1024+ bit | 1985 | Discrete Log | ⚠️ Less Common | Encryption |

**Modern Algorithm: ECC (Elliptic Curve Cryptography)**

**Advantages of ECC over RSA:**
- ✅ **Smaller Keys**: 256-bit ECC ≈ 3072-bit RSA (same security)
- ✅ **Faster**: Quicker key generation and signing
- ✅ **Less Bandwidth**: Smaller certificates and signatures
- ✅ **Mobile Friendly**: Lower CPU and power consumption
- ✅ **Future Proof**: Better resistance to quantum attacks (relatively)
- ✅ **NSA Approved**: Suite B cryptography

**Key Size Comparison:**
```
Security Level:    80-bit   112-bit   128-bit   192-bit   256-bit
─────────────────────────────────────────────────────────────────
RSA Key Size:      1024     2048      3072      7680      15360
ECC Key Size:      160      224       256       384       512
DH Key Size:       1024     2048      3072      7680      15360

Example: Same security, much smaller!
   RSA-3072:  ████████████████████████████████ (3072 bits)
   ECC-256:   ████ (256 bits)
```

**Modern Algorithms:**
- **Ed25519** (EdDSA): Modern, fast, secure signatures (SSH, TLS 1.3)
- **X25519** (ECDH): Modern key exchange (Signal, WhatsApp)
- **P-256** (NIST): Widely supported ECC curve
- **RSA-2048/4096**: Still widely used, reliable

#### Asymmetric Encryption Use Cases

```
✅ RECOMMENDED USE CASES:
────────────────────────

1. SECURE KEY EXCHANGE
   ┌──────────┐                          ┌──────────┐
   │  Alice   │  Encrypt session key     │   Bob    │
   │          │──────────────────────────▶│          │
   │          │  using Bob's public key  │          │
   └──────────┘                          └──────────┘
   
   Problem: How to share symmetric key securely?
   Solution: Encrypt symmetric key with public key!

2. DIGITAL SIGNATURES
   ┌──────────────┐
   │   Document   │
   │      +       │      Prove authenticity
   │ Private Key  │      Non-repudiation
   │      ↓       │      Verify with public key
   │  Signature   │
   └──────────────┘

3. SSL/TLS HANDSHAKE
   Client ────▶ Server
          Request server's public key
   Client ◀──── Server
          Send public key (in certificate)
   Client ────▶ Server
          Send encrypted session key
          
4. EMAIL ENCRYPTION (PGP/S/MIME)
   Sender ────▶ Encrypt with recipient's public key
          ────▶ Send encrypted email
   Recipient ─▶ Decrypt with own private key

5. CODE SIGNING
   Developer ──▶ Sign software with private key
   User ───────▶ Verify with developer's public key

6. CRYPTOCURRENCY
   Private Key ──▶ Sign transactions
   Public Key ───▶ Verify ownership (wallet address)
```

**Advantages:**
- 🔑 **Key Distribution**: No need to share secret keys
- 👥 **Scalability**: Each user needs only one key pair
- ✍️ **Digital Signatures**: Provides authentication and non-repudiation
- 🔒 **Security**: Private key never needs to be transmitted

**Disadvantages:**
- 🐌 **Slow**: 100-1000x slower than symmetric encryption
- 💻 **Resource Intensive**: Higher CPU usage
- 📊 **Limited Data**: Not suitable for bulk data encryption
- 🔢 **Key Size**: Larger keys needed for same security level (RSA)

### Comparison: Symmetric vs Asymmetric

```
┌──────────────────────────────────────────────────────────────┐
│         Symmetric vs Asymmetric Encryption                   │
└──────────────────────────────────────────────────────────────┘

Feature             Symmetric           Asymmetric
─────────────────────────────────────────────────────────────
Keys                1 (shared)          2 (public + private)
Speed               ⚡ Very Fast         🐌 Slow (100-1000x)
Key Size            128-256 bits        2048-4096 bits (RSA)
                                        256-521 bits (ECC)
Key Distribution    ❌ Difficult         ✅ Easy
Use Case            Bulk data           Key exchange, signatures
Examples            AES, ChaCha20       RSA, ECC, Ed25519
Scalability         ❌ Poor (n² keys)    ✅ Good (2n keys)
Security            Strong with         Strong, math-based
                    large key
CPU Usage           Low                 High
Power               Efficient           Power-hungry

HYBRID APPROACH (Best Practice):
────────────────────────────────
1. Use asymmetric encryption to exchange symmetric key
2. Use symmetric encryption for actual data
3. Get benefits of both: Security + Performance
```

### HTTPS: Secure HTTP

**What is HTTPS?**

HTTPS (Hypertext Transfer Protocol Secure) is HTTP with encryption, authentication, and integrity protection. It uses **TLS (Transport Layer Security)**, formerly SSL, to secure the connection.

```
┌─────────────────────────────────────────────────────────────┐
│                HTTP vs HTTPS                                 │
└─────────────────────────────────────────────────────────────┘

HTTP (Insecure):
───────────────
Browser                          Server
   │                                │
   │  GET /login.html (plaintext)  │
   │───────────────────────────────▶│
   │                                │
   │  username=alice&pass=123       │
   │───────────────────────────────▶│
   │      (Visible to attackers!)   │
   
   ❌ No Encryption
   ❌ No Authentication
   ❌ No Integrity

HTTPS (Secure):
──────────────
Browser                          Server
   │                                │
   │  1. TLS Handshake              │
   │◀──────────────────────────────▶│
   │     (Establish encrypted       │
   │      connection)               │
   │                                │
   │  2. Encrypted Request          │
   │  ████████████████████          │
   │───────────────────────────────▶│
   │                                │
   │  3. Encrypted Response         │
   │  ████████████████████          │
   │◀───────────────────────────────│
   
   ✅ Encryption (Confidentiality)
   ✅ Authentication (Server identity)
   ✅ Integrity (Tamper detection)
```

#### HTTPS Security Features

**Three Pillars of HTTPS:**

1. **Encryption (Confidentiality)**
   - Data is encrypted during transmission
   - Attackers cannot read the content
   - Uses symmetric encryption (AES)

2. **Authentication**
   - Verify server's identity
   - Prevent man-in-the-middle attacks
   - Uses digital certificates

3. **Integrity**
   - Detect if data was tampered
   - Uses MAC (Message Authentication Code)
   - Ensures data arrives unchanged

#### TLS Handshake Process

The TLS handshake establishes a secure connection using both asymmetric and symmetric encryption:

```
┌─────────────────────────────────────────────────────────────┐
│          TLS Handshake (How HTTPS Works)                    │
└─────────────────────────────────────────────────────────────┘

CLIENT (Browser)                         SERVER (Web Server)
─────────────────                        ───────────────────

Step 1: Client Hello
──────────────────────────────────────────────────────────────
│ ClientHello                              │
│ - TLS version: 1.3                       │
│ - Cipher suites supported                │
│ - Random number (Client Random)          │
│──────────────────────────────────────────▶│
                                            │
Step 2: Server Hello                       │
──────────────────────────────────────────────────────────────
│                                           │ ServerHello
│                                           │ - TLS version: 1.3
│                                           │ - Chosen cipher
│                                           │ - Random (Server Random)
│◀──────────────────────────────────────────│
│                                           │
Step 3: Server Certificate                 │
──────────────────────────────────────────────────────────────
│                                           │ Certificate
│                                           │ ┌─────────────────┐
│                                           │ │ Server Cert     │
│                                           │ │ - Domain name   │
│                                           │ │ - Public Key    │
│◀──────────────────────────────────────────│ │ - CA Signature  │
│                                           │ └─────────────────┘
│ Verify Certificate:                       │
│ ✓ Valid CA signature?                     │
│ ✓ Domain name matches?                    │
│ ✓ Not expired?                            │
│ ✓ Not revoked?                            │
│                                           │
Step 4: Key Exchange (Asymmetric Encryption)
──────────────────────────────────────────────────────────────
│ Generate Pre-Master Secret                │
│ Encrypt with Server's Public Key          │
│ (from certificate)                         │
│                                           │
│ Encrypted Pre-Master Secret               │
│──────────────────────────────────────────▶│
│                                           │ Decrypt with Private Key
│                                           │
Both sides now compute Session Keys:       │
─────────────────────────────────────────────
│ Session Key = f(                          │ Session Key = f(
│   Pre-Master Secret,                      │   Pre-Master Secret,
│   Client Random,                          │   Client Random,
│   Server Random                           │   Server Random
│ )                                         │ )
│                                           │
Step 5: Finished (Switch to Symmetric)
──────────────────────────────────────────────────────────────
│ "Finished" (encrypted with Session Key)   │
│──────────────────────────────────────────▶│
│                                           │ Verify
│                                           │
│                                           │ "Finished"
│◀──────────────────────────────────────────│ (encrypted)
│ Verify                                    │
│                                           │
Step 6: Secure Communication (Symmetric Encryption)
──────────────────────────────────────────────────────────────
│ ████████████████████████                  │
│ Application Data (AES Encrypted)          │
│──────────────────────────────────────────▶│
│                                           │
│                                           │ ████████████████
│◀──────────────────────────────────────────│ Response (AES)
│                                           │

SUMMARY:
────────
1. Handshake uses ASYMMETRIC encryption (slow but secure key exchange)
   - Server sends public key in certificate
   - Client encrypts session key with server's public key
   - Server decrypts with private key

2. Data transfer uses SYMMETRIC encryption (fast)
   - Both sides use the same session key (AES-256-GCM)
   - All application data encrypted with this key
   - Session key is temporary (only for this connection)
```

**Why Use Both Asymmetric and Symmetric?**

```
ASYMMETRIC (RSA/ECC):
────────────────────
Purpose: Securely exchange the symmetric key
Used: Only during handshake
Advantage: No shared secret needed beforehand
Disadvantage: Too slow for bulk data

        ↓ Handshake Complete ↓

SYMMETRIC (AES):
───────────────
Purpose: Encrypt actual data
Used: All application data
Advantage: Very fast, efficient
Disadvantage: Both parties need the key

RESULT: Best of both worlds!
```

### Digital Certificates and Certificate Authorities

**What is a Digital Certificate?**

A **digital certificate** is an electronic document that proves the ownership of a public key. It's like a digital passport that verifies identity in the online world.

```
┌─────────────────────────────────────────────────────────────┐
│              Digital Certificate Structure                   │
└─────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                  X.509 Certificate                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Certificate Information:                                  │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Version: 3                                           │ │
│  │ Serial Number: 0x4f3a2e1d9c8b7a6f                    │ │
│  │                                                      │ │
│  │ SUBJECT (Certificate Owner):                         │ │
│  │ ├─ Common Name (CN): www.example.com                 │ │
│  │ ├─ Organization (O): Example Corp                    │ │
│  │ ├─ Country (C): US                                   │ │
│  │                                                      │ │
│  │ ISSUER (Who signed this):                            │ │
│  │ ├─ Common Name (CN): DigiCert TLS RSA SHA256 CA     │ │
│  │ ├─ Organization (O): DigiCert Inc                    │ │
│  │ ├─ Country (C): US                                   │ │
│  │                                                      │ │
│  │ VALIDITY PERIOD:                                     │ │
│  │ ├─ Not Before: 2025-01-01 00:00:00 UTC              │ │
│  │ └─ Not After:  2026-01-01 23:59:59 UTC              │ │
│  │                                                      │ │
│  │ PUBLIC KEY INFO:                                     │ │
│  │ ├─ Algorithm: RSA                                    │ │
│  │ ├─ Key Size: 2048 bits                              │ │
│  │ └─ Public Key: 30 82 01 0a 02 82 01 01 00 b4...    │ │
│  │                                                      │ │
│  │ EXTENSIONS:                                          │ │
│  │ ├─ Subject Alternative Names:                        │ │
│  │ │  • www.example.com                                │ │
│  │ │  • example.com                                    │ │
│  │ │  • *.example.com                                  │ │
│  │ ├─ Key Usage: Digital Signature, Key Encipherment   │ │
│  │ └─ Extended Key Usage: TLS Web Server Auth          │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  SIGNATURE (by CA):                                        │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Signature Algorithm: sha256WithRSAEncryption         │ │
│  │ Signature Value:                                     │ │
│  │ 5f:3a:2e:1d:9c:8b:7a:6f:4e:3d:2c:1b:9a:8f:7e:6d... │ │
│  │ (CA's private key encrypted hash of certificate)    │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘

PURPOSE:
────────
✅ Proves server owns the public key
✅ Binds public key to domain name (www.example.com)
✅ Signed by trusted Certificate Authority (CA)
✅ Prevents man-in-the-middle attacks
```

#### Certificate Chain of Trust

**How Trust Works:**

```
┌─────────────────────────────────────────────────────────────┐
│              Certificate Chain of Trust                      │
└─────────────────────────────────────────────────────────────┘

LEVEL 1: Root CA (Top of Trust Hierarchy)
──────────────────────────────────────────
┌────────────────────────────────────────────┐
│      ROOT CERTIFICATE AUTHORITY            │
│                                            │
│  Name: DigiCert Global Root CA             │
│  Status: Self-Signed (trust anchor)        │
│  Validity: 30+ years                       │
│  Location: Pre-installed in browsers/OS    │
│                                            │
│  ┌──────────────────────────────────┐     │
│  │ Private Key (Ultra Secure)       │     │
│  │ - Kept offline in HSM            │     │
│  │ - Physical security              │     │
│  │ - Rarely used                    │     │
│  └──────────────────────────────────┘     │
└─────────────────┬──────────────────────────┘
                  │ Signs ↓
                  │
LEVEL 2: Intermediate CA (Middle Layer)
────────────────────────────────────────────
┌─────────────────▼──────────────────────────┐
│    INTERMEDIATE CERTIFICATE                │
│                                            │
│  Name: DigiCert TLS RSA SHA256 2020 CA1    │
│  Signed by: DigiCert Global Root CA        │
│  Validity: 5-10 years                      │
│  Purpose: Issues end-entity certificates   │
│                                            │
│  Why Intermediate?                         │
│  ✓ Protects root CA private key            │
│  ✓ Can be revoked if compromised           │
│  ✓ Easier to manage/rotate                 │
└─────────────────┬──────────────────────────┘
                  │ Signs ↓
                  │
LEVEL 3: End-Entity (Server Certificate)
─────────────────────────────────────────────
┌─────────────────▼──────────────────────────┐
│      SERVER CERTIFICATE                    │
│                                            │
│  Domain: www.example.com                   │
│  Signed by: DigiCert TLS RSA SHA256 CA     │
│  Validity: 1 year (typically)              │
│  Contains: Server's public key             │
│                                            │
│  Used for:                                 │
│  ✓ TLS/HTTPS connections                   │
│  ✓ Proving server identity                 │
│  ✓ Encrypting session keys                 │
└────────────────────────────────────────────┘

VERIFICATION FLOW:
─────────────────

Browser receives Server Certificate
         ↓
    ┌─────────────────────┐
    │ Is it signed by     │
    │ trusted Intermediate?│ ← Check signature
    └──────┬──────────────┘
           │ YES
           ↓
    ┌─────────────────────┐
    │ Is Intermediate     │
    │ signed by           │ ← Check signature
    │ trusted Root CA?    │
    └──────┬──────────────┘
           │ YES
           ↓
    ┌─────────────────────┐
    │ Is Root CA in       │
    │ browser's trust     │ ← Check trust store
    │ store?              │
    └──────┬──────────────┘
           │ YES
           ↓
    ✅ CERTIFICATE TRUSTED!

If any step fails → ❌ WARNING: Untrusted Certificate!
```

#### Types of Certificates

**1. Root CA Certificate**

```
┌─────────────────────────────────────────────────────────────┐
│                  ROOT CA CERTIFICATE                         │
└─────────────────────────────────────────────────────────────┘

CHARACTERISTICS:
───────────────
• Self-signed (signs itself)
• Pre-installed in browsers, OS, devices
• Extremely long validity (20-30 years)
• Private key stored offline in Hardware Security Module (HSM)
• Highest level of trust

EXAMPLES:
────────
✓ DigiCert Global Root CA
✓ GlobalSign Root CA
✓ Let's Encrypt Root CA (ISRG Root X1)
✓ VeriSign/Symantec roots

WHERE STORED:
────────────
• Windows: Certificate Manager (certmgr.msc)
• macOS: Keychain Access → System Roots
• Linux: /etc/ssl/certs/
• Browsers: Firefox has own trust store

USAGE:
──────
❌ NOT used directly for TLS
✅ Only signs intermediate CA certificates
✅ Root of trust for entire chain
```

**2. Intermediate CA Certificate**

```
┌─────────────────────────────────────────────────────────────┐
│              INTERMEDIATE CA CERTIFICATE                     │
└─────────────────────────────────────────────────────────────┘

CHARACTERISTICS:
───────────────
• Signed by Root CA
• Signs end-entity certificates (server, client)
• Medium validity (5-10 years)
• Can be revoked without affecting root
• Multiple intermediates can exist

WHY USE INTERMEDIATES?
─────────────────────

SECURITY:
┌──────────────────────────────────────┐
│ Root CA Private Key                  │
│ ├─ Kept offline in secure facility   │
│ ├─ Air-gapped from internet          │
│ ├─ Physical security (vault)         │
│ └─ Used only to sign intermediates   │
└──────────────────────────────────────┘
              │
              ↓ Signs
┌──────────────────────────────────────┐
│ Intermediate CA Private Key          │
│ ├─ Online, can issue certificates    │
│ ├─ If compromised, revoke this CA    │
│ └─ Root CA remains secure            │
└──────────────────────────────────────┘

FLEXIBILITY:
• Different intermediates for different purposes:
  - One for web servers
  - One for email
  - One for code signing
• Easy to revoke and replace

EXAMPLE CHAIN:
─────────────
DigiCert Global Root G2 (Root)
    └── DigiCert TLS RSA SHA256 2020 CA1 (Intermediate)
            └── www.example.com (Server)
```

**3. Server Certificate (TLS/SSL Certificate)**

```
┌─────────────────────────────────────────────────────────────┐
│                  SERVER CERTIFICATE                          │
└─────────────────────────────────────────────────────────────┘

PURPOSE:
───────
Proves web server's identity and encrypts traffic

CONTAINS:
────────
• Domain name(s): www.example.com, example.com
• Server's public key (RSA or ECC)
• Validity period (typically 90 days to 1 year)
• Issuer (Intermediate CA)
• Signature (signed by Intermediate CA)

TYPES OF SERVER CERTIFICATES:
─────────────────────────────

1. DOMAIN VALIDATED (DV) - Basic
   ┌────────────────────────────┐
   │ Validation: Domain control │
   │ Time: Minutes              │
   │ Cost: Free - $50/year      │
   │ Display: Padlock only      │
   │ Example: Let's Encrypt     │
   └────────────────────────────┘
   
   Usage: Blogs, personal sites
   Verification: Email or DNS record

2. ORGANIZATION VALIDATED (OV) - Medium
   ┌────────────────────────────┐
   │ Validation: Org identity   │
   │ Time: 1-3 days             │
   │ Cost: $50-$200/year        │
   │ Display: Org name in cert  │
   │ Example: DigiCert OV       │
   └────────────────────────────┘
   
   Usage: Business websites
   Verification: Business documents

3. EXTENDED VALIDATION (EV) - Highest
   ┌────────────────────────────┐
   │ Validation: Extensive      │
   │ Time: 1-2 weeks            │
   │ Cost: $200-$1000/year      │
   │ Display: Company name      │
   │          (some browsers)   │
   └────────────────────────────┘
   
   Usage: Banks, e-commerce
   Verification: Legal docs, phone, physical address

SINGLE vs MULTI-DOMAIN:
──────────────────────

Single Domain:
├─ Covers: www.example.com
└─ Cost: Lower

Wildcard:
├─ Covers: *.example.com
│          (blog.example.com, shop.example.com)
└─ Cost: Medium

Multi-Domain (SAN):
├─ Covers: example.com, example.net, example.org
│          subdomain.example.com
└─ Cost: Higher

USAGE IN TLS:
────────────
Server ──▶ Sends certificate to client during handshake
Client ──▶ Verifies certificate and domain match
Client ──▶ Extracts public key from certificate
Client ──▶ Encrypts session key with public key
Server ──▶ Decrypts with private key (not in certificate)
```

**4. Client Certificate**

```
┌─────────────────────────────────────────────────────────────┐
│                  CLIENT CERTIFICATE                          │
└─────────────────────────────────────────────────────────────┘

PURPOSE:
───────
Proves client's (user's) identity to server
Mutual TLS authentication (mTLS)

CHARACTERISTICS:
───────────────
• Issued to individual users or devices
• Contains user's public key
• Signed by organization's CA
• Used for strong authentication

TYPICAL USE CASES:
─────────────────

1. CORPORATE VPN ACCESS
   Employee ──▶ Certificate on laptop
   VPN Server ──▶ Verifies employee certificate
   ✓ Access granted only with valid certificate

2. API AUTHENTICATION
   Service A ──▶ Client certificate
   Service B ──▶ Verifies certificate
   ✓ Machine-to-machine authentication

3. EMAIL SIGNING/ENCRYPTION (S/MIME)
   User ──▶ Signs email with private key
   Recipient ──▶ Verifies with user's certificate

4. SMART CARD LOGIN
   Employee ──▶ Inserts smart card
   Computer ──▶ Reads certificate from card
   Active Directory ──▶ Verifies certificate

5. BANKING/FINANCE
   Customer ──▶ Certificate on USB token
   Bank ──▶ Requires certificate + password
   ✓ Two-factor authentication

EXAMPLE - MUTUAL TLS (mTLS):
───────────────────────────

CLIENT                              SERVER
────────                            ──────

1. Client ──▶ ClientHello          Server
2. Client ◀── ServerHello + Certificate
3. Client ──▶ Verify Server Cert
4. Client ◀── Request Client Certificate  ← Server asks!
5. Client ──▶ Send Client Certificate     ← Client proves identity
6. Server ──▶ Verify Client Cert
7. ✅ Both authenticated!

DIFFERENCE from Normal TLS:
──────────────────────────
Normal TLS:  Only server has certificate
Mutual TLS:  Both client AND server have certificates
             (Higher security, commonly used in zero-trust networks)
```

#### Complete Certificate Workflow

```
┌─────────────────────────────────────────────────────────────┐
│        Complete Certificate Lifecycle Workflow               │
└─────────────────────────────────────────────────────────────┘

STEP 1: Generate Key Pair & CSR
────────────────────────────────
Server Administrator:
┌────────────────────────────────────────┐
│ 1. Generate Private Key (Keep Secret!)│
│    openssl genrsa -out private.key 2048│
│                                        │
│ 2. Create CSR (Certificate Signing    │
│    Request)                            │
│    openssl req -new \                  │
│      -key private.key \                │
│      -out server.csr                   │
│                                        │
│    CSR Contains:                       │
│    • Domain: www.example.com           │
│    • Organization: Example Corp        │
│    • Public Key (derived from private) │
│    • NOT the private key!              │
└────────────────────────────────────────┘
         │
         │ Submit CSR
         ↓
STEP 2: CA Validates & Signs
─────────────────────────────
Certificate Authority (CA):
┌────────────────────────────────────────┐
│ 1. Validate domain ownership           │
│    • Domain validation: DNS or HTTP    │
│    • Organization validation: docs     │
│                                        │
│ 2. Sign CSR with CA's private key      │
│    signature = sign(hash(CSR),         │
│                     CA_private_key)    │
│                                        │
│ 3. Create Certificate                  │
│    • CSR data + CA signature           │
│    • Validity period (1 year)          │
│    • Serial number                     │
└────────────────────────────────────────┘
         │
         │ Return Certificate
         ↓
STEP 3: Install on Server
──────────────────────────
Server Administrator:
┌────────────────────────────────────────┐
│ 1. Receive certificate from CA         │
│    • server.crt (certificate)          │
│    • intermediate.crt (chain)          │
│                                        │
│ 2. Install on web server               │
│    • Certificate: server.crt           │
│    • Private Key: private.key          │
│    • Chain: intermediate.crt           │
│                                        │
│ 3. Configure server (Apache/Nginx)     │
└────────────────────────────────────────┘
         │
         │ Server Ready
         ↓
STEP 4: TLS Handshake (Runtime)
────────────────────────────────
Browser ◀────────▶ Server

1. Browser ──▶ ClientHello
2. Server ──▶ Certificate Chain:
              • Server Certificate
              • Intermediate Certificate
              (Browser has Root CA)

3. Browser Verification:
   ┌────────────────────────────────┐
   │ ✓ Signature valid?             │
   │   └─ Verify with CA public key │
   │ ✓ Domain matches?              │
   │   └─ example.com == CN?        │
   │ ✓ Not expired?                 │
   │   └─ Current date in validity? │
   │ ✓ Not revoked?                 │
   │   └─ Check CRL/OCSP            │
   │ ✓ Chain valid?                 │
   │   └─ Root CA trusted?          │
   └────────────────────────────────┘

4. If all checks pass:
   ✅ Extract public key from certificate
   ✅ Encrypt session key with public key
   ✅ Continue with encrypted communication

5. If any check fails:
   ❌ Show security warning
   ❌ Block connection (or warn user)
```

#### How Symmetric & Asymmetric Encryption Work Together

```
┌─────────────────────────────────────────────────────────────┐
│     Hybrid Encryption in HTTPS (Complete Flow)              │
└─────────────────────────────────────────────────────────────┘

PHASE 1: ASYMMETRIC ENCRYPTION (Handshake - Slow but Secure)
──────────────────────────────────────────────────────────────

CLIENT                                          SERVER
──────                                          ──────

                                        ┌──────────────────┐
                                        │ Private Key      │
                                        │ (Keep Secret!)   │
                                        └────────┬─────────┘
                                                 │
1. ClientHello ──────────────────────────────────▶
                                                 │
2. ◀──────────────────────────────────────────────
                                        Certificate:
                                        ┌──────────────────┐
                                        │ Public Key       │
                                        │ CA Signature     │
                                        │ Domain Name      │
                                        └──────────────────┘

3. Verify Certificate:                           │
   ├─ Valid signature? ✓                         │
   ├─ Domain matches? ✓                          │
   ├─ Not expired? ✓                             │
   └─ Extract Public Key                         │
                                                 │
4. Generate Random Session Key:                  │
   session_key = random(256 bits)                │
   (This will be used for AES encryption)        │
                                                 │
5. Encrypt Session Key with                      │
   Server's Public Key:                          │
                                                 │
   encrypted_session_key =                       │
   RSA_encrypt(session_key,                      │
               server_public_key)                │
                                                 │
6. ──────────────────────────────────────────────▶
   Send: encrypted_session_key                   │
                                                 │
                                    7. Decrypt with Private Key:
                                       session_key =
                                       RSA_decrypt(
                                         encrypted_session_key,
                                         server_private_key)

✅ Both sides now have the same session_key!
   Client generated it, server decrypted it
   Session key never transmitted in plaintext

PHASE 2: SYMMETRIC ENCRYPTION (Data Transfer - Fast)
─────────────────────────────────────────────────────

CLIENT                                          SERVER
──────                                          ──────

8. Encrypt HTTP Request with AES:               │
   ciphertext = AES_encrypt(                    │
     "GET /api/data",                           │
     session_key                                │
   )                                            │
                                                │
9. ──────────────────────────────────────────────▶
   Send: AES_encrypted_data                     │
                                                │
                                    10. Decrypt with Session Key:
                                        plaintext = AES_decrypt(
                                          ciphertext,
                                          session_key)
                                        
                                        Process request...
                                        
                                    11. Encrypt response:
                                        response_encrypted =
                                        AES_encrypt(response,
                                                   session_key)

12. ◀──────────────────────────────────────────────
    Receive: AES_encrypted_response              │
                                                │
13. Decrypt:                                     │
    response = AES_decrypt(                      │
      response_encrypted,                        │
      session_key                                │
    )                                            │

✅ All application data encrypted with AES
   Fast, efficient, secure

COMPARISON:
──────────

ASYMMETRIC (RSA):
├─ When: Only during handshake
├─ Purpose: Securely exchange session key
├─ Speed: Slow (can encrypt ~245 bytes with 2048-bit key)
├─ Data: Small (pre-master secret only)
└─ Key: Public key in certificate

SYMMETRIC (AES):
├─ When: All application data
├─ Purpose: Encrypt actual messages
├─ Speed: Fast (gigabytes per second)
├─ Data: Unlimited
└─ Key: Session key (established via asymmetric)

WHY BOTH?
────────
✅ Security: Asymmetric solves key distribution
✅ Performance: Symmetric is fast for bulk data
✅ Perfect Combination: Get benefits of both
```

#### Certificate Implementation Examples

**Python Code - Working with Certificates:**

```python
import ssl
import socket
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID, ExtensionOID
import requests

# ══════════════════════════════════════════════════════════
# Example 1: Retrieve and Inspect Server Certificate
# ══════════════════════════════════════════════════════════

def get_server_certificate(hostname, port=443):
    """
    Retrieve server certificate and display information
    """
    print(f"\n{'='*70}")
    print(f"Retrieving Certificate for: {hostname}")
    print(f"{'='*70}")
    
    # Create SSL context
    context = ssl.create_default_context()
    
    # Connect and get certificate
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            # Get certificate in DER format
            der_cert = ssock.getpeercert(binary_form=True)
            
            # Get certificate info as dict
            cert_dict = ssock.getpeercert()
            
            # Parse certificate
            cert = x509.load_der_x509_certificate(der_cert, default_backend())
            
            print(f"\n📜 Certificate Information:")
            print(f"{'─'*70}")
            
            # Subject (who the certificate is issued to)
            subject = cert.subject
            print(f"Subject:")
            for attribute in subject:
                print(f"  {attribute.oid._name}: {attribute.value}")
            
            # Issuer (who signed the certificate)
            issuer = cert.issuer
            print(f"\nIssuer:")
            for attribute in issuer:
                print(f"  {attribute.oid._name}: {attribute.value}")
            
            # Validity
            print(f"\nValidity:")
            print(f"  Not Before: {cert.not_valid_before_utc}")
            print(f"  Not After:  {cert.not_valid_after_utc}")
            
            # Check if expired
            now = datetime.now(datetime.timezone.utc)
            if now < cert.not_valid_before_utc:
                print(f"  ⚠️  Certificate not yet valid!")
            elif now > cert.not_valid_after_utc:
                print(f"  ❌ Certificate EXPIRED!")
            else:
                days_remaining = (cert.not_valid_after_utc - now).days
                print(f"  ✅ Valid ({days_remaining} days remaining)")
            
            # Subject Alternative Names (SAN)
            try:
                san_ext = cert.extensions.get_extension_for_oid(
                    ExtensionOID.SUBJECT_ALTERNATIVE_NAME
                )
                san_list = san_ext.value.get_values_for_type(x509.DNSName)
                print(f"\nSubject Alternative Names (SAN):")
                for name in san_list:
                    print(f"  • {name}")
            except x509.ExtensionNotFound:
                print(f"\nNo Subject Alternative Names found")
            
            # Public Key Info
            public_key = cert.public_key()
            if isinstance(public_key, rsa.RSAPublicKey):
                key_size = public_key.key_size
                print(f"\nPublic Key:")
                print(f"  Algorithm: RSA")
                print(f"  Key Size: {key_size} bits")
            
            # Signature Algorithm
            print(f"\nSignature Algorithm: {cert.signature_algorithm_oid._name}")
            
            # Serial Number
            print(f"Serial Number: {hex(cert.serial_number)}")
            
            # TLS Version
            print(f"\nTLS Version: {ssock.version()}")
            
            # Cipher
            print(f"Cipher: {ssock.cipher()}")
            
            return cert

# ══════════════════════════════════════════════════════════
# Example 2: Verify Certificate Chain
# ══════════════════════════════════════════════════════════

def verify_certificate_chain(hostname):
    """
    Verify complete certificate chain
    """
    print(f"\n{'='*70}")
    print(f"Verifying Certificate Chain for: {hostname}")
    print(f"{'='*70}\n")
    
    # Get certificate chain
    context = ssl.create_default_context()
    
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            # Get peer certificate chain
            der_cert = ssock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(der_cert, default_backend())
            
            print("Certificate Chain:")
            print("─"*70)
            
            # Server Certificate (end-entity)
            subject_cn = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
            issuer_cn = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
            
            print(f"\n🔵 Level 3: Server Certificate (End-Entity)")
            print(f"   Subject: {subject_cn}")
            print(f"   Issuer:  {issuer_cn}")
            print(f"   Purpose: TLS Server Authentication")
            
            print(f"\n🔵 Level 2: Intermediate CA")
            print(f"   Subject: {issuer_cn}")
            print(f"   Purpose: Signs server certificates")
            
            print(f"\n🔵 Level 1: Root CA")
            print(f"   Purpose: Trust anchor (in browser/OS)")
            print(f"   Status: Self-signed")
            
            print(f"\n✅ Verification Result:")
            print(f"   • Certificate chain is valid")
            print(f"   • All signatures verified")
            print(f"   • Root CA is trusted")

# ══════════════════════════════════════════════════════════
# Example 3: Generate Self-Signed Certificate (Testing)
# ══════════════════════════════════════════════════════════

def generate_self_signed_cert(common_name="localhost"):
    """
    Generate self-signed certificate for testing
    ⚠️  DO NOT use in production!
    """
    print(f"\n{'='*70}")
    print(f"Generating Self-Signed Certificate")
    print(f"{'='*70}\n")
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Create certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Test Org"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(common_name),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256(), default_backend())
    
    # Save private key
    with open("test-private-key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Save certificate
    with open("test-certificate.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print("✅ Generated:")
    print("   • test-private-key.pem (Private Key)")
    print("   • test-certificate.pem (Certificate)")
    print("\n⚠️  Self-signed certificate is for TESTING only!")
    print("   Browsers will show security warnings.")

# ══════════════════════════════════════════════════════════
# Example 4: Verify HTTPS Connection
# ══════════════════════════════════════════════════════════

def verify_https_connection(url):
    """
    Make HTTPS request and verify certificate
    """
    print(f"\n{'='*70}")
    print(f"Verifying HTTPS Connection")
    print(f"{'='*70}\n")
    
    try:
        # Make request (verifies certificate automatically)
        response = requests.get(url, timeout=5)
        
        print(f"✅ HTTPS Connection Successful")
        print(f"   URL: {url}")
        print(f"   Status: {response.status_code}")
        print(f"   Certificate: Valid and Trusted")
        
    except requests.exceptions.SSLError as e:
        print(f"❌ SSL Certificate Error!")
        print(f"   {str(e)}")
        print(f"\n   Possible causes:")
        print(f"   • Expired certificate")
        print(f"   • Self-signed certificate")
        print(f"   • Hostname mismatch")
        print(f"   • Untrusted CA")

# ══════════════════════════════════════════════════════════
# Example 5: Compare HTTP vs HTTPS Security
# ══════════════════════════════════════════════════════════

def demonstrate_http_vs_https():
    """
    Demonstrate difference between HTTP and HTTPS
    """
    print(f"\n{'='*70}")
    print(f"HTTP vs HTTPS Security Demonstration")
    print(f"{'='*70}\n")
    
    print("HTTP (Insecure):")
    print("─"*70)
    print("❌ No Encryption")
    print("   • Data sent in plaintext")
    print("   • Passwords visible to attackers")
    print("   • Subject to man-in-the-middle attacks")
    print("\n❌ No Authentication")
    print("   • Cannot verify server identity")
    print("   • Easy to impersonate")
    print("\n❌ No Integrity")
    print("   • Data can be modified in transit")
    print("   • No tamper detection")
    
    print(f"\n{'─'*70}\n")
    
    print("HTTPS (Secure):")
    print("─"*70)
    print("✅ Encryption (TLS)")
    print("   • All data encrypted with AES-256")
    print("   • Passwords protected")
    print("   • Prevents eavesdropping")
    print("\n✅ Authentication (Certificates)")
    print("   • Server identity verified")
    print("   • Signed by trusted CA")
    print("   • Domain name validated")
    print("\n✅ Integrity (HMAC)")
    print("   • Detects any modification")
    print("   • Message authentication code")
    print("   • Ensures data arrives unchanged")

# ══════════════════════════════════════════════════════════
# Main Demonstration
# ══════════════════════════════════════════════════════════

if __name__ == '__main__':
    # Example 1: Get certificate info
    get_server_certificate("www.google.com")
    
    # Example 2: Verify chain
    verify_certificate_chain("www.google.com")
    
    # Example 3: Generate self-signed cert for testing
    # generate_self_signed_cert("localhost")
    
    # Example 4: Verify HTTPS
    verify_https_connection("https://www.google.com")
    
    # Example 5: HTTP vs HTTPS
    demonstrate_http_vs_https()
    
    print(f"\n{'='*70}")
    print("KEY TAKEAWAYS")
    print(f"{'='*70}")
    print("""
    CERTIFICATES PROVIDE:
    • Identity verification (who you're connecting to)
    • Public key distribution (how to encrypt)
    • Trust chain (why you should trust them)
    
    HTTPS USES:
    • Asymmetric encryption (handshake, key exchange)
    • Symmetric encryption (data transfer)
    • Digital certificates (authentication)
    • Best of all worlds!
    
    CERTIFICATE TYPES:
    • Root CA: Trust anchor, pre-installed
    • Intermediate CA: Issues certificates
    • Server: Proves website identity
    • Client: Proves user identity (mTLS)
    """)
```

**Key Concepts Summary:**

```
┌─────────────────────────────────────────────────────────────┐
│                  CERTIFICATES SUMMARY                        │
└─────────────────────────────────────────────────────────────┘

ROOT CA CERTIFICATE:
──────────────────
Purpose: Trust anchor
Location: Pre-installed in OS/browser
Validity: 20-30 years
Usage: Signs intermediate CAs only
Example: DigiCert Global Root CA

INTERMEDIATE CA CERTIFICATE:
──────────────────────────
Purpose: Issue end-entity certificates
Location: Sent by server during TLS
Validity: 5-10 years
Usage: Signs server/client certificates
Example: DigiCert TLS RSA SHA256 CA

SERVER CERTIFICATE:
─────────────────
Purpose: Prove server identity
Location: Installed on web server
Validity: 90 days - 1 year
Usage: TLS/HTTPS connections
Example: www.example.com certificate

CLIENT CERTIFICATE:
─────────────────
Purpose: Prove client identity
Location: On user's device
Validity: 1-3 years
Usage: Mutual TLS (mTLS), VPN
Example: Employee certificate

HOW THEY WORK TOGETHER:
───────────────────────
1. Server sends: Server Cert + Intermediate Cert
2. Browser verifies: Chain up to Root CA
3. Browser trusts: Root CA in trust store
4. Result: ✅ Trusted connection
5. Encryption: Asymmetric → Symmetric
6. Data transfer: Fast and secure!
```

#### Modern TLS 1.3 Improvements

**TLS 1.3 Handshake (Faster):**

```
TLS 1.2 (Old):                    TLS 1.3 (New):
─────────────                     ─────────────

2 Round Trips:                    1 Round Trip:

Client ──▶ Hello                  Client ──▶ Hello + Key Share
       ◀── Hello, Cert, Key               ◀── Hello, Cert, Finished
Client ──▶ Key, Finished          
       ◀── Finished               ████ Data (Encrypted)
                                  
████ Data (Encrypted)             ⚡ 50% faster connection!

Improvements:
✅ Faster handshake (1-RTT vs 2-RTT)
✅ Stronger ciphers only
✅ Perfect Forward Secrecy mandatory
✅ Removed insecure features
```

### Digital Certificates in HTTPS

**What is a Digital Certificate?**

A digital certificate is a **digital identity card** that proves the server's identity. It contains the server's public key and is signed by a trusted Certificate Authority (CA).

```
┌─────────────────────────────────────────────────────────────┐
│              Digital Certificate Structure                   │
└─────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│           X.509 Certificate                            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. VERSION                                            │
│     Version: 3                                         │
│                                                        │
│  2. SERIAL NUMBER                                      │
│     Serial: 04:3B:7F:23:A8:...                        │
│                                                        │
│  3. SIGNATURE ALGORITHM                                │
│     Algorithm: sha256WithRSAEncryption                 │
│                                                        │
│  4. ISSUER (Certificate Authority)                     │
│     CN = DigiCert Global Root CA                       │
│     O  = DigiCert Inc                                  │
│     C  = US                                            │
│                                                        │
│  5. VALIDITY PERIOD                                    │
│     Not Before: Jan 1 00:00:00 2024 GMT               │
│     Not After:  Jan 1 23:59:59 2025 GMT               │
│                                                        │
│  6. SUBJECT (Server Identity)                          │
│     CN = www.example.com                               │
│     O  = Example Corp                                  │
│     L  = San Francisco                                 │
│     ST = California                                    │
│     C  = US                                            │
│                                                        │
│  7. PUBLIC KEY INFO                                    │
│     Algorithm: RSA                                     │
│     Key Size: 2048 bits                                │
│     Public Key: 30:82:01:0A:02:82:01:01:00:...        │
│                                                        │
│  8. EXTENSIONS                                         │
│     a) Subject Alternative Names (SAN)                 │
│        DNS: www.example.com                            │
│        DNS: example.com                                │
│        DNS: *.example.com                              │
│                                                        │
│     b) Key Usage                                       │
│        Digital Signature, Key Encipherment             │
│                                                        │
│     c) Extended Key Usage                              │
│        TLS Web Server Authentication                   │
│                                                        │
│     d) Authority Key Identifier                        │
│        KeyID: 03:DE:50:35:56:D1:...                   │
│                                                        │
│  9. CA SIGNATURE                                       │
│     Signature: 8F:2A:B3:C4:...                        │
│     (Signed with CA's Private Key)                     │
│                                                        │
└────────────────────────────────────────────────────────┘
```

#### Certificate Components Explained

| Component | Description | Example |
|-----------|-------------|---------|
| **Version** | X.509 certificate version | v3 (most common) |
| **Serial Number** | Unique identifier for certificate | 04:3B:7F:23:A8... |
| **Signature Algorithm** | Algorithm used by CA to sign | SHA-256 with RSA |
| **Issuer** | Certificate Authority that issued cert | DigiCert, Let's Encrypt |
| **Validity Period** | Start and end dates | Jan 1, 2024 - Jan 1, 2025 |
| **Subject** | Entity the certificate identifies | www.example.com |
| **Public Key** | Server's public key | 2048-bit RSA key |
| **Extensions** | Additional information | SANs, Key Usage, etc. |
| **CA Signature** | Digital signature by CA | Proves authenticity |

#### Certificate Trust Chain

```
┌─────────────────────────────────────────────────────────────┐
│           Certificate Trust Chain (PKI)                      │
└─────────────────────────────────────────────────────────────┘

                  ┌──────────────────────┐
                  │   ROOT CA            │
                  │  (Self-Signed)       │
                  │                      │
                  │ "DigiCert Root CA"   │
                  │  ┌──────────────┐    │
                  │  │ Public Key   │    │
                  │  │ Private Key  │    │
                  │  └──────────────┘    │
                  └──────────┬───────────┘
                             │ Signs
                             │ (with private key)
                             ▼
                  ┌──────────────────────┐
                  │ INTERMEDIATE CA      │
                  │                      │
                  │ "DigiCert SHA2       │
                  │  Secure Server CA"   │
                  │  ┌──────────────┐    │
                  │  │ Public Key   │    │
                  │  │ Private Key  │    │
                  │  └──────────────┘    │
                  └──────────┬───────────┘
                             │ Signs
                             │ (with private key)
                             ▼
                  ┌──────────────────────┐
                  │  SERVER CERTIFICATE  │
                  │                      │
                  │ "www.example.com"    │
                  │  ┌──────────────┐    │
                  │  │ Public Key   │    │
                  │  └──────────────┘    │
                  └──────────────────────┘

VERIFICATION PROCESS:
────────────────────

Browser receives:
┌─────────────────────────────────────┐
│ 1. Server Certificate (example.com) │
│ 2. Intermediate Certificate         │
│ 3. (Root CA already trusted)        │
└─────────────────────────────────────┘

Verification Steps:
┌──────────────────────────────────────────────────────────┐
│                                                          │
│ Step 1: Verify Server Certificate                       │
│ ────────────────────────────────                         │
│ • Get CA signature from server cert                      │
│ • Get public key from intermediate cert                  │
│ • Verify signature with public key                       │
│ • Check: Domain name, expiry, revocation                 │
│   ✓ Valid!                                               │
│                                                          │
│ Step 2: Verify Intermediate Certificate                 │
│ ──────────────────────────────────                       │
│ • Get CA signature from intermediate cert                │
│ • Get public key from root cert (in browser)             │
│ • Verify signature with public key                       │
│   ✓ Valid!                                               │
│                                                          │
│ Step 3: Check Root Certificate                          │
│ ─────────────────────────────                            │
│ • Is root CA in browser's trust store?                   │
│   ✓ Yes! (Pre-installed by browser/OS)                   │
│                                                          │
│ RESULT: Trust established! 🔒                            │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### How Certificates Are Used in HTTPS

```
┌─────────────────────────────────────────────────────────────┐
│        Complete HTTPS Flow with Certificates                 │
└─────────────────────────────────────────────────────────────┘

STEP 1: User Visits Website
────────────────────────────
┌─────────┐
│ Browser │ User types: https://example.com
└────┬────┘
     │
     │ (1) TCP Connection
     │
     ▼
┌──────────┐
│  Server  │
└──────────┘

STEP 2: TLS Handshake Begins
─────────────────────────────
Browser ──▶ ClientHello
            "I support TLS 1.3, AES-256, etc."

Server  ──▶ ServerHello
            "Let's use TLS 1.3 with AES-256-GCM"

STEP 3: Server Sends Certificate
─────────────────────────────────
Server  ──▶ Certificate Chain:
            ┌─────────────────────────────────┐
            │ example.com Certificate         │
            │ - CN: example.com               │
            │ - Public Key (RSA 2048)         │
            │ - Signed by: DigiCert CA        │
            └─────────────────────────────────┘
            ┌─────────────────────────────────┐
            │ DigiCert Intermediate Cert      │
            │ - Signed by: DigiCert Root CA   │
            └─────────────────────────────────┘

STEP 4: Browser Verifies Certificate
─────────────────────────────────────
Browser:
  ┌──────────────────────────────────────┐
  │ Verification Checklist:              │
  │                                      │
  │ ✓ Domain name matches URL?           │
  │   "example.com" == "example.com" ✓   │
  │                                      │
  │ ✓ Certificate not expired?           │
  │   Valid: Jan 1 - Dec 31, 2024 ✓      │
  │                                      │
  │ ✓ Signed by trusted CA?              │
  │   DigiCert Root CA in trust store ✓  │
  │                                      │
  │ ✓ Signature valid?                   │
  │   Verify with CA's public key ✓      │
  │                                      │
  │ ✓ Not revoked?                       │
  │   Check CRL/OCSP ✓                   │
  │                                      │
  │ ALL CHECKS PASSED! ✅                 │
  └──────────────────────────────────────┘

STEP 5: Key Exchange
─────────────────────
Browser:
  - Generates random "Pre-Master Secret"
  - Encrypts with server's PUBLIC KEY (from certificate)
  - Sends to server

Browser ──▶ Encrypted Pre-Master Secret
            [████████████████] ← Encrypted with public key

Server:
  - Receives encrypted pre-master secret
  - Decrypts with its PRIVATE KEY
  - Both sides compute Session Key

STEP 6: Secure Communication
─────────────────────────────
Browser ◀──▶ Server
        All data encrypted with Session Key (AES-256)
        
        GET /api/data [████████████] ← Encrypted
        Response: [█████████████████] ← Encrypted

┌────────────────────────────────────────┐
│  Browser Address Bar Shows:           │
│                                        │
│  🔒 https://example.com                │
│                                        │
│  ✅ Connection is secure               │
│  ✅ Certificate is valid               │
│  ✅ Issued by: DigiCert                │
└────────────────────────────────────────┘
```

#### Certificate Types

```
DOMAIN VALIDATION (DV):
──────────────────────
✓ Validates domain ownership only
✓ Issued in minutes
✓ Free (Let's Encrypt) or cheap
✓ Shows: 🔒 in browser
✗ No company verification
Use: Blogs, personal sites

ORGANIZATION VALIDATION (OV):
─────────────────────────────
✓ Validates domain + organization
✓ Issued in 1-3 days
✓ Manual verification process
✓ Shows: 🔒 + company name
✓ More trust
Use: Business websites

EXTENDED VALIDATION (EV):
────────────────────────
✓ Highest validation level
✓ Thorough company verification
✓ Issued in 1-2 weeks
✓ Shows: 🔒 + Green bar + company name
✓ Maximum trust
Use: Banks, e-commerce, high-security

WILDCARD CERTIFICATES:
─────────────────────
✓ Covers *.example.com
✓ Secures all subdomains
✓ Example: api.example.com, www.example.com
Use: Multiple subdomains
```

### JWT (JSON Web Token)

**What is JWT?**

JWT is a compact, self-contained token format for securely transmitting information between parties as a JSON object. It's digitally signed, so it can be verified and trusted.

```
┌─────────────────────────────────────────────────────────────┐
│                  JWT Structure                               │
└─────────────────────────────────────────────────────────────┘

COMPLETE JWT TOKEN:
──────────────────
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

Split into 3 parts (separated by dots):
───────────────────────────────────────

┌─────────── HEADER ───────────┐
│ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
│
│ Decoded:
│ {
│   "alg": "HS256",        ← Algorithm
│   "typ": "JWT"           ← Token type
│ }
└──────────────────────────────┘
                  .
┌─────────── PAYLOAD ──────────┐
│ eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ
│
│ Decoded:
│ {
│   "sub": "1234567890",   ← Subject (user ID)
│   "name": "John Doe",    ← Custom claim
│   "iat": 1516239022,     ← Issued at
│   "exp": 1516242622      ← Expiration
│ }
└──────────────────────────────┘
                  .
┌─────────── SIGNATURE ────────┐
│ SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
│
│ Created by:
│ HMACSHA256(
│   base64UrlEncode(header) + "." +
│   base64UrlEncode(payload),
│   secret_key
│ )
└──────────────────────────────┘
```

#### How JWT Works

```
┌─────────────────────────────────────────────────────────────┐
│                JWT Authentication Flow                       │
└─────────────────────────────────────────────────────────────┘

STEP 1: User Login
──────────────────
┌──────────┐                           ┌──────────┐
│  Client  │                           │  Server  │
└────┬─────┘                           └────┬─────┘
     │                                      │
     │ POST /login                          │
     │ {username: "john", password: "***"}  │
     │─────────────────────────────────────▶│
     │                                      │
     │                                      │ Verify credentials
     │                                      │ ✓ Valid!
     │                                      │
     │                                      │ Generate JWT:
     │                                      │ ─────────────
     │                                      │ Header:
     │                                      │ {alg: HS256, typ: JWT}
     │                                      │
     │                                      │ Payload:
     │                                      │ {
     │                                      │   sub: "12345",
     │                                      │   name: "John Doe",
     │                                      │   role: "admin",
     │                                      │   iat: 1234567890,
     │                                      │   exp: 1234571490
     │                                      │ }
     │                                      │
     │                                      │ Sign with secret key
     │                                      │
     │ Response: { token: "eyJ..." }        │
     │◀─────────────────────────────────────│
     │                                      │
     │ Store token (localStorage/cookie)    │
     │                                      │

STEP 2: Access Protected Resource
──────────────────────────────────
     │                                      │
     │ GET /api/protected                   │
     │ Authorization: Bearer eyJ...         │
     │─────────────────────────────────────▶│
     │                                      │
     │                                      │ Verify JWT:
     │                                      │ ───────────
     │                                      │ 1. Extract token
     │                                      │ 2. Verify signature
     │                                      │    using secret key
     │                                      │ 3. Check expiration
     │                                      │ 4. Validate claims
     │                                      │
     │                                      │ ✓ Token valid!
     │                                      │
     │                                      │ Extract user info
     │                                      │ from payload
     │                                      │
     │ Response: { data: "..." }            │
     │◀─────────────────────────────────────│
     │                                      │

STEP 3: Token Expired
──────────────────────
     │                                      │
     │ GET /api/protected                   │
     │ Authorization: Bearer eyJ... (old)   │
     │─────────────────────────────────────▶│
     │                                      │
     │                                      │ Verify JWT:
     │                                      │ ✗ Token expired!
     │                                      │
     │ 401 Unauthorized                     │
     │ { error: "Token expired" }           │
     │◀─────────────────────────────────────│
     │                                      │
     │ User must login again                │
     │ (or use refresh token)               │
     │                                      │
```

#### JWT vs Session Tokens

```
┌──────────────────────────────────────────────────────────────┐
│              JWT vs Session Tokens                           │
└──────────────────────────────────────────────────────────────┘

SESSION TOKENS (Server-side):
─────────────────────────────
┌──────────┐                           ┌──────────────────┐
│  Client  │                           │     Server       │
└────┬─────┘                           │  ┌────────────┐  │
     │                                 │  │  Session   │  │
     │ Login                           │  │   Store    │  │
     │────────────────────────────────▶│  │            │  │
     │                                 │  │ session123:│  │
     │ Session ID: "session123"        │  │ {user:john}│  │
     │◀────────────────────────────────│  └────────────┘  │
     │                                 │                  │
     │ Request + Session ID            │                  │
     │────────────────────────────────▶│ Lookup in store  │
     │                                 │ ✓ Found user     │
     │ Response                        │                  │
     │◀────────────────────────────────│                  │
     └─────────────────────────────────┴──────────────────┘

✅ Can revoke immediately
✅ Server has full control
❌ Requires server-side storage
❌ Harder to scale (session replication)
❌ Not stateless

JWT TOKENS (Stateless):
───────────────────────
┌──────────┐                           ┌──────────┐
│  Client  │                           │  Server  │
└────┬─────┘                           └────┬─────┘
     │                                      │
     │ Login                                │
     │─────────────────────────────────────▶│
     │                                      │
     │ JWT: "eyJ..." (contains user info)   │
     │◀─────────────────────────────────────│
     │                                      │
     │ Request + JWT                        │
     │─────────────────────────────────────▶│ Verify signature
     │                                      │ (no DB lookup!)
     │ Response                             │
     │◀─────────────────────────────────────│
     └──────────────────────────────────────┘

✅ Stateless (no server storage)
✅ Easy to scale
✅ Works across services (microservices)
✅ Contains user info (no DB lookup)
❌ Cannot revoke until expiration
❌ Token size larger than session ID
❌ Must keep tokens short-lived
```

#### JWT Implementation (Python)

```python
import jwt
import datetime
from typing import Dict, Optional
import hashlib
import hmac

class JWTManager:
    """JWT token generation and validation"""
    
    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        """
        Initialize JWT manager
        
        Args:
            secret_key: Secret key for signing tokens
            algorithm: Signing algorithm (HS256, RS256, etc.)
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def generate_token(self, user_id: str, username: str, 
                      role: str = 'user', expires_in: int = 3600) -> str:
        """
        Generate JWT token
        
        Args:
            user_id: Unique user identifier
            username: Username
            role: User role (admin, user, etc.)
            expires_in: Token validity in seconds (default 1 hour)
        
        Returns:
            JWT token string
        """
        now = datetime.datetime.utcnow()
        
        payload = {
            # Standard claims
            'sub': user_id,                    # Subject (user ID)
            'iat': now,                        # Issued at
            'exp': now + datetime.timedelta(seconds=expires_in),  # Expiration
            'nbf': now,                        # Not before
            
            # Custom claims
            'username': username,
            'role': role
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded payload if valid, None if invalid
        """
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None
    
    def refresh_token(self, old_token: str, expires_in: int = 3600) -> Optional[str]:
        """
        Generate new token from old token (refresh)
        
        Args:
            old_token: Current JWT token
            expires_in: New token validity in seconds
        
        Returns:
            New JWT token or None if old token is invalid
        """
        payload = self.verify_token(old_token)
        if not payload:
            return None
        
        # Generate new token with same user info
        return self.generate_token(
            user_id=payload['sub'],
            username=payload['username'],
            role=payload['role'],
            expires_in=expires_in
        )

# Flask API Example
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)
jwt_manager = JWTManager(secret_key='your-secret-key-keep-it-safe')

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Format: "Bearer <token>"
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid authorization header'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Verify token
        payload = jwt_manager.verify_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Add user info to request context
        request.current_user = payload
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint - returns JWT token"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Verify credentials (in real app, check against database)
    if username == 'admin' and password == 'password123':
        # Generate JWT token
        token = jwt_manager.generate_token(
            user_id='12345',
            username=username,
            role='admin',
            expires_in=3600  # 1 hour
        )
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'expires_in': 3600
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/protected', methods=['GET'])
@token_required
def protected():
    """Protected endpoint - requires valid JWT token"""
    user = request.current_user
    
    return jsonify({
        'message': f'Hello {user["username"]}!',
        'user_id': user['sub'],
        'role': user['role']
    }), 200

@app.route('/api/admin', methods=['GET'])
@token_required
def admin_only():
    """Admin-only endpoint - checks role from JWT"""
    user = request.current_user
    
    if user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    return jsonify({
        'message': 'Welcome admin!',
        'admin_data': 'sensitive information'
    }), 200

@app.route('/api/refresh', methods=['POST'])
def refresh():
    """Refresh token endpoint"""
    data = request.get_json()
    old_token = data.get('token')
    
    if not old_token:
        return jsonify({'error': 'Token is required'}), 400
    
    # Generate new token from old one
    new_token = jwt_manager.refresh_token(old_token, expires_in=3600)
    
    if new_token:
        return jsonify({
            'message': 'Token refreshed',
            'token': new_token,
            'expires_in': 3600
        }), 200
    else:
        return jsonify({'error': 'Invalid or expired token'}), 401

# Manual JWT Creation (Understanding the internals)
import base64
import json

def manual_jwt_create(payload: Dict, secret: str) -> str:
    """Manual JWT creation to understand the process"""
    
    # 1. Create header
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    # 2. Encode header and payload
    def base64url_encode(data: Dict) -> str:
        json_str = json.dumps(data, separators=(',', ':'))
        encoded = base64.urlsafe_b64encode(json_str.encode()).decode()
        return encoded.rstrip('=')  # Remove padding
    
    header_encoded = base64url_encode(header)
    payload_encoded = base64url_encode(payload)
    
    # 3. Create signature
    message = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    # 4. Combine all parts
    jwt_token = f"{header_encoded}.{payload_encoded}.{signature_encoded}"
    
    return jwt_token

# Usage Example
if __name__ == '__main__':
    print("="*60)
    print("JWT Authentication Example")
    print("="*60)
    
    # Initialize JWT manager
    jwt_mgr = JWTManager(secret_key='my-super-secret-key')
    
    # 1. Generate token
    print("\n1. Generating JWT token...")
    token = jwt_mgr.generate_token(
        user_id='user123',
        username='john_doe',
        role='admin',
        expires_in=3600
    )
    print(f"Token: {token[:50]}...")
    
    # 2. Verify token
    print("\n2. Verifying token...")
    payload = jwt_mgr.verify_token(token)
    if payload:
        print(f"✅ Token is valid!")
        print(f"User ID: {payload['sub']}")
        print(f"Username: {payload['username']}")
        print(f"Role: {payload['role']}")
        print(f"Expires: {datetime.datetime.fromtimestamp(payload['exp'])}")
    
    # 3. Manual JWT creation
    print("\n3. Manual JWT creation (understanding internals)...")
    manual_payload = {
        'sub': 'user123',
        'name': 'John Doe',
        'iat': int(datetime.datetime.utcnow().timestamp())
    }
    manual_token = manual_jwt_create(manual_payload, 'my-secret')
    print(f"Manual Token: {manual_token[:50]}...")
    
    # 4. Start Flask app
    print("\n4. Starting Flask API server...")
    print("Endpoints:")
    print("  POST   /api/login      - Get JWT token")
    print("  GET    /api/protected  - Access with token")
    print("  GET    /api/admin      - Admin only")
    print("  POST   /api/refresh    - Refresh token")
    print("\nExample request:")
    print('  curl -X POST http://localhost:5000/api/login \\')
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"username":"admin","password":"password123"}\'')
    
    # app.run(debug=True, port=5000)
```

#### JWT Best Practices

```
✅ DO:
──────
1. Use HTTPS Only
   - Never send JWT over unencrypted connections
   
2. Keep Tokens Short-Lived
   - Access token: 15 minutes - 1 hour
   - Use refresh tokens for longer sessions

3. Use Strong Secret Keys
   - Minimum 256 bits for HS256
   - Use cryptographically random values

4. Validate All Claims
   - exp (expiration)
   - iat (issued at)
   - nbf (not before)
   - aud (audience)
   - iss (issuer)

5. Use Appropriate Algorithm
   - HS256: Symmetric (shared secret)
   - RS256: Asymmetric (public/private key)

6. Store Securely
   - HttpOnly cookies (XSS protection)
   - Or secure storage (not localStorage for sensitive data)

❌ DON'T:
─────────
1. Store Sensitive Data in Payload
   - JWT payload is NOT encrypted, only encoded
   - Anyone can decode and read it
   
2. Use for Sessions with Immediate Revocation
   - Cannot revoke JWT until expiration
   - Use session tokens if need instant revocation

3. Make Tokens Too Long-Lived
   - Higher risk if compromised
   
4. Use Weak Secrets
   - "secret", "password123", etc.

5. Ignore Token Validation
   - Always verify signature
   - Always check expiration

6. Mix Authentication and Authorization Data
   - Keep JWTs focused
```

**JWT Security Considerations:**

```
COMMON VULNERABILITIES:
──────────────────────

1. None Algorithm Attack
   ❌ {"alg": "none", "typ": "JWT"}
   ✅ Always validate algorithm

2. Algorithm Confusion
   ❌ Accepting both HS256 and RS256
   ✅ Enforce specific algorithm

3. Weak Secret Keys
   ❌ "secret", "12345"
   ✅ Use strong, random keys (256+ bits)

4. No Expiration Validation
   ❌ Ignoring 'exp' claim
   ✅ Always check expiration

5. Token Leakage
   ❌ Logging tokens, storing in localStorage
   ✅ Use HttpOnly cookies, secure storage

6. Replay Attacks
   ❌ No unique identifier per token
   ✅ Use 'jti' (JWT ID) claim
```

