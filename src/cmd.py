import testing

print()
try:
    nTest=int(input('Input count of goods (1000 is recommended value): '))
except ValueError:
    print("Not a number")


fIris = testing.runIrisAddTest(nTest)
fEAX  = testing.runEAXAddTest(nTest)

print()
print("IRIS native globals: adding of {0} goods - {1:.4f} sec".format(nTest, fIris))
print("EAX (MySQL backend): adding of {0} goods - {1:.4f} sec".format(nTest, fEAX))
print()
print('====  ADDING: IRIS Native API {:.2f}x faster!  ===='.format(fEAX/fIris))

fIris = testing.runIrisReadTest(nTest)
fEAX  = testing.runEAXReadTest(nTest)

print()
print("IRIS native globals: adding of {0} goods - {1:.4f} sec".format(nTest, fIris))
print("EAX (MySQL backend): adding of {0} goods - {1:.4f} sec".format(nTest, fEAX))
print()
print('====  READING: IRIS Native API {:.2f}x faster!  ===='.format(fEAX/fIris))
print()
