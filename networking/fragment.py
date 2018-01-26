# fragment.py - simulate how the internet protocol would fragment a datagram
# usage: python fragment.py <payloadSize> <mtuSize>

import sys

printCount = 0

def printFragmentInfo(moreFragments, fragmentOffset, packetLength):
    global printCount
    printCount += 1
    print(" %3d |    %1d |   %4d |   %4d"% (printCount, moreFragments, fragmentOffset, packetLength))

headerSize = 20
payloadLeft = payloadSize = int(sys.argv[1])
mtuSize = int(sys.argv[2])

if payloadSize + headerSize > 65535:
    print("Oversize payload: the sum of payload and header must not exceed 65535")
    sys.exit()

print("   # | more | offset | length ")
print("=====|======|========|========")

currentOffset = 0

while True:   
    if payloadLeft + headerSize < mtuSize:
        printFragmentInfo(0, currentOffset / 8, payloadLeft + headerSize)
        break
    else:
        currentPacketSize = mtuSize
        payloadLeft -= (mtuSize - headerSize)
        printFragmentInfo(1, currentOffset / 8, currentPacketSize)
        currentOffset += (mtuSize - headerSize)
