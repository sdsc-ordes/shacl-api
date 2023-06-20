import subprocess

def runValidationTest():
    output = subprocess.run(["shaclvalidate.sh", "-datafile", "tests-files/val_imagingID.ttl", "-shapesfile", "tests-files/val_ImagingOntologyShapes.ttl"], stdout=subprocess.PIPE)

    with open("validationTest.ttl", 'wb') as f: 
        f.write(output.stdout)

def runFailedInferenceTest():
    output = subprocess.run(["shaclvalidate.sh", "-datafile", "tests-files/val_fail_imagingID.ttl", "-shapesfile", "tests-files/val_fail_ImagingOntologyShapes.ttl"], stdout=subprocess.PIPE)

    with open("validationFailTest.ttl", 'wb') as f: 
        f.write(output.stdout)


runValidationTest()
runFailedInferenceTest()