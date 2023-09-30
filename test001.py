
def getMessageType(controlCode: str):
    """Return the message type of the last read message."""
    try:
        print("OK")
        messageType = controlCode[:2]
    except:
        print("BAD")
        messageType = controlCode

    return messageType

myList = ""
print(getMessageType(myList))