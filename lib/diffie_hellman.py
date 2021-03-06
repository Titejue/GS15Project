from crypto_utils import *
import random

# Some of the functions, or parts of functions, come from third parties.
# Below are the sources of these functions :
# https://www.baylon-industries.com/news/?p=1430
# https://crypto.stackexchange.com/questions/9006/how-to-find-generator-g-in-a-cyclic-group

"""
    Alice and Bob want to communicate.
    Alice and Bob have their own couple of keys : PubK_Alice, PrivK_Alice, PubK_Bob, PrivK_Bob 
    They want to communicate with Diffie Hellman protocol  
    p is a 128 bytes number
    q is a 2p-1 = 128 bytes prime number
    """


# A_hex = int2bytes(com_key_alice, 128)
# print("Alice communicated key : ")
# bytesToString(A_hex)

def DH_gen_keys(lenth_p, lenth_q):
    """
    @brief      Generate a couple of asymmetric keys

    @param      lenth_q     q length in bytes
    @param      lenth_p     p length in bytes

    @return     Diffie Hellman parameters (g, p, q), Alice public shared key, Alice private random number a
    """
    if lenth_p is None:
        lenth_p = 128
    if lenth_q is None:
        lenth_q = 64
    print("* Starting to generate asymmetric keys with Diffie Hellman")
    DH_param = Schnorr_group(lenth_p, lenth_q)

    print("Generate a private key")
    private_key = random.randint(2, DH_param.q)

    print("Generate a public key")
    public_key = pow(DH_param.g, private_key, DH_param.p)
    # pow(DH_param.g, private_key, DH_param.p)

    return Key(DH_param, public_key, private_key)


def DH_comm_key_Bob(DH_param, client_public_key):
    """
    @brief      Génère une clé privé et de communication

    @param      DH_param           Les paramètres de la génération de clé
    @param      client_public_key  La clé publique de l'interlocuteur

    @return     La clé de communication, publique et privé de bob
    """
    print("Generate Bob keys : ")

    private_key = random.randint(2, DH_param.q)
    pub_key = pow(DH_param.g, private_key, DH_param.p)
    # pow(DH_param.g, private_key, DH_param.p)

    shared_key = pow(client_public_key, private_key, DH_param.p)
    # pow(client_public_key, private_key, DH_param.p)

    return shared_key, Key(DH_param, pub_key, private_key)


def DH_comm_key_Alice(my_key, server_pub_key):
    """
    @brief      Generate the shared key on Alice side

    @param      my_key          My key
    @param      server_pub_key  The server public key

    @return     Alice's shared key (or communication key)
    """
    my_shared_key = pow(server_pub_key, my_key.private_key, my_key.param.p)
    return my_shared_key
    # pow(server_pub_key, my_key.private_key, my_key.param.p)

