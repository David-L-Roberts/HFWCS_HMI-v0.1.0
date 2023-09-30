# types of messages and their control characters
masterMsgCodes = {
    "Poll":         b'\xFB',
    "Recall":       b'\xFD',
    "Control Data": b'\xFC',
    "Execute Controls": b'\xFE',
    "Ack Slave":    b'\xFA',
}

# types of control characters and their message types
msgTypeLookup = {
    "F1": "Acknowledge Master",
    "F2": "Indication Data Response",
    "F3": "Control Checkback",
    "F9": "Common Control",
    "FA": "Acknowledge Slave",
    "FB": "Poll Slave",
    "FC": "Control Data",
    "FD": "Recall",
    "FE": "Execute Controls",
}