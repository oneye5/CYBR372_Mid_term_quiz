import random
import re
import os
import sys
import time

# Database of questions and answers extracted from the documents
questions_db = [
       {
        "question": "What are the key goals of cryptography",
        "options": {
            "A": "All of these",
            "B": "Confidentiality",
            "C": "Data integrity",
            "D": "Non repudiation"
        },
        "correct": "A"
    },
    {
        "question": "Which property ensures that a digital signature cannot be created by anyone other than the signer?",
        "options": {
            "A": "Confidentiality",
            "B": "Data origin authentication",
            "C": "Non-repudiation",
            "D": "Integrity"
        },
        "correct": "B"
    },
    {
        "question": "What is the main purpose of non-repudiation in digital signatures?",
        "options": {
            "A": "To keep data secret",
            "B": "To ensure the sender cannot deny sending a message",
            "C": "To verify the length of a message",
            "D": "To prevent replay attacks"
        },
        "correct": "B"
    },
    {
        "question": "Which of the following is NOT a basic property of a secure digital signature scheme?",
        "options": {
            "A": "Easy for the signer to generate a signature",
            "B": "Easy for anyone to verify a signature",
            "C": "Easy for anyone to forge a signature",
            "D": "Hard for anyone to forge a signature"
        },
        "correct": "C"
    },
    {
        "question": "Which padding algorithm is recommended for RSA digital signatures to ensure security?",
        "options": {
            "A": "PKCS#7",
            "B": "RSA-PSS",
            "C": "OAEP",
            "D": "SHA-PAD"
        },
        "correct": "B"
    },
    {
        "question": "Entity authentication is best described as:",
        "options": {
            "A": "Verifying that the data has not been altered",
            "B": "Assuring that a specific entity is active in a communication session",
            "C": "Encrypting all transmitted messages",
            "D": "Checking that a message is confidential"
        },
        "correct": "B"
    },
    {
        "question": "Which freshness mechanism requires synchronised clocks between parties?",
        "options": {
            "A": "Nonce-based mechanism",
            "B": "Sequence numbers",
            "C": "Clock-based mechanism",
            "D": "Token-based mechanism"
        },
        "correct": "C"
    },
    {
        "question": "What is a nonce?",
        "options": {
            "A": "A private key used for encryption",
            "B": "A random number used only once",
            "C": "A timestamp",
            "D": "A session identifier"
        },
        "correct": "B"
    },
    {
        "question": "Which problem is most commonly associated with static passwords?",
        "options": {
            "A": "They are too complex to remember",
            "B": "They can be reused by an attacker in a replay attack",
            "C": "They require hardware tokens",
            "D": "They cannot be stored securely"
        },
        "correct": "B"
    },
    {
        "question": "Which of the following is a primary security service provided by a digital signature?",
        "options": {
            "A": "Message confidentiality",
            "B": "Data origin authentication",
            "C": "Key exchange",
            "D": "Access control"
        },
        "correct": "B"
    },
    {
        "question": "Which statement is true about RSA and digital signatures?",
        "options": {
            "A": "RSA can be used for digital signatures by swapping the public and private keys",
            "B": "Any public-key encryption scheme can be converted into a signature scheme by swapping keys",
            "C": "RSA cannot be used for digital signatures",
            "D": "RSA signatures do not require padding"
        },
        "correct": "A"
    },
    {
        "question": "Why is padding used in RSA digital signatures?",
        "options": {
            "A": "To hide the length of the message",
            "B": "To expand the message hash to match the modulus size",
            "C": "To encrypt the message",
            "D": "To make the signature more random"
        },
        "correct": "B"
    },
    {
        "question": "Which of the following is an example of a clock-based freshness mechanism?",
        "options": {
            "A": "Random number generation",
            "B": "Timestamps",
            "C": "Digital signatures",
            "D": "Hash functions"
        },
        "correct": "B"
    },
    {
        "question": "What is the main requirement for using sequence numbers as a freshness mechanism?",
        "options": {
            "A": "A secure hash function",
            "B": "A database to store the latest sequence numbers",
            "C": "Synchronized clocks",
            "D": "A public key infrastructure"
        },
        "correct": "B"
    },
    {
        "question": "Which type of attack replays an old valid message to gain unauthorized advantage?",
        "options": {
            "A": "Man-in-the-middle attack",
            "B": "Reflection attack",
            "C": "Replay attack",
            "D": "Brute force attack"
        },
        "correct": "C"
    },
    {
        "question": "What is the purpose of dynamic password schemes?",
        "options": {
            "A": "To make passwords longer",
            "B": "To change the password with each authentication attempt",
            "C": "To require mutual authentication",
            "D": "To allow password reuse"
        },
        "correct": "B"
    },
    {
        "question": "Which of the following is a major drawback of conventional passwords?",
        "options": {
            "A": "They require a secure MAC algorithm",
            "B": "They expose the password to the verifier each time they are used",
            "C": "They cannot be stored",
            "D": "They cannot be used in digital signatures"
        },
        "correct": "B"
    },
    {
        "question": "In a zero-knowledge authentication mechanism, who is the 'prover'?",
        "options": {
            "A": "The entity verifying the identity",
            "B": "The entity proving their identity without revealing secret information",
            "C": "The entity storing authentication data",
            "D": "The entity issuing digital certificates"
        },
        "correct": "B"
    },
    {
        "question": "Which standard specifies a suite of cryptographic protocols for mutual authentication and key establishment?",
        "options": {
            "A": "PKCS#1",
            "B": "ISO/IEC 11770",
            "C": "SSL/TLS",
            "D": "FIPS 140-3"
        },
        "correct": "B"
    },
    {
        "question": "What is a reflection attack in cryptographic protocols?",
        "options": {
            "A": "An attack where a message is mirrored back to the sender to trick them",
            "B": "An attack where the attacker replays an old message",
            "C": "An attack that decrypts messages by guessing keys",
            "D": "An attack on password hashes"
        },
        "correct": "A"
    },
    {
        "question": "Why is encryption alone not always sufficient for data origin authentication?",
        "options": {
            "A": "Encryption can be broken",
            "B": "Encryption does not guarantee the identity of the sender",
            "C": "Encryption requires a MAC",
            "D": "Encryption is too slow"
        },
        "correct": "B"
    },
    {
        "question": "What is the main advantage of including recipient identifiers in protocol messages?",
        "options": {
            "A": "It increases message size",
            "B": "It prevents reflection attacks",
            "C": "It hides message contents",
            "D": "It allows faster encryption"
        },
        "correct": "B"
    },
    {
        "question": "Which of the following is an example of a symmetric encryption algorithm?",
        "options": {
            "A": "RSA",
            "B": "AES",
            "C": "ECDSA",
            "D": "DSA"
        },
        "correct": "B"
    },
    {
        "question": "In entity authentication, what does 'freshness' ensure?",
        "options": {
            "A": "That the message is confidential",
            "B": "That the message was recently generated and is not a replay",
            "C": "That the message has been digitally signed",
            "D": "That the message is encrypted"
        },
        "correct": "B"
    }

    {
        "question": "What is the defining feature of a zero-knowledge authentication mechanism?",
        "options": {
            "A": "The verifier learns nothing that can be used to impersonate the prover",
            "B": "The prover sends their password in encrypted form",
            "C": "Both parties use the same password",
            "D": "It relies on mutual trust between entities"
        },
        "correct": "A"
    },
    {
        "question": "Which of the following is NOT typically part of a cryptographic protocol specification?",
        "options": {
            "A": "Protocol assumptions",
            "B": "Protocol flow",
            "C": "Programming language used",
            "D": "Protocol messages"
        },
        "correct": "C"
    }

       {
        "question": "What does D.O.A stand for in the context of cryptography",
        "options": {
            "A": "Data origin authentication",
            "B": "Dead on arrival",
            "C": "Do origin authentication",
            "D": "Diabolical original Arman"
        },
        "correct": "A"
    },
       {
        "question": "What best describes N.R.",
        "options": {
            "A": "A sender cannot deny having sent a message or performed a transaction",
            "B": "A youtuber who makes videos about chemistry",
            "C": "A famous river",
            "D": "Messages cannot be read by anyone who is not the recipient"
        },
        "correct": "A"
    },
       {
        "question": "What best describes E.A.",
        "options": {
            "A": "Process of verifying the identity of a device, person or entity",
            "B": "Ensuring messages sent from a device actually came from that device",
            "C": "A game studio",
            "D": "The verification that encrypted plaintext is propperly encrypted"
        },
        "correct": "A"
    },
       {
        "question": "What best describes a cryptographic primitive",
        "options": {
            "A": "All of these",
            "B": "Block cipher",
            "C": "MAC",
            "D": "Digital signatures"
        },
        "correct": "A"
    },
       {
        "question": "What best describes keyspace",
        "options": {
            "A": "The collection of all possible decryption keys",
            "B": "The secure portion of memory where keys are kept",
            "C": "G",
            "D": "D"
        },
        "correct": "A"
    },
       {
        "question": "Which one of these is wrong",
        "options": {
            "A": "M refers to the ciphertext message",
            "B": "K refers to encryption and decryption key spaces",
            "C": "E, refers to an encryption algorithm",
            "D": "D refers to a decryption algorithm"
        },
        "correct": "A"
    },
       {
        "question": "What is the key difference between symetric and asymetric cryptography",
        "options": {
            "A": "Asymetric cryptorgaphy involves public and private keys",
            "B": "Symetric cryptograpgy involves public and private keys with the goal of avoiding a known secret between parties",
            "C": "Symetric cryptography tends to be much slower than asymetric cryptography due to the underlying algorithms",
            "D": "Arman."
        },
        "correct": "A"
    },
       {
        "question": "Is keeping the specific algorithm used secret, a common and effective additional layer of security",
        "options": {
            "A": "No",
            "B": "Yes",
            "C": "Maybe so",
            "D": ""
        },
        "correct": "A"
    },
       {
        "question": "What best aligns with Kerckoff's principle",
        "options": {
            "A": "All secrets should concentrated in the decryption key",
            "B": "Assignments should be released on time, and of acceptable quality",
            "C": "Cryptography should be used where information is not public to everyone",
            "D": "The encryption algorithm should be hidden"
        },
        "correct": "A"
    },
       {
        "question": "Which would be considered 'more secure'",
        "options": {
            "A": "A publicly known algorithm",
            "B": "A proprietary algorithm, known by minimal parties",
            "C": "Unknown asymetric encrpytion",
            "D": ""
        },
        "correct": "A"
    },
       {
        "question": "What best describes KPA",
        "options": {
            "A": "An attacker knows some plaintext and ciphertext pairs",
            "B": "An attacker knows the private key of the target",
            "C": "An attacker knows only the encryption algorithm and some ciphertext",
            "D": "An attacker knows that Arman is the source of all evil"
        },
        "correct": "A"
    },
       {
        "question": "What are substitution ciphers most vulnerable to",
        "options": {
            "A": "Frequency analysis",
            "B": "Dictionary attack",
            "C": "",
            "D": ""
        },
        "correct": "A"
    },
       {
        "question": "What are some key takeaways from historical ciphers",
        "options": {
            "A": "All of these",
            "B": "Changing a single bit of plaintext should uniformly affect the entire ciphertext",
            "C": "None of these",
            "D": "Each bit should depend on several parts of the key"
        },
        "correct": "A"
    },
       {
        "question": "What is perfect secrecy",
        "options": {
            "A": "If after seeing the ciphertext, an interceptor gets no extra information about the plaintext",
            "B": "The key size is of sufficient size as to not be reasonably brute forcable",
            "C": "RSA",
            "D": "CBC"
        },
        "correct": "A"
    },
       {
        "question": "Which opperator alone can achieve 'perfect secrecy'",
        "options": {
            "A": "XOR",
            "B": "XNOR",
            "C": "NAND",
            "D": "MOD"
        },
        "correct": "A"
    },
       {
        "question": "Why is XOR not typically used in isolation for symetric cryptography",
        "options": {
            "A": "It requires an equal size key, which can be slow",
            "B": "It requires a shared secret with the recipient",
            "C": "The opperation itself is relatively slow when compared to alternatives",
            "D": "It is very simple to brute force"
        },
        "correct": "A"
    },
       {
        "question": "What is the key difference between stream and block ciphers",
        "options": {
            "A": "Block ciphers opperate on multiple bits at once",
            "B": "Stream ciphers tend to be used for asymetric cryptography where block ciphers tend to be for symetric",
            "C": "Stream ciphers typically use XOR, where block ciphers use more complicated opperations such as using mod with prime numbers",
            "D": "Arman"
        },
        "correct": "A"
    },
       {
        "question": "What is the key downside to stream ciphers",
        "options": {
            "A": "Reuse of keys results in information leakage",
            "B": "They are slow when compared to block ciphers, since block ciphers can be paralelized",
            "C": "They are unreliable due to error propigation",
            "D": ""
        },
        "correct": "A"
    },
       {
        "question": "Which are disadvantages of block ciphers (like AES)",
        "options": {
            "A": "Need for padding",
            "B": "Error propagation",
            "C": "All of these",
            "D": "None of these"
        },
        "correct": "A"
    },
       {
        "question": "What is the point of MAC",
        "options": {
            "A": "To ensure a message has not been altered, and to verify the senders identity",
            "B": "To encrypt communication using a shared secret",
            "C": "To verify that a file has not been altered after the creation of the MAC",
            "D": "CYBR371 meltdown assignment"
        },
        "correct": "A"
    },
       {
        "question": "What is a type of MAC (mentioned in lectures)",
        "options": {
            "A": "HMAC",
            "B": "DMAC",
            "C": "XMAC",
            "D": "QMAC"
        },
        "correct": "A"
    },
       {
        "question": "What is a type of MAC (mentioned in lectures)",
        "options": {
            "A": "CMAC",
            "B": "DMAC",
            "C": "XMAC",
            "D": "QMAC"
        },
        "correct": "A"
    },
       {
        "question": "What does MAC stand for (per the slides)",
        "options": {
            "A": "Message Authentication Code",
            "B": "Media access control",
            "C": "Mild Arman Comicality",
            "D": "Message Authoriztion Cipher"
        },
        "correct": "A"
    },
       {
        "question": "What is commonly the key opperation in the context of asymetric cryptography",
        "options": {
            "A": "Modulo",
            "B": "XOR",
            "C": "Pow",
            "D": "NAND"
        },

        "correct": "A"
    },
       {
        "question": "What is MOD(5,7)",
        "options": {
            "A": "5",
            "B": "2",
            "C": "9",
            "D": "7"
        },
        "correct": "A"
    },
       {
        "question": "What is MOD(6,3)",
        "options": {
            "A": "0",
            "B": "3",
            "C": "6",
            "D": "9"
        },
        "correct": "A"
    },
       {
        "question": "What is MOD(9,2)",
        "options": {
            "A": "1",
            "B": "11",
            "C": "9",
            "D": "2"
        },
        "correct": "A"
    },
       {
        "question": "What is RSA",
        "options": {
            "A": "An asymetric algorithm",
            "B": "A symetric algorithm",
            "C": "A MAC algorithm",
            "D": "A rman algorithm"
        },
        "correct": "A"
    },
       {
        "question": "If p=3 q=7, what is t and e (in the context of asymetric cryptography)",
        "options": {
            "A": "t=2, though e is not known",
            "B": "t=1, e=3",
            "C": "t is unknown, e=3",
            "D": "im so sorry for this evil question..."
        },
        "correct": "A"
    },
       {
        "question": "What is t? (in the context of asymetric cryptography)",
        "options": {
            "A": "t=lcm(p-1,q-1)",
            "B": "t=mod(p,q)",
            "C": "t=p^e - q^e",
            "D": "again... this is evil"
        },
        "correct": "A"
    },
       {
        "question": "Why use digital signatures over MAC",
        "options": {
            "A": "MAC requires shared secret keys, while digital signatures work with public/private keys",
            "B": "MAC is only used to ensure a file has not been modified",
            "C": "Digital signatures verify the identity of the sender where MAC does not",
            "D": "'This is madness and rediculus' yeah... I agree"
        },
        "correct": "A"
    },
       {
        "question": "What are some forms of E.A.",
        "options": {
            "A": "All of these",
            "B": "Timestamps",
            "C": "Sequence numbers",
            "D": "Nonce based mechanisms (numbers used only once, silly stupid name)"
        },
        "correct": "A"
    },
       {
        "question": "Which of the following is correct",
        "options": {
            "A": "Non repudiation is sufficient for data origin authentication",
            "B": "Confidentiality is sufficient for ensuring data integrity",
            "C": "Data origin authentication is sufficient for non repudiation",
            "D": "data integrity requires non repudiation"
        },
        "correct": "A"
    },
       {
        "question": "When encrypting an image, which algorithm still alows for inference of the original image (image shape isnt hidden)",
        "options": {
            "A": "ECB",
            "B": "CBC",
            "C": "Any algorithm using a short key",
            "D": "Any of these COULD be true"
        },
        "correct": "A"
    },
       {
        "question": "Which of the following statements about perfect secrecy is correct",
        "options": {
            "A": "Perfect secrecy is achieved with symmetric key encryption not public key encryption",
            "B": "Perfect secrecy can be implemented using a strong pseudo-random number generator to create a key stream",
            "C": "Perfect key secrecy is achievable with modern encryption algorithms like AES when used with a large key",
            "D": "In perfect secrecy every possible plaintext must be equally likely given any ciphertext"
        },
        "correct": "A"
    },
       {
        "question": "In the context of verifying a digital signature which of the following is NOT used as a parameter in the verification proess",
        "options": {
            "A": "The signing key",
            "B": "The digital signature itself",
            "C": "The verification key",
            "D": "The original message on which the signature is created"
        },
        "correct": "A"
    },
       {
        "question": "How many bits can be represented in a signle base64 character",
        "options": {
            "A": "6",
            "B": "7",
            "C": "8",
            "D": "4"
        },
        "correct": "A"
    },
       {
        "question": "( FUN QUESTION c: ) If a pool takes 10 minuites to fill, and the contents doubles every when filling minuite, when is the pool a quater full",
        "options": {
            "A": "8 mins",
            "B": "9 mins",
            "C": "5 mins",
            "D": "2.5 mins"
        },
        "correct": "A"
    },
       {
        "question": "Suppose you write an IOU document stating you owe $100, which property of the hash function ensures that someone cannot modify the file and change it to $1000",
        "options": {
            "A": "Seccond pre image resistance",
            "B": "Collision resistance",
            "C": "Pre image resistance",
            "D": "Replay sttack resistance"
        },
        "correct": "A"
    },
       {
        "question": "Which of the following correctly describes the differences or simularities between MAC and digital signatures",
        "options": {
            "A": "Security of both of them depends on keeping a secret key",
            "B": "Digital signatures are faster to compute then MACs",
            "C": "Both MAC and digital signatures can only be verified by the intended recipient",
            "D": "Both Mac and digital signatures provide non repudiation ensuring that the sender cannot deny having sent the message"
        },
        "correct": "A"
    },
       {
        "question": "Which is NOT a key property of a secure hashing algorithm",
        "options": {
            "A": "A secure hash function should keep the encryption key private",
            "B": "Given hash output h, it should be computationally infeasable to find any input m such that hash(m) = h",
            "C": "Given specific input m1, it should be infeasible to find another input m2 where m1 != m2 but hash(m1) == hash(m2)",
            "D": "It should be infeasible to find any two distinct inputs m1, m2 that prodce the same hash"
        },
        "correct": "A"
    },
       {
        "question": "Which is IS a key property of a secure hashing algorithm",
        "options": {
            "A": "A change of 1 bit, should cause a large unpredictable change in output",
            "B": "A secure hash function should keep the encryption key private",
            "C": "A secure hash should preserve the ordering of input values in the output values",
            "D": "A secure hash should be revsible so the original message can be recovered from the hash, this is important for MAC and signatures"
        },
        "correct": "A"
    },
       {
        "question": "Which is IS a key property of a secure hashing algorithm",
        "options": {
            "A": "The same input should always produce the exact same output",
            "B": "Larger inputs should produce proportionally larger hash values, because of the pidgeon hole prinsiple mentioned in lectures",
            "C": "If input A hashes to B, then B should hash back to A",
            "D": "Hash outputs should be easily read and remembered by humans"
        },
        "correct": "A"
    },
       {
        "question": "Which is IS a key property of a secure hashing algorithm",
        "options": {
            "A": "All possible hash values should be equally likely for random inputs",
            "B": "Larger inputs should produce proportionally larger hash values, because of the pidgeon hole prinsiple mentioned in lectures",
            "C": "If input A hashes to B, then B should hash back to A",
            "D": "Hash outputs should be easily read and remembered by humans"
        },
        "correct": "A"
    },
       {
        "question": "Which is IS a key property of a secure hashing algorithm",
        "options": {
            "A": "The hashing function should be fast enough for legitimate use, but slow enough as to make brute forcing infeasable",
            "B": "Larger inputs should produce proportionally larger hash values, because of the pidgeon hole prinsiple mentioned in lectures",
            "C": "If input A hashes to B, then B should hash back to A",
            "D": "Hash outputs should be easily read and remembered by humans"
        },
        "correct": "A"
    },
       {
        "question": "Which is true about XOR",
        "options": {
            "A": "When performing XOR on a key and plaintext, the resulting ciphertext can then be 'reversed' by simply XOR'ing with the key again",
            "B": "XOR always increases the size of the data to ensure security",
            "C": "XOR requires the key to be longer than the message for correct operation",
            "D": "XOR encryption is secure even if the same key is reused many times"
        },
        "correct": "A"
    },
       {
        "question": "Which is a common reason reusing a key in a stream cipher is insecure",
        "options": {
            "A": "It allows attackers to derive relationships between plaintexts",
            "B": "It makes the ciphertext longer and thus easier to intercept",
            "C": "It causes the key to randomly change during transmission",
            "D": "It prevents the ciphertext from being decrypted"
        },
        "correct": "A"
    },
       {
        "question": "Which is true about the avalanche effect in hashing",
        "options": {
            "A": "Changing one bit of input should cause a large unpredictable change in the output",
            "B": "Changing one bit of input should only slightly change the output",
            "C": "The avalanche effect ensures that the output is always shorter than the input",
            "D": "Avalanche effect means the hash function can be reversed"
        },
        "correct": "A"
    },
       {
        "question": "Which is true about collision resistance",
        "options": {
            "A": "It should be infeasible to find any two different inputs that produce the same hash output",
            "B": "It means a hash can never produce the same output twice",
            "C": "It ensures that a hash can be reversed to the original input",
            "D": "It guarantees that all outputs are prime numbers"
        },
        "correct": "A"
    },
       {
        "question": "Which is true about preimage resistance",
        "options": {
            "A": "Given a hash output h, it should be infeasible to find an input m such that hash(m) = h",
            "B": "Given a message, it should be infeasible to find the hash value",
            "C": "It ensures that the same input produces a different hash each time",
            "D": "It ensures the hash is always shorter than the input"
        },
        "correct": "A"
    },
       {
        "question": "Which is true about base64 encoding",
        "options": {
            "A": "Each base64 character represents exactly 6 bits of data",
            "B": "Each base64 character represents exactly 7 bits of data",
            "C": "Base64 encoding compresses the original data to a smaller size",
            "D": "Base64 encoding is a secure form of encryption"
        },
        "correct": "A"
    },
       {
        "question": "Which is true about ECB mode encryption",
        "options": {
            "A": "It encrypts identical plaintext blocks into identical ciphertext blocks",
            "B": "It ensures every block of ciphertext is unique regardless of plaintext",
            "C": "It automatically hides all patterns in the plaintext",
            "D": "It is slower than all other block cipher modes"
        },
        "correct": "A"
    },
{
  "question": "Which is true about ECB mode?",
  "options": {
    "A": "Identical plaintext blocks always produce identical ciphertext blocks",
    "B": "ECB mode uses a feedback mechanism to randomize each block",
    "C": "ECB mode is immune to pattern leakage in images",
    "D": "ECB mode encrypts each block using a different key"
  },
  "correct": "A"
},

{
  "question": "Which is true about CBC mode?",
  "options": {
    "A": "Each plaintext block is XOR'd with the previous ciphertext block before encryption",
    "B": "CBC mode can be parallelized for both encryption and decryption",
    "C": "CBC mode does not require an initialization vector (IV)",
    "D": "A single bit error in a ciphertext block only affects the corresponding plaintext block"
  },
  "correct": "A"
},
{
  "question": "Which is true about CFB mode?",
  "options": {
    "A": "It turns a block cipher into a self-synchronizing stream cipher",
    "B": "CFB mode requires padding to work correctly",
    "C": "CFB mode encrypts the plaintext directly without XOR",
    "D": "CFB mode cannot recover if synchronization is lost"
  },
  "correct": "A"
},
{
  "question": "Which is true about OFB mode?",
  "options": {
    "A": "OFB generates keystream blocks by repeatedly encrypting the previous output block",
    "B": "OFB mode requires the plaintext to be padded to a multiple of the block size",
    "C": "OFB mode is self-synchronizing after transmission errors",
    "D": "OFB mode encrypts each plaintext block independently, similar to ECB"
  },
  "correct": "A"
},

{
  "question": "Which is true about CTR mode?",
  "options": {
    "A": "CTR mode uses a counter value that is encrypted to produce the keystream",
    "B": "CTR mode requires padding for partial blocks",
    "C": "CTR mode cannot be parallelized",
    "D": "CTR mode encrypts plaintext blocks directly with the block cipher"
  },
  "correct": "A"
},
{
  "question": "Which is true about GCM mode?",
  "options": {
    "A": "GCM mode provides both encryption and authentication",
    "B": "GCM mode is based on CBC encryption with additional hashing",
    "C": "GCM mode is slower than CBC in most hardware implementations",
    "D": "GCM mode requires padding for plaintext"
  },
  "correct": "A"
},
       {
        "question": "What is the main idea behind the Birthday Attack on hash functions?",
        "options": {
            "A": "It exploits the fact that collisions can be found in about 2^(L/2) attempts for an L-bit hash",
            "B": "It allows an attacker to recover the original message from its hash",
            "C": "It is a brute-force attack that tries all possible inputs up to 2^L",
            "D": "It relies on reversing the compression function of the hash algorithm"
        },
        "correct": "A"
    },
       {
        "question": "What is a replay attack?",
        "options": {
            "A": "Re-sending previously captured valid messages to trick the receiver into accepting them again",
            "B": "Brute forcing a password by replaying guessed values until accepted",
            "C": "Intercepting a message and modifying it before delivering",
            "D": "Replacing a key exchange with a fake public key"
        },
        "correct": "A"
    },
       {
        "question": "In the MAC-then-encrypt protocol, what is the correct order of operations for the receiver?",
        "options": {
            "A": "Separate the MAC from the ciphertext, decrypt the ciphertext, compute a MAC on the plaintext, and compare",
            "B": "Verify the MAC on the ciphertext before decrypting it",
            "C": "Decrypt the ciphertext, then compare it directly to the received MAC without recomputing",
            "D": "Use the MAC to derive the decryption key"
        },
        "correct": "A"
    },
       {
        "question": "Which security services are provided by the MAC-then-encrypt protocol described in the course?",
        "options": {
            "A": "Confidentiality and detection of accidental errors",
            "B": "Confidentiality only",
            "C": "Integrity only",
            "D": "Authentication only"
        },
        "correct": "A"
    },
       {
        "question": "What is an advantage of using a password-based key derivation function (PBKDF)?",
        "options": {
            "A": "Users can remember passwords more easily than long random cryptographic keys",
            "B": "PBKDFs make encryption completely immune to brute-force attacks",
            "C": "PBKDFs ensure the password itself never needs to be remembered",
            "D": "PBKDFs make encryption run faster than using a raw key"
        },
        "correct": "A"
    },
       {
        "question": "What is the role of a salt in password-based key derivation?",
        "options": {
            "A": "It ensures the same password generates different keys, preventing use of precomputed dictionaries",
            "B": "It makes the password impossible to brute-force",
            "C": "It hides the password from the key derivation function",
            "D": "It replaces the need for a strong password"
        },
        "correct": "A"
    },
       {
        "question": "The security of Diffie-Hellman key exchange relies on the difficulty of which problem?",
        "options": {
            "A": "Computing the discrete logarithm in a large prime field",
            "B": "Factoring the product of two large primes",
            "C": "Finding two numbers that multiply to a given composite",
            "D": "Reversing a cryptographic hash function"
        },
        "correct": "A"
    },
       {
        "question": "In a certain block cipher mode, flipping one bit in a ciphertext block affects only the same bit in the corresponding plaintext block. Which property is this describing?",
        "options": {
            "A": "Minimal error propagation",
            "B": "Complete avalanche effect",
            "C": "Self-synchronizing stream mode",
            "D": "Chained block dependency"
        },
        "correct": "A"
    },
       {
        "question": "Which of the following is NOT a valid encryption scheme structure?",
        "options": {
            "A": "Using the XOR of the plaintext with the bitwise NOT of the key",
            "B": "Using the XOR of the plaintext with the key",
            "C": "Using the XOR of the plaintext with the key XOR an IV",
            "D": "Using the XOR of the plaintext with the key AND an IV"
        },
        "correct": "A"
    },
   ]



def shuffle(items):
    shuffled = []
    list_copy = list(items)
    while len(list_copy) > 0:
        shuffled.append(list_copy.pop(random.randint(0, len(list_copy) - 1)))
    return shuffled

def clear_screen():
    """Clear the console screen based on operating system"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_question(q_data, q_num, q_count):
    """Display a question and its options"""
    print(f"\nQuestion {q_num} of {q_count}:")
    print(q_data["question"])
    print()
    q_data_shuffled = shuffle(q_data["options"].items())
    i = 0
    for key, value in q_data_shuffled:
        print(f"{['A', 'B', 'C', 'D'][i]}. {value}")
        i += 1
    print()
    return q_data_shuffled

def get_user_answer():
    """Get and validate user input"""
    while True:
        answer = input("Your answer (A/B/C/D): ").strip().upper()
        if answer in ['A', 'B', 'C', 'D']:
            return answer
        else:
            print("Invalid input. Please enter A, B, C, or D.")

def run_quiz():
    """Main function to run the quiz"""
    score = 0
    total_questions = 0
    incorrect_questions = []
    
    try:
        clear_screen()
        print("======================================")
        print("CYBR372 PRACTICE QUIZ")
        print("======================================")
        print("God help us all...")
        #x = input("Press Enter to begin normal quiz, input 'mini' to start a trimmed version of the quiz\n")
        x = input("Press enter to begin")
        shuffled_questions = []

        if x == "mini":
            shuffled_questions = shuffle(questions_db[120:])
        else:
            shuffled_questions = shuffle(questions_db)
        
        for question in shuffled_questions:
            total_questions += 1
            
            clear_screen()
            answer_order = display_question(question, total_questions, len(shuffled_questions))
            user_answer = get_user_answer()
            
            # Check if answer is correct
            i = 0
            for item in answer_order:
                if item[0] == question["correct"]:
                    correct_answer = ['A', 'B', 'C', 'D'][i]
                i += 1
            is_correct = user_answer == correct_answer
            
            if is_correct:
                print("\n✓ Correct! Well done!")
                score += 1
            else:
                print(f"\n✗ Incorrect. The correct answer is {correct_answer}.")
                explanation = question['options'][question["correct"]]
                print(f"Explanation: {explanation}")
                incorrect_questions.append(f"Q: {question['question']}\nYour Answer: {user_answer}\nCorrect: {correct_answer}\nExplanation: {question['options'][correct_answer]}")
                input("Press enter to continue")
            
            print(f"\nCurrent score: {score}/{total_questions} ({score/total_questions*100:.1f}%)")
            
            time.sleep(2)
            
            
    except KeyboardInterrupt:
        clear_screen()
        print("\nQuiz interrupted.")
    
    finally:
        # Display final score
        if total_questions > 0:
            clear_screen()
            print("\n======================================")
            print("QUIZ COMPLETED")
            print("======================================")
            print(f"Final Score: {score}/{total_questions} ({score/total_questions*100:.1f}%)")
            
            if score/total_questions >= 0.9:
                print("Excellent! You're well prepared for the test!")
            elif score/total_questions >= 0.6:
                print("Good job! With a bit more study, you'll be well prepared.")
            elif score/total_questions >= 0.2:
                print("You might need some more study time to prepare for the test.")
            else:
                print("L.")


if __name__ == "__main__":
    run_quiz()
