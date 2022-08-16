class Server:
    def __init__(self):
        pass


    ######################################## PSI Protocol
    """
    As defined in the article: https://eprint.iacr.org/2017/299.pdf
    Should hold:
        *   given some y, we have to calculate r * PAI_x∈X(y-x) = SIGMA_i (a^i * y^i)
            so we should calculate a and hold a's list accordingly
        *   Customized CuckooHashing for the passwords in the DB
    """
    # TODO: implement


    ######################################## Communication
    """
    Manage a conversation with the client according to the protocol https://eprint.iacr.org/2017/299.pdf
        *   Support multi-client?
    """
    # TODO: implement


    ######################################## Backend
    """
    DB Management
    """
    # TODO: implement
