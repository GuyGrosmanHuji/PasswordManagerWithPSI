class Client:
    def __init__(self):
        pass

    ######################################## UI
    """
        *   Let user sign a master password
        *   Let user sign passwords - these will be encrypted using the master-password as a key
        *   Each password is mapped to some title (e.g name of website), user can ask for title and get the password
            *   TODO: How he gets the password? Print or copied to clipboard?
        *   Let user check if he has any leaked-password
            *   TODO: how? maybe we should do it anytime the user signs in
        *   GUI?
    """
    # TODO: implement


    ######################################## PSI Protocol
    """
    As defined in the article: https://eprint.iacr.org/2017/299.pdf
    Should hold:
        *   for any password(:=y), [y^i] for i in 0,...,logN
            * How will we decide N?
            * Maybe it should be calculated each time differently?
            
        *   Cuckoo-Hashing for the passwords
    """
    # TODO: implement


    ######################################## Communication
    # TODO: implement


    ######################################## Backend
    # TODO: implement

