import hashlib

def GetRef(User):

    User = str(User).encode()
    Hash = hashlib.md5(User).hexdigest().upper()

    (Ref, Count) = ('', 0)

    for Chr in Hash:

        if Count == 4:

            (Ref, Count) = (Ref + '-', 0)

        (Ref, Count) = (Ref + Chr, Count + 1)

    return Ref
