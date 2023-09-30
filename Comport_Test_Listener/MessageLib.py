# types of Master messages and their control characters
masterMsgCodes = {
    "Poll Slave":   b'\xFB',
    "Recall":       b'\xFD',
    "Control Data": b'\xFC',
    "Execute Controls": b'\xFE',
    "Acknowledge Slave":    b'\xFA',
}

# types of slave messages and their control characters
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